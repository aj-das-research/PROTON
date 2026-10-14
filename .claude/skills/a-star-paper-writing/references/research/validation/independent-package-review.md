# Independent package review

Scope: `/root/.codex/skills/remote-skills/a-star-paper-writing`. Read-only review of entrypoint, references, scripts, examples, and LaTeX fragments. `research-basis.md` was excluded as requested. No skill files or remotes were changed.

No release-blocking defect was demonstrated. The following are concrete nonblocking defects or advertised-capability gaps, not editorial preferences.

## P2 — Static benchmarks are incorrectly required to have interactive environments

**Location:** `references/experiments-and-analysis.md:30`.

“A new benchmark needs an environment contract” then universally requires observation/action spaces, transitions, episode limits, resets, and tools. These do not apply to static classification, retrieval, or question-answering datasets. This contradicts `references/paper-architecture.md:40`, which conditions such requirements on dynamic environments, and the explicit static-benchmark exception in `references/figure-integration.md`.

**Impact:** A writer following the empirical reference can invent irrelevant interaction semantics or incorrectly flag a complete static benchmark as missing essential specifications.

**Fix:** Start with a general benchmark contract (construct, population/task, inputs/outputs, instance construction, splits, scoring, validation); add observation/action/transition/reset/termination requirements only for interactive environments. Preserve the evaluator testing requirement for both.

## P2 — The advertised theory branch has no actionable main-paper architecture

**Locations:** `SKILL.md:12`; `references/paper-architecture.md:12` and `:28`.

The entrypoint directs a theory-paper request to “select its branch” in the architecture reference. That reference contains only a one-row description of theory; its actual section sequence, method guidance, result questions, and page heuristics remain empirical. The useful proof paragraph in `references/appendix-and-prompts.md:43` does not provide the promised main-paper branch or a theory-specific review process.

**Impact:** Pure-theory requests lack guidance for arranging preliminaries, theorem statements, assumption comparisons, proof ideas, and consequences. The provided structure can overemphasize experiments while leaving the central proof argument in the appendix.

**Fix:** Add a compact theory branch: problem/preliminaries → precisely quantified main results → comparison to prior bounds under matched assumptions → central proof idea and indispensable lemmas → implications/tightness/limitations. Add a proof review checklist covering quantifiers and parameter ranges, theorem–lemma dependency consistency, use of assumptions, boundary/counterexample checks, and whether each claimed corollary follows. State that numerical examples are optional and cannot validate a proof. Alternatively narrow the advertised support rather than claim this branch exists.

## P2 — Human-study reporting omits the records needed to substantiate ethics statements

**Locations:** `references/experiments-and-analysis.md:54`–`:62`; `references/appendix-and-prompts.md:79`; `assets/project-brief.md:35`.

Human evaluation and dataset annotation are covered in detail, but the package has no instructions to record consent, applicable ethics approval/exemption, participant recruitment, compensation, or exposure to sensitive/harmful material. The brief asks generically for venue ethics rules, which does not establish what actually happened in a study.

**Impact:** A manuscript can satisfy the package's evaluation/reproduction prompts while still lacking the factual basis for a required human-subjects or crowdsourcing statement. This is a reporting capability gap, not a reason to demand blanket approval for ordinary writing work.

**Fix:** Add an applicability-conditioned human-study record: recruitment and population, instructions/task burden, actual consent process, approval/exemption status and source where applicable, compensation, relevant risks/privacy handling, and declared access restrictions. Recover these from author artifacts; never invent approval or imply retroactive approval. Keep absent records unresolved and reflect material limitations in the paper.

## P3 — Unsafe project-root resolution bypasses the audit's documented JSON/error contract

**Location:** `scripts/paper_audit.py:351`.

The project directory is resolved before the guarded input handling. A symlink loop passed as `PROJECT_DIR` raises an uncaught `RuntimeError`, emits no JSON even with `--json`, and exits 1. The documented contract reserves exit 1 for unresolved checks and exit 2 for invalid input or unsafe paths.

**Reproduction:** In a temporary directory, create `loop -> loop`; run `python paper_audit.py /path/to/loop --json`. Observed exit 1, empty stdout, traceback ending in `RuntimeError: Symlink loop ...`.

**Fix:** Guard project-root expansion/resolution against `OSError`, `ValueError`, and `RuntimeError`, emit the same structured invalid-input report used for other unsafe paths, and return 2. A small regression check for this boundary is appropriate.

## Verification performed

Exercised 648 malformed-container/field substitutions against the ledger and venue validators without modifying the package; none raised an unexpected exception. Separately reproduced the project-root symlink-loop defect above. No external policy facts were independently reverified in this package review, and no claim of compiled LaTeX validation is made.
