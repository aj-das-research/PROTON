# Explain the method so a reader can reconstruct it

Use this reference when a method, algorithm, mathematical argument, or measurement procedure is difficult to understand. Work from the actual implementation, specification, proof, and author notes. Preserve established notation and LaTeX commands. Improving exposition does not authorize inventing a cleaner algorithm or a rationale the study never tested.

## Start with the decision and constraint

Before naming modules, say what the system must decide, what information it has, and what constraint makes that decision difficult. Explain the desired output before describing intermediate machinery. An adjacent ML researcher may know standard losses but not the application's data semantics; introduce the missing background where it becomes necessary.

Connect each important design choice to its purpose: what does this operation make possible, and what alternative does it replace? Separate a design motivation from an established explanation of effectiveness. “We select tiles to limit the encoder budget” describes an operation's purpose. “Selection removes irrelevant information” requires evidence about relevance. When the rationale is unavailable, describe the operation accurately and leave a focused editorial question.

Present the simplest faithful overview first, then refine it. If a simpler variant is intentionally incomplete, say so before teaching it. Do not lead readers through discarded designs as though they were the proposed method. Mark inherited components and the actual modification; a renamed standard loss is not a contribution.

## Carry one example through the difficult step

Use a small example when it reveals information flow, an unusual constraint, or a consequential branch. Omit it when it merely restates an obvious formula. Keep the same objects and names through the explanation, diagram, and algorithm. Distinguish an illustrative construction from an actual evaluated example; neither establishes prevalence by itself.

**Synthetic teaching example; no experimental findings.** An image has three tiles, A, B, and C, with supplied scores 0.7, 0.2, and 0.6. A two-tile budget selects A and C before encoding. Explaining that selection first makes the reader ready to ask how scores are obtained, whether scoring itself is expensive, and what happens to omitted tiles. Answer those questions from the real design rather than letting “adaptive selection” stand in for them.

If the example includes a tie, an empty set, or a stopping condition, follow the implementation's actual behavior. Do not quietly choose a convenient outcome. A running example is useful only if its trace agrees with the general rule.

## Make equations executable in the reader's mind

Introduce a formula's purpose in ordinary language. Then give the expression, define its symbols, and explain its operational consequence. State domains or tensor shapes where they disambiguate an operation; a notation table does not replace local explanation. Identify the axes of reductions, normalization, masking, and aggregation. Distinguish an index set from its values and a distribution from one sampled outcome.

Continuing the **synthetic** tile example, let selected features be \(h_i\in\mathbb R^d\), supplied scores be \(s_i\in\mathbb R\), selected indices be \(S\), and temperature be \(\tau>0\). An illustrative aggregate is

\[
z=\sum_{i\in S}w_i h_i,
\qquad
w_i=\frac{\exp(s_i/\tau)}{\sum_{j\in S}\exp(s_j/\tau)}.
\]

The output \(z\in\mathbb R^d\) averages selected features, with weights normalized over selected tiles. This expression alone specifies neither the scoring procedure nor how an empty selection is handled. It also does not establish that weighting improves representations. Transfer the explanatory pattern, never this invented formula, into a real paper.

For an actual objective, state what parameters are optimized, which quantities are fixed or detached, the training distribution or finite sample average, loss terms, coefficients, and constraints. Explain whether coefficients are chosen, learned, or scheduled. For probabilities, specify conditioning information and the source of randomness. For expectations, identify the distribution; for an approximation, identify what is approximated and what implementation replaces it. Do not let one symbol alternate between a ground-truth label and a prediction.

## Separate learning from execution

Describe what happens during training and what happens when the deployed system receives a new input. State which information is available at each stage. A training label, future observation, privileged teacher, or ground-truth environment state must not appear silently in an inference procedure.

Trace parameter ownership and data flow: what is learned, frozen, cached, recomputed, retrieved, or externally provided? For staged optimization, identify the order and which outputs become another stage's inputs. If a discrete selection is trained through a surrogate, a relaxation, or no gradient, explain that distinction. Do not imply that a differentiable aggregation makes the entire pipeline differentiable.

Attach costs to the operations that incur them. In the tile illustration, fewer encoded tiles alone does not establish end-to-end speedup: scoring and selection also have costs. Keep measured resource claims and theoretical operation counts distinct.

## Check a complete execution trace

Use pseudocode when order, mutable state, sampling, branching, or stopping is otherwise ambiguous. Name inputs, returned outputs, initialization, updates, and termination using the same notation as the text. Include branches that define the method; move routine library plumbing to the appendix or implementation.

Walk one admissible input through the described procedure. Can every consumed quantity be located, every update ordered, and every returned value identified? Check applicable boundary cases such as empty candidates, exhausted budget, ties, invalid tool output, or nonconvergence. State documented fallbacks; if behavior is unspecified, flag the missing definition rather than inventing one. Repeat this reasoning for any figure arrows that appear to bypass an operation.

## Connect formal results to the implemented system

Keep the exact guarantee next to its assumptions and explain the new proof idea. Map each relevant ideal object to the numerical or estimated object actually used: for example, an exact null space versus one chosen by a singular-value threshold. Identify the approximation, which guarantee survives it, and what remains to be established. Which sentence becomes false if the implemented approximation is substituted into the formula? Revise that sentence or supply the missing argument.

An idealized guarantee can be informative without proving that the deployed system inherits it. Conversely, numerical agreement with a predicted trend does not prove the theorem. Use the fuller [theory guidance](paper-architecture.md#theory-branch) when the proof is the contribution.

## When the contribution is a measurement procedure

For a benchmark, explain how the intended capability becomes an observable task: source instance, transformation or annotation, permitted system information, system response, scoring, and aggregation. Walk one instance through this chain. Identify where an error in construction or scoring could change the measured conclusion, and describe the validation actually performed. Separate the construct from its operational proxy. A benchmark measuring answer correctness does not automatically measure the reasoning process that produced the answer. Link to [evaluation guidance](experiments-and-analysis.md) for appropriate checks and uncertainty.

## Source influence

This is original operational guidance informed by the example-first exposition in [Peyton Jones](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/07/How-to-write-a-great-research-paper.pdf), reader-oriented method explanation in [Ernst](https://homes.cs.washington.edu/~mernst/advice/write-technical-paper.html), and distinctions between intuition, formal claims, and empirical evidence in [Lipton and Steinhardt](https://arxiv.org/html/1807.03341v2). Sources inspected 2026-09-19; their stylistic preferences are not venue requirements.
