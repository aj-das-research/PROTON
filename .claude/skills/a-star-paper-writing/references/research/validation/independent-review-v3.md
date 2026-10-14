# Independent review of v3 writing changes

Reviewed 2026-09-19 against `research-v3/baseline/skills/a-star-paper-writing`. Read-only review of the actual differences in `SKILL.md` and ten changed/new top-level writing references, plus the new research summary for provenance. Did not inspect `research-v3/evaluation`, change the skill, execute its tests, or push anything.

## Overall assessment

No blocking scientific or numerical defect was found in this review. The update materially improves composition, not merely compliance: it explains how to select a supported argument, supply reader prerequisites, teach a mechanism, interpret findings, and produce replacement prose after review. The additions preserve the author's Overleaf workflow and figure-skill dependency. They do not promise acceptance, manufacture experiments, impose a universal paper structure, or confuse an agent's missing access with a study limitation.

The three new references are proportionate and routed by task. `SKILL.md` remains about 1,923 whitespace-delimited words in the reviewed snapshot. It explicitly exempts narrow edits from whole-paper planning, and the new references avoid additional mandatory ledgers. I did not find a consequential bloat or rigidity issue that warrants removing an entire section.

## Findings and verified resolutions

### 1. Make the requirement-enumeration actor explicit in the worked example

**Priority: medium; semantic clarification in teaching material. Resolved and read back.**

Location: `references/worked-writing-example.md`, lines 8, 28, 34, and 42 in the reviewed snapshot.

The fixed facts say that **authors** enumerate requirements before reading responses. The abstract and introduction instead say that a protocol enumerates and judges them. Combined with the one-call claim, this can be read as the judge automatically performing both operations. Those are different methods and costs. A composition example should preserve this distinguishing fact as carefully as it preserves its numbers.

Concrete fix: write an explicit actor in the abstract/introduction, for example, “Authors enumerate the requirements before viewing responses; the fixed judge then labels each supplied requirement and accepts the response only when all labels pass.” In the cost discussion, clarify that reported output tokens describe judge generation, not the human effort to enumerate requirements. Do not invent a labor estimate or claim an end-to-end efficiency gain. If the intended synthetic protocol was automatic enumeration, change the fixed fact packet explicitly rather than silently changing it in the prose.

This was an ambiguity rather than a confirmed false numerical claim. All arithmetic remains correct.

**Resolution verified:** the revised abstract assigns enumeration to authors; the introduction says the judge receives the author-created list; the results explicitly exclude enumeration labor from output-token accounting. No unsupported labor estimate was added.

### 2. Add an explicit outcome for accessible evidence that gives no support

**Priority: low; classification completeness with a concrete downstream effect. Resolved and read back.**

Location: `references/literature-and-citations.md`, line 35 in the reviewed snapshot.

The new instruction asks the agent to record one of four citation outcomes: supports, partial, contradicts, or unavailable. The next sentence correctly says that an accessible source that does not address the assertion supplies no support and is not contradictory. None of the four named outcomes describes that case. This leaves a common irrelevant-citation case liable to be classified as unavailable or contradictory.

Concrete fix: add **no support** (or **irrelevant to this assertion**) as a fifth outcome, distinct from contradiction and inaccessible evidence. A sentence can then be narrowed, supported by another source, or have the irrelevant citation removed. No tool/schema change is implied unless those labels are actually enforced elsewhere.

**Resolution verified:** line 35 now includes **no support** for an accessible source that does not address the assertion, separately from contradiction and unavailable evidence.

## Numerical and semantic checks of the examples

| Item | Result |
|---|---|
| Evaluation responses | 80 prompts × 3 response models = 240 responses; consistent. |
| Holistic agreement | 188 / 240 = 78.333…%; displayed 78.3% is correct. |
| Requirement-level agreement | 204 / 240 = 85.0%; correct. |
| Absolute difference | 16 / 240 × 100 = 6.666… percentage points; displayed 6.7 is correct. |
| Error difference | 52 holistic errors versus 36 structured errors = 16 fewer; correct. |
| Error coding totals | 22 + 14 = 36; post-hoc status is retained in the results. |
| Cost | 64 and 118 are output-token means; text correctly avoids an unsupported runtime or dollar ratio. Actor/labor clarification was verified after finding 1. |
| Uncertainty | No confidence interval, significance test, ranking claim, or independence assumption is manufactured. The final teaching note recognizes shared prompts. |
| Model quality | The example explicitly distinguishes judge agreement from improved instruction-following by the evaluated response models. |
| Synthetic status | Clear at document entry, with no claim that experiments were performed. |
| Tile selection example | Scores A=0.7, B=0.2, C=0.6 under a two-tile budget select A and C as stated. |
| Tile aggregation | The softmax normalizes over the selected set, requires positive temperature, and returns a vector in the stated feature space. Empty-set behavior and scoring cost remain explicitly unspecified rather than invented. |

The worked example is a useful connected demonstration; it should stay compact. Expanding it into a fabricated full paper, inventing uncertainty estimates, or adding decorative citations would weaken it.

## Source and scope spot checks

The added sources are presented as motivation for original guidance, not as causal evidence of acceptance. I checked the following primary sources directly:

- [ALCE Section 3.3](https://aclanthology.org/2023.emnlp-main.398.pdf) separates completeness of citation support from irrelevant citations. The package correctly uses this distinction and explicitly declines to treat automated entailment as a truth certificate.
- [NeurIPS 2026 reviewer guidance](https://neurips.cc/Conferences/2026/ReviewerGuidelines) contains use-inspired, concept/feasibility, and negative-result guidance. The new architecture branch explicitly labels these as edition-specific inspiration, not universal submission categories.
- [PaperBench Sections 2.2–2.4](https://arxiv.org/html/2504.01848v2) distinguishes reproduction execution and result matching. The package applies this cautiously to bounded result regeneration, with actual authorization and scope limits.
- [CORE-Bench Section 2.1](https://arxiv.org/html/2409.11363v2) describes benchmark construction for computational reproducibility. Its use as motivation for separating successful execution from recovering the correct result is reasonable.

The method and story additions also agree with the nine bounded exemplar notes from the separately completed research task: worked examples, exact-to-implemented distinctions, diagnostic alternatives, and operating regimes are optional explanatory moves. They do not become experiment quotas. This review is not a full verification of every source in the package or every scientific recommendation.

## Recommendation

Both localized findings are resolved, and no blocking issue remains from this review. Retain the overall design. Further meaningful improvement should be driven by observed manuscript failures and author feedback, rather than adding more generic checklists or promising that source breadth ensures excellent writing.
