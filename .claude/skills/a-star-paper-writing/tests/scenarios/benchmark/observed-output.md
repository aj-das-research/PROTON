# AuditBench: editorial plan, prompt record, and readiness review

**Status: not submission-ready.** The supplied notes support a benchmark-development description, but not performance findings, annotation-reliability claims, or a claim of generalization to unseen source documents.

**Writing constraint.** The author-supplied target rule permits polishing author-written text and prohibits generating manuscript prose (`input/research-notes.md`, lines 19–21). No draft paragraphs or official policy source are supplied. The A-Star Research Paper Writing skill requires editing-only assistance under that rule. This document therefore provides a separate editorial outline, research critique, literal prompt record, and figure handoff plans. It does not supply newly generated Introduction, Method, or caption prose for insertion into the manuscript. Author-written sections are needed for a polishing pass. Official venue/year/track/stage rules, template, and disclosure requirements remain unverified; no external verification was attempted, as requested.

## 1. Evidence boundary and constructive positioning

Only `input/research-notes.md` was supplied as project evidence. Counts and procedural statements below are author-reported, not independently validated against data or logs.

| ID | Supplied information | Source location | Permissible use and boundary |
| --- | --- | --- | --- |
| N1 | AuditBench concerns contradictions across revisions of the same source; contribution is a dataset and annotation protocol. | Lines 3–5 | Center the benchmark's measurement purpose. Do not introduce a new QA algorithm. |
| N2 | 120 source documents; 10 revision-pairs per source; 1,200 pairs in total. | Lines 7–8 | Arithmetic is consistent: 120 × 10 = 1,200. Actual records, filtering, and coverage remain unavailable. |
| N3 | Random pair-level assignment in a reported 60/20/20 train/dev/test ratio; a source may occur across splits; no manifest. | Lines 8–9 | Describe the reported assignment at pair level. Do not call the splits source-disjoint. Exact realized split counts and overlaps are unverified. |
| N4 | Three public systems were run; final scores unavailable; pair-level contradiction accuracy intended; no uncertainty computed. | Lines 11–12 | Record evaluation activity as author-reported. No numerical findings, rankings, improvement, or significance claims. |
| N5 | Two annotators participated; agreement not calculated. | Line 13 | Report participation only. Independent double annotation of every item, adjudication, and label reliability are not established. |
| N6 | One evaluator instruction saved; possible notebook system/retry prompts not inventoried. | Lines 15–17 | Preserve the saved instruction exactly. Do not describe it as the complete experimental prompt set. |
| N7 | Editing-only author rule; no draft paragraphs; figure dependency unavailable. | Lines 19–21 | Supply editorial work and figure briefs. Do not claim manuscript drafting, figure rendering, or official policy verification. |

**Editorial emphasis:** a focused diagnostic question; a dataset organized around revisions of the same source; an explicit annotation and evaluation contract once recovered. These are a constructive basis for a benchmark paper without requiring an algorithmic advance or favorable system rankings.

**Unestablished distinctions:** novelty relative to existing benchmarks, validity of the contradiction construct, representativeness, label reliability, system weaknesses, and practical utility. No bibliography or closest-work comparison was supplied. Avoid “first,” “comprehensive,” “robust,” “reliable,” or “state of the art” claims until the corresponding evidence exists.

**Competing explanations to address:** variation in apparent system accuracy could reflect class balance, annotation ambiguity, document truncation, prompt/parsing behavior, or source familiarity. No observed score pattern is available to select among these explanations.

## 2. Introduction: author drafting and polishing brief

This is an editorial sequence, not manuscript prose. Populate it with author-written paragraphs before language polishing.

| Paragraph function | Available content | Input needed before finalization |
| --- | --- | --- |
| 1. Make the diagnostic task concrete. | Contradiction identification across revisions of one source (N1). | A real, permission-compatible pair with stable IDs, gold label, and annotation rationale. Clarify why its claims conflict rather than merely change over time. |
| 2. Establish the measurement gap. | Intended focus of AuditBench (N1). | Supplied closest-work sources and an explicit comparison of task, unit, labels, source/revision structure, and evaluation protocol. No claim that prior work omits this capability yet. |
| 3. Explain the resource contribution. | Dataset and annotation protocol; reported scale (N1–N2). | Provenance, selection rules, label definition, guidelines, quality checks, and access conditions. Explain why the design measures the intended construct; size alone is insufficient. |
| 4. Bound the evaluation summary. | Three public systems reportedly evaluated; intended accuracy metric (N4). | System identities and versions, matched conditions, raw predictions, verified scores, and source-aware uncertainty. Until supplied, no findings paragraph or relative ranking. |
| 5. State substantiated contributions. | Two candidate contribution categories: diagnostic dataset; documented annotation/evaluation protocol. | Evidence for each category and a qualified closest-work distinction. Add an empirical finding only after the results support one; do not pad to an arbitrary number of contributions. |

Main-text caveats needed at the relevant claim: possible source overlap across splits, incomplete annotation validation, and any limits imposed by missing or noncomparable evaluation artifacts. Do not reserve a caveat that changes the central interpretation for the appendix alone.

## 3. Method: benchmark construction and evaluation specification

Use “Method” for the dataset/annotation/evaluation procedure if desired. A section titled “Benchmark Construction and Evaluation” may communicate the contribution more directly. Neither requires a new model, loss, optimizer, training architecture, or agent loop.

| Subsection | Supported core | Unresolved specification |
| --- | --- | --- |
| Task and construct | Same-source revision comparison for contradictions (N1). | Exact system input: full versions, extracted claims, questions, or another representation; output label set; definition of contradiction; temporal scope; treatment of compatible additions, corrections, ambiguity, and insufficient context. Do not assume a binary label set from the prompt alone. |
| Data provenance and pair construction | Reported 120 sources and 10 pairs per source (N2). | Source domains, collection/version dates, licenses/access conditions, inclusion/exclusion rules, revision selection, pairing algorithm, reused revisions, length distributions, and deduplication. Ten pairs need not imply ten distinct revisions. |
| Annotation | Two annotators (N5). | Instructions and label ontology, assignment and double-annotation coverage, independent labels, training/calibration, adjudication, unresolved cases, exclusions, and final gold-label provenance. Compute agreement from pre-adjudication labels on the actual shared set. |
| Split protocol | Reported pair-randomized 60/20/20 assignment (N3). | Pair/source/revision manifest, actual counts, seed and implementation, source/revision intersections, duplicate pairs or content, and any subsequent filtering. |
| Evaluated systems | Three public systems reportedly run (N4). | Names, references supplied by authors, implementation/model versions and dates, context limits, input preprocessing, retrieval if any, decoding, budgets, adaptation/tuning, and actual train/dev/test use. |
| Scoring | Intended pair-level contradiction accuracy (N4). | Gold labels, output schema, parser, invalid/missing response handling, abstentions, retries, denominator, exclusions, aggregation, and the role of the saved evaluator instruction. Clarify whether an LLM judges responses or whether it directly produces the evaluated contradiction decision. |
| Analysis and reporting | No supplied scores, uncertainty, or agreement. | Recovered per-pair outputs, score-generation code, class counts, source counts, confidence intervals, relevant failures, and complete comparable system results. |

### Split diagnosis and a minimal corrective plan

- The reported split rule allows same-source pairs across splits. The notes do not establish the realized overlap, duplicate-pair leakage, model training exposure, or measured score inflation. Recover the manifest before asserting any of those outcomes.
- A 60/20/20 allocation of 1,200 items corresponds arithmetically to 720/240/240. These are nominal counts, not verified realized split sizes.
- Determine the intended claim. Pair-level evaluation with potentially shared sources cannot establish held-out-source generalization. If that generalization is central, create a separate source-grouped split, assign every pair from a source to one split, freeze the manifest, and rerun affected evaluations. This is a proposed experiment, not completed work.
- Preserve the existing assignment and run provenance. Do not silently relabel old scores as results from a redesigned split. If retaining the existing protocol, bound conclusions to its actual source-overlap setting and document system exposure to train/dev data.
- Audit shared revisions and near-duplicate content as well as source IDs. Even if systems were evaluated zero-shot, within-source dependence still matters for uncertainty and the scope of generalization.

### Proposed analysis contract — not an implemented result

If each pair has one resolved gold class and the parser returns one predicted class, pair accuracy can be specified as the number of correct pair predictions divided by the number of scored pairs. The authors must first fix invalid-output, retry, and exclusion rules; otherwise the denominator remains ambiguous.

Report label frequencies and an appropriate trivial-reference score so accuracy is interpretable under class imbalance. Recover source IDs before selecting uncertainty calculations. A source-cluster bootstrap that resamples sources and retains their pairs is one candidate for sampling uncertainty; justify it against the intended estimand and report the interval level, resampling procedure, number of sources, and pairing of comparisons. Do not treat all 1,200 pairs as independent or confuse source-sampling uncertainty with run-to-run generation variability. No interval or significance result has been calculated here.

For annotation quality, recover independent labels, report the overlap denominator and raw agreement, and select an agreement statistic suited to the actual label type and missingness. Agreement after adjudication would not measure independent annotation reliability. No agreement value can be recovered from “two annotators” alone.

## 4. Prompt appendix: exact source packet and missing inventory

**Coverage status: incomplete.** This is reproducibility documentation for author review, not a finished appendix narrative. It contains the only saved prompt text supplied in the notes; it does not reconstruct the complete experimental request.

**Editorial record ID:** `P-EVAL-SAVED-01` (assigned for this review; not an original run identifier).

**Exact supplied instruction** (`input/research-notes.md`, line 17):

```text
Compare the supplied document versions and decide if their claims conflict.
```

The instruction has been copied literally. Its original message role, surrounding messages, version, and document-insertion format are unknown. Do not add role labels, placeholders, demonstrations, or output schemas and then describe the result as the prompt used in the experiments.

| Prompt category | Evidence/status | Required recovery |
| --- | --- | --- |
| Principal evaluator instruction | Exact text above is supplied. | Original file/cell and revision, role, receiver/model, ordered request, run linkage, and whether evaluator means judge or task model. |
| System prompt | Possible; neither presence nor content verified. | Inspect notebook/configuration execution paths and recover exact text if used. |
| Retry or repair prompt | Possible; neither presence nor content verified. | Exact variants, trigger conditions, attempt limits, response selection, and whether scores count retries. |
| Per-system task prompts, demonstrations, other experimental stages | Not supplied; applicability unknown. | Inventory every material prompt path actually executed for each system/run. Mark absent only after inspection. |
| Document/context assembly | Not supplied. | Ordering, delimiters, version identifiers, preprocessing, truncation, escaping, retrieval if used, and exact variable-substitution rules. |
| Outputs and execution | Not supplied. | Schema/parser, validation/repair, model versions/dates, decoding and token limits, tools if used, and prompt/config hashes associated with predictions. |

Fast recovery sequence: obtain the notebook and run configurations; trace actual executed prompt paths; export canonical role-ordered messages and templates; map each variant to system/run/result IDs; preserve one fully instantiated real request with its output and score when release permissions allow. Any representative reconstruction must be labeled as a reconstruction. No missing prompt has been invented here.

Once author-written appendix text is available, organize it around dataset/split records, annotation instructions and agreement, system configurations, scoring, and all exact experimental prompts. Keep material scoring and split limitations in the main text as well.

## 5. Teaser, method, and environment figure handoff plans

**Production state: briefs only.** The supplied notes state that the figure dependency is unavailable. No dependency was fetched, invoked, or represented as available. No figure, caption prose, numerical plot, or rendered-page inspection was produced. Venue dimensions and typography are unverified; finalize them from the official template. A later renderer should preserve editable vector sources and a manuscript export, then inspect at insertion size.

| Role | Reader question and proposed composition | Evidence and immutable facts | Missing inputs and caption requirements |
| --- | --- | --- | --- |
| Teaser: diagnostic focus | What does contradiction detection across revisions require? Plan a matched pair of actual revision excerpts, the relevant claim spans, and the adjudicated label. | N1; no actual example supplied. No system output, success rate, or ranking may be illustrated as observed. | Recover a stable pair ID, provenance, label and rationale. State selection rule and any excerpting/annotation transformations. Caption must distinguish source text, author highlights, gold labels, and measured system output if eventually included. |
| Method: benchmark construction protocol | How is the resource made auditable? Plan stages for source/revision collection, pair construction, annotation, split assignment, and release records. Verify the actual order and decision branches before drawing arrows. | N1–N3, N5. Retain 120 reported sources, 10 reported pairs per source, 1,200 reported pairs, two annotators, and pair-level split assignment as author-reported facts. No QA architecture or invented adjudication component. | Recover collection/pairing/annotation/split procedures. Visually distinguish completed documented operations from unresolved ones in an internal draft. Final caption must identify source and pair units and explain any changed split protocol. |
| Environment: evaluation contract | What does a system observe, what does it return, and how is it scored? Plan an evaluation-boundary diagram separating model-visible inputs, predictions, evaluator-only gold information, and aggregate reporting. | N4, N6. Unit intended for accuracy is a revision-pair. Three public systems reportedly run; identities absent. Do not add tools, action loops, resets, or interactive state without evidence. | Resolve exact input/output contract, prompt role, gold-label access, parser, retries, budgets, and score aggregation. Caption must define the scored population and explain information boundaries and invalid-output rules. |

**Avoid redundant figures:** the teaser should explain the construct; the method figure should explain resource construction; the environment figure should explain evaluation access and scoring. Combine the latter two if their recovered protocols do not justify separate diagrams.

**Figure evidence gate:** trace every example to its source pair and annotation, every arrow to a documented operation, and every number to a manifest or result artifact. For qualitative output panels, use matched inputs and a declared selection rule; include material failure modes rather than selecting only favorable outputs. Omit quantitative panels until actual comparable results are available. Current briefs have no resolved rendering dependency/version, final caption, export, or visual sign-off.

## 6. Prioritized unresolved-input notes

These actions identify the shortest path to a defensible paper. They are recommendations and artifact requests, not claims that experiments or recovery work have occurred.

| Priority | Input / decision | Smallest concrete next action | Completion evidence |
| --- | --- | --- | --- |
| P0: writing | Author-written Introduction/Method/appendix passages; exact target policy. | Supply the prose plus venue, year, track, stage, and official policy/template text or locally saved official source. | Text eligible for polishing; resolved assistance and disclosure requirements. External verification remains outside this task. |
| P0: construct | Operational contradiction definition and annotation protocol. | Recover guidelines, pair-construction criteria, labels, and examples that distinguish contradiction from nonconflicting revision. | Auditable task definition, gold-label construction, coverage and quality documentation. |
| P0: split | Actual manifest and intended generalization claim. | Export pair/source/revision IDs, split membership, seed, and filtering history; inspect overlap and system data use. | Reconciled counts and exposure report; appropriate claim scope or separately evaluated source-held-out protocol. |
| P0: reproducibility | Notebook, configurations, and raw outputs for all three systems. | Recover complete prompts and model/config/run mappings before interpreting scores. | Exact executed input-to-output path and unambiguous evaluator role. |
| P0: results | Final score artifacts and scoring implementation. | Recompute from fixed gold labels and retained per-pair predictions under documented missing/invalid/retry rules. | Reproducible system results with denominators and all material outcomes. |
| P1: annotation quality | Independent annotation records and adjudication history. | Establish shared coverage, calculate agreement, and document disagreements and resolutions. | Agreement method/results with actual denominator and label provenance. |
| P1: uncertainty | Source-linked scored predictions and repeated-run records if used. | Select an uncertainty procedure matching source dependence and the claim; compute on recovered artifacts. | Reported method, sample units/counts, interval and comparison conditions. |
| P1: positioning | Author-supplied closest-work sources and dataset documentation. | Compare the construct, task contract, revision structure, and coverage; verify citations against supplied sources. | Supported novelty scope without priority claims based on absent literature. |
| P1: release and presentation | Data provenance/access terms, official template, figure dependency or approved local renderer. | Assemble release records; have authors draft captions; render and inspect the completed package. | Usable artifacts, template compliance, legible figures, and resolved cross-references. |

## 7. Checks completed and readiness decision

- Read the source notes and applicable A-Star guidance for benchmark architecture, evidence, prompts, figures, policy, and readiness review.
- Inventoried the project: only the research-notes file was present before this output. No dataset, manifest, notebook, score files, annotation labels, bibliography, manuscript, or template was available for inspection.
- Checked the reported count arithmetic and preserved the exact saved evaluator instruction.
- Obtained an independent review of the supplied notes; incorporated its distinction between allowed source overlap and proven leakage, its annotation and prompt gaps, and its restriction on unsupported empirical claims.
- Ran the skill's `paper_audit.py` on this project in both `draft` and `ready` modes. Both exited **2**, with status **invalid**, because `evidence-ledger.json` and `venue-profile.json` were absent. This is a missing-audit-input result, not a measured scientific verdict. No audit pass or readiness certification is claimed; creating those files alone would not resolve the evidence gaps.
- No experiments, statistical estimates, new manuscript prose, external searches/actions, figure rendering, compilation, or PDF visual inspection were performed. No skill files were changed.

**Decision:** retain this as an internal editorial and research-recovery packet. The scientific contribution can be presented positively through the clarity and utility of its diagnostic design, but those qualities need documented construct validity, trustworthy labels, an appropriate split claim, and reproducible evaluation. Recover those artifacts and supply author-written prose before polishing the requested manuscript sections. The paper is not ready for submission on the supplied evidence.
