# Experiments and analysis

Use this reference to design, audit, interpret, or write an empirical evaluation. Begin with available artifacts: configurations, dataset documentation, run logs, raw outputs, analysis code, and recorded decisions. A proposed experiment belongs in a plan until it has run and its outputs have been checked. Missing results remain missing; never infer a measurement from a plausible mechanism.

## Questions determine the evaluation

Express each research question as a decision the evidence should resolve. Separate questions about effectiveness, mechanism, generalization, reliability, and cost. A contribution about efficiency needs an efficiency comparison; a claim about a component needs an intervention on that component. Additional benchmarks cannot substitute for the required test.

Before execution, record the hypothesis, target population, intervention, comparator, primary outcome, unit of analysis, relevant confounders, analysis plan, and conditions under which the claim would fail. Distinguish confirmatory questions from exploratory analyses suggested by observations. Exploratory findings can motivate further study without being presented as prespecified discoveries.

Create a compact evaluation map:

| Question | Required evidence | Interpretation boundary |
|---|---|---|
| Does performance improve? | Comparable runs on the same eligible test units | Restricted to tested settings and uncertainty |
| What produces the improvement? | Controlled removals, replacements, or interventions | Coupled changes may prevent attribution |
| When does the approach fail? | Prespecified slices, shifts, and inspected outputs | Unobserved conditions remain unknown |
| Is the benefit worth its cost? | Quality and resource use under comparable budgets | Hardware, workload, and accounting matter |

Use this map to decide what belongs in the main paper. Report evidence necessary to assess central claims there; place supporting configurations and expanded analyses in the appendix with explicit pointers.

## Data, splits, and benchmark environments

Report dataset identity, version, source, eligibility criteria, preprocessing, exclusions, and final counts. Distinguish examples from independent entities: images versus patients, queries versus users, or trajectories versus environments. Show train, validation, and test sizes in both relevant units, together with class balance, missingness, length distributions, and other properties that affect the task. Explain changes from published dataset statistics.

Split at the level that prevents information sharing across partitions. Keep related subjects, documents, conversations, near-duplicates, scenes, or generated variants together when they create dependence or leakage. Fit preprocessing, normalization, vocabulary adaptation, feature selection, and learned retrieval components using permitted training information. Select hyperparameters and checkpoints using validation data. Do not repeatedly adapt the method to a nominally held-out test set.

For temporal tasks, establish the prediction time and ensure that features, labels, retrieval sources, and model-accessible information respect the intended cutoff. Document temporal overlap, distribution changes, and any embargo or grouping rule. For pretrained models, describe contamination checks and their limits; inability to access training data is not evidence that contamination is absent.

A new benchmark needs a task and evaluation contract: eligible inputs, outputs, information access, construction, splits, success/failure conditions, scoring, and evaluator implementation. Interactive environments additionally need observation/action spaces, initial-state distributions, transitions, episode limits, reset behavior, randomness, and accessible tools. Do not invent actions or transitions for static benchmarks. Record relevant simulator/service versions and evaluation dates when behavior changes. Specify annotation, adjudication, filtering, and scoring, including invalid outputs, timeouts, refusals, retries, and partial credit. Test the evaluator on known cases before interpreting rankings.

For a benchmark contribution, explain why its score measures the claimed capability. Begin with what should change the correct answer or score, what should leave it unchanged, and plausible alternative routes to a high score. Choose the smallest validation that distinguishes the intended construct from a live alternative explanation:

- A shortcut control can test whether labels are predictable from source, length, formatting, or other incidental cues without the intended reasoning.
- A controlled transformation can test an expected invariant or response to a changed fact. Verify that the transformation really preserves or changes the target label before interpreting model behavior.
- Scoring or aggregation sensitivity can reveal whether a ranking depends on a particular parser, judge, weighting rule, or narrow slice. Report justified alternatives and their effects, rather than select the rule that produces a preferred ranking.
- Coverage and difficulty analysis can establish which claimed domains, cases, and ability ranges are represented, and expose floor/ceiling effects or missing regimes.

Select these checks from the actual task and claim; there is no experiment quota. Correct evaluator code and annotator agreement are useful but do not alone establish construct validity. Keep decisive validation in the main paper, document fuller protocols in the appendix, and narrow the capability claim when an alternative explanation remains unresolved. A useful benchmark should reveal a scientific distinction, not merely contain more instances.

## Baselines and fair comparisons

Select comparators that test the scientific claim: nearest prior work, strong relevant alternatives, a simple competitive baseline, and useful reference bounds. Explain omissions and unavailable implementations. Label published numbers, independently reproduced results, and results obtained with modified implementations distinctly; differing protocols may require separate table groups.

Document what is matched and what differs: training data, pretrained checkpoints, parameter count, inference access, tools, retrieval corpus, tuning budget, training compute, and test-time compute. Perfect matching is sometimes impossible; state the mismatch and constrain the conclusion. A method that uses extra data or additional search must not attribute the full gain to its architecture alone.

Give baselines a reasonable and documented tuning procedure. Use validation performance for selection, disclose search spaces and trial counts, and apply equivalent selection opportunities where feasible. Preserve standard recommended settings unless there is a justified alternative. Investigate unexpectedly weak reproductions through configuration, preprocessing, and metric checks before using them as evidence. Report unsuccessful reproductions honestly.

For resource-sensitive claims, compare both at a matched budget and across a quality–cost curve when possible. A single operating point can hide a trade-off. Include failure rates and usable throughput when invalid or rejected outputs consume resources.

## Repeated runs, uncertainty, and statistical decisions

Define the object of comparison: **fixed trained models**, **fixed training recipes**, or **procedures that include tuning and checkpoint selection**. Uncertainty conditional on one selected configuration does not characterize the whole selection procedure. State the target population, actual sampling unit, varied and fixed factors, and assumptions needed for the inference. Match wording to the executed design; do not imply that tuning was repeated because several seeds were run. [Accounting for Variance, Sections 2–3](https://arxiv.org/pdf/2103.03098v1) explains this distinction.

Choose repetition and sample sizes around the intended comparison, expected variability, and available resources. Record the choice before inspecting the decisive result. Do not keep adding runs until a desired significance threshold appears or discard unfavorable seeds. Sequential designs require a stated stopping rule and suitable analysis. If budget limits repetitions, disclose that limitation rather than inventing precision.

Distinguish training randomness, inference randomness, and sampling of test units. Three seeds do not automatically make an evaluation reliable, and thousands of correlated responses do not create thousands of independent observations. State what each reported interval or error bar varies over. Standard deviation describes dispersion; standard error and confidence intervals address estimation uncertainty under assumptions. They are not interchangeable.

Use paired comparisons when systems are evaluated on the same units and preserve that pairing in analysis. For clustered or hierarchical data, resample or model the relevant independent units and retain within-cluster structure. Examples include patients with multiple scans, tasks with repeated rollouts, and datasets with several model seeds. An interval over examples alone does not capture training-run variation. An interval over runs alone may not represent uncertainty over deployment tasks. Identify the population to which the estimate applies.

Report the measured effect and its uncertainty in interpretable units. Distinguish percentage points from relative percentage changes and identify the denominator of every ratio. For bounded, skewed, heavy-tailed, or sparse outcomes, choose an appropriate estimation method and explain it. Bootstrap procedures must preserve dependence and may be unstable with very few independent units. Do not present narrow intervals from an unsuitable resampling scheme as assurance.

Use a significance test only when its assumptions and question are appropriate. Record test choice, alternatives, pairing, multiple-comparison handling, and exact analysis inputs. Never manufacture a p-value, convert an error bar into an unsupported significance claim, or equate a nonsignificant difference with equivalence. Establish equivalence or noninferiority margins in advance if that is the question. Statistical significance alone does not establish practical value.

## LLM and human evaluation

Treat an LLM judge as a measurement instrument with possible bias. Record provider, model identifier or snapshot, evaluation date, complete prompt and rubric, decoding settings, response parsing, and error handling. Preserve prompts and raw judgments where permitted. A changed judge version or rubric constitutes a changed measurement procedure.

Blind method identity where possible, randomize or counterbalance presentation order, and test order sensitivity. Inspect preferences associated with answer length, formatting, familiar model style, and self-generated outputs. Use an explicit tie option when appropriate. Avoid assuming that agreement between several closely related judges establishes correctness.

Calibrate against an independently labeled, representative sample with clear criteria and adjudication. Report sampling, annotator expertise or instructions, disagreements, and agreement measures appropriate to the task. Human labels are fallible too. Separate rubric development and judge tuning from the final evaluation sample. If human validation is unavailable, name the measurement limitation and restrict claims accordingly.

For work involving people, record actual recruitment/eligibility, consent procedures, institutional ethics approval or exemption where applicable, privacy handling, risks, and compensation or lack of compensation. Use real study documentation; do not invent approval, consent, or demographics. Distinguish trained annotation from a user study and report relevant expertise, workload, and instructions. Follow institutional and venue requirements rather than assume every annotation task has the same approval process.

Track exclusions and failed judgments in the denominator. Where judgments are stochastic, measure relevant repeatability. Keep uncertainty over tasks distinct from uncertainty introduced by repeated judging of the same response.

## Ablations, robustness, and cost

Design each ablation around a mechanism claim. Removing a component may simultaneously change parameter count, training stability, compute, or information access. Include controlled replacements or matched-budget variants when those changes offer alternative explanations. State whether ablations are retrained and how each variant is tuned. A test-time removal answers a different question from training a model without the component.

When components interact, inspect selected combinations or a factorial design appropriate to the scope. Do not infer independent contributions from one-at-a-time removals alone. Check sensitivity over plausible hyperparameter ranges selected without test-set optimization, including the default setting and unstable regimes. Explain what remains unidentified if resources prevent further controls.

Robustness tests should follow plausible failure mechanisms: domain or temporal shift, noise, missing inputs, longer contexts, distribution tails, tool failures, changed environments, or adversarial conditions relevant to the claim. Specify how shifts were constructed and their severity. Keep adaptation data separate from the final shifted evaluation. Success on one constructed shift does not justify an unrestricted claim of robustness or out-of-distribution generalization.

For efficiency, define the resource accounting boundary. Report applicable totals for training, tuning, inference, retrieval, judging, preprocessing, storage, and failed attempts; component measurements supplement totals. State hardware, precision, batch size, concurrency, context lengths, cache conditions, warmup, synchronization, and measurement repetitions as relevant. Distinguish latency, throughput, memory, energy, tokens, and monetary cost. Report cost dates and assumptions if pricing is involved. Amortize setup costs only over an explicit workload.

## Qualitative examples and error analysis

Use actual recorded examples with traceable identifiers and consistent preprocessing. Define selection before choosing illustrative successes: random sampling, representative strata, or a documented diagnostic criterion. Purposefully chosen examples are valid illustrations when labeled as such; they do not estimate prevalence. Show favorable examples when supported, alongside representative failures, trade-offs, and counterexamples relevant to central claims. Never alter outputs to improve the apparent result.

For side-by-side comparisons, use identical inputs and display sufficient context to understand ground truth, predictions, intermediate actions, and scoring. Mark truncation, redaction, annotation, or reconstruction. Explain what each example demonstrates and what it cannot establish. A compelling visualization cannot substitute for aggregate evaluation.

Build an error taxonomy with operational definitions and a consistent annotation procedure. State whether categories overlap, how ambiguous cases are resolved, and which sample was inspected. Report counts and denominators: an error type may be a fraction of all examples, all failures, or only inspected failures. These quantities answer different questions. Include residual or unclassified errors rather than forcing every case into a favorable explanation. Check difficult labels and report disagreement when it materially changes conclusions.

Use error findings to bound claims and propose mechanisms, clearly separating observed patterns from causal explanations. Additional experiments may test those explanations; they do not become established facts through repeated discussion.

## Writing and reproducibility handoff

For each result cluster, write the question, relevant setup, measured finding, uncertainty, interpretation, and scope limitation. Interpret the important pattern instead of narrating every cell. Captions define units, metric direction, aggregation, sample size, error bars, abbreviations, and exceptional settings. Define highlighting rules consistently, including how ties are handled. Do not call a best mean a statistically established improvement without the appropriate comparison.

Connect evidence at the level it supports: a controlled example can explain an operation, a component experiment can test its local effect, and an end-to-end evaluation can establish a system outcome. A downstream gain alone does not identify its mechanism; a component gain does not establish downstream benefit. Organize the explanation around observed operating conditions: where the advantage appears, where it shrinks or disappears, and which measured bottleneck or control supports that boundary. Keep untested causal explanations provisional. Use available evidence; this is an explanatory structure, not a required sequence of experiments.

Provide an appendix and artifact manifest sufficient to reconstruct reported results: code revision, environment and dependency versions, data identifiers and split rules, preprocessing, configurations, hyperparameters and search spaces, checkpoint selection, seeds, hardware, runtime, prompts, judge settings, baseline modifications, commands, raw-result paths, analysis scripts, and figure/table generation steps. Record unavailable or restricted artifacts and practical access requirements. Every reported number should resolve to its source and transformation. Keep exploratory runs and excluded data in the audit trail with reasons; the final paper may summarize them without concealing decisions that affect interpretation.

When a reproducibility check is in scope, take a bounded path through a central table or figure: saved predictions or raw outputs → analysis command/configuration → generated result → displayed value/panel → claim. Run the documented analysis in a fresh output directory when feasible and authorized; verify identity, units, exclusions, aggregation, uncertainty, and rounding. Report the level actually tested: regenerating a table, rerunning checkpoint evaluation, and retraining are distinct. A writing edit does not imply expensive reruns. Diagnose mismatches instead of manually changing results to match expectations. [PaperBench, Section 2.2](https://arxiv.org/html/2504.01848v2) and [CORE-Bench, Section 2.1](https://arxiv.org/html/2409.11363v2) motivate separating execution from correct output recovery.
