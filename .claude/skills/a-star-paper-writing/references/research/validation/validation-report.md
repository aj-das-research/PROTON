# Package validation

Date: 2026-09-17. This report concerns the skill package, not the quality or acceptance of a research paper.

## Deterministic tools

The dependency-free Python tools were executed through 24 observable CLI tests. They cover a valid registered evidence record; empty projects; unsupported/unlinked claims; duplicate/dangling IDs and duplicate JSON keys; finite numbers; missing/empty/modified artifacts; safe relative paths and symlinks; malformed types; source/date requirements; unknown venue/AI-assistance rules; proof support for theoretical guarantees; and refusal to overwrite an existing project. All 24 passed after the fixes described below.

Run from the skill directory:

```bash
python -m unittest discover -s tests -v
```

The tools explicitly say that mechanical success does not certify truth, scientific validity, coverage of manuscript claims, policy compliance in actual usage, PDF layout, submission readiness, or acceptance. Test values and example citations are synthetic fixtures, not scientific results.

## Independent forward tasks

Two fresh-context agents received only the skill, a realistic request, and small raw note fixtures. They were not given expected answers. The scenarios and their observed outputs are preserved under `tests/scenarios/`.

| Scenario | Observed behavior | Assessment and limit |
|---|---|---|
| Adaptive sampling method: small positive mean test difference, fewer reported calls, negative shifted-domain result, missing uncertainty/logs, requested 11 pages/one-column appendix against supplied 8-page/two-column rules | Computed 0.2 percentage points and 33.3% fewer reported calls; retained 6-point shift loss; did not invent significance, timing, example outputs, or novelty; scoped figures and adapted page/column plan | Appropriate bounded draft. Underlying experiments and supplied venue profile remain unverified; this was not a real submission. |
| Static contradiction benchmark: document variants randomly split, missing scores/agreement/prompt inventory, supplied editing-only AI policy, no author draft | Withheld prohibited manuscript generation, produced a separate editorial plan, preserved only the provided prompt, flagged split leakage risk, missing records, and unavailable figure dependency; did not claim readiness | Appropriate task routing and useful partial work under the supplied constraints. Leakage was identified as a risk requiring manifest inspection, not declared proven. |

These are two behavioral samples, not a broad measured success rate. They do not demonstrate guaranteed behavior across projects or models.

## Independent package review and resolutions

The original review is preserved in `independent-package-review.md`. All four reported issues were addressed:

1. Replaced the blanket interactive-environment requirement with separate static-task and interactive contracts.
2. Added a theory-specific architecture, theorem/proof dependencies, assumption alignment, bounds, and proof-review guidance.
3. Added factual human-study consent, approval/exemption, compensation, privacy, and recruitment reporting where applicable.
4. Fixed the project-root symlink-loop error to return a structured invalid-input report and exit 2; added and ran a regression test.

The independent reviewer also exercised malformed input fields without finding further exceptions. This is targeted validation, not exhaustive fuzzing or a security certification.

## LaTeX content fragments

Compiled the prompt and table fragments with pdfLaTeX/latexmk in a generic two-column article fixture. Rendered the resulting one-page PDF and visually inspected it after correcting a run-in heading spacing problem. The final build had no overfull/underfull boxes or unresolved references; fonts were embedded. Prompt text, wrapping, light box, and blank table cells remained legible at reading size.

This validates the provided example in the tested generic harness only. It does not prove compatibility with every official conference template, arbitrary Unicode prompt, long table, or submission rule. Full paper/appendix fragments are content scaffolds and contain no factual results. Use the actual venue template and visually inspect the final paper separately.
