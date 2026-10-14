# Second review: writing quality, Overleaf, and audit reliability

Reviewed and implemented on **2026-09-17**, against repository baseline commit
`bf97a58eb250b6cbf32583e3a8576f56c3d27045`. This records a bounded review of the
full skill, targeted fixes, executable regressions, and fresh agent tasks. It is
not an acceptance prediction or proof that every future manuscript will be sound.
The [initial validation report](validation-report.md) remains historical.

## Findings and implemented changes

| Finding | Resolution | Evidence / check |
|---|---|---|
| The previous initializer produced Markdown, with no primary workflow for the user's intended Overleaf environment. | TeX is now the default. New projects get a generic compilable root, section files, ordered appendix, empty bibliography, exact-prompt directory, and an unresolved Overleaf profile. Existing projects are edited in place. | Ten initializer tests, including real compilation and titles containing TeX metacharacters; manual two-page scaffold inspection. |
| A repository change could be confused with a connected Overleaf update; settings and coauthor changes needed explicit treatment. | Added capability-based connector, direct Git, GitHub bridge, and source-handoff routes. Discover the actual root/engine/backend/version, preserve review state, reconcile base/current/proposed changes, and distinguish source, local/remote build, visual, and synchronization status. | Official documentation linked in [Overleaf workflow](../../overleaf-workflow.md); independent handoff task below. No live Overleaf integration was tested. |
| Novelty and correctness did not sufficiently operationalize contribution significance. | Added a separate appraisal: what belief, decision, or capability changes at the demonstrated scale, compared with the closest alternative? No score or state-of-the-art requirement. | Reviewed argument/evidence guidance and synthetic prose examples. |
| An editor's missing access could leak into manuscript prose as an alleged study limitation. | Manuscript uses author voice; editorial notes carry access and verification gaps. Actual one-run, missing-measurement, or other scientific limitations remain in the paper. | Fresh narrow TeX-edit task preserves supplied facts and separates private-log access status. |
| Local edits could trigger unnecessary full-project scaffolding or auditing. | Narrow edits preserve macros, labels, citations, and file organization; inspect affected evidence and build output without requiring unrelated ledgers. | Fresh TeX task changed only the requested existing file. |
| Benchmark rigor needed a clearer link from score to the claimed capability. | Added conditional shortcut controls, valid transformations, scorer/aggregation sensitivity, and coverage/difficulty analysis chosen for the actual claim. | Guidance review; no experiments or scientific results were fabricated. |
| Some dated venue retrieval gaps were being treated too broadly, and official sources differed. | Refreshed accessible primary sources; preserved unresolved discrepancies and unavailable fields. Unknown unrelated formatting no longer blocks otherwise permitted drafting. | Dated sources and remaining gaps in [venue policy](../../venue-policy.md). |
| Malformed URL ports and embedded control characters could pass the evidence audit. | Validate port syntax/range and reject control characters; retain valid explicit ports. | Two new paper-audit regression tests. |
| Corpus flags, duplicate notes, identity aliases, and scope/date inconsistencies could overstate recorded reading or crash. | Strict record/type/date checks, canonical identities, unique notes, and cross-file scope reconciliation, retaining custom proceedings-note support. | Twenty-one corpus regression tests; original corpus passes unchanged. |
| A new log helper initially missed recovered file/line TeX errors and reused an earlier PDF marker when a later compiler invocation was interrupted. | Recognize generic file/line diagnostics with warning/advisory exclusions; require completion evidence in the final engine invocation and retain earlier diagnostics conservatively. | Ten log tests, including actual recovered errors, missing citations, interrupted final run, and two completed runs. |

## Executable validation

Run from the repository root:

```bash
python -m unittest discover -s skills/a-star-paper-writing/tests -v
python skills/a-star-paper-writing/scripts/audit_corpus.py
```

Observed full-suite result: **67 tests passed**, no skips, in 8.286 seconds:

- 26 paper-tool tests, including the original checks and new URL regressions.
- 21 corpus tests covering malformed shapes/types, unique identities, scope links,
  valid custom inputs, date consistency, and preservation of the real index.
- 10 TeX-initializer tests, including no-overwrite behavior, Markdown compatibility,
  source graph/profile, and actual pdfLaTeX builds.
- 10 LaTeX-log tests, including actual compiler diagnostics and interrupted runs.

The skill package validator passed. All checked relative Markdown file links
resolved. Examples/profile JSON parsed. The generic TeX scaffold was built with
pdfTeX 1.40.25 using shell escape disabled; its fresh log returned no recognized
issues. Both rendered A4 pages were inspected: title special characters, draft
banner, abstract placeholder, section headings, and ordered appendix rendered
without clipping. This empty scaffold is deliberately not a polished manuscript
or official venue template.

## Fresh forward tasks

Both agents started from the skill and supplied fixtures without inheriting the
implementation discussion. Inputs are explicitly synthetic. These are two
observed executions, not a statistically representative benchmark.

### Existing TeX abstract edit

[Input](../../../tests/scenarios/tex-section-edit/input/author-notes.md),
[observed abstract](../../../tests/scenarios/tex-section-edit/observed/abstract.tex),
[editorial note](../../../tests/scenarios/tex-section-edit/observed/editorial-note.md).

The agent changed only `sections/abstract.tex` in a copy, preserving the method
macro, root document, introduction, citation key, and all supplied numbers. It
removed an unsupported universal superiority claim, described the gating
mechanism and matched comparison, retained the one-seed/one-dataset scope, and
kept unavailable private-log access in its editorial note. No uncertainty estimate
or significance test was invented.

Baseline and candidate pdfLaTeX builds succeeded. Both logs exposed the same
pre-existing unresolved `selective2017` citation; the agent reported this rather
than claiming a clean whole paper or inventing a bibliography entry. The fresh
one-page candidate PDF was visually inspected with no abstract overflow or
clipping. This test establishes a useful bounded edit, not publication quality.

### Stale Overleaf/GitHub snapshot and failed build

[Input](../../../tests/scenarios/overleaf-handoff/input.md),
[observed response](../../../tests/scenarios/overleaf-handoff/observed-output.md).

The agent combined the approved spelling correction with the coauthor's newer
latency-budget wording. It retained the supplied `manuscript.tex`, XeLaTeX,
TeX Live 2025, and Biber settings without claiming remote readback. It identified
the missing authentic figure as the build blocker, rejected the old PDF as
candidate validation, and reported source prepared with application and
synchronization pending. No real account or remote mutation was performed.

## Research continuity and remaining limits

The corpus and original reading notes were not edited. The corrected auditor
reports exactly **622 unique papers**, **622 abstract inspections**, **602
abstract-only notes**, **20 targeted narrative/structure reviews**, **557 HF
monthly discoveries**, and **50 official ICML metadata crosschecks**. One partial
abstract-source limitation remains explicitly recorded. Full-paper reading and
visual-paper review counts remain **zero**; this review did not expand reading
depth or claim otherwise.

The project profile is a workflow record; it is not a connector implementation
or an automatically validated schema. Log triage is conservative pattern
recognition and cannot prove compiler success, freshness, visual correctness,
or source/Overleaf synchronization. Live project integration, official-template
builds, all bibliography engines, every TeX package/Unicode combination, and
real concurrent coauthor writes were not end-to-end tested. Each actual paper
still needs scientific review, verified venue rules, a current build, visual
inspection, and observed synchronization evidence where applicable.
