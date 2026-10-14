# Third review: deep research and manuscript composition

Date: **2026-09-19**. Previous published baseline:
`fa491fd8936c68cabfe1846de763b0e784c84433`.
The [research review](../deep-review-2026-09-19.md) records the source search,
inspection scopes, implementation choices, and research limits.

## Package checks

- **67 automated tests passed**, no skips, in 15.851 seconds using
  `python -m unittest discover -s skills/a-star-paper-writing/tests -v`.
- The skill-package validator passed; all 112 checked relative Markdown file
  links resolved, and all 14 JSON files parsed.
- The original corpus audit passed with no issues: 622 unique papers, 622
  abstract inspections, 20 targeted narrative reviews, and unchanged historical
  source/reading records. The nine new exemplar readings remain separate.
- No runtime script, external dependency, JSON audit schema, or Overleaf
  synchronization implementation was added. The update changes writing guidance,
  the project brief, examples, and research/evaluation records.

These checks establish mechanical consistency. They do not grade prose or prove
scientific soundness, source authenticity, submission readiness, or acceptance.

## Independent package review

The [independent review](independent-review-v3.md) inspected the changed writing
instructions and examples without seeing evaluation artifacts. It found two
specific issues, both corrected and read back:

1. The synthetic measurement example needed to state that authors prepare the
   requirement list and the judge labels it. Its output-token comparison now
   explicitly excludes that author preparation labor.
2. Citation assessment needed a **no support** outcome for an accessible but
   irrelevant source, distinct from contradiction and unavailable evidence.

The reviewer reconciled all teaching-example counts and differences and checked
that claims concern judge agreement rather than better response-model behavior.
No blocking issue remained in that review. This was not an independent review
of every paper or all code in the source repositories.

## Matched writing tasks

Separate fresh agents used identical requests and raw synthetic artifacts, with
either the previous skill or the initial revised skill. They received no intended
answer, diagnosis, or other agent's output. Each produced actual LaTeX and
editorial notes. A separate reader received anonymous A/B passages and the raw
input packet, with labels counterbalanced across tasks; it did not receive the
skills, implementation discussion, or condition key.

| Task | Observed scientific fidelity and behavior | Blind assessment |
|---|---|---|
| [Selective reranking](../../../tests/scenarios/v3-method/input/request.md) | Both versions preserved the frozen-model routing mechanism, held-out threshold selection, numbers, mixed baseline comparison, and single-run scope. Both met the requested word limits and compiled. | Previous skill narrowly preferred for pairing random-baseline accuracy gains with the small measured latency difference. The initial revised text was accurate but less complete on this comparison. |
| [Exact versus thresholded linear update](../../../tests/scenarios/v3-theory/input/request.md) | Both preserved dimensions, zero-dimensional null space, exact-arithmetic assumptions, the thresholded bound, the numerical illustration, and the fixed-example scope. Both compiled. | Revised skill narrowly preferred for placing each statement, proof, and operational interpretation together, reducing backtracking. |

The [anonymous comparison](blind-writing-comparison-v3.md) preserves the actual
findings, including the preference for the earlier method draft. Mapping:
method A = initial revised, B = baseline; theory A = baseline, B = revised.
No material factual or mathematical defect was found in either pair.

The four initial manuscript builds succeeded locally with pdfLaTeX and had
clean final logs; their rendered pages were visually inspected by the producing
agents. This validates the supplied exercise sources, not any official venue
template or live Overleaf project. The theory passages were built in temporary
article wrappers, keeping the requested deliverables as fragments.

One sample per condition and one qualitative judge cannot establish a general
improvement rate or isolate instruction effects from sampling variation. These
are bounded diagnostic observations, not a writing leaderboard or acceptance
predictor. Baseline and revised outputs are retained alongside each task's raw
inputs so the comparison can be inspected.

## Feedback-driven refinement

The mixed comparison led to one narrow addition in
[argument-and-style.md](../../argument-and-style.md): when interpreting a
quality–resource tradeoff, present a consequential baseline comparison as a pair
of measured quality and resource use. Equal configured budgets do not guarantee
equal realized cost. The instruction applies to resource-sensitive claims; it
does not require narrating every table cell.

A fresh agent then completed the same raw method request using the final skill,
without seeing prior outputs or the comparison diagnosis. Its
[final method passage](../../../tests/scenarios/v3-method/final/manuscript.tex)
reports the random-baseline accuracy gain with equal or 1 ms higher latency,
and distinguishes the shared development target from realized test routing.
It retains the negative comparison on one dataset and invents no tie-breaking
rule. This resolves the specific omission in this execution; it does not establish
an overall preference over the earlier draft.

The follow-up met its 170/300/170 word limits (reported counts 147/226/160),
compiled twice locally, had no recognized final log issues, and its two pages
were visually inspected. This fifth manuscript build adds a targeted check,
not a replacement for the mixed initial comparison.

## Citation and reviewer-response task

A separate fresh agent used the revised skill to
[repair a supplied paragraph and prepare a response](../../../tests/scenarios/v3-citation-review/input/request.md).
It narrowed a cross-domain accuracy/runtime claim to the source's actual
in-domain result, corrected the assertion that a comparator cannot evaluate
shifted inputs, and removed an unsupported first-ever claim. It preserved the
usable citation keys and invented no bibliography.

It also checked the reviewer's missing-experiment allegation against the frozen
manuscript and found the existing appendix sweep. The 125-word response retained
its exploratory status and absent seed repetitions, pointed to its actual
location, and did not pretend a new experiment had been run. Compilation and
bibliography resolution remained unverified because the task supplied only a
fragment and synthetic source notes. This is the appropriate scope of that check.

## Records and remaining limits

Scenario directories store raw requests, supplied facts, and observed source or
response files. Editorial notes preserve the producing agents' actual checks;
any execution-workspace paths refer to temporary verification artifacts, not
additional files promised in this repository. Rendered PDFs and logs were
inspected during execution but are not bundled as publication artifacts.

The skill's research breadth and richer examples do not establish that every
future output will improve. A real manuscript still needs actual research,
source verification, scientific judgment, author feedback, its official template,
and observed compilation/synchronization state. No live Overleaf operation,
conference submission, costly training, or public release of research was tested
or performed here.
