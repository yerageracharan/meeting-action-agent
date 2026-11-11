# Contributing

Thanks for improving Meeting Action Agent. The central product promise is careful extraction: useful follow-up work without invented meeting facts.

## Before changing code

1. Search existing issues and commits for overlapping work.
2. Open an issue before substantial new features or schema changes. Include the user problem, proposed behavior, alternatives, and validation plan.
3. For defects, provide a minimal notes sample, model/provider configuration (redacted), exact command, expected output, actual output, and logs.
4. Keep changes focused; do not mix unrelated refactors and dependency changes.

## Development setup

Python 3.10 or newer.

```bash
python -m venv .venv
# macOS/Linux: source .venv/bin/activate
# Windows PowerShell: .venv\\Scripts\\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[test,ui]"
```

## Validation

```bash
python -m pytest -q
meetagent --help
```

Add focused tests for malformed JSON, missing fields, unsupported evidence, null owners/deadlines, and rendering. Use deterministic mocked model responses; tests must not call paid APIs or external model endpoints.

## Engineering expectations

- Validate the model response at the boundary before downstream code consumes it.
- Keep evidence quotes byte-for-byte present in the original notes where the contract requires exact evidence.
- Escape untrusted text in Markdown/HTML output.
- Keep local provider errors actionable without exposing credentials.
- Update README/docs when commands, supported providers, schema, or output format changes.

## Pull requests

Use the pull-request template. Include the problem, user impact, exact tests/commands and results, and remaining limitations. Link related issues where applicable.

## Sensitive data

Never commit meeting transcripts, personal information, credentials, or unredacted provider logs. Use [SECURITY.md](SECURITY.md) for private vulnerability reports.
