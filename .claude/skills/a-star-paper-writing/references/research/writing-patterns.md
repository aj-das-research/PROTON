# Transferable writing patterns from the inspected subset

These are analyst inferences from 20 purpose-selected papers, not frequency estimates or acceptance predictors. See `primary-paper-notes.json` for exact versions, source links, original observations, and bounded reading scopes.

## 1. Make the research claim more specific than the topic

DPO motivates a change of variables in a difficult optimization pipeline; GDPO diagnoses a specific normalization failure. A strong opening connects the practical problem to a technical obstacle that the proposed mechanism actually addresses. A useful drafting test is: *If this obstacle disappeared, would the proposed mechanism still be necessary?*

The user's preferred abstract sequence is a good default: problem and motivation → limitation or challenge → proposal and mechanism → evaluated evidence and scope. It is not a sentence-count rule. Avoid spending most of the abstract on generic claims about the importance of AI.

## 2. Let the contribution determine the section order

The observed papers differ substantially:
- DPO uses preliminaries and a separate theoretical analysis.
- SAM and SAM 2 give task and data construction their own space.
- SWE-bench leads with benchmark construction before a baseline model.
- s1 presents data curation before inference mechanics and combines discussion with related work.
- LLaDA places related work after the experiments.
- Titans places related work in an appendix.
- Large model reports separate architecture, pretraining, post-training, infrastructure, and evaluation.

Use the user's preferred outline as a starting point, then justify deviations by reader dependencies and venue rules. Background belongs where the reader needs it. The labels *Method*, *Methods*, *Approach*, or a named method are editorial choices; the number of variants does not impose a heading.

## 3. Contributions are commitments to evidence

Prefer three or four concise contributions when there are three or four independently supported claims. Do not invent extra contributions to fill a quota. Each contribution should identify the new object or finding and point to its supporting theorem, experiment, dataset validation, or resource.

Keep a claim-to-evidence map. Separate scientific novelty from implementation work, resource release, and empirical findings. Report the conditions under which a statement holds.

## 4. Match evaluation to the scientific question

KAN separates accuracy and interpretability evidence. GDPO separates correctness from constraints and stability. GEAR separates quality from memory and throughput. s1 separates curation criteria from inference-budget control.

Build the evaluation around research questions and competing explanations. Explain what each comparison can establish. Baselines need comparable resources, tuning access, data, and inference budgets, with exceptions disclosed. Descriptive benchmark performance does not establish that every architectural component caused the gain.

## 5. Useful results include boundaries and failures

SWE-bench's low initial model success supports its benchmark motivation. Tree of Thoughts discusses cases where search adds little value. Self-RAG's inspected appendix includes unsupported and partially supported outputs. SAM 2 identifies concrete tracking failures. Kimi K3's abstract acknowledges stronger systems that remain ahead.

Qualitative analysis should use real logged examples with a documented selection procedure. Show successes that explain the mechanism and informative failures that define its scope. Never select or rewrite examples solely to make the proposed method look positive.

## 6. The appendix is a reproducibility interface

Map each main-paper section to its detailed counterpart. Depending on the paper, include notation and proofs, algorithms, data construction and splits, baseline configurations, model versions, hyperparameter search and chosen values, compute, inference settings, evaluation scripts, annotation instructions, prompts, extended results, and failure cases.

DPO and Self-RAG expose evaluation prompts. s1 documents nondeterminism beyond random seeds. SWE-bench exposes execution and instance construction details. SAM 2 separates data, model, evaluation, and annotation material. These are useful patterns; the appendix must still follow the target venue's actual rules and remain navigable.

A compact main paper cannot defer the information required to understand or judge its central claim. The appendix deepens the argument rather than hiding its missing premises.

## 7. Prompts are experimental artifacts

Give each prompt a stable identifier and its exact text, role, variables, model/version, decoding settings, parsing rules, and connection to an experiment. Separate system, user, tool, and judge prompts. Specify ordering/randomization and calibration for model judges. Typeset long prompts with readable line breaks and modest styling permitted by the venue.

Use literal source files as the canonical artifact; prevent manuscript formatting from changing whitespace-sensitive or executable content. A prompt used only in an exploratory run must not be presented as the final evaluation prompt.

## 8. FAQ is a user preference, not an observed acceptance rule

The inspected subset does not justify a universal 12–15-question appendix FAQ. Use one only when it improves navigation and fits the venue. Keep at most 12–15 substantive questions, answer from existing evidence, and link each answer to the relevant section, table, experiment, or limitation.

Questions should address likely confusion: novelty boundaries, baseline fairness, leakage, compute, tuning, generalization, failure conditions, ablations, prompt dependence, reproducibility, and deployment assumptions. Never use an FAQ to hide essential methodology or promise evidence that does not exist.

## 9. Do not copy the surface form of a technical report

Large technical reports can reveal valuable reporting practices while exceeding conference space limits and using different layouts. The observed corpus does not establish a universal 11-page body, unlimited reference allowance, single-column appendix, mandatory number of figures, or one-paragraph discussion. Check the exact venue, year, track, submission stage, and official template before setting those constraints.

No wording pattern can guarantee acceptance. Writing quality helps reviewers understand supported work; it cannot substitute for novelty, soundness, evidence, or fit.

