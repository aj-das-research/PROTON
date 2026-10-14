# Section playbooks for ML venues (ICLR, NeurIPS, ICML, CVPR)

These are concrete orders of moves for each section. They combine the author's
skeleton (abstract and introduction as problem, motivation, challenge,
proposal, evaluation, then 3 to 4 contributions) with the lab's September 2026
refinements (Nils Lukas). Use them as defaults and adapt them to the paper
type ([paper-architecture.md](paper-architecture.md)). Apply the sentence rules
in [house-style.md](house-style.md) to every section.

## Contents

Title · Abstract · Introduction · Related work · Benchmark or environment ·
Method · Experiments · Discussion, limitations, conclusion · Appendix

## Title

- **Check every name the paper coins.** Search the method, benchmark and metric
  names. If published work already uses a name, tell the author and propose a
  rename before submission. Reviewers raise a collision at once.
- A short noun phrase: a coined name plus what it does, or a verb-led phrase.
  For example, "GROVE: Benchmarking and Training LLM Agents to Persuade".
- Sell the phenomenon, not a technical workflow. The title is no broader than
  the evidence, and it does not state the result.
- Offer two or three options in chat. The author chooses. Once they submit a
  title, it is canonical.

## Abstract

One paragraph of 150 to 220 words. Follow Michael Black's template, which is
the same as the author's arc:

1. **Topic and need.** What systems need, in one sentence. Sell the
   phenomenon.
2. **What prior work does.**
3. **Why it fails.** The specific gap, stated as a fact.
4. **Our idea.** The method or benchmark by name, and the core idea in one
   sentence.
5. **What we find.** The finding in words, then at most one or two numbers at
   the very end. Give each as a relative improvement over a named baseline on
   a named metric, with its direction clear.
6. Optionally, one closing line on what this enables. Never a caveat.

Avoid:

- digits before the method;
- more than one results sentence;
- "extensive experiments";
- citations, "pilot", "toy", "earlier study";
- ending on limitations.

An abstract the author wrote, or edited and submitted, is canonical. Polish
only what the author asks.

## Introduction

This is the ML-venue order the lab settled on in September 2026. It replaces
the security ordering when no adversary is at the centre.

1. **The need.**
   - The first sentence names the high-level problem as a need, with the
     canonical citation, and makes only that point.
   - Then one sentence each gives a concrete example of the problem, the use
     cases, and a definition of the central quantity, using the abstract's
     verb.
   - Make the need urgent with one credible, recent piece of evidence.
2. **Why it is hard, what exists, what is missing.**
   - Open with the one fact that makes the problem hard, in plain words, and
     give its consequence.
   - Name each family of approaches as a response to that fact, one sentence
     each, with its cost or failure.
   - **Position against the closest recent work by name.** Before writing
     this paragraph and the contributions, search for the closest 2025 to
     2026 papers with general topic queries, never pasted text, and verify
     each hit (title, authors, year, venue or arXiv id). Name the one to three
     closest papers, each with one clause on what it does and one on how our
     method differs.
     - A novelty claim positioned only against old or weak work is the first
       thing reviewers attack.
     - A "first" claim that recent work contradicts is fatal. Cut it, and
       state the delta instead.
     - Adding the verified entries to the `.bib` is part of the rewrite.
       Rewriting Related Work to match is a separate proposal.
   - Where the paper's own results show the problem, use them as the
     evidence. For example: "the prompted agent asks 0.4 questions per task,
     and the SFT agent asks 3.9 yet succeeds less often (Table 1)". This is
     stronger than a general statement.
   - End on the gap as an opportunity that leads into the idea.
3. **The insight, then the method.** Show the key observation through the
   Figure 1 example, citing Figure 1 inside that sentence, followed by the one
   number that shows it generalizes. The
   method (and the benchmark) follows as a consequence. Explain any meaningful
   word in the method's name. Answer the most likely objection in one clause
   where the claim is made, for example why a simpler fix (a per-question
   penalty, a larger model) does not suffice, when the paper has the evidence.
4. **Evidence.**
   - Open with one line on what is evaluated.
   - Lead with the comparison a reviewer asks for first, usually the strongest
     simple baseline. Give one finding per sentence, as trends, keeping raw
     numbers only where they carry the argument.
   - Close the loop to a use case named in paragraph 1.
   - Label results that come from a variant.
   - Preview only the limits a reviewer would otherwise call hidden.
5. **Contributions.**
   - Three or four numbered bullets (a subsection is fine where the co-authors
     prefer one), ordered method, key insight, benchmark or dataset.
   - Each bullet has a verb, the named artifact, and one fact or number that
     the paragraphs above did not state.
   - No activity bullets ("we conduct experiments").

Keep paragraphs to 6 or 7 lines, and put the teaser on page 1. The introduction
expands the abstract with the example and the evidence. It never reuses the
abstract's sentences.

## Related work (or Background and Related Work)

- Tell it as a timeline or taxonomy of the problem and the methods tried. Open
  each paragraph with the challenge its methods address, then place the named
  systems as answers.
- Describe what each important method does in one clause a newcomer
  understands.
- Include the closest and most recent work (2025 to 2026). The author treats
  narrow related work as a defect.
- Use at most one short sentence per paragraph on how our work differs, and
  only in the paragraph on the closest line of work. Refer to "our work", not
  to the method's acronym.
- Put the background the method needs (formulations and losses of GRPO, DPO or
  process rewards, with citations) before the method. When a venue expects
  it, use "Background and Related Work".

## Benchmark or environment section (when the setup is new)

- **No evaluation numbers or findings in this section.** The results belong in
  the experiments.
- **Opener, one point per sentence:**
  - what we design ("We design X, a benchmark that ...");
  - what existing benchmarks do instead, with recent citations;
  - why that falls short;
  - what it therefore comprises, as an (i) to (iv) list of tasks;
  - a one-sentence map of the subsections.
- **Labels.** Give the setup and the one core equation, justify the target by
  the use case, and cover the design choices a reviewer would question.
- **Tasks or tiers.** Say why there are exactly this many. Give one run-in
  paragraph per task on how it is built, and put construction details and
  sizes in the appendix.
- **Metrics.**
  - Motivate each metric by the use it serves.
  - Make the primary metric one direct measure of the target, which the ideal
    method (oracle, exact computation) maxes out.
  - Do not use weighted composites. Every constant needs a reason or a
    sensitivity check.
  - Give acronyms with their formulas.

## Method (or Methods, when two or more are proposed)

- **Opener.** State the idea in one plain sentence, then one sentence per step
  with its subsection. There is no slogan sentence and no recap.
- **Each subsection:**
  - Open with the problem it solves, in one sentence, then name the mechanism.
  - After a display equation, explain each term in plain words, one sentence
    per term.
  - Give numbered steps (i), (ii), (iii) that match the numbered markers in the
    method figure, using the figure's exact words.
- **Keep numbers and details in their place:**
  - Constants and hyperparameters go in the experiments or the appendix. The
    text names the symbols and says where the values are.
  - Reward names stay distinct from the evaluation metric names.
  - A heuristic's limitations go to the limitations section.
- **Keep the method honest:**
  - The method as written is the method that was run.
  - Unimplemented components do not appear.
  - The method figure must be faithful: initialization, what is frozen and what
    is trained, and the data flow.

## Experiments (one section)

- **Setup** opens the section as run-in paragraphs (Models, Training,
  Baselines, Evaluation), with no "Setup" subsection heading. It covers:
  - data statistics and splits, stated explicitly;
  - how checkpoints and hyperparameters were selected (on validation, never
    test);
  - what the ± is over;
  - the compute.
- Open with one sentence that maps each subsection to the question it answers.
- **Each results subsection:**
  1. the question, in one sentence;
  2. what the figure or table plots (rows or curves, and both axes);
  3. how to read it ("a curve above the dashed line beats ContextCite");
  4. one or two bold takeaways, giving only the numbers the reader cannot see.

  Do not restate values the figure shows.
- **Content that belongs:**
  - the closest baselines in the main table;
  - a frozen or base reference row;
  - error analysis and qualitative analysis on real examples;
  - scaling studies (model size, family, context length) where the claim
    needs them.
- There are no valuing adjectives, and no run names, file paths or experiment
  numbers.

## Discussion, limitations, conclusion

- At page-limited venues, merge them into "Discussion and Conclusion" (about
  one paragraph each). The last run-in paragraph is **Conclusion.**, in the
  present tense ("We introduce ..."), restating the contribution and the
  strongest result. It ends on the prescription or the release.
- **Limitations** are written as future work (see
  [house-style.md](house-style.md) section 8). They can move to the appendix
  when the venue allows, and they never read as a confession.
- **Required statements.** Add the venue's statements after the conclusion:
  - the ICLR 2027 AI-use statement, which is mandatory;
  - the ethics and reproducibility statements;
  - the ICML impact statement.

  Write "AI use" from the actual activity log, for example "we used AI
  assistants for grammar checks and to improve the coherence of text the
  authors wrote".

## Appendix

Follow the lean-appendix contract in
[appendix-and-prompts.md](appendix-and-prompts.md): about 8 to 10 pages, graphs
over tables, interpretation over number dumps, and nothing that contradicts or
undersells the main text. No FAQ section unless the author asks for one.
