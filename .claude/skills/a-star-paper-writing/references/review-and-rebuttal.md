# Scientific review, response, and revision

The objective is a defensible paper with a clear contribution and an auditable evidence trail. An internal review can expose defects; it cannot predict or guarantee acceptance. Use the target venue's current rubric and `venue-policy.md` before applying this procedure.

## What official guidance supports

Primary sources accessed **2026-09-17**:

- [ARR reviewer guidance](https://aclrollingreview.org/reviewerguidelines) asks reviewers to evaluate contribution type and scoped claims. It warns against treating missing state-of-the-art performance, negative results, simplicity, or disclosed limitations as automatic rejection reasons. Additional experiments should be necessary to the paper's claims, rather than merely interesting. Its visible notice says the version applies through the August 2026 review cycle and will be updated; refresh for later cycles.
- [AAAI-26 main-track CFP](https://aaai.org/conference/aaai/aaai-26/main-technical-track-call/) evaluates novelty, significance, soundness, relevance, clarity, responsible research, and reproducibility. Track-specific rubrics can differ.
- [ICML 2026 author instructions](https://icml.cc/Conferences/2026/AuthorInstructions) describe responses as an opportunity to resolve important uncertainty and misunderstandings, and disallow revised-paper upload during feedback. Reviewers need not follow response links.
- [CVPR 2026 response template](https://github.com/cvpr-org/author-kit/blob/main/rebuttal.tex) sets a one-page total including figures/references and restricts new unrequested contributions. See the precise snapshot and source hash in `venue-policy.md`.

The workflow below is an original operational synthesis. It is not presented as a conference-mandated scoring system.

## First pass: reconstruct the argument without the appendix

Give a fresh reader only the frozen manuscript for this first pass, before explaining the research or supplying the project brief and intended argument. Read the title, abstract, introduction, overview figure, method, primary results, and conclusion. Then reconstruct, without copying sentences:

1. What question is answered, for whom, and under what setting?
2. What was not adequately addressed by the closest prior work?
3. What is the new mechanism, resource, theorem, evaluation, or finding?
4. What observation or argument could disprove the strongest claim?
5. What evidence addresses that possibility, and where is it in the main paper?
6. What remains uncertain or outside scope?

If an answer is unclear, locate the first missing dependency: an undefined object, unexplained step, absent comparison, or unsupported inference. Supply a usable replacement sentence, transition, or reordered passage at that location. Repair the argument before polishing later sentences. An attractive figure or fluent abstract must not compensate for invalid evidence. If an indispensable answer appears only in the appendix, bring the necessary explanation into the main argument. Technical review may then consult the full evidence packet.

## Independent review roles

When agents or collaborators are available, assign separate bounded reviews of the same frozen draft. Ask each to cite exact manuscript locations and evidence identifiers. Do not tell them that the proposed method must win or that the paper deserves acceptance.

| Role | Questions to resolve | Required output |
|---|---|---|
| Closest-prior-work reviewer | Is the gap accurate? What changes relative to the nearest methods? Does the paper credit reused ideas? | Novelty map, missing verified sources, overstated distinctions. |
| Technical reviewer | Are definitions and assumptions sufficient? Are equations, algorithm and implementation consistent? Is each theorem actually established? | Localized correctness issues and concrete checks. |
| Empirical reviewer | Are splits, metrics, budgets, baselines, uncertainty and selection procedures appropriate? Could leakage or a confound explain the gain? | Claim-critical threats and minimum discriminating tests. |
| Reproduction reviewer | Could another researcher reconstruct the main table from the documented artifacts? Are unavailable assets clearly identified? | Missing configuration, version, prompt, data or compute details. |
| Reader and presentation reviewer | Does the narrative match the evidence? Are figures, captions and tables legible and self-contained? | Ambiguities, redundancies, terminology/notation inconsistencies. |
| Venue reviewer | Does the actual rendered package meet the verified year/track/stage rules? | Documented rule violations or unresolved policy fields. |

Reviewers must distinguish observed defects from suspicions. “Possibly contaminated” is a hypothesis requiring inspection; “contaminated” needs evidence. Do not invent citations to strengthen criticism. Do not infer misconduct from style, affiliation, topic popularity, or an automated AI-detector score.

Adjudicate comments against that snapshot before revising: **confirmed defect**, **plausible unresolved concern**, **already addressed**, or **unsupported criticism**. Check the cited location and evidence, including the appendix where relevant. Merge duplicates; agreement among agents does not create independent scientific evidence. Resolve conflicting criticisms through the claim and source rather than majority vote. LLM feedback can be useful yet generic or technically shallow ([Liang et al., limitations and discussion](https://arxiv.org/pdf/2310.01783v1)); another review pass alone need not resolve a substantive uncertainty.

## Issue ledger and decisions

Create one issue per material concern:

```text
issue_id:
claim_id:
manuscript_location:
finding:
evidence_or_reproduction_steps:
severity: blocking | major | minor
confidence: high | medium | low
disposition: revise_text | run_check | new_experiment | narrow_claim | no_change_with_reason
owner:
resolution_evidence:
status: open | resolved | explicitly_deferred
```

Treat fabricated citations/results, an invalid central proof, test-set tuning, a broken evaluation, and an unsupported headline claim as blocking. A missing discriminating baseline, inadequate uncertainty for a central comparison, or an untested decisive confound is usually major. Cosmetic wording is minor unless it changes scientific meaning. Calibrate severity to the manuscript's actual claim and contribution type.

Do not average issue severity into an invented acceptance probability. A single central correctness defect can dominate many presentation strengths. Resolve a defect by adding evidence, correcting the claim, or narrowing scope; relabeling it as a limitation does not make an invalid conclusion valid.

For a writing repair, provide replacement prose grounded in available evidence, not only a scorecard or a request to “clarify.” Explain the scientific change briefly and preserve technical meaning. Recheck affected claims and dependent passages after revision. Stop when material concerns are resolved or accurately bounded, not when simulated reviewers produce a desired score.

Separate experiments that resolve a live validity threat from optional breadth. For each proposed experiment, record the question, competing explanations, minimum protocol, decision criterion, expected cost, and how either outcome changes the manuscript. A useful negative outcome should still update the paper. Stop adding experiments once the remaining scoped claims are adequately supported; reserve ambitious new work for a separate study.

## Result honesty and qualitative evidence

Report the actual central tendency and variability, number of runs or samples, evaluation unit, excluded runs and their reasons, and all material outcomes of the declared protocol. Compare under compatible data, access, compute and tuning conditions, or explicitly label differences. A best-of-many score must not be presented as a typical run. Statistical significance does not by itself establish practical importance.

For qualitative examples, retain an example manifest: source split, example identifier, selection method, exact system configuration, raw output, annotation or scoring procedure, and any transformation for display. Show representative strengths and failure modes relevant to the claim. An illustrative success can explain a mechanism but does not establish prevalence. Do not fabricate dialogues, hide a system's failure, or reword outputs without labeling the change.

Maintain a consistency check across abstract, introduction contributions, method definitions, tables, plots, captions, conclusion and appendix FAQ. When new evidence weakens a claim, update all of these locations. Error analysis earns its place by explaining which conditions change performance and what that implies about the mechanism.

## Prepare the response before drafting it

Freeze the submitted paper and supplement as immutable reference versions. Retrieve the actual response rules: character/word/page limit, whether limits are per-review or total, permitted links, anonymity, whether revised PDFs are allowed, and whether new results are permitted. Never borrow another venue's rebuttal mechanics.

Parse every review into actionable points, including positive observations that clarify what the reviewer understood. Merge shared issues, keep reviewer identifiers, and mark the smallest factual disagreement. Build a response matrix:

| Reviewer / concern | What is being questioned? | Existing evidence | Needed action | Planned response location |
|---|---|---|---|---|
| Placeholder | Novelty / validity / clarity / scope / reproducibility | Section, table, claim or artifact ID | Clarify, correct, test, narrow, or acknowledge | Shared response or individual answer |

Prioritize matters that could change the assessment: a misunderstood method, an unfair comparison concern, an incorrect novelty attribution, a missing key detail, or an actual correctness error. Address minor presentation suggestions efficiently. Do not spend the response budget rebutting every preference.

If a reviewer asks for an experiment, first check whether it bears on a claim and whether it is feasible and permitted at the current stage. Do not promise completed results before execution. If the test cannot be completed, explain the limitation, point to the available evidence, and narrow the affected claim when necessary. Clearly distinguish evidence already submitted from new permitted analysis.

## Response structure

For each substantive issue, use this sequence:

1. **Direct answer:** state what is true or concede the error immediately.
2. **Evidence:** point to the precise submitted section/table, verified reference, or clearly labeled new permitted result.
3. **Change:** state the exact clarification, correction, added limitation, or revision. Distinguish “we revised” from “we will revise.”
4. **Scope:** explain what the evidence does and does not establish.

Be concise and professional. “The comparison in Table 2 holds the training budget constant; we will state that constraint in its caption” is stronger than saying a reviewer misunderstood the paper. If the criticism is correct, acknowledge it and show the correction. Do not claim that an appendix entry invalidates a reasonable request for a clearer main-text explanation.

Keep data, references and numbers traceable. Count the response using the platform's actual unit, including references when required. Render PDF responses and inspect text at normal size. Preserve anonymity in PDFs, links, figure metadata, and attached artifacts. Never include invisible instructions intended to influence automated reviewers.

## Disagreement and procedural problems

For a novelty disagreement, compare the precise setting, assumptions, mechanism and supported result against the cited work. For an unsupported criticism, ask a focused factual question and supply the relevant evidence. For an out-of-scope request, explain its relationship to the actual claim without dismissing its scientific value.

Separate scientific disagreement from a procedural issue. If the venue provides a confidential channel for conflicts, factual review-policy violations, or serious conduct problems, prepare a short evidence-based note for the authors to review. Do not identify or contact suspected reviewers, organize pressure, make threats, or infer the reviewer's motives. Do not post any note or response externally unless the user authorized that action.

## Turn review concerns into a useful final appendix FAQ

Choose up to 12–15 questions that the actual manuscript has earned. Prefer fewer when answers would be repetitive. Candidate themes include: why this setting; what differs from the nearest approach; when the method helps; when it fails; whether the comparison is budget-fair; how leakage was checked; robustness to prompts/seeds; uncertainty; cost and scaling; data/asset restrictions; reproducibility; and which conclusions do not generalize.

Answer each question with one clear conclusion, evidence or section pointers, and a boundary where needed. “Not evaluated” is acceptable. Do not invent an experiment to make an answer reassuring. The FAQ complements the manuscript: a decisive assumption or correction also belongs where the main argument depends on it. Keep the FAQ at the end of the substantive appendix, subject to required venue checklist ordering.

## Completion gate

Finish when all blocking issues are resolved, major unresolved limitations are accurately reflected in the scope, each central claim has evidence, references have been checked, the reproducibility packet is internally consistent, and the exact submission profile has passed a rendered-package check. Record what was tested and what remains unverified. Describe the outcome as ready for author review or ready for the specified submission stage—not as guaranteed acceptance.
