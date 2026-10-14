Existing related-work paragraph:
Method A improves accuracy across domains while reducing runtime~\cite{sourceA}. Method B cannot handle distribution shift~\cite{sourceB}. Our method is the first to support shifted inputs efficiently.

Supplied source notes (complete available source evidence for this passage):
sourceA, section 4: On one in-domain image dataset, A obtains 84% accuracy compared with 82% for its matched baseline. Runtime was not measured. No cross-domain experiment appears in the supplied source.
sourceB, section 5: B reports accuracy on two distribution-shift benchmarks, 71% and 68%. Compared with its own baseline under those same settings, this is +1 and -2 percentage points. Compute cost is not reported.
Author's current contribution description: Our pipeline selects among existing encoders using observed input statistics. No novelty search beyond A/B has been completed. The authors' current draft reports a matched latency comparison and two held-out shifts; the task is to fix positioning, not to invent a priority claim.

Reviewer comment: 'The paper has no threshold sensitivity experiment. It must add one before any claim can be assessed. Also Method B cannot evaluate shifted data, so remove it as a baseline.'

Frozen manuscript extract:
Main text section 4.2: 'We fix the routing threshold on the development split. Detailed threshold sensitivity is in Appendix C, Figure 8.'
Appendix C: 'Figure 8 evaluates thresholds 0.1, 0.2, 0.3 and 0.4 using the unchanged test set. Accuracy is 78.0%, 79.2%, 79.1% and 78.6%; mean latency is 22, 27, 34 and 43 ms. These are exploratory analyses after the primary threshold had been fixed; they were not used to select the submitted primary result. We did not repeat this sweep across random seeds.'
These supplied frozen-paper values are the authoritative fixture. No new experiment has been run. Do not say the main text was changed unless you actually produce the changed text as part of the deliverable.
