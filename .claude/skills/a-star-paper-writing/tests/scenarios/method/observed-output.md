# BudgetRoute: provisional abstract and paper plan

This draft uses only `input/research-notes.md`. The strongest supported claim is improved **reported model-call efficiency in the supplied test setting**, with a small increase in observed mean accuracy and a material accuracy loss under the tested domain shift. Broader superiority, statistical significance, runtime savings, and novelty relative to prior work remain unestablished.

The author-provided venue profile allows AI drafting with disclosure and specifies **8 main-content pages, unlimited references, and a two-column appendix**. This plan follows that profile. An 11-page main text and one-column appendix could be internal working formats, but would not satisfy the supplied profile. The venue, year, track, submission stage, official policy, and template remain unverified; no external verification was performed because this task excludes searches and external actions. This is a working draft, not a submission-ready package.

## Abstract

Fixed sampling budgets allocate the same number of model samples to every question. We study whether adaptive allocation can reduce model calls while retaining similar observed answer accuracy. We present BudgetRoute, a router trained only on the development split that uses a learned uncertainty score to choose one or three samples before producing a final answer. Compared with a fixed-three-sample baseline using the same base model and test examples, BudgetRoute achieves mean accuracy of 71.0% across three reported runs, versus 70.8% for the baseline. Author-reported mean model calls decrease from 3.0 to 2.0 per question, a 33.3% reduction. These results establish a favorable observed accuracy–call tradeoff in the reported test setting; confidence intervals and statistical tests are not available. The advantage does not establish robust transfer: on a single shifted-domain run, BudgetRoute obtains 49.0% accuracy versus 55.0% for the baseline. BudgetRoute therefore offers a promising way to reduce sampling calls, with distribution shift remaining a material limitation. Timing was not measured, so the reported call reduction does not establish a runtime improvement.

## Introduction contribution bullets

- **Adaptive sampling allocation.** We introduce BudgetRoute, which uses a learned uncertainty score to select one or three samples before the final answer, with router training restricted to the development split. The method changes the sampling budget per question rather than assigning three samples uniformly. *(Main Method; Figure 2. Architectural and training details still need to be supplied.)*
- **A favorable observed accuracy–call tradeoff.** With the same base model and test examples, BudgetRoute reduces author-reported mean calls from 3.0 to 2.0 per question while attaining 71.0% mean accuracy across three runs, compared with 70.8% for the fixed-three-sample baseline. This is a 33.3% call reduction and a 0.2-percentage-point difference in observed mean accuracy; no significance or equivalence claim is made. *(Main Results; Figures 1 and 3.)*
- **An explicit boundary under domain shift.** A shifted-domain evaluation records 49.0% accuracy for BudgetRoute and 55.0% for the baseline in one run. This result identifies a setting where the reported test-set advantage does not extend and motivates further evaluation of routing under shift. It does not establish the cause of the degradation. *(Main Results and Limitations; Figure 3.)*

These three bullets describe the mechanism, its observed benefit, and its measured boundary. A fourth distinct contribution is not supported by the notes. Claims of novelty beyond this baseline require a supplied, verified closest-work comparison.

## Three main figures

All figures below are **plans**, not rendered or visually inspected artifacts. Source numbers come exclusively from `input/research-notes.md`. The `paper-figure-creation` skill was not available in the installed catalog or local skill directory, and no dependency was fetched. The briefs and captions are ready for a later rendering handoff. Use editable vector sources and PDF exports; final dimensions and typography must follow the official template once supplied.

### Figure 1 — Teaser: reducing reported sampling calls

**Question and supported takeaway:** What concrete resource changes? BudgetRoute uses 2.0 reported model calls per question versus 3.0 for the baseline.

**Design:** A compact two-column-width teaser in the introduction. Use a small conceptual panel showing “fixed budget: 3 samples” and “adaptive budget: 1 or 3 samples,” followed by a larger quantitative panel with two zero-based bars at 3.0 and 2.0. Label the metric “Author-reported mean model calls per question” and annotate “33.3% fewer reported calls.” Keep the conceptual panel schematic: no fabricated question, answer, routing trace, or empirical route-frequency graphic. In particular, do not infer a 50/50 route split from rounded aggregate call counts.

**Source and scope:** The notes’ “Mean model calls per question” line. Per-example logs, aggregation denominator, run weighting, and inclusion of router/final-answer overhead are unavailable. Do not attach these averages to individual runs or to the shifted domain without confirmation.

**Caption draft:** “BudgetRoute selects a budget of one or three samples, whereas the baseline uses three. Author-reported mean model calls are 2.0 and 3.0 per question, respectively, a 33.3% reduction. Per-example call logs were not supplied, and timing was not measured. Figure 3 reports answer accuracy, including the adverse shifted-domain result.”

### Figure 2 — Method: the routing decision

**Question and supported takeaway:** Where does BudgetRoute change inference? A learned uncertainty score informs the choice between one and three samples before the final answer.

**Design:** A two-column-width method schematic with a separate training annotation, “Router trained on development split only,” and an inference panel containing the learned uncertainty score, budget selection, the two sample-budget branches, and the final answer. Both sampling branches use the shared base model. Use the same method names as the text. Keep score inputs, score computation, decision rule, and final-answer combination in explicitly unresolved draft annotations until recovered from the implementation; do not invent thresholds, losses, calibration, voting, additional model calls, or a low-score/high-score branch direction.

**Source and scope:** The opening paragraph of the notes. This supports an overview, not an executable algorithm. Add measured routing traces only after they are supplied.

**Caption draft:** “BudgetRoute uses a learned uncertainty score to choose one or three samples before producing the final answer. Router training uses the development split only. The diagram summarizes the supplied method description; the score interface, budget-selection rule, and final-answer procedure remain to be specified.”

### Figure 3 — Results: observed accuracy and the domain-shift boundary

**Question and supported takeaway:** How does accuracy compare in the reported settings? The original test setting shows a small positive mean difference; the single shifted-domain run shows a substantial negative difference.

**Design:** A two-panel, two-column-width plot in Results. Panel A shows every reported test-run accuracy as an unpaired dot, with a distinct mean marker: baseline 70.2, 70.8, 71.4; BudgetRoute 70.4, 71.0, 71.6. Panel B shows the single shifted-domain observation for each method: baseline 55.0; BudgetRoute 49.0. Label run counts directly and use clearly labeled accuracy axes. Use common 0–100% axes; supply exact data labels so small differences remain readable. Do not connect run dots across methods because run pairing is unspecified, draw confidence intervals, or add significance symbols. Avoid connecting original and shifted conditions as paired trajectories.

**Source and scope:** The notes’ test-accuracy and shifted-domain-accuracy entries. This replaces a benchmark/environment figure: the notes do not describe a new benchmark or provide enough construction and scoring details to depict one.

**Caption draft:** “Accuracy in the reported test and shifted-domain settings. (a) Three reported runs yield mean accuracy of 70.8% for the fixed-three-sample baseline and 71.0% for BudgetRoute. Dots are individual run values, not confidence intervals. (b) One shifted-domain run yields 55.0% and 49.0%, respectively. No statistical tests were run. The positive test-setting difference does not establish a robust accuracy advantage under shift.”

## Main-paper allocation

Plan for the supplied 8-page limit, including figures and captions. This is a content budget, not a rendered page-count verification.

| Material | Pages |
| --- | ---: |
| Title and abstract | 0.50 |
| Introduction and teaser | 1.00 |
| Closest related work | 0.50 |
| Problem setting and method, including Figure 2 | 1.75 |
| Evaluation protocol | 0.75 |
| Results and material limitations, including Figure 3 | 2.50 |
| Discussion and conclusion | 0.50 |
| Layout reserve and required statements as applicable | 0.50 |
| **Total** | **8.00** |

Keep the shifted-domain failure, uncertainty limits, call-count definition, and essential method choices in the main text. Allocate required statements after their official placement and page accounting are known. Do not compress typography or pad the manuscript to fill this budget.

## Brief appendix and FAQ plan

Use the supplied **two-column appendix** format, preserving official typography. Mirror the main paper with explicit cross-references:

- **A. Method specification:** uncertainty-score inputs and model, training objective and supervision, budget-selection rule, final-answer procedure, and pseudocode grounded in the actual implementation.
- **B. Reproducibility:** dataset identities and split sizes; development/test separation; base-model version; decoding; baseline implementation and tuning; run identities; scoring; call-accounting definition; configurations and commands. Include the exact experimental prompts, message roles, variable substitutions, and variant-to-run mapping when supplied. Do not write new prompts and label them as used.
- **C. Complete results:** retain all six reported test accuracies, both shifted-domain accuracies, and the author-provided call aggregates with their limitations. Add later analyses only when completed and sourced. Candidate future controls are fixed-one-sample, fixed-two-sample, and an equal-budget nonlearned routing policy, followed by repeated shifted-domain evaluations and end-to-end timing; these experiments have not been run in the supplied record.
- **D. Matched examples and errors:** request exact inputs, references, both outputs, scoring, and routing traces for all supplied IDs. Use the explicit selection rule “all three author-supplied examples”: `ex001` both correct; `ex002` BudgetRoute correct/baseline wrong; `ex003` BudgetRoute wrong/baseline correct. This is an illustrative set, not a representative sample or evidence of error frequency. Until the text arrives, report only these labels.
- **E. Reader FAQ:** finish with a short set of evidence-linked questions; keep decisive answers in the main text as well.

Suggested FAQ entries and current answers:

| Question | Answer to develop and link |
| --- | --- |
| What improves over the fixed-three-sample baseline? | Reported call count falls by one call per question, with a +0.2-point observed mean test-accuracy difference; cite Main Results and Appendix C. |
| Is the accuracy improvement significant or equivalent? | Neither is established; no statistical tests or confidence intervals were supplied. |
| Does the result transfer under shift? | The one supplied shifted-domain run is worse by 6.0 points; cite Figure 3. |
| Does one-third fewer calls mean one-third faster or cheaper? | No such conclusion is supported; timing, token use, monetary cost, and overhead accounting are unavailable. |
| Is learned uncertainty responsible for the tradeoff? | The comparison does not isolate that mechanism; equal-budget controls and ablations are unresolved. |
| What is required to reproduce the result? | The complete method, datasets/splits, configurations, prompts, model version, per-example predictions/call logs, and scoring implementation; cite Appendices A–B when populated. |

## Unresolved inputs and checks

1. **Venue and disclosure:** supply the exact venue/year/track/stage, official policy and template, and required AI-disclosure wording/location. The activity to disclose is AI assistance drafting the abstract and contribution bullets and planning figures/appendix; do not claim author review or official compliance before it occurs.
2. **Method and provenance:** supply the actual router specification, implementation, model version, datasets/splits, run identities, evaluation/scoring procedure, and precise model-call accounting, including aggregation and overhead.
3. **Evidence and positioning:** supply per-example outputs and call logs, exact example text, experimental prompts, and a bibliography/closest-work comparison. The proposed controls, repeated shift runs, uncertainty analysis, and timing are future work, not completed evidence.

Checked locally: arithmetic gives means of 70.8% and 71.0%, a +0.2-percentage-point test difference, a 33.3% relative call reduction, and a −6.0-percentage-point shifted-domain difference. These checks validate arithmetic from the notes, not the underlying experiments. No external sources were consulted, experiments run, figures rendered, or template compiled.
