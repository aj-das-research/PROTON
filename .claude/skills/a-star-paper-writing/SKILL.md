---
name: a-star-paper-writing
description: Write and revise ML/AI conference papers (ICLR, NeurIPS, ICML, CVPR, ACL) in Overleaf or LaTeX, in the author's house style and the SPOT AI lab standard. Covers turning research materials into a full manuscript or rewriting one section; abstracts, introductions, contributions, related work, benchmark and method sections, experiments, and discussion; fitting to the page limit; lean reproducible appendices; and reviewer responses. Use this whenever the user asks to write, rewrite, polish, restructure, shorten or "make great" any part of their paper, to sell the contributions, to fix a "report-like" draft, or to prepare a submission, even if they only paste a paragraph. For reviewing or annotating a paper, use a-star-paper-review.
---

# A-Star Research Paper Writing

Produce a clear scientific argument that a skeptical expert can inspect and
reproduce, written the way the author and their lab write. Optimize for
significance, technical validity, fair evaluation, precise positioning, and
readable, concise presentation. No workflow, score, rhetorical formula or paper
corpus guarantees acceptance. The author's bar is still acceptance by real
reviewers, and "it all depends on presentation".

## Start with the requested deliverable

- **One section:** work on that section and inspect its supporting evidence.
  Do not force a whole-paper process.
- **A complete paper:** use the workflow below.
- **A rebuttal or readiness review:** see
  [review-and-rebuttal.md](references/review-and-rebuttal.md).
- **An annotated review of an existing draft:** use the `a-star-paper-review`
  skill.
- **A benchmark, dataset or theory paper:** select its branch in
  [paper-architecture.md](references/paper-architecture.md).

For a draft that is correct but hard to follow, diagnose the first missing
explanation rather than adding more process. For an unsupported central
claim, repair the evidence or the scope before polishing. Return the requested
manuscript or source edit, with only the editorial decisions and open
questions the author needs.

Inspect the existing project before scaffolding. Preserve the author's
decisions, wording the author submitted, notation, citation keys, the official
template, and verified results, unless the requested change requires
otherwise. Ask only for missing information that blocks the task.

**Overleaf and LaTeX are the primary workflow.** Use
[overleaf-workflow.md](references/overleaf-workflow.md) for connection and
synchronization. For every edit in the author's projects, follow
[revision-workflow.md](references/revision-workflow.md):

- pull first;
- propose before editing;
- edit only what was asked. Verified citations the rewritten section needs
  are part of the edit, and changes to other sections are proposed first;
- mark rewrites in yellow with labreview, and new numbers in orange;
- check the layout in the final-mode PDF after every edit;
- push as Mishrakshitij with no AI co-author trailer, and confirm the push.

For a genuinely new project, `python scripts/init_paper.py PROJECT_DIR --title "Working title"`
creates a generic compilable TeX draft. It is not an official template or a
live connection. Never scaffold over existing work.

## House style (always)

Read [house-style.md](references/house-style.md) before writing prose, and
[section-playbooks.md](references/section-playbooks.md) before writing a
section. The rules that matter most:

1. **Each sentence makes one checkable point**, in 15 to 30 words. No filler, no
   framing or recap sentences, no em dashes, few semicolons, no colon
   expansions. Show the facts; do not announce conclusions.
2. **A paper, not a report.** No run-log prose ("across three seed runs"), run
   names, file paths or experiment numbers. State the protocol once in the
   setup.
3. **Results read value ± SD plus the margin** ("an 11.7% relative gain over
   SFT+GRPO"). Say what the ± is over, and write ± only when the protocol
   supports it: if the setup and appendix disagree on the number of runs, flag
   it. Put ± on every row, leading zeros everywhere (0.645), and make sure
   relative and absolute changes are computed right.
4. **Sell without overselling.** Do not undersell the abstract, introduction or
   contributions (no "pilot", "toy", "earlier study", and no closing caveat).
   Write limitations as future work, with the measured number. Never let a
   claim exceed the evidence.
5. **Define before use, and keep one term per concept.** Model names go in
   `\texttt{}`. Expand acronyms or drop them. Explain every display-equation
   term in plain words. The paper is self-contained, "not only for experts".
6. **Abstract** (Michael Black's template): need, what exists, why it fails,
   our idea, what we find. Numbers go only at the end: one or two relative
   gains over a named baseline.
7. **Introduction:** the need with an example, then why it is hard and what
   exists, then the insight and the method, then the evidence, then 3 to 4
   numbered contributions.
   - **Position against the closest 2025 to 2026 work by name.** Search for it
     and verify it first. Cut any "first" claim it contradicts, and state the
     delta.
   - Tie the motivation to the paper's own results.
   - Answer the obvious objection in one clause.
   - Check that the coined names are not already taken.
   - Paragraphs run at most 6 to 7 lines, and the teaser is on page 1.
8. **Experiments** are one section. Setup run-ins come first, then one
   subsection per question: the question, what the figure plots, how to read
   it, bold takeaways. The closest baselines are in the main table. There are
   no evaluation numbers inside the benchmark or method sections.
9. **Figures are faithful to the method and made from real data**, with no
   overflow or overlap. Use compact rows of three or four plots, wrapped
   floats, a bold-takeaway caption, and arrows on axes and headers. See
   [figure-integration.md](references/figure-integration.md).
10. **Lean appendix:** about 8 to 10 pages, graphs over tables, interpretation
    over number dumps, and nothing that contradicts or undersells the main
    text. No FAQ section unless asked. See
    [appendix-and-prompts.md](references/appendix-and-prompts.md).
11. **Citations are recent and inline.** Do not use parenthetical
    cross-references or "Figure X shows" openers. Point first, then cite.
12. **Before returning prose, run the checklist** at the end of
    house-style.md and `python scripts/style_lint.py <files>`.

## Scientific boundaries

- Separate verified observations, interpretations, hypotheses and planned
  experiments. Never invent a citation, result, baseline run, statistical test,
  proof, quote, human study or implementation detail. An agent's suggestion
  is not an experiment.
- Use `[[NEEDS EVIDENCE: specific item]]` in working prose when needed. Never
  turn a missing quantity into a plausible value, and never leave markers in a
  document claimed to be ready for submission.
- Tell the strongest story that all the relevant evidence supports. Select
  positive examples by a stated rule. Report material failures, null results,
  costs and boundaries at their proper place, which is usually the results or
  the limitations, not the abstract. Never select or alter results to make the
  method win.
- Keep manuscript prose in the authors' voice. Put agent access gaps,
  verification status and requests in editorial notes, not in the paper.
- Narrow an unsupported claim, retrieve the missing evidence, or mark it open.
  Do not run expensive experiments, upload unpublished research to external
  services, change repository visibility, or submit a paper merely because
  writing is authorized.
- Verify the venue's current AI-assistance rule for the intended
  venue/year/track/stage **before drafting**
  ([venue-policy.md](references/venue-policy.md)). ICLR 2027 permits drafting
  with a mandatory AI-use statement. The NeurIPS 2026 position track allows
  only copyediting. Follow the disclosure rules, and write the AI-use
  statement from what was actually done.
- Page limits are the venue's. A longer working draft is fine as a scaffold,
  but never compress fonts or margins to evade a limit.
- Cite intellectual debt, reused data, methods, losses and implementations.
  Build original prose; do not reuse another paper's paragraphs or
  distinctive phrasing.

## Workflow for a complete manuscript

### 1. Establish the paper contract

Read [venue-policy.md](references/venue-policy.md) and
[evidence-and-claims.md](references/evidence-and-claims.md). Record:

- the target, paper type, reader, stage and template version;
- the page accounting and anonymity rules;
- the required statements, with sources and retrieval dates.

Inventory the code, configurations, logs, tables, figures, datasets and
splits, proofs, bibliography, drafts, and inaccessible materials. Write an
evidence-backed one-sentence thesis, the strongest alternative explanation, and
the narrowest defensible novelty statement. Build a claim-evidence map before
polishing prose.

### 2. Design the argument and evidence

Use [story-and-reader.md](references/story-and-reader.md) to select the central
question and order the reader's dependencies. Read
[argument-and-style.md](references/argument-and-style.md),
[literature-and-citations.md](references/literature-and-citations.md) and the
[evaluation guidance](references/experiments-and-analysis.md).

Map the field by problem, assumptions, mechanism, supervision and evaluation,
as a timeline where it explains the change. Compare with the closest and most
recent work, not only weak or old work. For each empirical contribution, state
the research question, comparison, controlled factors, measurement,
uncertainty and the decision it enables. Construct the outline and page budget
([paper-architecture.md](references/paper-architecture.md)).

### 3. Draft from evidence outward

Draft section by section with
[section-playbooks.md](references/section-playbooks.md) and
[house-style.md](references/house-style.md). For the method, use
[method-exposition.md](references/method-exposition.md). A useful order for a
completed study is formulation and method, protocol and results, positioning
and introduction, then abstract, title and conclusion; honor the author's
requested order. The [worked composition example](references/worked-writing-example.md)
shows how to turn a fact packet into prose; its synthetic facts must never
enter a real paper.

The author's reader-facing skeleton is:

1. **Abstract:** problem and need, what exists, why it fails, our idea, what we
   find (numbers last).
2. **Introduction:** need and example, hard and existing, insight and method,
   evidence, then 3 to 4 contributions that sell the paper.
3. **Related Work** or **Background and Related Work:** a timeline, the
   closest and most recent work, and one clause on how we differ.
4. **Benchmark or Environment**, when the setup is new. It contains no results.
5. **Method** or **Methods**, when two or more are proposed. Lab papers
   supervised by Nils may use "Conceptual Approach"; follow the co-authors.
6. **Experiments:** setup run-ins (data and splits, models, baselines,
   metrics), results by question, error analysis, and qualitative analysis on
   real examples.
7. **Discussion and Conclusion:** short, with limitations as future work. Add
   the venue's required statements after it.
8. **References**, then the **lean Appendix:** background, method details,
   experimental details for reproducibility (hyperparameters, baselines, data),
   the prompts the claims need, and extended results as graphs. No FAQs
   unless asked.

Adapt for theory, dataset-only, systems, diagnostic or negative-result work.
Do not invent a method to fit a template.

### 4. Build figures, tables and the appendix

Read [figure-integration.md](references/figure-integration.md), including its
author and lab rules, and use the author's `paper-visual-design` or
`paper-figure-creation` skill when it is available. Numerical plots and
tables come from real data. Read
[appendix-and-prompts.md](references/appendix-and-prompts.md) and apply the
lean-appendix contract. Use [assets/latex/](assets/latex/) only as fragments
inside the official template. Read
[production-and-delivery.md](references/production-and-delivery.md) for the
build and visual inspection.

### 5. Review with independent perspectives

Read [review-and-rebuttal.md](references/review-and-rebuttal.md). For an
annotated pre-submission review with reviewer simulation, number tracing and
labreview margin notes, run the `a-star-paper-review` skill on the frozen
draft. Prioritize validity and evidence defects before rhetoric. Verify each
finding against the draft, and turn confirmed writing concerns into
revisions. If the evidence contradicts the story, change the story.

### 6. Validate and deliver honestly

- For full projects with ledgers, run `python scripts/paper_audit.py PROJECT_DIR --mode draft --json`
  while drafting and `--mode ready --json` for readiness.
- Run `python scripts/style_lint.py` on the changed `.tex` files.
- Compile the configured root with its real engine and template, then inspect
  fresh logs (`python scripts/audit_latex_log.py BUILD.log --json`).
- Look at the rendered pages at reading size. Report the page where the main
  text ends, and check that Figure 1 is on page 1 and that no short last
  lines remain.
- Report separately: the source saved, the local build, the remote build, the
  PDF inspection, and the Overleaf synchronization.
- A GitHub commit alone does not establish an Overleaf update. Writing does
  not authorize submission or contacting co-authors or reviewers.

## Reference routing

| Task | Resource |
|---|---|
| Voice, sentence mechanics, lexicon, numbers, citations, selling vs overselling | [house-style.md](references/house-style.md) |
| Section playbooks: title, abstract, introduction, related work, benchmark, method, experiments, discussion, conclusion | [section-playbooks.md](references/section-playbooks.md) |
| Editing in the author's Overleaf: marking, layout checks, page cuts, pushing | [revision-workflow.md](references/revision-workflow.md) |
| Evidence, novelty, numerical assertions | [evidence-and-claims.md](references/evidence-and-claims.md) |
| Central question, reader prerequisites, representation, order | [story-and-reader.md](references/story-and-reader.md) |
| Method explanation, equations, execution, theory-to-code link | [method-exposition.md](references/method-exposition.md) |
| Original annotated composition example | [worked-writing-example.md](references/worked-writing-example.md) |
| Story, abstract and introduction, language revision | [argument-and-style.md](references/argument-and-style.md) |
| Sections, page budgets, paper-type variants | [paper-architecture.md](references/paper-architecture.md) |
| Search, closest work, bibliographic verification | [literature-and-citations.md](references/literature-and-citations.md) |
| Comparisons, ablations, statistics, real examples | [experiments-and-analysis.md](references/experiments-and-analysis.md) |
| Lean appendix, reproducibility details, the prompts the claims need | [appendix-and-prompts.md](references/appendix-and-prompts.md) |
| Author and lab figure and table rules; the external figure skill | [figure-integration.md](references/figure-integration.md) |
| Venue rules and permitted assistance | [venue-policy.md](references/venue-policy.md) |
| Critical review and rebuttal | [review-and-rebuttal.md](references/review-and-rebuttal.md) |
| Overleaf connection, existing TeX projects, conflicts, synchronization | [overleaf-workflow.md](references/overleaf-workflow.md) |
| LaTeX, accessibility, build and delivery | [production-and-delivery.md](references/production-and-delivery.md) |
| Initializer, JSON schemas, audit commands and limits, style lint | [tool-contracts.md](references/tool-contracts.md) |
| Source skills and paper exemplars | [research-basis.md](references/research-basis.md) |

Load only the references relevant to a small edit. Refresh the literature for
each project, because the development corpus is not a substitute for a current
novelty search.

## Improving this skill

Fold each generalizable piece of author feedback in as a short rule with its
date, in house-style.md or section-playbooks.md, and note it in the README's
change log. Brief subagents with the relevant rules, or have them load this
skill.
