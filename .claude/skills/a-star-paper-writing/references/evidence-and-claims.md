# Evidence and claims

## Build a defensible thesis

Distinguish problem (what is unknown/inadequate), gap (why closest evidence does not resolve it), insight (what changes the approach), mechanism (what is implemented/proved), and consequence (what evidence establishes). A paper may contribute a better measurement, resource, impossibility result, or reliable negative finding; a new module is not required.

Use a working thesis: “Under [setting/assumptions], [mechanism/finding] enables/shows [outcome], established by [evidence], with [boundary].” Fill it only with facts. A thesis requiring three unrelated mechanisms often needs a narrower central question.

Assess **significance** separately from correctness and novelty. What can a reader now infer, measure, explain, or accomplish that the closest alternative did not adequately enable? Explain why that change matters at the demonstrated scale, under the actual assumptions, costs, and access conditions. An important application does not make every modification important; a statistically significant difference does not establish useful value.

Make the consequence specific to the contribution: a meaningful quality–cost tradeoff, a distinction a benchmark can now measure, a theorem informative in a relevant regime, or a negative result that changes an accepted explanation. Compare with the closest alternative and separate demonstrated value from possible future uses. Simplicity and modest effect size do not automatically imply insignificance. Record a reasoned appraisal and its uncertainty, not an impact score or a requirement to beat state of the art.

## Type the claims

| Claim | Necessary support | Frequent mismatch |
|---|---|---|
| Empirical improvement | Comparable measurements and protocol | Different data/tuning/budgets/versions |
| Robustness/generalization | Defined shift and independent test conditions | One in-distribution test called generalization |
| Efficiency | Matched quality/budget; hardware and cost definition | Parameter count presented as latency |
| Mechanistic/causal explanation | Controlled intervention or identification argument | Ablation association called a complete explanation |
| Theoretical guarantee | Formal statement, assumptions, proof, applicability | Empirical trend described as a theorem |
| Benchmark validity | Construct, coverage, splits, scoring reliability | More instances mistaken for better measurement |
| Novelty | Current closest-work comparison with qualified scope | A keyword search treated as proof of priority |
| Reproducibility | Sufficient artifacts and tested instructions | Repository link without configurations/data |

For “first,” “state of the art,” “universal,” “optimal,” “significant,” or “human-level,” specify scope and evidence or narrow the claim. Statistical significance requires an actual test and assumptions; ordinary importance needs different wording.

## Evidence ledger

For each central claim record ID, exact wording, type, scope, status, evidence IDs, contradictory/qualifying evidence, source artifacts/locators, and manuscript locations. Evidence should identify data/version/split, metric/direction/unit, baseline/version, compute/interaction budget, run/seed IDs, aggregation/uncertainty, and exclusions. Citation records need verified metadata, source URL/version, locator, and supported claim.

Use the packaged JSON example and audit interface for machine-readable fields. Extend it for project needs; a schema does not excuse omitting substantive context. Link raw outputs → analysis code/config → derived table/plot → written claim. Record hashes or immutable revisions when feasible. Author-supplied aggregates can support provisional prose with their source and verification status recorded separately; they cannot establish unprovided seeds or confidence intervals.

Keep raw outputs immutable. Document corrections, filters, failed runs, exclusions, aggregation changes, and retuning. Distinguish pre-specified from exploratory analyses. Pending/planned/unsupported evidence cannot support an affirmative final finding. A “verified” label is an assessment, not proof.

### Manuscript voice and editorial notes

Write manuscript prose in the authors' voice. Keep the assistant's access and verification state in an editorial note or evidence record: “aggregate supplied; raw logs not yet inspected.” Do not describe the authors' own measurements as “author-reported” throughout their paper or put “files were not supplied to the assistant” in a caption. Maintain attribution for actual third-party results.

Distinguish an unavailable artifact from an unperformed study procedure. If the assistant lacks run logs, it cannot conclude that the study lacked repeated runs; flag that question for verification. If the study actually used one run or did not measure runtime, state that limitation where it constrains the scientific claim. Keep unresolved findings provisional or marked with a specific working placeholder; fluent author-voice prose does not upgrade their evidence status. Required AI-use disclosure remains in its prescribed location.

## Numerical assertions

Distinguish percentage points and relative changes: from 60% to 63% is 3 percentage points and 5% relative increase. Calculate from unrounded authoritative values and round for display. Do not imply precision beyond the measurements.

For every average define units being averaged—examples, tasks, seeds, domains, runs—and weights. Do not average incompatible metrics. State denominators and missing-data rules. Separate run standard deviation, standard error, bootstrap confidence interval, and across-task variation.

For “up to,” identify the condition and show typical effects or the distribution. Never promote the best seed to a general result. Do not combine one baseline's accuracy with another's compute cost. Label literature numbers as reported rather than rerun and check comparability before ranking them together.

## Scope ladder

A single run establishes an observation under recorded conditions. Repeated runs characterize variability. Multiple datasets test selected settings. An ablation isolates a comparison. A proof applies under assumptions. No step automatically supplies the next.

For mixed results, identify beneficial and failing regimes. This can be more useful than an unsupported universal win. Include costs, sensitivity, and limitations that affect application. An unperformed experiment is not reassuring evidence.

## Make gaps actionable

Choose retrieving an artifact, running authorized analysis, proposing an experiment, narrowing a claim, moving an explicitly preliminary observation out of the headline, or removing it. State the minimum discriminating test and interpretation under competing explanations without predicting its outcome as fact.

A sound handoff is: “The method and protocol are drafted. Cross-domain generalization remains pending because only in-domain outputs are available.” A polished unsupported abstract is not a better deliverable.
