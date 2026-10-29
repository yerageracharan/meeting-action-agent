# Codebase Onboarding Report — Template

Replace every placeholder with evidence from the inspected repository. Delete sections that do not apply, and label missing information as unknown. This template is not an analysis of a real repository.

## 1. The 30-second explanation

**In one sentence:** [What the project does, supported by README/source.]  
**Who it seems to serve:** [Supported use case or “not stated”.]  
**Evidence inspected:** [URL or archive, branch/revision if known, files.]  
**Confidence:** [High / Medium / Low with reason.]

## 2. What was inspected

- Source: [URL or uploaded archive]
- Revision: [Commit/branch or unavailable]
- Read: [Important file paths]
- Not inspected / inaccessible: [List or “none known”]

## 3. Architecture map

Use a small Mermaid graph based only on verified components:

~~~mermaid
flowchart TD
    A[Actual input] --> B[Verified entry point]
    B --> C[Observed module or service]
    C --> D[Actual output]
~~~

Explain each arrow in plain English and cite supporting files. Replace the illustrative nodes before sending.

## 4. How the program starts

1. [Documented launch command and source]
2. [Entry point function/file and evidence]
3. [Next important call]
4. [Output or side effect]

Mark inferred steps. Give separate paths if there are multiple entry points.

## 5. Important files, functions and classes

| File / symbol | Plain-English job | Inputs / output or effect | Evidence | Confidence |
|---|---|---|---|---|
| [path + symbol] | [explain] | [explain] | [path/line if available] | [level] |

## 6. Setup, run and tests

### Requirements
[Only those supported by manifests, lock files or docs.]

### Install and run
[Commands from source, annotated in plain language. Label inferred steps.]

### Tests and quality checks
[Paths, configured test scripts, and what tests appear to cover. Do not claim they were run unless they were.]

### Configuration
| Variable / setting | Purpose shown in source | Required? | Safe handling note |
|---|---|---|---|

## 7. Dependencies explained

| Dependency | Evidence | Apparent role | Runtime/dev/optional | Confidence |
|---|---|---|---|---|

## 8. Beginner-friendly first contributions

### Idea 1: [small task]
- **Why it helps:**
- **Files to inspect:**
- **Smallest useful change:**
- **How to verify:**
- **Difficulty:** Easy / Moderate — [reason]
- **Assumptions to confirm:**

Repeat for 3–5 grounded ideas. Do not call them existing GitHub issues unless the issue tracker was inspected.

## 9. Unknowns, risks, and safety

- [Unanswered question and why it remains unknown.]
- [Potential config or unsafe-execution risk, without revealing secrets.]
- [Important behavior not verified by static source inspection.]

## 10. Recommended next step

[One concrete, low-risk action.]
