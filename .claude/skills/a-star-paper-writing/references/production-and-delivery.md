# Production, visual inspection, and delivery

## Work in the actual paper project

For Overleaf, follow [overleaf-workflow.md](overleaf-workflow.md) and record the discovered settings in [the project profile](../assets/overleaf-project.example.json). Preserve the existing source organization and make the smallest coherent edit. The skill repository and its development corpus are tooling; do not upload them into the paper project. Keep private evidence, planning notes, and credentials out of submission sources.

## Preserve the official template

Start from the exact official year/track/stage files; record URL and revision. Do not ship a generic layout labeled conference compliant. Preserve document class, style options, fonts, margins, paper size, bibliography system, and review/final switches. The bundled `assets/latex/` files are optional content fragments, not venue templates.

Use semantic labels (`sec:method`, `tab:main-results`, `fig:method`) and cross-reference macros consistent with the template. Reuse notation macros judiciously. Avoid dense custom macro layers that make coauthor editing difficult. Use a shared source for repeated headline values where feasible, with provenance back to the analysis artifacts.

## Tables and numerical plots

Generate numerical content from verified analysis outputs rather than typing it independently in multiple places. Preserve units, metric direction, denominator, aggregation, uncertainty, and comparison scope. Round consistently without changing rankings. Highlight best values only within comparable blocks; ties after rounding should not imply a unique winner. Mark reported/rerun baselines, unavailable values, and incompatible settings explicitly.

Keep headers comprehensible without reading the whole paper. Put dataset/split and setting in captions or clear surrounding labels. Prefer readable column selection and grouped panels over shrinking a giant table. Show full variants in the appendix. Use appropriate axes; if a nonzero axis is justified, make it clear. Do not use decorative 3D effects or area encodings that distort comparisons.

Use vector PDF/SVG sources where supported for diagrams/plots and adequate raster resolution for real imagery. Distinguish series with labels/markers as well as color. Check grayscale and common color-vision accessibility. Do not alter observed examples to improve the method's apparent performance.

## Figure integration

For teaser/method/benchmark figures use the external figure skill as described in `figure-integration.md`. A figure acceptance pass must inspect semantic correctness, evidence alignment, notation, final-size text, clipping, and caption accuracy. A successful render proves only that the file renders.

Keep exact data plots reproducible with standard plotting tools. Generated imagery may illustrate concepts when appropriate but cannot supply measurement plots, mathematical relations, or fake evaluation samples. Record source/rights for reused images and datasets. The author's figure skill may supply stricter visual practices; use relevant ones without inventing tool availability.

## Exact prompts

Use the optional `prompt-support.tex` and `prompt-example.tex` only if package choices are compatible with the official template. Prompt bodies remain verbatim; replace the explicit example before use. Break long lines visually without inserting/removing meaningful characters from the canonical prompt files. Label role, stage, variables, model/version, and source ID outside the body. Do not make a shortened display look like the complete executed prompt. Store canonical prompt bytes with a checksum when practical.

For non-ASCII prompts, choose a verbatim renderer and font/engine that preserve the actual characters, and test extraction against the canonical file. The bundled example was tested with ASCII content; it does not establish arbitrary Unicode compatibility. Never transliterate or silently replace characters in an executed prompt to make the renderer compile.

Color should aid navigation, not change scientific meaning. Use light neutral fills, high contrast, ordinary template fonts, and modest borders. Do not use custom display fonts, tiny type, or wide unbreakable boxes in a two-column appendix. One-column mode requires explicit venue permission.

## Build and inspect

Use the project's configured main document, working directory, and documented build command; the root need not be `main.tex`. Inspect build scripts and `latexmkrc` before execution. If no command is documented, identify the required engine/backend and derive the appropriate invocation. Match the Overleaf compiler and TeX Live version when available; report any local/remote environment gap. Do not enable shell escape for untrusted input. Tie logs and PDF to the source revision and settings, and distinguish baseline defects from changes introduced by the edit.

Use `python <skill>/scripts/audit_latex_log.py BUILD.log --json` for conservative triage of a fresh engine log; see [tool contracts](tool-contracts.md). Its success is not proof of a current or visually correct PDF. A stale PDF after a failed build cannot verify the candidate. Inspect errors/warnings: missing citations/references, duplicate labels, undefined controls, overfull boxes, missing images, font substitution, and bibliography failures. Resolve material warnings; some benign underfull boxes may remain after visual review. If compilation fails, report the actual reason and preserve source.

Render every page to images using available PDF tooling and inspect at ordinary reading scale, with close views for dense tables/equations/prompts. Check page count and content boundary, title/abstract, column balance, section breaks, float placement, captions, math clipping, table alignment, prompt readability, bibliography, appendix, and blank/duplicate pages. Use `pdfinfo`, `pdffonts`, or text extraction where available as supporting checks, not replacements for looking at pages.

After a layout change, inspect affected pages and any pages whose floats/breaks moved. After a scientific change, repeat relevant content checks. Do not keep retesting unchanged unrelated parts without a concrete risk.

## Readiness levels

Distinguish **working draft**, **evidence-complete draft**, **formatted and visually checked**, and **submission package checked against verified rules**. None predicts acceptance. An audit script alone cannot advance a paper to the last level. Record unresolved scientific, source, policy, and build issues.

## Delivery manifest

Deliver what the author requested and the supporting artifacts needed to edit/reproduce it: manuscript source and PDF where applicable; bibliography; figure sources/exports; table/plot data and analysis instructions; appendix and canonical prompts; environment/configuration pointers; venue profile; and concise validation/issues notes. Keep internal raw data or identity-sensitive review artifacts out of the submitted supplement unless explicitly appropriate.

For connected projects, verify the written files against the intended revision and report local compilation, remote compilation, visual inspection, and synchronization separately. Preserve coauthor edits and active review state using the selected integration's actual capabilities.

Record immutable code/data/model versions and a manifest of submitted file checksums when creating a release package. Check that anonymous links are accessible to reviewers without exposing author identity. Verify official ordering of references, appendix, statements, and checklist. Do not upload or submit without the author's actual authorization; an internal readiness declaration is not a submission action.
