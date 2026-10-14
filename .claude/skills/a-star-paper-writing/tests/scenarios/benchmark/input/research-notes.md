# Author notes

We study AuditBench, a diagnostic benchmark for whether document QA systems
identify contradictions across revisions of the same source. We introduce a
dataset and annotation protocol, not a new QA algorithm.

There are 120 source documents with 10 revision-pairs each. We randomly assigned
the 1,200 pairs to train/dev/test in a 60/20/20 ratio. Same source documents may
occur in all three splits. No split manifest is attached.

Three public systems were run, but final score files are not available. The
intended metric is pair-level contradiction accuracy; no uncertainty is computed.
Annotation involved two annotators. Agreement results have not been calculated.

Only the principal evaluator prompt is saved. The notebook may contain a system
prompt and a retry prompt; nobody has inventoried them yet. The saved evaluator
prompt is: Compare the supplied document versions and decide if their claims conflict.

Target track author rule supplied by author: AI may polish author-written text,
but generating manuscript prose is prohibited. No official URL is supplied.
Draft paragraphs are not supplied. Figure dependency unavailable in environment.
