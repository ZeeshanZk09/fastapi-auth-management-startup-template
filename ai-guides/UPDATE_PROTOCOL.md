# Update Protocol

_Changelog: 2026-04-05 - Initial version._

This protocol defines the mandatory process for updating the guide files located in the `/ai-guides/` directory.

## Process

After **every** user prompt that results in a change to the codebase, architecture, or established conventions, the following steps must be executed:

1.  **Identify Affected Guides**: Analyze the user's request and the resulting changes to determine which guide files are now out of date or incomplete.
    - Example: A new FastAPI endpoint affects `PROJECT_CONTEXT.md` (new route) and potentially `TECH_SPECIFIC_NOTES.md` (new FastAPI pattern).
    - Example: A change in testing strategy affects `CODING_CONVENTIONS.md`.

2.  **Update the Guide(s)**:
    - For each affected file, add a new entry at the top of the file under a "Changelog" section. The entry should be dated (YYYY-MM-DD).
    - Append the new information or modify the existing content to reflect the changes accurately.
    - Keep the guides concise and actionable.

3.  **Report Updates in Response**:
    - In the final response to the user, include a dedicated section at the end:
      ```
      ### Guide Files Updated
      - **`[FILE_NAME]`**: Summary of the change.
      - **`[ANOTHER_FILE_NAME]`**: Summary of the change.
      ```
    - This provides transparency and ensures the user is aware of the evolving documentation.

This is a non-negotiable, automated step. Permission will not be asked.
