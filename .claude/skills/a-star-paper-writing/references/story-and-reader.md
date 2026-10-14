# Choose the argument and guide the reader

Use this for a full draft, a major reorganization, or research materials that admit
several plausible paper identities. A local wording edit normally needs only
[argument-and-style.md](argument-and-style.md). Keep these decisions in the
existing project brief; do not create another mandatory set of planning files.

## Find the contribution the evidence can carry

Start with what the work changes for a reader: an explanation, a measurable
capability, a useful resource, a simpler procedure, a practical tradeoff, or a
formal result under specified conditions. Distinguish that change from the
application's general importance and from the fact that a component is new.

When the framing is genuinely ambiguous, compare the few plausible central
questions using the same research inventory. For each, identify the closest
alternative, decisive supporting result, strongest contrary result, and missing
assumption or comparison. Prefer the most consequential question that the work
actually answers. Do not score stories by predicted acceptance or keep generating
alternatives after the evidence makes the choice clear.

A method that does not improve peak accuracy might provide a useful measured
quality–cost tradeoff; a failed proposed mechanism might yield an informative
diagnostic result. Such reframing must preserve original primary outcomes,
material contrary findings, and exploratory status. Choosing a favorable subset
or new metric after seeing results does not establish a pre-specified success.
A simple useful finding needs no invented pipeline or dramatic novelty claim.

Write a short working account: what the reader currently cannot infer or do,
what this work adds, which evidence warrants the change, and where it stops.
Check whether every claimed contribution advances that account. Combine
contributions that merely name pieces of the same method; retain multiple
contributions when their connection is real. This is a test of coherence, not a
requirement that all research fit one sentence or one type of paper.

## Build the explanation around what the reader needs next

Identify the intended reader's likely prerequisites. An adjacent ML researcher
may know optimization but not this task's information constraints or this
benchmark's scoring semantics. Supply the missing context where it is needed;
do not replace it with a broad tutorial.

For each major passage, ask what the reader must understand before it and what
they should understand after it. A paragraph that introduces several unexplained
objects creates work for later paragraphs; resolve the earliest consequential
gap. Preview the idea before asking the reader to retain its implementation
labels. Use one small running example across connected steps when it genuinely
reduces abstraction, clearly identifying a constructed example as illustration.
See [method-exposition.md](method-exposition.md).

Choose the order by the argument's dependencies. A benchmark may need its
measurement validity established before a ranking is meaningful. A systems
paper may need its workload and bottleneck before the design makes sense. A
diagnostic paper can introduce competing explanations and then show which
intervention distinguishes them. A theorem needs its setting and assumptions
before a rate comparison. Use the author's preferred sections, adapting their
contents and order to this dependency; do not force every paper into a
method-first story.

## Choose the representation that answers the question

| Reader needs to… | Useful representation | Check before using it |
|---|---|---|
| Recover exact values or compare configurations | Table with comparable groups | Units, aggregation, uncertainty, and missing/incompatible entries are explicit. |
| Understand a relationship, trend, or tradeoff | Plot | Axes and sampling support the inferred relationship; the visual does not imply unmeasured operating points. |
| Follow state, branching, or an update sequence | Algorithm or operational trace | Inputs, available information, stopping, and edge behavior match the implementation. |
| Understand an objective, invariant, or guarantee | Equation or formal statement with interpretation | Definitions, assumptions, quantifiers, and implemented approximations are clear. |
| Understand information flow or architecture | Diagram | Arrows have a defined meaning, and inherited versus new elements are distinguishable. |
| See what a failure or improvement means concretely | Real case or labeled constructed example | Selection and provenance are explicit; the example is not used to infer prevalence. |

A figure, theorem, or table earns space by resolving a reader's question. Do not
add a representation merely because a template has a slot. Conversely, do not
compress an inherently operational method into opaque prose to avoid an
algorithm. Follow [figure-integration.md](figure-integration.md) for the author's
external figure skill; this reference selects explanatory roles, not a competing
figure-generation system.

## Support several ways of reading the same paper

Readers may inspect the title and abstract, then figures and captions, then
selected sections. Keep the central finding and its scope consistent across
these routes. Purposeful brief restatement is useful: a caption can repeat a
setting needed to interpret a plot without duplicating a results paragraph.
Each restatement should add the detail appropriate to its location.

Use informative headings where the venue allows them. A heading may name a
question or a supported finding; it should not promise causality or generality
that the evidence does not support. Captions identify what is displayed, how to
read it, and the conditions needed for a fair interpretation. The main text
explains why it matters and connects it to the next claim.

Before final prose polish, reconstruct the argument from the title, abstract,
headings, main figures/tables, and conclusion. Then read the main text without
the appendix. Move a definition, assumption, or decisive qualification forward
if either route would otherwise mislead. Preserve optional depth and complete
reproducibility in the appendix.

## Draft to learn, then revise to match the completed work

When research is unfinished and drafting is permitted, a provisional abstract,
method explanation, or empty table can expose a missing definition or comparison.
Leave unknown cells empty or explicitly unresolved; anticipated findings remain
separate from observed results. After evidence changes, revisit the framing and
all affected passages. An outline is a working hypothesis about the paper.

Deliver prose or the requested source edit, not an expanding collection of
planning tables. Show a framing choice only when it materially helps the author
decide. Stop restructuring when a reader can recover the contribution, follow
the explanation, and locate its support; address the remaining concrete defect
rather than repeating the entire process.

## Basis and limits

This is an original editorial synthesis informed by the primary writing guides,
public skill comparisons, and bounded exemplar readings in the
[2026-09-19 research review](research/deep-review-2026-09-19.md). In particular,
[Mensh and Kording](https://doi.org/10.1371/journal.pcbi.1005619) discuss reader
orientation at several scales, while [Olah and Carter](https://distill.pub/2017/research-debt/)
treat explanatory design as substantive intellectual work. These sources do not
establish a universal section order or an acceptance effect.
