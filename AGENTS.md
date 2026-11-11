# Agent Instructions

These instructions apply across Meeting Action Agent.

## Non-negotiable behavior

- Every retained action item must include an exact evidence quote found in the original meeting notes.
- Never invent owners, deadlines, decisions, priorities, or commitments. Unknown owner/deadline stays null and the status needs clarification.
- Suggestions are not decisions unless the notes explicitly record agreement.
- Treat model output as untrusted structured data; validate it before rendering or exporting.
- Keep local-model and OpenAI-compatible provider support configurable; never require a paid API for the basic code path unless the feature explicitly does so.

## Repository map

- `meetagent/`: extraction, validation, provider integration, CLI, and Markdown/JSON rendering.
- `app.py`: Streamlit interface.
- `docs/`: setup and usage guidance.
- `examples/`: safe example inputs/outputs.
- `tests/`: automated tests.

## Implementation rules

- Read the relevant module and tests before changing a contract.
- Keep model calls injectable/mocked in tests.
- Do not log prompts, transcripts, API keys, or provider authorization headers by default.
- Add schema-validation tests whenever a model-output field changes.
- Do not claim provider integration is tested unless a real endpoint was intentionally exercised; mocked tests prove only the adapter contract.
- Prefer narrow error types and actionable messages over swallowing exceptions.

## Validation

```bash
python -m pytest -q
meetagent --help
```
