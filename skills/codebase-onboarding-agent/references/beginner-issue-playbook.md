# Beginner contribution playbook

Generate contribution ideas from observed friction or gaps. Never apply these patterns blindly.

## Documentation gap

Use when a real command, option, configuration value or behavior exists in source but is unclear or missing from setup docs.

- Scope: update one paragraph or example.
- Evidence: source symbol/config plus existing docs.
- Verification: compare with the manifest or safely follow the updated instructions.

## Missing edge-case test

Use when a function has a visible branch or boundary condition but inspected tests do not appear to cover it.

- Scope: add one focused test.
- Evidence: function logic and current test files.
- Verification: run the documented test command if safe and available. Otherwise provide the command but say it was not run.

## Error message improvement

Use when a confirmed failure path omits a detail that would help a user recover.

- Scope: improve one message without changing behavior.
- Evidence: exception path and caller.
- Verification: existing tests plus an error-path test if appropriate.

## Example or fixture

Use when a real API/config format is supported but an example is missing or unclear.

- Scope: add one minimal non-secret example.
- Evidence: schema/parser and current docs.
- Verification: ensure the example matches the actual schema.

## Small validation improvement

Use when source already validates a value but a directly related edge case is missing.

- Scope: extend one validation rule, not redesign validation.
- Evidence: current code, tests and contract.
- Verification: positive and negative tests.

## Avoid as a first issue unless strongly justified

- Large refactors, migrations, or new frameworks.
- New database, authentication, or deployment architecture.
- Security changes requiring expert review.
- External integrations needing credentials or product approval.
- “Add more tests” with no named behavior or fixture.
- Fixes based only on assumptions about product intent.
- A task described as an existing issue without checking the live issue tracker.
