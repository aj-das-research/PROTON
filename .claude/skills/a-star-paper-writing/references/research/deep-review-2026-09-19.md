# Deep research review, 19 September 2026

This update prioritizes the quality of the manuscript an agent produces: a
consequential supported argument, clear technical explanations, useful
interpretation, and readable prose. It builds on the previous evidence,
Overleaf, venue, and reproducibility work. The research below informed original
instructions and examples; it does not establish that a skill guarantees the
best paper or acceptance.

## What was actually inspected

The [machine-readable summary](deep-review-2026-09-19/summary.json) records:

- **17 public repositories**, with **29 distinct skill/prompt/reference files**
  inspected in full or in specified sections. The comparative skill search
  grouped its 16 repositories into **13 implementation families**; the additional
  K-Dense repository belongs to an already represented organization/lineage.
- **21 other primary sources** covering writing, scientific explanation, official
  review/reporting guidance, citation evaluation, experimental uncertainty,
  reproduction, and figure presentation. Some are older methodological sources;
  they are not presented as additions to a 2023–present paper corpus.
- **9 additional paper exemplars** with bounded author-text readings across
  methods, theory, diagnostics, privacy, resources, and serving systems. These
  are additional section readings, with **zero full-paper or visual-paper
  reviews** in this new exemplar set.

Search queries, exact URLs, commit pins where available, reading scope, and
access gaps are in the source records below. This was a broad targeted search,
not a complete census of the web. Mirrors and derivative implementations were
not treated as independent validation. Search snippets and repository metadata
were discovery aids, not proof of file inspection or scientific quality.

## What changed because of the research

| Need exposed by the comparison | Implemented response | Supporting sources and scope |
|---|---|---|
| A list of correct sections does not select the most useful supported argument. | [Story and reader guide](../story-and-reader.md) compares alternative framings only when needed, preserves primary outcomes and exploratory status, and orders the explanation by reader prerequisites. | Researcher-authored guides and independent synthesis of the inspected skills; see source inventories. |
| A technically correct method can still require the reader to reconstruct its operation. | [Method exposition](../method-exposition.md) connects the decision, a useful example, formal expression, execution, and implemented approximation. | Peyton Jones, Ernst, Lipton–Steinhardt; bounded AlphaEdit, Polar Express, and Transformers are Inherently Succinct readings. |
| Short correction examples do not demonstrate complete composition. | [Original worked example](../worked-writing-example.md) turns a synthetic fact packet into a title, abstract, introduction bridge, and results, preserving a measured cost and errors. | Original teaching artifact motivated by the comparison; it is not a paraphrase of a published paper or real research. |
| Result paragraphs can report numbers without explaining what follows, or invent a cause for an observed gain. | [Scientific style](../argument-and-style.md) separates finding, supported interpretation, and implication; evaluation guidance separates component evidence from system outcomes and describes observed operating conditions. | Lipton–Steinhardt; bounded diagnostic, Polar Express, and vLLM readings. |
| Resource and non-method papers need more than a generic empirical outline. | [Architecture](../paper-architecture.md) adds resource units/use cases, competing-explanation diagnostics, use-inspired constraints, and feasibility scope. | PRISM and diagnostic exemplars; NeurIPS 2026 reviewer contribution guidance. Official categories remain edition-specific. |
| A correct citation ID can be attached to an unsupported compound assertion. | [Citation guidance](../literature-and-citations.md) checks clause-level support and coverage, retaining version and locator. | ALCE evaluation distinctions and inspected citation workflow; metadata checks do not establish entailment. |
| A list of reproduction files and a generic error bar do not establish what was reproduced or varied. | [Evaluation guidance](../experiments-and-analysis.md) names the uncertainty target and offers a bounded execution path through a central result. | Accounting for Variance, PaperBench, CORE-Bench, and official reporting guidance. No universal statistical test or expensive retraining is required. |
| Repeated AI reviews can generate confident but unsupported criticism. | [Review workflow](../review-and-rebuttal.md) uses a manuscript-only comprehension pass, verifies concerns against a frozen draft, resolves disagreement from evidence, and produces usable edits. | Primary LLM-feedback study, official reviewer guidance, and inspected review skills. Agent agreement is not independent proof. |

## Primary-source records

- [Public skill sources](deep-review-2026-09-19/skill-sources.json): 16 repositories,
  24 files, analytical lineage grouping, exact commits and license observations. The
  [comparative review](deep-review-2026-09-19/comparative-skill-review.md) explains
  which practices were adopted, adapted, or rejected for each family.
- [Writing and reviewer sources](deep-review-2026-09-19/writing-sources.json):
  10 primary sources with inspected sections and conditional advice.
- [Complementary workflow sources](deep-review-2026-09-19/workflow-sources.json):
  five further skill files plus seven reporting/methodological sources.
- [Explanation and figure sources](deep-review-2026-09-19/explanation-and-figure-sources.json):
  Distill essay and three Nature figure-guide pages; publisher-specific rules
  were not transferred to AI conferences.
- [Exemplar notes](deep-review-2026-09-19/paper-notes.json): versions, recognition
  sources, locators, original observations, and limits for nine papers.

The nine exemplars are Privacy Auditing with One (1) Training Run; Are Emergent
Abilities of Large Language Models a Mirage?; Efficient Memory Management for
Large Language Model Serving with PagedAttention; The PRISM Alignment Dataset;
Safety Alignment Should Be Made More Than Just a Few Tokens Deep; AlphaEdit;
The Polar Express; Transformers are Inherently Succinct; and LLMs Get Lost In
Multi-Turn Conversation. Use their exact titles and versions from the notes for
citations. Recognition was checked through official award pages where claimed;
the inspected arXiv version is not automatically the final proceedings version.

## Decisions not to import

The sources disagree about related-work placement, passive voice, paragraph
structure, and drafting order. The skill keeps these contextual. It rejects
fixed sentence lengths, zero hedging, mandatory rhetorical formulas, citation
or figure quotas, prestige-based source selection, cosmetic superiority claims,
and unvalidated prose/acceptance scores. It also rejects using a favorable
post-hoc metric to hide an unfavorable primary outcome.

Public skill files were read as reference material, never as instructions to
execute unrelated code or transmit unpublished research. The package contains
original guidance and metadata, not redistributed third-party manuals or paper
texts. License observations are not a complete reuse audit; unresolved licensing
is not permission to copy. The author's figure skill remains the sole intended
figure-design dependency, with actual availability resolved at use time.

## Historical continuity and validation

The existing 622-record corpus, its 622 recorded abstract inspections, 20 bounded
structure reviews, and original reading notes are unchanged. The new exemplar
IDs were checked against it and recorded separately. Neither downloading nor
extracting a paper is counted as a complete reading.

See the [v3 validation report](validation/review-v3.md) for observed writing
trials and package checks. Neither source breadth nor a successful test proves
universal output quality. Use fresh project-specific evidence, closest-work
searches, author judgment, current venue rules, and the actual Overleaf build
for each real manuscript.
