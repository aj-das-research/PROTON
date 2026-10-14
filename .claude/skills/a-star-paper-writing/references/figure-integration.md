# Figure-skill integration

Read this when planning or producing the paper's scientific figures. Delegate figure design to the user's `paper-figure-creation` skill when available; keep the manuscript, evidence, notation, and captions synchronized here. This is a handoff contract, not a second figure renderer.

## Resolve the dependency honestly

Preferred dependency: [Mishrakshitij/paper-figure-creation-skill](https://github.com/Mishrakshitij/paper-figure-creation-skill).

1. Check the environment's available skills for the exact capability `paper-figure-creation`; read that installed skill through its declared provider or path. Do not assume its repository name is a callable tool.
2. If it is not installed, use an already accessible checkout or fetch the repository's `skills/paper-figure-creation/SKILL.md`, then its relevant references and scripts. Resolve relative paths against that skill directory. Repository access alone does not install or activate a skill.
3. Record the source location and installed version or repository commit in the figure brief. If using a checkout, verify its commit and preserve local edits. If fetching remote files, pin them to the same commit so the instructions, assets, and scripts are mutually consistent.
4. If access or required rendering capabilities are unavailable, finish the figure brief, caption draft, evidence mapping, and manuscript placeholders. Report the exact unavailable step. Do not claim invocation, rendering, source review, or visual inspection occurred unless it did.

Inspected integration baseline: commit `66739085a15c2cb7c85a1522e8811bf0e0af6161`, retrieved 2026-09-17. [Pinned entrypoint](https://github.com/Mishrakshitij/paper-figure-creation-skill/blob/66739085a15c2cb7c85a1522e8811bf0e0af6161/skills/paper-figure-creation/SKILL.md). Re-read the resolved version at execution time when its contract differs; this snapshot is provenance rather than a requirement to remain on an old version.

At that snapshot, relevant paths are `references/evidence.md`, `references/spec-format.md`, `references/delivery.md`, and `assets/benchmark-brief.md`. Its rendering scripts are `scripts/validate_evidence.py` and `scripts/render_figure.py`; these are filesystem scripts, not presumed MCP tools. Run them only after resolving the actual skill directory and inspecting the selected spec contract. An instruction such as “use $paper-figure-creation with this brief” is an agent handoff, not proof of execution.

## Figure and table rules from the author and the lab (always)

These are the author's recurring corrections (September 2026) and Nils Lukas's
figure rules. Check them before accepting any figure.

**Faithful and real**

- The figure matches the method exactly: initialization, what is frozen and
  what is trained, the data flow and the order of steps. The author caught
  "figure 3 says GROVE initialisation is base model which never is the case".
- Plots come from result files through code, never typed-in numbers or TikZ
  mock-ups. Examples are real inputs and outputs from runs.
- Show an entry only when every method in the figure has that entry. Missing
  runs go to the appendix, or the entry is dropped.

**Clean**

- Zero tolerance for geometry defects: text overflowing a box, overlaps,
  connectors cutting through boxes or text, clipped glyphs, text boxes that
  render as empty quotes. Inspect every block at print size and enlarged, and
  report each defect by block and element.
- Build diagrams as flows of icons and arrows with minimal text and generic
  labels ("LLM agent", not a model id). Drop seed numbers, "8x", asterisks and
  formulas as labels. A combined top-down and left-to-right flow reads best.
- Improve incrementally. Do not redesign a figure the author likes; keep the
  layout and encodings when the data change, and update every label.

**Legible and consistent**

- No figure text below about 5.3 pt at print size. Labels are about 6 pt and
  panel titles about 7.5 pt.
- Use one colour per method or task across all figures, with the proposed
  method starred in a fixed hot colour and "(ours)" in the legend. Keep one
  scale per quantity across figures and tints at 15% or less. Unify the style of
  all result plots, which must not look like default spreadsheet charts.
- Every axis and every table metric header carries a better-direction arrow
  (↑ or ↓). Bold the best value, shade our rows, and put $n$ and the seed
  count in the legend or caption.
- Heatmaps show percentages only, keep one orientation and one colour
  direction across games or tasks, and take about 30% of a page at most.

**Compact**

- Figures fill the text width (`width=\linewidth`) unless they are wrapped.
  Put three or four plots in one row. Use `wrapfigure` or `wraptable` for
  smaller floats. Never leave a page holding only one figure.
- The teaser, Figure 1, is on page 1 with the introduction. It is referenced
  from the introduction, and it is numbered 1.
- Captions open with a bold takeaway sentence, stay short and concrete, and do
  not repeat what the text explains.
- Every figure and table is referenced from the text, and the point comes
  before the figure reference.

**Tables**

- Tables are complete: fill empty cells or drop the column. The closest
  baselines are in the main table, with a frozen or base reference row.
  Mismatched setups go in separate labelled panels.
- ± appears on every row. Leading zeros everywhere. Decimals are consistent.
- A table must not overflow its column, and it is not shrunk with
  `\resizebox`. For every main-text table, ask whether it should be a graph,
  whether its finding fits in two sentences, or whether it belongs in the
  appendix.

## Choose the applicable figure roles

The user prefers a strong visual narrative built around these three roles. Select each role only when the science provides it; assign final figure numbers after manuscript order is settled.

| Role and likely slot | Question it should answer | Required source material | Omit or adapt when |
| --- | --- | --- | --- |
| Introduction teaser | What concrete problem changes, what is the idea, and what evidence supports the takeaway? | A sourced or clearly illustrative example; a bounded claim; comparable results if a quantitative panel is used | A conceptual teaser suffices before experiments exist; unsupported result panels remain absent or explicitly draft |
| Method or architecture | What actually computes the output, and where does the contribution enter? | Inputs and outputs, ordered operations, branches/loops, states, losses, training/inference distinction, equations or implementation | A benchmark-only or analysis-only paper has no proposed algorithm; show the substantive protocol only if it aids understanding |
| Benchmark or environment setup | How are tasks created, what can the model observe or do, and how is success scored? | A described setup in the manuscript or supplement, with source location and new/adapted/existing status | The paper merely names standard datasets or reports benchmark scores; do not invent a setup or claim existing infrastructure as novel |

For a benchmark paper, the teaser and setup may carry the main story without a method diagram. For a method paper on standard datasets, the teaser and method may be sufficient. Additional plots and tables serve specific evidence questions rather than a quota. Avoid making the teaser, method, and setup repeat the same boxes.

The inspected figure skill prefers an evidence-heavy quantitative teaser, starting near 35% concept and 65% evidence. Treat that as a composition preference when results exist. It does not apply to the method or setup figure and never justifies inventing numbers.

## Prepare one handoff brief per figure

Extract from existing project artifacts before asking for missing facts. Supply paths or exact source locations, not an unsupported prose summary of the science.

```yaml
figure_id: fig-method
role: method
status: draft
dependency:
  name: paper-figure-creation
  resolved_location: null
  version_or_commit: null
manuscript:
  source_file: null
  relevant_sections: []
  label: fig:method
  target_width: null
  target_height: null
  venue_template: null
purpose:
  reader_question: null
  supported_takeaway: null
  claim_ids: []
sources:
  evidence_ledger: null
  result_ids: []
  source_ids: []
  exact_locations: []
semantics:
  canonical_component_names: {}
  notation_source: null
  example_id: null
  example_status: null
  visible_inputs: []
  operations: []
  outputs: []
  training_only_elements: []
  inference_access: []
  immutable_facts: []
delivery:
  output_directory: null
  canonical_editable_format: null
  manuscript_export_format: pdf
  caption_file: null
unresolved: []
```

This is an empty drafting schema, not a valid final figure specification. Replace the applicable nulls, remove irrelevant fields, and adapt to the dependency's actual input format. Keep uncertainty explicit rather than inserting plausible defaults.

For a setup, additionally record eligibility and source section, new/adapted/existing status, instance construction, split assignment, unit of evaluation, model-visible information, evaluator-only information, output/actions, scoring unit and aggregation. Interactive environments also need observation, state transition, reset/persistence, budget, and termination. Static benchmarks do not acquire an artificial interaction loop. Use the dependency's `assets/benchmark-brief.md` when it is present.

For quantitative figures, additionally pass metric direction/unit, method/checkpoint identity, dataset version/split, evaluation conditions, resource conditions, uncertainty definition, raw or reported values, and exact table/file coordinates. For qualitative panels, pass the same sample IDs and display processing for all compared methods, plus the selection rule. Distinguish measured output, annotation, and illustrative reconstruction.

## Preserve evidence and identities across the boundary

The paper's authoritative evidence ledger remains authoritative. A layout change must not change experimental facts. Preserve source IDs, result IDs, claim IDs, dataset/split names, metric units, and example IDs across tables, plots, manuscript text, and the figure brief.

If the dependency's schema needs different identifiers, create an explicit one-to-one mapping and retain the original IDs as provenance. Detect collisions; do not silently rename or merge results with the same display name. A result is specific to its model/checkpoint, data, protocol, seed/run aggregation, and budget. Two results called “Ours” are not interchangeable.

Copy or transform evidence programmatically when practical. Record the transformation for percent conversion, normalization, aggregation, smoothing, or logarithmic axes. Keep the original values and precision. Missing measurements stay missing. Do not manually retouch labels, error bars, axis limits, rankings, or numbers to make a claim more favorable.

Do not duplicate a result ledger into independently editable versions that can drift. Prefer references to the canonical ledger; when the renderer requires embedded data, preserve the source revision or content hash and regenerate the embedded copy when the ledger changes. Record which manuscript and evidence versions the export represents.

Caption claims have the same evidence standard as body prose. A figure title can overclaim even when every plotted value is correct. Recompute percentage-point versus relative improvements; check cost-quality tradeoffs and unmatched conditions. Treat a validator's success as a structural check, not scientific verification.

## Accept the returned figure only when its contract holds

| Acceptance area | Concrete check |
| --- | --- |
| Scientific fidelity | Trace one example through every operation or environment transition; verify information boundaries, losses, trainable/frozen states, and evaluation timing |
| Evidence fidelity | Match plotted values and annotations to ledger IDs and exact source locations; preserve uncertainty, missing data, limitations, and unfavorable results |
| Manuscript consistency | Component names, notation, equation references, sample identity, dataset splits, model versions, colors, and labels match the current draft |
| Comprehension | A reader can answer the role's question from the figure and caption; novelty appears in an operation or protocol rather than an unexplained “Ours” box |
| Publication size | Inspect the actual export at the template's insertion width and in the compiled paper; verify labels, line weights, crop, contrast, and grayscale distinctions |
| Editability | Keep the canonical SVG, plotting code/spec, TikZ, or native diagram source with data references; PNG alone is insufficient |
| Delivery | Include the requested figure export, preview, source, caption, provenance/review record, and any unresolved issue |

Use vector PDF for LaTeX when suitable, retain editable sources, and use a high-resolution preview for review. Select other output formats for the actual authoring environment. Scientific charts and exact mechanism wiring should be rendered from data or vector/code sources; generative imagery may support clearly labeled illustrative content only where the target venue permits it, without supplying numerical or structural truth. Do not import another publisher's typography, size, or generative-image rules into the target conference.

For quantitative panels, identify the experimental unit, aggregation, uncertainty, and comparison setting in the caption or an unambiguous nearby key. Do not let a reader infer that a selected operating point is a complete tradeoff curve. For a multi-panel figure, give each panel a distinct evidential job and order the caption accordingly. A reader should be able to recover the displayed finding without scanning unrelated methods paragraphs.

The writing agent owns the final caption and manuscript integration even when the figure agent drafts them. Each caption should identify the task or mechanism, explain panels and encodings, state conditions and uncertainty when material, and give a scoped takeaway. Do not repeat the whole method section. Reference the figure near the point where the reader needs it.

## Coordinate revisions without drift

Return figure review requests as specific defects: “the loss reaches the frozen encoder although the method says stop-gradient,” “sample 0182 differs between rows,” or “the legend is illegible at column width.” Include the source that resolves the defect. Avoid vague requests to make a figure more impressive.

When experiments change, update the canonical ledger first, then regenerate affected tables/plots, caption claims, abstract numbers, introduction claims, and FAQ answers. When methods change, update the notation and architecture brief before changing arrows. Re-render and inspect the changed figure in the compiled paper. A figure previously marked reviewed becomes stale when its data, semantics, caption, or scale changes.

The final figure report should distinguish `draft`, `evidence verified`, `rendered`, and `visually inspected` states. If a needed step is unavailable, preserve the usable outputs and report the gap. Do not silently upgrade a draft into a submission artifact.

## Inspected upstream sources

- [Entrypoint at the inspected commit](https://github.com/Mishrakshitij/paper-figure-creation-skill/blob/66739085a15c2cb7c85a1522e8811bf0e0af6161/skills/paper-figure-creation/SKILL.md): role routing, brief, design/review workflow.
- [Evidence contract](https://github.com/Mishrakshitij/paper-figure-creation-skill/blob/66739085a15c2cb7c85a1522e8811bf0e0af6161/skills/paper-figure-creation/references/evidence.md): result provenance, comparability, arithmetic and uncertainty.
- [Specification contract](https://github.com/Mishrakshitij/paper-figure-creation-skill/blob/66739085a15c2cb7c85a1522e8811bf0e0af6161/skills/paper-figure-creation/references/spec-format.md): renderer modes and declared setup fields.
- [Delivery guidance](https://github.com/Mishrakshitij/paper-figure-creation-skill/blob/66739085a15c2cb7c85a1522e8811bf0e0af6161/skills/paper-figure-creation/references/delivery.md): editable outputs and final manuscript inspection.
- [Setup brief](https://github.com/Mishrakshitij/paper-figure-creation-skill/blob/66739085a15c2cb7c85a1522e8811bf0e0af6161/skills/paper-figure-creation/assets/benchmark-brief.md): conditional environment handoff.

This integration document is original guidance derived from inspecting those interfaces; it does not vendor the dependency or assert that figure generation has already run.
