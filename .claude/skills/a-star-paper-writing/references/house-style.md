# House style: how the author and their lab write

Read this before writing or rewriting any manuscript prose. It condenses two
sources:

- **The author's own instructions.** Kshitij Mishra, from their ICLR 2027 drafting
  sessions.
- **The SPOT AI lab standard they write under.** This is Nils Lukas's
  `lukas-writing-style` skill in `spotai-mbzuai/spotai-research`, adapted here
  for ML venues. Nils's skill remains the authority on Nils's personal voice and
  on security papers. Use it directly when the user asks for "Nils style" or
  writes a security paper.

When the two conflict, the author's newest direct instruction wins. Where this
file reconciles them, the reconciliation is stated.

## Contents

1. The voice in one paragraph
2. Sentence mechanics
3. Paragraphs and flow
4. Terms, definitions, notation
5. Numbers and results
6. Pointers, citations, credit
7. Lexicon: banned, restricted, and LLM-marker phrasing
8. Selling without overselling
9. LaTeX mechanics
10. The pre-return checklist

## 1. The voice in one paragraph

Write sober, direct, evidence-first prose that a skeptical expert can check.
Each sentence makes one checkable point: a fact, a definition, a decision or a
number. Surprise belongs in the result, never in the adjectives. The paper
reads as a scientific paper, not a project report: no run logs, file paths or
experiment numbers. It sells the contribution plainly and hides nothing a
reviewer would call hidden. Simple words beat impressive ones: "if I had
more time I would have said it in fewer words" (Nils). "Less is more. Don't
show things that are irrelevant; that can only hurt you." Every sentence
should sound like a researcher who could defend it aloud, not like generated
text.

## 2. Sentence mechanics

1. **One checkable claim per sentence, 15 to 30 words.** Split a sentence that
   carries two points. Avoid both run-ons and staccato fragments.
2. **"We" for what the authors did, and the method's name for what the method
   does.** Write "We find that ..." for the paper's own measurements, so that
   reviewers credit them. Write "CID ranks the inputs", not "we rank the
   inputs". Name the actor in motivating examples (the operator, the provider,
   the user).
3. **No em dashes, few semicolons, no colon expansions.** Recast "X: Y"
   sentences with a comma, "because", parentheses or a second sentence. Colons
   survive in titles and run-in labels.
4. **Every sentence carries content.** Delete sentences that only announce,
   recap or hand off ("We now turn to...", "This section presents...", "The
   picture worsens."). The topic sentence states the paragraph's claim.
5. **Show, don't tell.** State the facts that lead to the conclusion instead of
   announcing it ("This shows that ..."). Spell a conclusion out only for the
   central insight or the gap.
6. **One argument per point, the strongest.** Never argue a point twice, and
   never restate it in a later paragraph or bullet.
7. **Most arguments in fewest words.** After drafting, cut the intensifiers
   and fillers ("actually", "merely", "just", "very", "clearly", "indeed")
   and the framing clauses. Every pass makes the text shorter without making it
   choppy.
8. **Enumerations.** Write (i), (ii), (iii) inline for findings, reasons and use
   cases. Displayed contribution lists are numbered, so readers can cite
   "contribution 2". Each item says what it is, not just its name.
9. **Concede in the same breath as the claim.** "robust to almost all ...",
   "reduces but does not prevent ...". Guardrails ride along with strong claims.
10. **Hedges are specific or absent.** "To the best of our knowledge" for
    priority claims. Never stack hedges ("might potentially suggest").

## 3. Paragraphs and flow

- **Length.** A paragraph runs at most about 6 to 7 printed lines (Nils: "Far
  too long (13 lines)... Split it").
- **One purpose per paragraph.** It opens by naming its role in the argument,
  and its last sentence leads into the next paragraph.
- **Link sentences with content.** Open each sentence with something the
  previous one established, and end it on the new information ("these calls",
  "such reports"). Use a transition word only when the logic is a turn,
  an addition or a consequence, and at most once per paragraph.
- **Refine, don't reintroduce.** When a paragraph picks up a concept, refine it.
  Do not restate its definition.
- **Protect the last line.** Check the final PDF for paragraphs that end on one
  or two words, and trim a clause. This usually also saves a line.

## 4. Terms, definitions, notation

- **Define before use**, in plain words, including named baselines ("ContextCite
  masks random subsets of inputs and fits a linear model") and cost terms. The
  paper must be self-contained: "we should not write papers only for experts"
  (Nils).
- **One term per concept, forever.** Coin a term once with `\emph{}`, then
  repeat it verbatim. Before rewriting a section, list its terms and map each to
  the word earlier sections already use. Never align an early section to a
  later one.
- **Loaded words** (truth, causal, understanding, reasoning, realistic, safe,
  self-improving) need an operational definition, or they go.
- **Acronyms.**
  - Expand at first use, and use memorable names for methods and metrics.
  - Drop an acronym used only once or twice.
  - Write GRPO or DPO with a citation instead of spelling out a well-known
    name.
  - Use "(ours)" only for the proposed method.
- **Notation.** One symbol family per object. Keep the appendix notation
  identical to the main text. Drop notation that is never reused. Number every
  equation. Explain each term of a display equation in plain words right after
  it.
- **Model names** go in `\texttt{}` everywhere: prose, captions and tables
  (`\texttt{Qwen3.5-9B}`). In figures, use generic labels ("LLM agent")
  unless the figure is about a specific model.

## 5. Numbers and results

- **Report value ± SD and the margin.** Examples: "$65.1 \pm 1.4$" and "an
  11.7% relative gain over SFT+GRPO". State the protocol once in the setup:
  seeds, what varies, and what the ± is over. Never write run-log prose such as
  "across three seed runs".
- **Say what the ± is over.** Three evaluation runs of one checkpoint are not
  three training runs. Report the same statistic on every row of a table.
- **Write ± only when the protocol supports it.** Before copying a "± SD" into
  the abstract or introduction, check that the setup and the appendix agree
  on the number of runs. If the paper says "three seeds" in one place and "run
  once" in another, write the point estimate, and flag the contradiction to the
  author. Do not spread a ± the evidence may not have.
- **Leading zeros everywhere**: 0.645, never .645.
- **Know which change you mean.** Percentage points and relative percent
  differ: 60% to 63% is +3 points, or +5% relative. Name the baseline of
  every relative number, and make it the strongest baseline when the sentence
  says "strongest".
- **Justify every specific number.** A threshold, weight or constant needs its
  reason in the same sentence, from a measurement, a citation or a definition.
  An arithmetic restatement is not a reason. If there is no reason, cut the
  number.
- **Numbers in the abstract.** The reconciled rule: the abstract states the
  finding, and ends with at most one or two numbers. Each is a relative
  improvement over a named baseline on a named metric, which is Kshitij's
  preference. They go only at the end (Nils, 2026-09-24). Do not list several
  results with numbers.
- **Numbers in the motivation.** The paragraphs that motivate the problem carry
  no statistics unless the number itself is the point. An oddly specific
  number reads as cherry-picked.
- **Multipliers** are written as math, `$10\times$`, never "10x". Write units
  out.
- **Mark new numbers.** A number first computed during a rewrite gets the
  orange `\NewFinding{}` highlight and a margin note naming its source file (see
  [revision-workflow.md](revision-workflow.md)).

## 6. Pointers, citations, credit

- **Point first, then cite the figure inside the sentence.** Write "..., as
  Figure 1a shows". Never open with "Figure 1a shows that". Do not use
  parenthetical cross-references such as "(App. B.2)" or "(Figure 20)"; they
  read as generated.
- **Keep appendix pointers few.** Use at most one per subsection, and only
  where it backs a claim. Consolidate the rest into one sentence per section,
  and drop figure numbers from pointers.
- **No forward references** to later sections in body text. Roadmap sentences
  in section openers are fine.
- **Keep citations inline, and never in footnotes.** Name the method or dataset
  in the text so the citation does not interrupt ("CaMeL constrains ...
  (Debenedetti et al., 2025)"). Do not re-cite a work in the next section, and
  do not cite common knowledge.
- **Re-check every citation the draft already had.** A citation carried over
  into a rewritten sentence must support that sentence. Move it to the sentence
  it supports, replace it with a verified source, or flag it for the authors.
- **Prefer recent work.** Cite the last three years, except for the canonical
  source of a definition. Grade sources: peer-reviewed papers and primary
  reports outrank analyst forecasts, which outrank vendor surveys. Never
  stack weak sources on one point.
- **Credit borrowed components**, such as a reward term or a gate, where they
  are used, and narrow the novelty claim to what differs.

## 7. Lexicon

**Banned:**

- paradigm, holistic, cutting-edge, groundbreaking;
- crucially, importantly, notably (as sentence adverbs);
- delve, showcase, tapestry, realm, pivotal, harness, unlock, empower,
  seamless, meticulous;
- "significantly" without a test;
- any stacked intensifiers, exclamation marks, rhetorical questions in prose;
- "allows to", "it can be observed that", contractions;
- "more" or "better" without "than what";
- evaluative superlatives ("the cheapest way"), where you should state the
  measured property;
- valuing adjectives in the experiments section ("realistic", "reasonable",
  "impressive", "striking").

**Formulaic openers.** These mark text as generated, so start with the content
instead:

- "To address these limitations, ..."
- "To obtain this property, ..."
- "In this paper, we ..."
- "Concretely, ..."
- "In recent years, ... has gained significant attention"

**Permitted sparingly:** novel (for genuinely new methods or definitions),
state of the art (for established external systems), leverage, comprehensive,
rigorous.

**LLM-marker pairings.** Prefer the words a researcher would say aloud:

- "synthetic premises" becomes "simple reasoning tasks that we generate";
- "surface cues" becomes the actual cue, such as "word overlap or position";
- "low-credibility report" becomes "unreliable report";
- "stale state" becomes "outdated records".

If a phrase would sound odd in a talk, rewrite it.

**Report language.** None of these may appear in the paper:

- run names, host names, job ids, file paths, "Exp36";
- "pilot", "toy", "earlier study", "previous version";
- "we were unable to";
- FAQ sections.

## 8. Selling without overselling

Kshitij wants the work sold ("don't undersell anything", "no stone unturned")
and every claim true. Hold both:

- **A false or unsupported claim is never acceptable.** Narrow it, add the
  evidence, or cut it.
- **An honest caveat does not belong in the abstract, the contributions or
  the last line of the introduction.** Put it in the results or the limitations,
  framed as scope. Preview only the limits a reviewer would otherwise call
  hidden.
- **Replace a cut hedge with precise scope.** When a rewrite removes an
  underselling hedge such as "pilot study on toy tasks", keep the facts it
  carried: state once what the evidence covers ("one benchmark and one 9B base
  model"), in the introduction's evidence paragraph or the results, never in the
  abstract's last line. Flag other sections that still carry the old hedge, such
  as the conclusion.
- **Limitations are written as future work.** Name the limitation as a
  research direction ("Towards larger settings"), state the fact with its
  measured number, and describe scope by what it covers ("models up to
  \texttt{Qwen3-14B}"), not by how small it is. End with the extension it opens.
- **Frame a result that favours a baseline as what the method adds** ("training
  lets X overtake the baseline with two fewer masks"). Do not frame it as a
  concession that opens with "However".
- **Keep the strong results and the qualitative analysis in the main text.**
  Moving them to the appendix undersells the paper.
- **Sell the phenomenon, not the vehicle.** The task or benchmark is the
  vehicle. The finding about the models is the story.

## 9. LaTeX mechanics

- **One sentence per line**, separated by a bare `%` line. This is the lab's
  diff-friendly format; preserve it when editing.
- Use `\emph{}` to coin terms and `\textbf{Topic.}` for run-in paragraph
  headers. Use `\Cref{}` for references and `\texttt{}` for model names.
- **Never change the venue template**, margins, fonts or spacing. Preserve
  every existing macro and every co-author annotation (`\Review[...]`,
  `\nils{}`).
- Figures use `width=\linewidth` unless wrapped. Captions open with a bold
  sentence that states the takeaway, and stay short.
- Put the teaser figure on page 1 with the introduction.

## 10. The pre-return checklist

Before returning prose, check each of these:

- [ ] Each sentence makes one point; the cut pass is done; no filler, no
  framing sentences, no colon expansions, no em dashes.
- [ ] Every term is defined before use and keeps one name. Model names are in
  `\texttt{}`. Acronyms are expanded or dropped.
- [ ] Every number is correct against its source, carries its ± and baseline,
  and has leading zeros. The relative and absolute changes are right.
- [ ] No run-log phrasing, file paths, "pilot" or "earlier study". Nothing
  undersells the work in the abstract, introduction or contributions.
- [ ] No parenthetical cross-references, and no figure-first sentences.
  Citations are inline and recent.
- [ ] Every sentence could be defended aloud by a researcher. Nothing sounds
  generated.
- [ ] In the final-mode PDF: no short last lines, Figure 1 on page 1, and the
  main text within the page limit.
- [ ] `python scripts/style_lint.py <files>` reports no issues you have not
  consciously accepted.
