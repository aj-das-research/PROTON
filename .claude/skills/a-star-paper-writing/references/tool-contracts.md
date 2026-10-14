# Paper tools: contracts and limits

These dependency-free Python 3.9+ tools initialize working files and check their
consistency. Read this when creating or updating structured ledgers, initializing a new TeX project, or checking a build log. Every command supports `--help`. Python 3.10+ also supports the development-corpus auditor.

```bash
python <skill>/scripts/init_paper.py ./new-paper --title "Working title"
python <skill>/scripts/paper_audit.py ./new-paper --mode draft --json
python <skill>/scripts/paper_audit.py ./new-paper --mode ready
python <skill>/scripts/audit_latex_log.py ./new-paper/main.log --json
```

`init_paper.py` requires a new directory and never overwrites existing work. It
defaults to `--format tex`: `main.tex`, section files under `sections/`, ordered
appendix files under `appendix/`, empty `references.bib`, and directories for
figures, exact prompts, and evidence artifacts. Both formats create
`project-brief.md`, empty `evidence-ledger.json`, and unknown `venue-profile.json`.
`--format markdown` retains the optional `paper.md` and `supplement/` layout.
Titles are treated as text, with TeX special characters escaped.

The TeX scaffold is a generic article, explicitly labeled as a working draft,
not an official template. It can compile with pdfLaTeX before any research is
added; bibliography commands remain inactive until verified entries exist.
`overleaf-project.json` records these local defaults while remote identity,
TeX Live version, connection, synchronization, bibliography backend, and venue
verification remain unresolved. It does not create or connect an Overleaf project.
Adopt the verified venue template and its settings before claiming compliance.
Never run the initializer on an existing project: edit its source in place.
It invents no research records. A new project intentionally does not pass the audit.

Audit exit codes: **0** means mechanical checks passed; **1** means unresolved
records or rules; **2** means invalid input, schema, or unsafe paths. Draft mode
labels unresolved items `pending`; ready mode labels them `blocker`. Invalid
schema is an `error` in either mode. JSON output includes status, counts, issues,
limitations, and `submission_readiness_certified: false`. The audit is read-only.

## Evidence ledger, schema version 1

Root: `{ "schema_version": 1, "claims": [], "evidence": [], "citations": [] }`.
See [the unresolved example](../assets/evidence-ledger.example.json). All listed
fields are required unless marked optional. Unknown text/date/year values may be
`null` while drafting; unresolved required values prevent a clean report. IDs
start with a letter and use letters, digits, `_`, `.`, `:`, or `-`.

| Record | Fields |
|---|---|
| Claim | `id`, `text`, `kind`, `status`, `evidence_ids` (array of evidence IDs), `citation_ids` (array of citation IDs) |
| Evidence | `id`, `kind`, `status`, `artifact` (project-relative file path), `locator` (exact row, section, key, or lines), `scope`, `provenance` |
| Citation | `id`, `status`, `title`, `authors` (array of names), `year` (four-digit integer), `source_url` (HTTP(S)), `verified_on` (ISO date) |

Claim kinds: `empirical`, `theoretical`, `methodological`, `background`,
`limitation`. Evidence kinds: `experiment`, `proof`, `analysis`, `literature`,
`artifact`. Record status: `verified`, `pending`, `unsupported`.

`scope` contains `dataset`, `split`, `metric`, `unit`, `baseline`, and `budget`.
All six are strings or null; experiment/analysis evidence requires each to be
populated. Use an explicit `not applicable: reason` where warranted.
`provenance` contains `producer`, `created_on` (ISO date), and `description`.
Optional `provenance.sha256` is checked against the artifact's bytes. Optional
provenance fields such as `command`, `code_commit`, seeds, and environment can
document reproduction, but their contents are not automatically validated.
Optional evidence `values` maps names to finite JSON numbers. Nonfinite numbers,
including NaN, Infinity, and overflow, are rejected throughout either input file.

Empirical claims require experiment or analysis evidence; theoretical guarantees
require at least one **proof** artifact. Methodological claims require project
evidence. Background claims require a citation; limitation claims require
evidence or a citation. A record marked verified does not override missing
metadata or support. Empty claim, evidence, or citation collections cannot pass.
IDs must be unique within their record type; links must resolve without duplicate
entries. Artifacts must be nonempty regular files inside the project. Absolute
paths, traversal, and symlinks escaping the project are rejected.

## Venue profile, schema version 1

Root fields: `schema_version: 1`, `venue`, `year`, `track`, `stage`,
`verified_url`, `retrieved_on`, `rules`. Record the exact venue/year/track/stage
and the official source URL/date. See [the unknown-rule starter](../assets/venue-profile.example.json).
`rules` requires all four objects below. Rule status is `unknown` or `verified`.

| Rule | Required fields and values |
|---|---|
| `main_text` | `status`, `page_limit` (positive integer), `notes` (string or null) |
| `references` | `status`, `policy`, `page_limit`, `notes` |
| `appendix` | `status`, `policy`, `page_limit`, `columns`, `notes` |
| `ai_assistance` | `status`, `mode`, `disclosure`, `source_url`, `retrieved_on`, `notes` |

Reference/appendix `policy`: `unknown`, `included_in_main_limit`,
`separate_limited`, `unlimited`, or `not_allowed`. A separate positive integer
`page_limit` is required only for `separate_limited`; use null otherwise.
Appendix `columns`: `unknown`, `one_column`, `two_column`, `venue_template`, or
`not_applicable` (only when an appendix is prohibited). Unknown rules or an
unknown main-text page limit prevent a clean report.

AI-assistance `mode`: `unknown`, `drafting_allowed`,
`editing_author_text_only`, or `prohibited`. Its own `source_url` and
`retrieved_on` must contain a valid HTTP(S) URL and ISO date; `disclosure` must
state the verified requirement, including an explicit statement if no disclosure
is required. Null disclosure means unresolved. `notes` is optional in substance
(string or null). Dates use `YYYY-MM-DD` and must not be in the future.

Verify the applicable AI-assistance rule **before drafting**, then follow the permitted
mode. Unknown unrelated formatting rules remain audit findings but do not block
otherwise permitted drafting. A small section edit need not create these ledgers;
inspect the affected claims and evidence directly. A known restrictive rule can pass metadata checks; that does not authorize
drafting or prove that actual usage and disclosure comply. The agent must apply
that rule to the requested work separately.

## What passing does not establish

Artifact presence, hashes, and declared provenance do not establish scientific
truth or authenticity. The tool does not read all artifact contents, verify
citation entailment, extract every manuscript claim, fetch official policies,
parse LaTeX, count PDF pages, or validate actual AI use and disclosure. Inspect
the evidence, rendered paper, and official rules separately. Passing mechanical
checks never guarantees submission readiness or acceptance.

Additional JSON fields are allowed for project context but are not validated
unless documented above. Do not treat unchecked metadata as a verified result.

## Overleaf project profile

[overleaf-project.example.json](../assets/overleaf-project.example.json) is a
workflow record, not a connector configuration or an automatically validated
schema. It records observed identity/settings, connection capabilities, base
revision/hashes, dependency files, collaborative review state, local/remote
builds, and readback/synchronization evidence. `null`, `unknown`, and
`not_attempted` must stay unresolved until observed. `paper_audit.py` does not
validate this profile. Follow [overleaf-workflow.md](overleaf-workflow.md) to
inspect and use it; never store access tokens in it.

## LaTeX log triage

`audit_latex_log.py LOG [--json]` reads a UTF-8 log without running TeX or writing
files. Exit **0** means it recognized a LaTeX engine/format and reported PDF
output with no recognized problematic diagnostics; **1** means errors, unresolved
citations/references, duplicate labels, rerun requests, overflow/font problems,
or an incomplete/non-LaTeX log; **2** means the log cannot be read. Benign
underfull messages are counted separately, with layout still requiring inspection.
For concatenated engine runs, completion markers must come from the final
recognized invocation; diagnostics from earlier runs are conservatively retained.
The JSON includes log SHA-256, invocation count, line-located issues, and explicit false flags for
source revision, PDF, and synchronization verification.

This is a conservative pattern-based helper, not an exhaustive TeX parser.
It can miss package-specific diagnostics or flag an acceptable overflow for human
review. Inspect relevant engine and bibliography logs and the rendered PDF;
associate them with the current source revision. A passed old log cannot verify
a new source revision, and a PDF output line alone never proves a successful build.

## Development-corpus audit

`audit_corpus.py [--corpus JSONL] [--notes JSON] [--abstract-notes JSON]`
checks this package's dated research index and original reading notes. It uses
Python 3.10+, exits **0** for consistent records or **1** for findings/input
errors, and never modifies the corpus. Valid-shaped inputs produce a JSON
summary/issues report; malformed input produces a location-specific diagnostic.

The schema requires actual JSON booleans for reading flags, valid dates within
the recorded 2026-09-17 cutoff, canonical unique paper identities, unique notes,
and corresponding reading scopes. Targeted reviews need matching primary notes;
only explicitly abstract-inclusive notes support an abstract-read flag. Primary
notes accept `arxiv_id` or an explicit non-arXiv `paper_id`; both identifiers must
agree when supplied together. Custom files use the same dated schema; this is
not a general current-literature search tool. Cross-file consistency cannot prove
that reading happened, certify source authenticity, or assess writing quality.

## House-style lint

```bash
python <skill>/scripts/style_lint.py sections/ --json
python <skill>/scripts/style_lint.py sections/intro.tex --rules S01,S07,S11
```

`style_lint.py` reads only the prose a reader sees. It ignores LaTeX comments,
verbatim, display and inline math (except for the leading-zero rule, which
applies everywhere) and the comment arguments of labreview margin notes. Rules
S01 to S14 implement the mechanical parts of
[house-style.md](house-style.md): em dashes, semicolons, hype and LLM-marker
words, formulaic openers, parenthetical cross-references, figure-first
sentences, decimals without a leading zero, model names outside `\texttt{}`,
`10x` multipliers, "significant" without a test, underselling, report-style
phrasing, long paragraphs, and number-heavy abstracts. Exit code 0 means no
findings, 1 means findings, and 2 means bad input. A clean lint does not mean
good prose; read the text.
