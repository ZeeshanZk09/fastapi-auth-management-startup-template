from sqlmodel import create_engine, Session, SQLModel
from app.config import settings

engine = create_engine(settings.DATABASE_URL, echo=settings.IS_LOCAL, future=True)


def init_db():
    from app.models import user, session, account  # noqa
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
