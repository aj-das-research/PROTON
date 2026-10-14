# Lessons from the broader author-abstract review

These are bounded qualitative inferences from the original per-paper notes in `abstract-reading-notes.json`. They are neither measured frequencies nor evidence that a rhetorical pattern causes acceptance. Follow each note's actual source URL; current abstract versions can differ from the version present when a historical HF ranking was formed. One source's incomplete available text is flagged in its note.

## Make the diagnosed gap imply the intervention

A precise bottleneck gives the proposal a reason to exist. The notes on Medusa (`arxiv:2401.10774`), ControlNet++ (`arxiv:2404.07987`), and MathForge (`arxiv:2601.20614`) identify links between the diagnosed constraint and the component introduced to address it. The transferable editing question is: which part of the proposed mechanism would be unnecessary if the stated bottleneck were absent?

For a multi-part proposal, map each diagnosed issue to a component and a relevant test. Do not convert that rhetorical correspondence into a causal claim unless controlled evidence supports it. Add targeted replacements or interactions where several components can explain a gain.

## Give each claimed property its own evidence

WebVoyager (`arxiv:2401.13919`) distinguishes agent success from agreement about evaluation. Notes on `arxiv:2607.27205` distinguish quality, latency, memory, and hardware conditions. A useful abstract reports what was measured and against what comparison, rather than treating one number as evidence of every desirable property.

If the paper claims effectiveness and efficiency, preserve both axes and their conditions. If an evaluator is itself part of the contribution, its reliability needs evidence separate from the system ranking it produces. Avoid replacing a missing axis with an adjective.

## Explain what a benchmark makes measurable

The notes on Claw-Eval (`arxiv:2604.06132`), FrontierChallenge (`arxiv:2608.24979`), and the paraphrase benchmark `arxiv:2603.28301` focus on evaluation channels, completion criteria, diagnostic transformations, and failure localization. Size alone does not explain why a benchmark is useful.

State the unit, construct, task distribution, scoring, and question that existing evaluations fail to answer. Give the denominator and compare capability dimensions fairly. A benchmark's value may be exposing low scores or ranking instability; it need not introduce a winning method.

## Keep resource accounting explicit

Notes on Minitron (`arxiv:2407.14679`) and LightMem (`arxiv:2510.18866`) highlight the need to distinguish resource dimensions and online versus deferred work. A reduced online cost does not by itself establish lower total cost. Put named comparators, budgets, and operating conditions beside efficiency claims.

In the main evaluation, retain preprocessing, training/tuning, retrieval, judging, failures, and amortization assumptions when they affect the claim. In the abstract, choose the resource actually supported—calls, tokens, memory, latency, throughput, or total measured compute.

## Use boundaries and negative findings to sharpen the claim

The controlled KAN/MLP comparison (`arxiv:2407.16674`), clean-arithmetic diagnostic (`arxiv:2507.10532`), and Spectra (`arxiv:2407.12327`) illustrate that a diagnostic or conditional finding can be the central contribution. Other notes preserve explicit scope: `arxiv:2607.14952` separates execution capacity from training correctness; `arxiv:2608.10744` constrains a transfer result to a shared representation family.

Keep a material boundary in the abstract when omitting it would change the reader's interpretation. Do not confuse a proof of concept with general production capability. Preserve observed weaknesses and unresolved alternative explanations; writing can clarify them without presenting them as strengths they are not.

## Let theory abstracts state assumptions and guarantees

The ICML abstracts identified by `pmlr:attia23a`, `pmlr:anagnostides23a`, `pmlr:agoritsas23a`, and `pmlr:agarwala23b` motivate an assumption → result/rate → consequence → technical ingredient pattern. Distinguish a proved low-dimensional statement from empirical higher-dimensional behavior. Do not force a theory abstract to include an empirical win or omit a restrictive assumption to simplify the story.

## Limits of this synthesis

The corpus is dominated by popularity-selected HF candidates, with a convenience sample from ICML 2023 and purpose-selected structural exemplars. It mixes technical reports, preprints, and proceedings papers. Abstracts expose author claims and rhetorical choices; they do not establish that experiments, proofs, or headline comparisons are valid. No acceptance inference, field-representative prevalence estimate, or full-paper reading is claimed here.
