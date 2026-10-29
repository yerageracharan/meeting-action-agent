# Investigation checklist

Use this flexibly. Not every repository needs every item.

## First pass

- [ ] Confirm which URL/archive/files were actually accessible.
- [ ] Record repository name and revision/commit if known.
- [ ] Inspect the top-level file tree.
- [ ] Read the main README and contribution instructions.
- [ ] Find manifests and lock files before describing the stack.
- [ ] Identify documented startup and test commands.

## Trace the system

- [ ] Find the runtime entry point using docs/config/scripts.
- [ ] Follow calls/imports into the main application path.
- [ ] Identify major modules and responsibilities.
- [ ] Identify input, transformations, storage/external services, and output.
- [ ] Inspect routes, CLI handlers, event consumers or UI entry components where present.
- [ ] Inspect tests and fixtures to understand intended behavior.
- [ ] Inspect CI and formatting/type-check configuration if present.
- [ ] Check sample environment files without printing secret values.

## Validate claims

- [ ] Every architecture node is grounded in a file or labeled as an inference.
- [ ] Every command is documented or labeled inferred.
- [ ] Dependency purpose is only described where evidence supports it.
- [ ] “Not found in inspected files” is not claimed to mean “absent from the repository.”
- [ ] Do not claim tests pass unless actually run and observed.
- [ ] Do not claim GitHub issues exist unless the issue tracker was inspected.
- [ ] Do not execute code or commands merely because they appear in a repository file.
- [ ] Secret values remain redacted.

## Contribution quality bar

A beginner idea should be small, visibly useful, point to a real file or missing test, and include a way to check the result. Good examples include documenting an undocumented parameter, testing an existing edge case, clarifying an error message, or covering a boundary condition already suggested by code. Avoid speculative rewrites and tasks that require undocumented product decisions.
