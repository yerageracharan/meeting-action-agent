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

## Change ownership and proof

- Keep one authoritative owner for each domain rule and each persisted state. UI, CLI, MCP, and provider adapters translate inputs and outputs; they must not reimplement business policy or become competing sources of truth.
- Before changing a contract, trace the input through its owner to every consumer. Update callers, schemas, examples, docs, and regression tests together. Remove superseded paths unless a documented public-compatibility requirement keeps them.
- Keep optional external model/provider integrations behind adapters. Use injected or mocked adapters for deterministic unit tests; label live network/provider checks separately and never describe a mock as live verification.
- Validate untrusted user, model, file, and network data at the boundary. Preserve the product's evidence/provenance rules and reject malformed inputs rather than silently inventing defaults.
- Verify the supported user entry point and at least one relevant failure path. Report exact commands and results; CI on a different commit SHA is not proof for the current change.
- Keep the root README as the user entry point, `docs/README.md` as the documentation map, and focused guides as the owners of detailed contracts. Update links when files move. Do not hand-edit generated output when a source or generator owns it.


## Repository automation rules

- Treat files under `.github/workflows/` as production code. When changing a workflow, inspect the triggered run for the exact commit SHA; a prior green run is not proof for a newer commit.
- Pin third-party GitHub Actions to full 40-character commit SHAs and keep the upstream release tag in a trailing comment. Do not replace a pinned SHA with a floating major-version tag.
- Use the least-privilege `permissions` block. Default to read-only; grant write access only to the specific job that must publish or commit generated output.
- Give every job a finite `timeout-minutes`. Add a clear `concurrency` group for expensive or supersedable work; cancel stale pull-request runs, but do not cancel workflows whose purpose is to publish a completed artifact or evidence.
- Keep workflow logs and uploaded artifacts free of secrets and personal data. Set retention to the shortest period that still serves the evaluation or debugging purpose.
- Rely on the existing Dependabot configuration for action updates, then review release notes and run the affected workflow before considering the update complete.
