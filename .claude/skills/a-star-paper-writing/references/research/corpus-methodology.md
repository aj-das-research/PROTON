# Paper corpus: method and limits

Access date and research cutoff: **2026-09-17**. This is a discovery and writing-analysis resource, not a ranking of the best papers or evidence that a writing pattern causes acceptance.

## What was actually done

The completed snapshot contains 622 unique records:
- 557 Hugging Face paper pages with independently resolved arXiv identifiers.
- 50 ICML 2023 bibliographic records seeded from the user's figure-skill corpus and title-crosschecked against the official PMLR proceedings index.
- 15 additional purpose-selected primary papers, beyond the HF set.

Author abstracts were inspected for all 622 records: 602 have individual abstract-level notes, and 20 are covered by the deeper notes below. One source (`arxiv:2601.18418`) supplies an abstract that ends mid-sentence; its limited available text was inspected and explicitly flagged. Do not describe all 622 as complete full-paper readings or conceal this source limitation.

Within this corpus, 20 papers received bounded narrative and structure reviews: author abstracts, introduction excerpts, main section outlines, and appendix outlines. Six also received additional selected appendix/evaluation passages. These are **not full-paper readings**. Final counts: 602 abstract-narrative reviews, 20 targeted narrative/structure reviews, zero metadata-only records, zero full-paper reviews, and zero visual reviews.

The 602 additional reviews were divided among five independent reading assignments. Each inspected actual author text and recorded a distinct 25–45-word original observation with its accessed URL. HF's generated summaries were excluded. When HF returned rate limits, readers stopped repeated requests there and used the primary arXiv or PMLR source; one truncated arXiv view was recovered from an accessible author abstract on HF. Author-abstract inspection does not validate the paper's experiments, theory, novelty, or prose beyond that scope.

The observations are in `abstract-reading-notes.json` and `primary-paper-notes.json`, with paper-specific original notes, source URLs, scope, and version information where inspected. Read the notes before transferring a pattern. These summaries evaluate writing choices, not mathematical correctness, reproduced results, acceptance status, or visual design.

## Sampling

For each accessible selected month, the first 50 entries of the browser-visible HF monthly ranking were selected:
2024-01, 2024-04, 2024-07, 2025-01, 2025-04, 2025-07, 2025-10, 2026-01, 2026-04, 2026-07, 2026-08.
The top 10 entries for 2026-09 were added with their displayed publication dates checked against September 17. Three entries in the eleven 50-item monthly samples did not resolve to usable paper IDs and were excluded; no fabricated replacement was inserted.

For the September sample, displayed publication dates ranged from August 29 to September 14, 2026. Where HF omitted the year, the arXiv identifier and current-month context supplied it. HF list membership records discovery month, not publication month.

Ranks and votes are observations from browser-returned snapshots, which may have different crawl times. Votes can change; a historical monthly page is not a historical freeze of votes. Upvotes identify visibility and interest, not scientific quality, acceptance, reproducibility, or writing quality. AI-generated HF summaries and user comments were not treated as the paper's author abstract.

Some 2023 month URLs and 2024-10 failed or were unavailable. Ordinary terminal HTTP requests were denied by the environment. Browsing and the authorized GitHub connector were used instead; no access restrictions were bypassed.

## 2023 proceedings provenance

Seed:
https://github.com/Mishrakshitij/paper-figure-creation-skill/blob/66739085a15c2cb7c85a1522e8811bf0e0af6161/research/corpus-500.jsonl

Independent metadata crosscheck:
https://proceedings.mlr.press/v202/

The original 500-record figure corpus includes papers from 2021–2024. It was not relabeled as a 2023–2026 reading corpus. Only 50 eligible 2023 titles found in the browser-visible official ICML index were retained here. All inherited caption-reading and visual-review statuses were discarded. This is a convenience sample with proceedings-order bias, not a representative sample of ICML or award winners.

## Reading-depth fields

- `metadata_only`: title, identifier, discovery/proceedings provenance. Does not mean abstract read.
- `abstract_narrative_review`: author abstract actually inspected and a paper-specific original narrative note recorded. Add only after that work.
- `targeted_narrative_structure_review`: the scopes named in the record were actually inspected; broader reading is not implied.
- `full_text_read`: false throughout this snapshot. Retrieval alone never sets it true.
- `visual_reviewed`: false throughout this snapshot. HTML text and captions do not establish visual inspection.

`arxiv_id_year_inferred` and `arxiv_id_month_inferred` are parsed from the identifier, not certified first-publication dates. Month-boundary releases can display a different date; Titans, for example, has a January identifier and a December 31 version date. `year` on an official proceedings record means proceedings year. The summary's year grouping combines those two different bases and must be labeled accordingly.

HF papers include technical reports and preprints. Venue and awards remain `not_verified` / `not_checked` unless checked separately against official sources. Do not cite the corpus as evidence of conference acceptance.

## Updating the corpus

1. Revisit official proceedings and official award pages for the target venue; add newer work and underrepresented areas.
2. Add monthly HF candidates as a supplementary discovery channel, retaining access date, rank, votes, and exact source.
3. Resolve canonical IDs; deduplicate versions. Verify first-publication dates near cutoff boundaries.
4. Assign a reading stage only after completing it. For abstract work, retain a 30–80 word original note about problem, gap, mechanism, evidence, and scope; do not store copied abstracts.
5. For structure work, inspect abstract, introduction, method, evaluation, conclusion, and appendix navigation, explicitly noting missing sections. Full prose reading and rendered-page inspection are separate actions.
6. Select a balanced deeper sample by paper type and field, including weaker/null findings and strong benchmark papers. Do not sample only papers claiming improvements.
7. Recompute counts from the ledger. State the number at each depth every time the corpus is described.

No full paper texts, abstracts, figures, or PDFs are redistributed in this repository. Temporary retrieval snapshots were kept only in scratch during analysis. The durable corpus retains identifiers, bibliographic provenance, observed discovery signals, and original notes.
