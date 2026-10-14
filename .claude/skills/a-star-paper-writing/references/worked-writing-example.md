# Worked example: composing a measurement paper

Use this example when the agent needs to turn evidence into connected manuscript prose. **Every study, model, dataset, and number below is synthetic teaching material.** No experiment was performed for this example. Do not reuse its facts or claim priority from its wording. The manuscript excerpts are deliberately written in an ordinary author voice; their synthetic status belongs to this teaching document.

## Fixed fact packet

- Question: Does judging individual requirements improve response-level agreement with human reference labels for prompts containing several instructions?
- Protocol: Authors enumerate requirements before examining model responses. A fixed judge model J either gives one holistic pass/fail decision or labels each requirement and returns pass only when all requirements pass. Both use one call per response and the same model version and decoding settings.
- Data: 20 development prompts were used to settle the protocol. The separate evaluation set contains 80 prompts across four instruction families and three fixed response models, yielding 240 responses. No evaluation response was excluded.
- Reference: Two human annotators independently label each requirement; a third adjudicates disagreements. Their final requirement labels determine the response-level reference.
- Main comparison: Holistic judging matches 188/240 reference labels (78.3%); requirement-level judging matches 204/240 (85.0%). These are observed proportions, with no uncertainty analysis supplied.
- Cost: Mean judge output length is 64 tokens for holistic decisions and 118 tokens for requirement-level decisions. Runtime and monetary cost were not measured.
- Error analysis: Of the 36 remaining requirement-level errors, 22 involve an ambiguous requirement according to the adjudicator's error coding; 14 miss a requirement expressed in the response. These categories were assigned after inspecting errors.
- Scope: One judge model, the specified instruction families, and three response models. No claim about model rankings, open-domain reliability, or generalization to other judges is supported.

## Decide what each passage must accomplish

The title names the measurement operation and setting. The abstract connects the evaluation problem to an explicit protocol, the matched comparison, its gain, and its measured cost. The introduction bridge makes the design understandable before discussing its scores. The results passage answers the evaluation question and uses the remaining errors to identify a concrete boundary.

This is a measurement contribution: more explicit judgments agree more often with the supplied human reference in the studied setting. It is not evidence that the response models follow instructions better.

## Title

**Requirement-Level Judging for Compositional Instruction Following**

## Abstract

Evaluating a response to a prompt with several instructions requires deciding whether each requirement was satisfied. A single pass/fail judgment gives no explicit account of which requirements support that decision. We study requirement-level judging: authors enumerate instructions before examining responses, and the judge labels the supplied requirements separately, returning a response-level pass only when every requirement passes. We compare this protocol with holistic judging using the same judge model on 240 responses from three models to 80 held-out prompts. Agreement with adjudicated human response labels increases from 78.3% to 85.0%, while mean judge output length increases from 64 to 118 tokens. Requirement-level judging therefore improves observed agreement in this setting at the cost of longer outputs. Ambiguous requirements account for 22 of its 36 remaining errors, identifying requirement interpretation as a continuing obstacle for this protocol.

## Introduction bridge

A response can satisfy the most visible instruction in a prompt while missing another. For example, a response may contain the requested information but violate an instruction about its ordering. A holistic pass/fail label does not expose how these separate requirements contributed to the decision. The measurement question is whether making them explicit improves agreement with human assessment.

In our protocol, authors enumerate requirements before inspecting model responses. The judge receives this list and produces a separate judgment for each requirement. The response passes only if every requirement passes. This rule makes the connection between local judgments and the final label inspectable: an incorrectly accepted response must involve either an omitted requirement or an incorrect local judgment. Enumerating requirements first also prevents the particular response from determining which instructions are checked.

We evaluate whether this representation of the task changes the judge's decisions. Holding the judge model and decoding settings fixed, we compare the protocol with holistic judging against adjudicated human labels. The evaluation measures both agreement and output length, while error analysis examines where explicit decomposition still leaves the judge's decision incorrect.

## Results excerpt

**Explicit requirements improve observed agreement.** Requirement-level judging matches 204 of 240 human reference labels, compared with 188 for holistic judging: 85.0% versus 78.3%, a difference of 6.7 percentage points. The structured protocol thus makes 16 fewer response-level errors on this evaluation set. This comparison measures agreement with the reference, rather than a change in the quality of the responses being evaluated.

The improvement comes with longer judge outputs in this comparison. Mean output length rises from 64 to 118 tokens per response, although both protocols use one judge call. Output length captures this measured resource difference; it does not establish a runtime or monetary-cost ratio and does not account for the authors' requirement-enumeration labor.

Decomposition does not resolve every interpretive difficulty. Post hoc coding attributes 22 of the 36 remaining errors to ambiguous requirements and 14 to missed evidence of a requirement in the response. These cases motivate separating requirement interpretation from response checking in subsequent evaluation.

## Why the composition works

The passages explain a specific operation before asserting its value. The numerical comparison carries the positive finding; no adjective substitutes for it. The added token use appears beside the benefit, where it changes the reader's assessment. The error categories suggest a next measurement question without proving a causal explanation. Repetition serves different purposes: the abstract summarizes, the introduction explains, and the results quantify. A full paper would add the actual model identifiers, prompts, annotation instructions, complete protocol, appropriate uncertainty analysis accounting for responses sharing a prompt, and source-backed related work; those details cannot be manufactured from this fact packet.

