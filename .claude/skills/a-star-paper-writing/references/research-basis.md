# Research basis, provenance, and limits

This skill combines the author's requested preferences, original operational guidance, inspected source-skill interfaces, verified venue-policy snapshots, and explicit reading notes. These are different kinds of support: author preferences are not conference requirements, observed paper patterns are not causal explanations of acceptance, and popularity is not peer review.

## New research review: 2026-09-19

The [deep research review](research/deep-review-2026-09-19.md) documents 17 public repositories, 29 inspected skill/prompt/reference files, 21 other primary sources, and nine additional bounded paper readings. It maps evidence to the new story, method-explanation, composition-example, citation, evaluation, and revision guidance. Counts describe different source categories, not independent quality validations. The historical corpus below is unchanged. Read this review for development provenance; ordinary writing tasks should load the relevant practical reference instead.

## Research records

Snapshot: 622 paper records spanning identifier/proceedings years 2023–2026 through 2026-09-17. Author abstracts were inspected for all records, with one explicitly flagged incomplete source; 20 papers additionally received bounded introduction/section/appendix-organization review. Full-paper and visual-paper review counts are zero. The exact machine-readable summary distinguishes these scopes.

Read only what helps the current task:

- [Corpus methodology](research/corpus-methodology.md): selection, dates, coverage, reading levels, and sampling limitations.
- [Paper index](research/paper-corpus.jsonl): paper IDs, source links, discovery provenance, and reading depth for each record.
- [Corpus summary](research/corpus-summary.json): exact counts, recomputed from the index.
- [Primary section-review notes](research/primary-paper-notes.json): 20 bounded abstract/introduction/outline studies with original narrative observations and version information; some include additional appendix excerpts.
- [Author-abstract reading notes](research/abstract-reading-notes.json): paper-specific original observations, actual accessed URLs, and explicitly flagged source limitations.
- [Broader abstract-writing lessons](research/abstract-writing-lessons.md): evidence-linked qualitative synthesis without frequency or acceptance claims.
- [Writing-pattern synthesis](research/writing-patterns.md): analyst inferences from that purpose-selected subset.
- [Source-skill review](research/source-skill-review.md): the six user-supplied resources, inspected paths/revisions, licensing, and adopt/adapt/reject decisions.
- [Figure-interface provenance](research/figure-source-audit.json): the inspected version and files of the author's external figure dependency.

Use `python scripts/audit_corpus.py` to inspect bookkeeping consistency. It does not verify that reading occurred or that a paper's claims are correct. Source snapshots and downloaded paper texts are not distributed; the package stores metadata and original notes.

## What changes actual writing decisions

| Observed pattern in inspected sources | Operational choice in this skill | Boundary |
|---|---|---|
| DPO links an optimization obstacle to a mathematical change | State the mechanism and its evidential consequence, not only a framework name | A derivation still needs checked assumptions/proof |
| SAM/SAM 2 and SWE-bench separate task/data construction from evaluation | Use distinct task/benchmark/data sections when these carry the contribution | Do not add a fictitious environment to static tasks |
| Mamba and GEAR connect modeling choices to systems consequences | Separate quality, memory, latency, and implementation evidence | Asymptotics alone do not establish measured speed |
| Self-RAG and SAM 2 expose meaningful failure cases | Tie real examples to records and report material boundaries | A selected example does not establish prevalence |
| s1 treats selection and inference budget as separate design choices | Match each design claim with its discriminating comparison | Ablations do not eliminate every confound |
| Large technical reports expose stages and versions | Preserve model/data/prompt/version-to-result mappings | Report length and layout do not transfer to conference rules |

These are original inferences from the scopes documented in the notes, not complete scientific audits of those papers. Do not repeat an exemplar's headline result without checking its actual evidence for the current use.

## Source skill use and attribution

Inspected resources: [Master-cai](https://github.com/Master-cai/Research-Paper-Writing-Skills), [SNL-UCSB](https://github.com/SNL-UCSB/paper-writing-skill), [Victor Chen's writing guide](https://victorchen96.github.io/auto_research/skill/paper-writing.html), [lishix520](https://github.com/lishix520/academic-paper-skills), [ARS-Codex](https://github.com/Imbad0202/academic-research-skills-codex), and [PaperBanana](https://paper-banana.org/paper-skills). Detailed provenance is in the source review.

This package uses original prose and code. It does not vendor their skill manuals or silently inherit their licenses. The inspected ARS-Codex repository uses CC BY-NC 4.0; several others use MIT. Re-check permissions before copying any upstream code or text. The user's figure skill remains an external dependency, with its actual contract described in [figure-integration.md](figure-integration.md).

Useful design influences include progressive reference loading, persistent briefs, claim–evidence ledgers, evidence-specific review, and explicit source verification. The package rejects purported acceptance guarantees, arbitrary citation quotas, prestige-based citation selection, invented results, success-only analysis, and thresholds optimized to obtain a desired statistical conclusion.

## Keep the evidence current

The corpus is not representative of all AI, an award census, a ranking of writing quality, or an exhaustive 2023–present review. HF sampling favors visible topics and communities; some entries are technical reports or unreviewed preprints. Dates can refer to discovery, identifier issuance, version, or venue, and are labeled accordingly. Inspect primary records before claiming exact first-publication dates or accepted status.

Refresh closest work for each manuscript and official venue rules for each edition/track/stage. A useful future corpus update adds original notes with explicit reading scopes; it never increments a full-reading count because a file was downloaded or parsed.
