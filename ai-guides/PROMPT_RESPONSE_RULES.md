# Prompt Response Rules

_Changelog: 2026-04-05 - Initial version._

## Response Format

- Responses will be concise and directly address the prompt.
- Clarifying questions will be asked if the request is ambiguous or lacks critical information.
- Code will be provided using appropriate markdown blocks.

## Mandatory Sections for Code Output

When providing new or modified code, the response will be structured as follows:

- **File path**: The full, relative path to the file being discussed.
- **Purpose**: A brief explanation of the file's role.
- **Dependencies**: Key imports and their purpose.
- **Implementation**: The code itself, with comments for complex logic.
- **Tests/validation**: A description of how to test or validate the changes.

## Guide File Updates

- After every response where code or architecture is changed, the relevant guide files in `/ai-guides/` will be updated automatically as per `UPDATE_PROTOCOL.md`.
- The response will conclude with a list of updated files.
