# Paper architecture and page budget

## Structure follows the contribution

Default empirical sequence: Abstract; Introduction; Related Work or Background and Related Work; Problem Setting if needed; Method; Experiments; Discussion; Conclusion; required statements; References; Appendix. Section titles are editorial choices subject to the official template, not acceptance conditions. Use “Method” for a unified approach and “Methods” when useful for genuinely distinct approaches.

| Paper type | Argument center | Evidence priority | Common structural error |
|---|---|---|---|
| Method | A mechanism addresses a failure/constraint | Matched comparisons, ablations, boundaries | Novelty explained only in a diagram |
| Benchmark/environment | A task/measurement contract exposes a gap | Construct validity, splits, scoring, coverage, baselines | Size treated as the entire contribution |
| Dataset/resource | A documented artifact enables research | Provenance, quality, representativeness, utility, access | Curation/access restrictions hidden |
| Theory | A precise question resolved under assumptions | Statements, proofs, prior bounds, applicability | Essential assumptions omitted from main text |
| Systems/efficiency | A design changes a resource–quality tradeoff | End-to-end cost, workloads, hardware, bottlenecks | Component timing called system speedup |
| Analysis/negative result | An observation revises understanding | Controls, confounds, robustness, alternative explanations | Inventing an algorithm to fit a method template |
| Use-inspired | A real user need changes the problem framing or design | Domain-relevant comparisons, constraints, utility | A convenient benchmark substituted for the actual need |
| Concept/feasibility | A new idea has a supported path to broader value | Decisive feasibility evidence and explicit scope | Proposed potential presented as demonstrated capability |

## Related work and background

Related work may follow the introduction, precede the conclusion, or be interleaved. Put closest comparisons where needed to understand novelty. Background is useful for essential notation, existing objectives, task semantics, and assumptions; avoid a textbook chapter.

Attribute standard losses and explain their role. Distinguish inherited definitions from new ones. Put optional derivations/tutorials in Appendix A while retaining enough main-text context to assess the method without the appendix.

## Problem formulation

Specify input, output, available information, objective, supervision, deployment, constraints, and assumptions. For interaction define observation/action spaces, state/hidden state, transition, termination, horizon, reset, success, and budget. For data define the sampling unit and independence. Separate the problem from the proposed solution so alternatives remain conceivable.

Use a notation table only when helpful. Explain formal expressions in prose and relate them to observable operations. Equations should reveal computations/assumptions, not decorate the page.

## Method

Begin with the decision, available information, constraint, and essential idea. Read [method-exposition.md](method-exposition.md) when explaining a mechanism, objective, algorithm, or mathematical connection: it covers concrete examples, equations, training versus deployment, execution traces, and inherited versus new operations.

Keep the choices that define the method and its central assumptions in the main text. Move exhaustive tuning and routine engineering details to the appendix with pointers. The reader should be able to reconstruct the mechanism before consulting implementation detail.

For multiple methods, give shared interfaces/setting, each distinct approach, and its evidence. Do not multiply sections simply because one pipeline has modules.

## Benchmark/environment

Explain the construct measured; existing benchmark gap; task/environment contract; creation/curation; splits and contamination prevention; scoring; quality assurance; baselines; and observed behavior. Distinguish new, adapted, and inherited components. Using an existing environment does not mean creating it.

Provide statistics that affect interpretation: counts by split, domain/task distributions, lengths/horizons, class balance, source/time coverage, annotation/agreement, exclusions. For dynamic environments give version, reset seeds, stochasticity, inaccessible actions, tools, time/resource budgets, failure and partial-credit rules.

For a dataset or resource, explain the unit of each record and the relationships between record types: for example, participants, sessions, and individual responses are different units. Show the schema or a small record example when it makes the resource usable. Demonstrate a feasible reader question, the variables and analysis needed to answer it, the observed finding if available, and its limitation. Proposed uses remain proposals. Rich metadata or large volume alone does not establish representativeness, causal identification, or utility.

## Other contribution-centered variants

**Use-inspired work:** establish the existing user need, the constraints that change the technical problem, and how the evaluation reflects that need. Explain domain terminology for an ML audience. Include relevant established non-ML approaches when they are meaningful alternatives. Distinguish demonstrated utility from a motivating future application.

**Concept and feasibility:** explain the broader idea, identify what this study actually establishes, and justify why the tested setting informs the larger question. Preserve the boundary between supported feasibility and proposed potential; a promising idea still needs sound evidence for its stated claims.

**Diagnostic and negative results:** organize the observed phenomenon and its operational definition around competing accounts, their distinct predictions, and tests that discriminate between them. Explain what ambiguity each available test removes and which alternatives remain. Mark explanations developed after seeing results as exploratory. State how the finding changes understanding; a remedy is optional. An unexplained failed experiment is not automatically a consequential negative result.

These are adaptable writing branches, informed by the [NeurIPS 2026 contribution-type guidance](https://neurips.cc/Conferences/2026/ReviewerGuidelines), inspected 2026-09-19. They are not universal track definitions or experiment quotas. Verify the target's actual categories before selecting a formal submission type.

## Results

Organize around answerable questions: Does it work under matched conditions? What component matters? Where does it generalize? What does it cost? When does it fail? Separate protocol and interpretation even within a unified Experiments section. Give the main result early, followed by analysis explaining it.

Prioritize decisive comparisons, relevant controls, and material boundaries. Move exhaustive sweeps, full per-dataset tables, extra examples, and secondary derivations into a navigable appendix. Contradictory central evidence belongs in the main argument, not hidden supplemental tables.

## Page budget

Record the true content limit and what counts: captions, figures, limitations, impact, references, appendix, checklist. Do not infer limits from accepted PDF lengths; review and final stages differ.

Allocate by argumentative need. As an initial empirical heuristic, use roughly one fifth for introduction/positioning, one quarter for formulation/method, two fifths for evaluation/results, and the remainder for abstract, conclusion, and required material. These are planning heuristics, not measured acceptance predictors. Adapt for theory, benchmark, and systems work and actual figures.

If the **verified** venue permits 11 content pages, one starting allocation is: title/abstract 0.5; introduction 1.5; related/background 1; formulation/method 2.5; setup 1; results/analysis 3.5; discussion/conclusion 0.5; layout slack 0.5. These include figures/tables. Rebalance after rendering rather than forcing allotments. For an 8-page limit, redesign for 8 pages rather than squeeze 11 typographically.

To shorten: remove repeated arguments/weakly relevant content; consolidate redundant visuals; sharpen prose; move optional detail with pointers; reconsider peripheral claims. Preserve claim-critical assumptions and evidence, official fonts/margins/spacing, and legibility.

## Main-to-appendix contract

The main paper must make central claims understandable and assessable. The appendix deepens trust and enables reproduction. Map every appendix section to a main section or specific reader need. Add an index when long and stable labels instead of hard-coded numbers. Do not assume reviewers must read supplements.

## Theory branch

Use Introduction and closest results; Setting and assumptions; Main results; Proof ideas or analysis; optional algorithm/empirical illustrations; Discussion and Conclusion; complete proofs and auxiliary results in the appendix. Do not require experiments for a wholly theoretical contribution. Empirical illustrations do not prove the theorem.

State quantified variables, probability space, domain, regularity/realizability assumptions, constants/asymptotic conventions, and dependence on sample size, dimension, horizon, confidence, and other key quantities. Distinguish expectation, high-probability, worst-case, finite-sample, and asymptotic statements. State what is fixed and where a bound is informative. Keep restrictions next to rate-improvement claims.

Explain each result in plain language after its formal statement. Compare nearest theorems under aligned assumptions, objectives, and regimes; qualify special-case comparisons. Separate existence from efficient construction, stationarity from global optimality, and identifiability from practical recovery.

Show the main proof idea and new step in the main paper. Map theorem -> lemmas -> assumptions -> proof locations. Place full proofs, auxiliary inequalities, and cases in the appendix where permitted. Restatements must match originals, including constants and assumptions. Keep a notation/dependency map.

Review proof steps independently of prose fluency: inequality directions, conditioning, limit/expectation interchanges, independence, boundary cases, existence, and circular dependencies. Toy cases and numerical limiting regimes diagnose mistakes but are not proofs. Check symbolic-tool assumptions. An unproved key lemma makes a theorem incomplete; do not replace the gap with “it is easy to show.”

For lower bounds/impossibility, define algorithm/distribution/information classes and whether the claim is minimax, instance-specific, computational, or information-theoretic. Matching upper/lower rates need compatible classes and regimes. A counterexample must satisfy the assumptions of the claim it refutes.

Make the appendix sufficient to reconstruct the argument: complete proofs, omitted cases, necessary constants, inherited assumptions, exact invoked statements, and primary citations for reused lemmas and adaptations.
