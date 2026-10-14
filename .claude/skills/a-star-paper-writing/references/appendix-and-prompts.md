# Appendix, prompts, and reader questions

Read this when planning supplementary material, documenting reproducibility, or preparing the final appendix. The appendix should let a careful reader reconstruct the research and locate the evidence behind its claims. It is a navigable extension of the paper, not a place to hide caveats that change the main conclusion.

## The lean-appendix contract (author and lab rule, September 2026)

This section overrides any tendency below toward completeness for its own sake.
Nils Lukas and the author set it for their ICLR 2027 papers:

- "We're loading the gun for the reviewer to find something in the appendix
  that they will discuss to the Wazoo."
- "Nobody in their right mind is ever going to read [number tables]... In each
  section you should only summarize the interpretation."
- "Nobody is going to read it anyway, so everybody is going to put it into their
  agent and the agent is always negative on this."

The contract:

- **Length.** Aim for about 8 to 10 pages. Cut anything the main text does not
  need to be believed or reproduced. "If you don't need it, cut it."
- **Tables.** Use at most 5 or 6. Turn long tables into graphs, with several
  panels per row. Merge related tables, and report mean ± SD rather than
  per-seed rows.
- **Interpretation over numbers.** Every appendix section opens with the
  question it answers and the finding, and keeps only the evidence that
  carries it.
- **Nothing contradicts or undersells the main text.** Check every number,
  configuration (steps, samples, seeds, splits), term and claim against the
  main text. Remove "pilot", "failed", "historical diagnostics" and run logs,
  and state scope positively.
- **No report material.** No file paths, run names, job ids or experiment
  numbers.
- **Prompts.** Include only the prompts the paper's claims need: model-facing
  prompts for the proposed method, the judge rubric, and any prompt a baseline
  depends on. Drop the rest.
- **No FAQ section** unless the author asks for one ("no need for FAQs",
  2026-09-21). Put an important answer where the argument needs it.
- **Keep strong evidence in the main text.** Do not move key results or the
  qualitative analysis into the appendix to save space. Cut prose instead.

## Establish the appendix contract

Check the current venue, year, track, and submission phase before choosing page count, one- versus two-column layout, separate supplement files, anonymity, or permitted packages. The user's preference is a readable, mostly one-column appendix where allowed. Keep the official typeface, margins, spacing, and heading hierarchy. Do not redefine the template or shrink text to fit a self-imposed length.

Retain in the main paper the information needed to assess the central contribution: problem assumptions, key mechanism, evaluation protocol, essential baseline conditions, primary evidence, and limitations that materially bound the claims. The appendix can give complete derivations, execution details, full tables, prompts, examples, and additional analysis. Do not put the only evidence for a headline claim in material reviewers may not be required to read.

Create an appendix map before drafting. Every section should answer a reader question and identify its source artifacts. Use stable labels and references rather than hard-coded page numbers. For a long appendix, add a short contents list if the template permits. Begin each section with one or two sentences explaining what it adds and where it connects to the main paper.

Preferred order, omitting genuinely inapplicable sections:

| Section | Purpose | Typical contents |
| --- | --- | --- |
| A. Additional background and notation | Supply the foundations needed to reproduce or understand the work | Problem setting, notation, standard objectives, assumptions, prerequisite results |
| B. Method details | Specify the proposed computation completely | Derivations, algorithms, interfaces, proofs, complexity, boundary cases |
| C. Experimental details | Make the evaluation reconstructable | Implementation, hyperparameters, baselines, datasets, environment/protocol, prompts |
| D. Extended results | Expose the evidence beyond the main tables | Full benchmark results, ablations, sensitivity, robustness, resources, negative results |
| E. Qualitative and error analysis | Explain where and why behavior changes | Matched examples, failure taxonomy, sample selection, case studies |
| F. Additional discussion | Address scope and remaining uncertainty | Mechanistic hypotheses, tradeoffs, limitations, validity threats, future work |
| G. Reader questions (only on request) | Resolve targeted questions the author asked for | Evidence-linked FAQs, only when the author requests them |

Keep the experimental-details subsections ordered as implementation, hyperparameters, baselines, data, evaluation setup, and prompts, adapting when the paper's logic requires a different dependency. A dataset/benchmark paper may need data construction before model implementation. Section lettering is illustrative; follow the chosen template and existing manuscript.

## A. Background and notation

Define mathematical objects, domains, units, shapes, and conventions once. Include a compact notation table only when it removes repeated lookup. Distinguish observations from latent variables, training distributions from test distributions, and instance-level quantities from averages. Carry the exact symbols into the method, algorithms, and figures.

Explain standard losses or procedures with a citation and only the detail required to understand this paper's modification. Mark what is established background and what is proposed. State support, differentiability, independence, boundedness, or other assumptions when a derivation depends on them; do not add conventional assumptions that the actual implementation violates.

Background can live partly in the main paper. If a definition is necessary to understand the main method, introduce it there and place the full derivation here. Avoid repeating the related-work survey. A theoretical paper may instead place formal preliminaries early in the main paper and reserve supplementary lemmas for the appendix.

## B. Complete method specification

Provide the contract at each interface: input/output types, dimensions, preprocessing, state, parameter sharing, and what is learned or frozen. Describe training and inference separately when they differ. State initialization, update order, normalization, objective coefficients, stop-gradient boundaries, sampling, filtering, thresholds, constraints, and termination when relevant. Resolve differences between the manuscript, code, and figure instead of describing an idealized algorithm the experiments did not run.

For iterative or agentic systems, document state persistence, memory updates, observation/action availability, tool schemas, retries, recovery, stopping, and resource limits. Separate model-visible information from evaluator-only information. Explain whether feedback changes the same episode, later episodes, model weights, or none of these. For multi-method papers, give each method a stable name and state which components and assumptions are shared.

Pseudocode should expose decisions a reader cannot reconstruct from prose. Define every operation and return value, indicate random draws, and state meaningful failure conditions. Do not present illustrative pseudocode as bit-for-bit executable code. Point to the actual implementation version when available.

For mathematical claims, state each proposition with its assumptions, then provide the proof without skipping the step that carries the novelty. Reference background results precisely. Identify approximations and empirical hypotheses separately from proved statements. For complexity, name the variables and count the relevant operations or memory terms; a theoretical bound is not a measured runtime result.

Close with edge cases that materially affect correctness: empty candidate sets, context truncation, invalid outputs, unavailable retrieval, exhausted budgets, degenerate parameters, or failed optimization. Include only cases relevant to the implemented method.

## C. Reproducible experimental details

### Implementation and execution

Record software and model versions at the resolution actually known: repository commit, package lockfile or environment, checkpoint identifier/revision, API model identifier and access dates, precision/quantization, tokenizer, preprocessing, and relevant nondeterministic behavior. Do not invent an unavailable immutable API revision. Explain that such a dependency may drift when appropriate.

Report hardware and execution conditions needed to interpret cost: accelerator type/count, memory, relevant CPU resources, batch size, parallelism, warm-up, synchronization, caching, and throughput or latency measurement procedure. Distinguish total study cost, training cost, per-run cost, and inference cost. Preserve the unit and denominator, such as seconds per example, tokens per episode, or GPU-hours per run.

Provide commands or configuration references that reproduce data preparation, training/adaptation, evaluation, and table generation. Use project-relative paths and list required inputs. State which artifacts are released, unavailable, or scheduled for release without claiming availability prematurely. Maintain anonymity when required by the submission phase.

### Hyperparameters and model selection

Use an explicit table rather than scattering settings across prose:

| Component | Setting | Value or search range | Selection rule and data | Applies to |
| --- | --- | --- | --- | --- |
| Named component | Actual parameter | Exact value/range or unresolved | How chosen; validation split; tuning budget | Model/dataset/experiment IDs |

Document optimizer, learning-rate schedule, warm-up, effective batch size/accumulation, training steps or epochs, weight decay, clipping, initialization, seeds, stopping, checkpoint choice, and objective weights when used. For generation, include decoding, temperature, top-p/top-k, sampling count, length limits, stop sequences, and determinism settings. For retrieval, include corpus/index version, chunking, embedding model, top-k, reranking, and context budget. Do not include irrelevant settings merely to make the table long.

Distinguish chosen values from the search space and distinguish per-dataset tuning from a shared setting. State tuning trials and comparable selection effort for baselines when known. Explain use of training, validation, development, and test data; report any test-set adaptation directly. Missing settings remain marked unresolved until recovered from logs/configurations.

### Baseline details

List each baseline with its primary reference, implementation source/version, checkpoint, inputs, adaptation, prompting, tuning procedure, and resource conditions. Distinguish numbers copied from a publication, obtained through an official evaluator, and reproduced locally. Record source locations for copied numbers and reasons an exact reproduction was unavailable.

Explain material deviations from a reference implementation and the resulting comparability limit. Use the strongest relevant alternatives available under the paper's stated scope; identify incomparable conditions visibly instead of silently pooling them into a ranking. Preserve failed reproductions and exclusions in the experiment record, then summarize their implications where they affect the interpretation. Do not attribute a failed reproduction to the baseline's inherent quality without evidence.

### Data and splits

Provide dataset/source version, license or access constraints when relevant, collection dates when material, unit of observation, sizes after filtering, and the rule assigning examples to train/development/test. Explain group-, source-, subject-, document-, time-, or task-level separation when ordinary random splitting could leak information. State deduplication and contamination checks actually performed and their limitations.

For constructed datasets, document inclusion/exclusion, generation, annotation instructions, annotator qualification where relevant, adjudication, agreement, filtering, quality checks, and category distributions. Distinguish raw, filtered, sampled, and evaluated counts. The table's counts should reconcile with the manifest or explain differences such as excluded invalid examples.

For benchmark environments, document version, construction, unit of evaluation, observation/actions, evaluator-only information, reset/persistence, seeds, budget, termination, and scoring. An existing environment remains existing even when used in a new evaluation. Reference the setup figure through the figure-integration contract when it helps explain the protocol.

### Evaluation and uncertainty

Define metrics, units, direction, aggregation, weighting, tie handling, invalid-answer handling, exclusions, and score normalization. For a learned or LLM judge, give the exact rubric and prompt, judge identity/version, order randomization, repeated judging, calibration or human comparison if performed, and bias limitations. A metric's familiar name does not make all implementations equivalent.

Describe the independent unit underlying uncertainty and statistical tests: training seed, sampled item, subject, task, or another unit. Report the number of runs/items, interval method and level, and bootstrap/resampling unit when used. Avoid treating correlated outputs as independent. Identify planned primary comparisons and exploratory analyses when that distinction affects interpretation. Link computations to raw results and scripts.

### All experimental prompts

Include the exact prompts that were actually used for the reported study: system, user, assistant demonstrations, evaluator/judge, retrieval query generation, tool descriptions, output schemas, revision/repair, and any stage-specific prompts. “All prompts” means all material experimental prompt variants, not a paraphrase of the central instruction. It does not mean disclosing private platform instructions unrelated to the experiment.

Maintain a prompt inventory before formatting:

| Field | Required meaning |
| --- | --- |
| Prompt ID and version | Stable identity used by configs, runs, and result tables |
| Purpose and stage | What receives it and when it is used |
| Model and message roles | Model/checkpoint/API identity; exact ordered message roles |
| Template source | Repository-relative path and revision or file hash |
| Variables | Exact placeholders, types, source, escaping, truncation, and insertion order |
| Demonstrations | Source, count, selection/order, and whether shared across conditions |
| Execution | Decoding settings, budget, retries, tools and context assembly |
| Output | Expected schema, parser, validation, repair, and scoring |
| Coverage | Experiments, datasets, methods, and results that use this version |

Keep a canonical plain-text or structured message file alongside the formatted appendix. Preserve role order, delimiters, punctuation, meaningful whitespace, examples, and output schema. Make omitted large variable content explicit through a typed placeholder plus the exact construction rule; supply a representative fully instantiated example when permitted and useful. Mark that example as illustrative if it was not an actual evaluation instance.

Use visually distinct but restrained presentation: a short descriptive title, stable prompt ID, role labels, readable body text, and a thin rule or pale neutral background if permitted. Maintain the official body font for surrounding prose; use a legible monospaced face for literal prompt content and schemas. Color may reinforce roles but must not be the only distinction. Avoid dark filled pages, screenshots of text, tiny type, decorative fonts, and boxes that clip or become unreadable in grayscale.

Long prompts should break across pages cleanly, with continuation labels and intact role boundaries. Prefer a standard listing or simple breakable environment already compatible with the template; avoid new package dependencies unless necessary. Do not squeeze prompts into a figure that destroys text selection or accessibility. A table can summarize prompt metadata, while a separate listing preserves the exact content.

Show all materially different variants. If variants differ only by documented substitutions, give the canonical template plus a complete variant table instead of duplicating pages. If a wording change was evaluated, preserve each tested wording and its result mapping. An improved prompt drafted after the experiment must not replace the prompt associated with reported numbers.

When sensitive or restricted dataset content must be omitted, label the redaction, explain its effect on reproducibility, and retain a safe description of the field and process. Never silently replace experimental content while calling it exact. If a hidden proprietary prompt prevents exact reproduction, state that limitation.

## D. Extended results and analyses

Build this section from the experiment inventory and the paper's research questions. Include complete per-dataset or per-task results behind aggregate claims, the relevant baseline rows, run summaries, and full ablation/sensitivity tables. Preserve negative or null findings that change the claim. Consolidate redundant tables rather than appending every intermediate formatting draft.

Give each table or plot a purpose: validate a mechanism, test robustness, quantify cost, explain variation, or expose a boundary. Start each subsection with the question and experimental control, then report the observation, uncertainty, interpretation, and limit. Clearly label exploratory or post-hoc analysis. Do not turn correlation into a causal explanation without an appropriate intervention or design.

Sensitivity studies should show the tested range and selection procedure, not just the favorable neighborhood. Ablations should isolate the claimed component and account for changed parameter count, data access, or compute where these can explain the result. Robustness and generalization claims should name the shifts actually tested. Cost studies should align quality, budget, and hardware conditions or label the tradeoff explicitly.

Keep measured values, metrics, and significance markers tied to the canonical result ledger. Table notes must define abbreviations, uncertainty, missing entries, bold/underline conventions, data source, and comparison conditions. Use “not evaluated” or “not reported” rather than zero for absence. Do not use visual emphasis to imply a statistically established difference when only point estimates were compared.

Include supplementary figures through the same provenance and visual inspection standard as main-paper figures. If raw full outputs are too extensive for the appendix, provide a clear manifest and released artifact link where allowed. State what is available rather than promising a nonexistent archive.

## E. Qualitative examples and error analysis

Select examples through a documented rule: seeded sampling, stratification by predefined categories, or clearly labeled illustrative case selection. Present matched inputs across methods with the same crop, scale, truncation, postprocessing, and output budget. Include enough input/context for the reader to assess correctness independently. Mark author annotations separately from model outputs.

A persuasive success case reveals the proposed mechanism; it does not replace aggregate evidence. Include representative failures and cases where improvements disappear when these delimit the contribution. If a visually favorable case was selected to explain a mechanism, say so and do not call it typical without data.

For an error taxonomy, define categories, assignment procedure, overlap, sample size, and denominator. Report counts or proportions from the inspected set, not an impression of frequency. Preserve ambiguous cases. If humans label errors, describe the process and agreement when measured. If a model labels errors, disclose its prompt/model and validate the relevant claims where possible.

Use case studies to distinguish observed behavior from the proposed explanation. A trace may show which tool was called; it does not directly reveal an unobserved internal reasoning process. Tie examples to stable IDs so readers can locate the associated prompts, predictions, and scoring decisions.

## F. Additional discussion

Use this space for implications and remaining uncertainty that need more explanation than the main paper permits. Separate supported conclusions, plausible mechanisms, hypotheses, and future experiments. Discuss the conditions under which the method is useful, what it costs, where it fails, and whether its assumptions fit the intended deployment or scientific setting.

The user's preference is a concise main-paper discussion/conclusion, often a paragraph each or one combined paragraph when appropriate. The appendix can expand that reasoning without introducing a different central claim. Material limitations, invalid comparisons, data leakage concerns, and unsupported generalization must also be reflected in the main paper and abstract as needed.

## G. Reader and reviewer FAQ (only when the author asks for it)

The author dropped FAQ sections from their papers (2026-09-21). Add one only on an explicit request, and then keep it short. If the author asks for a FAQ, finish with a focused one when it materially improves navigation and resolves likely questions. Use no more than 15 questions, and do not pad a shorter paper. Select questions from actual ambiguity, independent review, and the gap between claims and evidence. Avoid a generic checklist disguised as questions.

Each answer should contain a direct response, the strongest relevant evidence and section/table reference, and a boundary or unresolved point where necessary. If an anticipated question exposes missing evidence, add an experiment request or narrow the claim rather than inventing a confident answer. Critical information revealed by a FAQ belongs in the corresponding main or appendix section too.

Candidate question families, select and specialize only those that matter:

1. What is the precise contribution beyond the closest prior method or benchmark?
2. Which assumption makes the approach useful, and when does it fail?
3. Could the gain come from extra data, parameters, compute, or prompt tuning?
4. Are the baseline and proposed-method conditions comparable?
5. How were train/development/test separation and contamination checked?
6. Which component is responsible for the improvement, and what supports that attribution?
7. How stable are the results across seeds, tasks, or model variants?
8. What is the strongest counterexample or failure category?
9. Do results transfer beyond the tested distribution or environment?
10. How much training, inference, memory, or monetary cost is required?
11. How sensitive is the method to hyperparameters, prompts, or decoding?
12. Could the evaluator or judge favor a method or output style?
13. What exactly is needed to reproduce the main result?
14. What data, code, checkpoints, prompts, and licenses are available?
15. What remains untested or unresolved, and how does it limit the conclusion?

Questions are candid reader aids, not simulated rebuttal victories. Do not frame known limitations as strengths or promise acceptance. Avoid answering with “see appendix” alone: give the actual answer, then the locator.

## Final appendix review

Check the compiled manuscript and supplement together. Confirm that every cross-reference resolves, table/figure numbering is consistent, notation matches, prompts are complete and legible, links respect anonymity, counts reconcile, and all declared artifacts exist. Inspect page images for clipping, stranded headings, overflowing listings, excessive whitespace, tiny captions, and unexpected font changes. A successful compile does not establish readability.

Trace a central claim backward from abstract to main result to extended table to raw result/config/prompt. Trace one qualitative example through input, output, scoring, and selection record. These checks should expose inconsistencies that a heading checklist cannot.

When material remains unavailable, leave the appendix's status explicit: what is complete, what is missing, and which claims depend on the missing material. Preserve useful progress without fabricating reproducibility or implying that an unreadable or incomplete supplement is submission-ready.
