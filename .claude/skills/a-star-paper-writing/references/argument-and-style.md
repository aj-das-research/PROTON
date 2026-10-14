# Argument and scientific style

## Find the reader's question

Answer one consequential research question. Test the story in three sentences: What can an expert not yet do/explain? What precise idea changes that? What observation/proof would make a skeptic believe it? If the third answer is weak, stronger adjectives will not repair the paper.

Separate motivating application from evaluated setting. A medical motivation does not establish clinical benefit; a coding benchmark does not establish production reliability. Connect the application honestly and identify remaining gaps.

Use established capability → bottleneck → insight → implementable consequence → discriminating evidence → scope. Start with the task or finding rather than generic claims about AI transforming the world. Explain how a design decision follows from the bottleneck; do not list modules and retrofit motivations.

For full-paper framing or reorganization, use [story-and-reader.md](story-and-reader.md). For dense method or mathematical prose, use [method-exposition.md](method-exposition.md). These develop the explanation; they do not add mandatory planning outputs.

## Title and abstract

Prefer a compact searchable title describing the object and main idea, with a task/domain qualifier where needed. When the framing is unsettled, compare a concrete mechanism title with a supported finding title and choose the one that best represents the paper. Do not make the author choose among a long list of slogans. Check acronym overlap and avoid a title broader than the measured capability.

Follow the official abstract limit. A provisional 150–250 words is a drafting convenience only. Write a self-contained paragraph with these moves, combining them naturally:

1. Concrete problem and its importance.
2. Specific limitation of the strongest relevant approach or current evidence.
3. Insight and proposal, including the distinguishing mechanism.
4. Evaluation setting or proof scope.
5. Most informative supported result, fair comparison, and meaning.

An abstract is not a table of contents. “We conduct extensive experiments” supplies no evidence. Prefer tested scope and one or two central quantitative findings when verified. If results are absent, label the abstract provisional without inventing measurements. Theory and benchmark abstracts need their own evidential center.

Reverse-audit every assertion against the main paper. Reconcile result units and baseline names. Check if a reader would infer a broader setting than evaluated. Remove unnecessary abbreviations. Follow actual rules for abstract citations rather than assuming a universal prohibition.

## Introduction

Give paragraphs purposes, not fixed sentence counts:

- **Problem/stakes:** define the task and demonstrate importance with evidence, a real concise example, or a concrete consequence.
- **Capability/limitation:** credit current approaches, then identify the unresolved setting. Introduce closest work early enough to assess novelty.
- **Challenge:** explain why the obvious solution is inadequate using technical constraints, conflicting objectives, missing information, or failed assumptions.
- **Insight/mechanism:** explain the conceptual change and essential design. Intuition motivates a mechanism; it does not prove it.
- **Evidence/boundary:** summarize evaluation questions and verified findings with material qualifications.
- **Contributions:** normally 3–4 parallel bullets when that many distinct contributions exist.

Merge/split for density and convention. Benchmark papers may present an evaluation contract before baselines; theory papers may center a theorem and assumptions.

Contribution bullets should be falsifiable deliverables: a defined resource with validated properties, a specified mechanism, theorem, or demonstrated finding. “We review related work,” “extensive experiments,” and “novel framework” are activities/adjectives. Do not count a method and its renamed modules as separate contributions. Map each bullet to a section and evidence item.

## Paragraphs and technical prose

Lead with a claim/question, develop it through explanation and evidence, and connect it to the next decision. Topic sentences should form a coherent reverse outline. Combine repeated points; split unrelated claims.

Keep names and notation consistent across text, equations, algorithms, figures, and code descriptions. Define symbols at first substantive use. Distinguish training/inference, observed/latent quantities, predictions/ground truth, component losses/total objective, and frozen/trainable parameters.

Use concrete verbs: retrieves, reweights, measures, conditions, bounds. Replace promotional adjectives with measured properties. “Efficient” needs a resource; “robust” a perturbation; “scalable” a scaling axis; “interpretable” a reader/task or criterion. Hedge to reflect uncertainty, not hide missing evidence.

Avoid unnecessary history, ornamental analogies, stacked acronyms, and long parenthetical qualifications. Preserve needed nuance. Active voice helps identify operations/actors; passive voice is useful when the procedure/object is the focus. Do not enforce arbitrary bans on common scientific words.

For a passage that reads awkwardly, trace the information rather than replace words mechanically. Does its opening connect to something already established? Is the subject separated from its verb by several qualifications? Does “this” name an identifiable operation or claim? Split a sentence when it contains distinct conclusions, and put the defining condition close to the claim it qualifies. Keep the same technical name for the same object; synonym variety can imply a distinction that does not exist.

If the author provides approved passages, use them to calibrate density, terminology, and voice while preserving scientific precision. Do not imitate another paper's distinctive phrasing or force a uniform sentence rhythm. Read the revision aloud or as a fresh reader: remove generic transitions when the causal, comparative, or evidential relation can be stated directly.

## Results and real examples

For each question, give the answer, table/figure, effect and uncertainty, interpretation, and boundary. Do not narrate every cell. Highlight surprising failures/costs that change the conclusion. Separate association from causal explanation.

Distinguish three moves: what was measured; which explanation the evidence supports; and what decision or understanding follows. A design motivation is not automatically the observed cause. If an ablation changes several factors, do not attribute its effect to one without a discriminating check. Refer to the particular comparison, curve region, or case that warrants the interpretation. When the claim concerns a quality–resource tradeoff, present the important baseline comparison as a quality–resource pair. A shared configured budget does not guarantee equal realized latency, calls, or throughput; keep a consequential difference beside the gain it qualifies. When available, explain the observed regime where a gain grows or disappears; label untested explanations as hypotheses.

Write confidently at the demonstrated scope. A useful tradeoff deserves a clear statement even when there is no universal winner. Keep qualifications that change the reader's interpretation beside the claim; put secondary procedural detail in its appropriate section. Do not end every paragraph with a list of untested possibilities, and do not remove a material exception merely to sound positive. See the [worked example](worked-writing-example.md) for a complete composition path.

For examples connect input, reference/target, method output, baseline output, and criterion. Explain the concrete difference. Label success-selected examples and provide meaningful failures elsewhere. Synthetic illustrations must be labeled and cannot substitute for evaluation evidence.

## Discussion and conclusion

Aim for one discussion paragraph interpreting implications, cost, limitations, and a next question; one conclusion paragraph restating the problem, insight, strongest finding, and boundary. Combine if appropriate. Do not introduce new results or repeat the abstract verbatim. Keep separately required limitations, impact, ethics, or checklist sections.

## Three revision passes

1. Read title, abstract, headings, topic sentences, contribution bullets, figures, and conclusion. Check a coherent thesis, significance, novelty, evidence, and scope.
2. Trace assumptions, notation, equations, algorithms, numbers, and citations; reconcile repeated results and caveats.
3. Remove redundant reasoning, replace vague claims, shorten overloaded sentences, then inspect the rendered page. Preserve concise restatements needed by independent reading of abstract, captions, and conclusion.

Preserve author voice and evidence-appropriate structure rather than making every paper sound identical.

When reducing length, remove a redundant argument before abbreviating every sentence. Merge duplicated protocol descriptions using a precise pointer; move optional derivations or sweeps with their labels intact. Preserve assumptions, comparison conditions, uncertainty meaning, numerical denominators, and the logical bridge from evidence to claim. Re-read the shortened passage by itself: a grammatically complete paragraph can still have lost its explanation. Compile after changes that move floats or alter page boundaries.

## Edit an existing passage

For a local edit, identify the passage's function and the concrete obstacle: unclear claim, missing logical link, ambiguous referent, poor ordering, or repetition. Edit the existing LaTeX directly when that is the project format. Preserve scientific facts, claim scope, terminology, notation, commands/macros, labels, citation keys, and cross-references; change their structure only when needed by the requested revision. Inspect surrounding definitions or supporting artifacts where the edit could change meaning.

Return the requested text or source patch, with consequential scientific questions in a separate editorial note. Use the distinction in [evidence-and-claims.md](evidence-and-claims.md#manuscript-voice-and-editorial-notes): assistant access gaps are not automatically study limitations. Check that the revision has not strengthened a claim, changed a number, or altered a mathematical dependency. Use the established build and inspect affected output when available.

Reuse the still-applicable project and venue profile; resolve assistance restrictions relevant to the requested work. A wording edit does not require a new project, complete ledgers, a fresh literature survey, or a whole-paper readiness audit. Broaden the check only to resolve a specific scientific ambiguity or changed claim.

## Compact revision examples

These examples use **synthetic teaching facts**, not research evidence. Methods A and B are invented stand-ins. Never transfer their facts or numbers into a real manuscript; apply the editing move to the author's actual evidence and preserve its citations.

**Connect a design to its purpose.** Facts: a fixed-budget baseline reviews every item; the proposed gate requests review only when two candidate answers disagree and otherwise keeps the initial answer; no benefit has been measured.

- Before: “Our powerful framework comprises candidate generation, a gate, and a reviewer.”
- After: “To concentrate review on candidate disagreement, the gate requests a reviewer only when the two answers differ. Other items retain the initial answer.”
- Why: the revision explains the decision and information flow without claiming that selective review improves quality or cost.

**Separate the result from the editor's access status.** Facts: on the same 100 test items with the same base model, both systems score 70%; mean calls per item are 3.0 for the baseline and 2.0 for the proposed method. The study did not measure runtime. The assistant has the summary but has not inspected raw logs.

- Before: “Author-reported results show that our system is much more efficient, although raw logs were not supplied.”
- After: “On the matched 100-item test, both systems achieved 70% accuracy, while our method used 2.0 model calls per item on average compared with the baseline's 3.0. Runtime was not measured.”
- Why: the revision names the measured resource and study boundary without asserting statistical equivalence or runtime savings. Keep “summary supplied; raw logs not inspected” in the editorial note and retain provisional status until verification.

**Make closest work comparative.** Facts: Method A retrieves before generation; Method B also retrieves after every draft; the proposed variant triggers that later retrieval only after a failed validation check. No performance comparison is available.

- Before: “Unlike all prior work, our novel adaptive retrieval framework solves unreliable generation.”
- After: “Method A retrieves before generation, whereas Method B also retrieves after every draft. Our variant conditions that later retrieval on a failed validation check.”
- Why: a concrete operational distinction replaces unsupported priority and reliability claims. Its usefulness still needs evidence.
