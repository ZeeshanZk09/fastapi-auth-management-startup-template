import re
import secrets
from datetime import datetime, timedelta, timezone
from urllib.parse import urlencode

import httpx
from fastapi import HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlmodel import Session, select

from app.config import settings
from app.models.account import Account
from app.models.session import Session as UserSession
from app.models.user import User
from app.utils.jwt import create_access_token
from app.utils.redis_client import get_redis_client


def _provider_config(provider: str) -> dict[str, str]:
    normalized_provider = provider.lower()
    if normalized_provider == "google":
        return {
            "provider": "google",
            "client_id": settings.GOOGLE_CLIENT_ID,
            "client_secret": settings.GOOGLE_CLIENT_SECRET,
            "auth_url": "https://accounts.google.com/o/oauth2/v2/auth",
            "token_url": "https://oauth2.googleapis.com/token",
            "userinfo_url": "https://www.googleapis.com/oauth2/v3/userinfo",
            "scope": "openid email profile",
        }
    if normalized_provider == "github":
        return {
            "provider": "github",
            "client_id": settings.GITHUB_CLIENT_ID,
            "client_secret": settings.GITHUB_CLIENT_SECRET,
            "auth_url": "https://github.com/login/oauth/authorize",
            "token_url": "https://github.com/login/oauth/access_token",
            "userinfo_url": "https://api.github.com/user",
            "scope": "read:user user:email",
        }
    raise HTTPException(status_code=400, detail="Unsupported OAuth provider")


def _normalize_name(full_name: str | None) -> tuple[str, str]:
    if not full_name:
        return "OAuth", "User"
    parts = full_name.strip().split()
    if len(parts) == 1:
        return parts[0], "User"
    return parts[0], " ".join(parts[1:])


def _sanitize_username(raw_value: str) -> str:
    sanitized = re.sub(r"\W", "_", raw_value).strip("_").lower()
    return sanitized or "oauth_user"


def _next_available_username(db: Session, preferred_username: str) -> str:
    base = _sanitize_username(preferred_username)
    candidate = base
    suffix = 1
    while db.exec(select(User).where(User.user_name == candidate)).first():
        candidate = f"{base}_{suffix}"
        suffix += 1
    return candidate


def _next_available_phone(db: Session, provider: str, provider_user_id: str) -> str:
    base = f"oauth-{provider}-{provider_user_id}"
    candidate = base
    suffix = 1
    while db.exec(select(User).where(User.phone == candidate)).first():
        candidate = f"{base}-{suffix}"
        suffix += 1
    return candidate


async def _exchange_code_for_token(
    provider: str,
    token_url: str,
    client_id: str,
    client_secret: str,
    code: str,
    redirect_uri: str,
) -> str:
    token_request_data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "code": code,
        "redirect_uri": redirect_uri,
    }
    if provider == "google":
        token_request_data["grant_type"] = "authorization_code"

    async with httpx.AsyncClient(timeout=15.0) as client:
        token_response = await client.post(
            token_url,
            data=token_request_data,
            headers={"Accept": "application/json"},
        )
    if token_response.status_code >= 400:
        raise HTTPException(status_code=400, detail="OAuth token exchange failed")

    token_payload = token_response.json()
    access_token = token_payload.get("access_token")
    if not isinstance(access_token, str) or not access_token:
        raise HTTPException(status_code=400, detail="OAuth provider did not return an access token")
    return access_token


async def _fetch_google_profile(client: httpx.AsyncClient, auth_headers: dict[str, str]) -> dict[str, str]:
    profile_response = await client.get("https://www.googleapis.com/oauth2/v3/userinfo", headers=auth_headers)
    if profile_response.status_code >= 400:
        raise HTTPException(status_code=400, detail="Unable to fetch Google user profile")

    google_profile = profile_response.json()
    profile_id = google_profile.get("sub")
    if not isinstance(profile_id, str) or not profile_id:
        raise HTTPException(status_code=400, detail="Google profile is missing user id")

    email = google_profile.get("email")
    return {
        "id": profile_id,
        "email": email if isinstance(email, str) else "",
        "name": google_profile.get("name") or "",
        "login": google_profile.get("email") or "",
    }


async def _resolve_github_email(client: httpx.AsyncClient, auth_headers: dict[str, str]) -> str:
    email_response = await client.get("https://api.github.com/user/emails", headers=auth_headers)
    if email_response.status_code >= 400:
        return ""

    email_candidates = email_response.json()
    if not isinstance(email_candidates, list) or not email_candidates:
        return ""

    primary_verified_email = next(
        (
            item.get("email")
            for item in email_candidates
            if isinstance(item, dict) and item.get("primary") and item.get("verified")
        ),
        None,
    )
    if isinstance(primary_verified_email, str):
        return primary_verified_email

    first_email = email_candidates[0].get("email") if isinstance(email_candidates[0], dict) else None
    return first_email if isinstance(first_email, str) else ""


async def _fetch_github_profile(client: httpx.AsyncClient, auth_headers: dict[str, str]) -> dict[str, str]:
    profile_response = await client.get("https://api.github.com/user", headers=auth_headers)
    if profile_response.status_code >= 400:
        raise HTTPException(status_code=400, detail="Unable to fetch GitHub user profile")

    github_profile = profile_response.json()
    profile_id_raw = github_profile.get("id")
    if profile_id_raw is None:
        raise HTTPException(status_code=400, detail="GitHub profile is missing user id")

    email = github_profile.get("email")
    normalized_email = email if isinstance(email, str) and email else await _resolve_github_email(client, auth_headers)
    return {
        "id": str(profile_id_raw),
        "email": normalized_email,
        "name": github_profile.get("name") or github_profile.get("login") or "",
        "login": github_profile.get("login") or "",
    }


async def _fetch_oauth_profile(provider: str, access_token: str) -> dict[str, str]:
    auth_headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json",
    }

    async with httpx.AsyncClient(timeout=15.0) as client:
        if provider == "google":
            return await _fetch_google_profile(client, auth_headers)
        return await _fetch_github_profile(client, auth_headers)


def _get_or_create_oauth_user(db: Session, provider: str, profile: dict[str, str], provider_token: str) -> User:
    provider_user_id = profile["id"]

    existing_account = db.exec(
        select(Account).where(
            Account.provider == provider,
            Account.provider_user_id == provider_user_id,
        )
    ).first()
    if existing_account:
        existing_account.access_token = provider_token
        db.add(existing_account)
        db.commit()

        linked_user = db.get(User, existing_account.user_id)
        if not linked_user:
            raise HTTPException(status_code=500, detail="OAuth account is linked to a missing user")
        return linked_user

    email = profile.get("email") or f"{provider_user_id}@{provider}.oauth.local"
    user = db.exec(select(User).where(User.email == email)).first()

    if not user:
        first_name, last_name = _normalize_name(profile.get("name"))
        preferred_username = profile.get("login") or email.split("@")[0]
        user = User(
            first_name=first_name,
            last_name=last_name,
            user_name=_next_available_username(db, preferred_username),
            email=email,
            phone=_next_available_phone(db, provider, provider_user_id),
            email_verified=True,
            phone_verified=False,
            hashed_password=None,
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    oauth_account = Account(
        user_id=user.id,
        provider=provider,
        provider_user_id=provider_user_id,
        access_token=provider_token,
    )
    db.add(oauth_account)
    db.commit()
    return user


async def handle_oauth_login(provider: str, request: Request):
    provider_cfg = _provider_config(provider)
    if not provider_cfg["client_id"] or not provider_cfg["client_secret"]:
        raise HTTPException(status_code=503, detail=f"{provider_cfg['provider'].title()} OAuth is not configured")

    oauth_state = secrets.token_urlsafe(32)
    redis_client = await get_redis_client()
    await redis_client.set(f"oauth_state:{oauth_state}", provider_cfg["provider"], ex=600)

    redirect_uri = str(request.url_for("oauth_callback", provider=provider_cfg["provider"]))
    query_params = {
        "client_id": provider_cfg["client_id"],
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "scope": provider_cfg["scope"],
        "state": oauth_state,
    }
    if provider_cfg["provider"] == "google":
        query_params["access_type"] = "offline"
        query_params["prompt"] = "consent"

    auth_url = f"{provider_cfg['auth_url']}?{urlencode(query_params)}"
    return RedirectResponse(url=auth_url)


async def handle_oauth_callback(provider: str, request: Request, db: Session):
    provider_cfg = _provider_config(provider)
    if not provider_cfg["client_id"] or not provider_cfg["client_secret"]:
        raise HTTPException(status_code=503, detail=f"{provider_cfg['provider'].title()} OAuth is not configured")

    oauth_error = request.query_params.get("error")
    if oauth_error:
        raise HTTPException(status_code=400, detail=f"OAuth error from provider: {oauth_error}")

    auth_code = request.query_params.get("code")
    oauth_state = request.query_params.get("state")
    if not auth_code or not oauth_state:
        raise HTTPException(status_code=400, detail="Missing OAuth code or state")

    redis_client = await get_redis_client()
    expected_provider = await redis_client.get(f"oauth_state:{oauth_state}")
    await redis_client.delete(f"oauth_state:{oauth_state}")
    if expected_provider != provider_cfg["provider"]:
        raise HTTPException(status_code=400, detail="Invalid OAuth state")

    redirect_uri = str(request.url_for("oauth_callback", provider=provider_cfg["provider"]))
    provider_access_token = await _exchange_code_for_token(
        provider=provider_cfg["provider"],
        token_url=provider_cfg["token_url"],
        client_id=provider_cfg["client_id"],
        client_secret=provider_cfg["client_secret"],
        code=auth_code,
        redirect_uri=redirect_uri,
    )

    oauth_profile = await _fetch_oauth_profile(provider_cfg["provider"], provider_access_token)
    user = _get_or_create_oauth_user(db, provider_cfg["provider"], oauth_profile, provider_access_token)

    expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    app_access_token = create_access_token(data={"sub": user.user_name}, expires_delta=expires_delta)

    user_session = UserSession(
        user_id=user.id,
        token=app_access_token,
        expires_at=datetime.now(timezone.utc) + expires_delta,
    )
    db.add(user_session)
    db.commit()

    return {
        "access_token": app_access_token,
        "token_type": "bearer",
        "user": user,
    }
