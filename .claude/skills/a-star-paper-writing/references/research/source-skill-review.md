# Comparative review of the six requested writing-skill sources

Accessed 2026-09-17. This is an original design synthesis, not a redistribution of source manuals. GitHub repositories were read through the GitHub connector; the two sites were read through web browsing. The sources are advice and implementations to evaluate, not authoritative conference rules or evidence that an agent-written paper will be accepted.

## Source inventory and inspected material

| Source | Snapshot | Actual material inspected | Observed license |
|---|---|---|---|
| [Master-cai/Research-Paper-Writing-Skills](https://github.com/Master-cai/Research-Paper-Writing-Skills) | `77e7c2c1ba06f7d71844873147665437a03aac1b` | `research-paper-writing/SKILL.md`; `references/method.md`, `experiments.md`, `paper-review.md`; root LICENSE | MIT, © 2026 Master-cai |
| [SNL-UCSB/paper-writing-skill](https://github.com/SNL-UCSB/paper-writing-skill) | `676f8520bba54208eb4fe1d41620e365d9af6a24` | `SKILL.md`; `author_profile/gate_semantic.md`, `compression_patterns.md`; `red_team_protocol.md`; root LICENSE | MIT, © 2026 Arpit Gupta |
| [Victor Chen / Deli AutoResearch](https://victorchen96.github.io/auto_research/skill/paper-writing.html) | Page labels itself v2.0, June 2026; no revision independently established | Full rendered scientific-paper-writing skill-group page, including literature ranking, experiment iteration, peer-review scoring and gates | No license verified on inspected page; linked source path `docs/scientific_paper_writing_skill.md` could not be retrieved through guessed public repository path |
| [lishix520/academic-paper-skills](https://github.com/lishix520/academic-paper-skills) | `c325557646e9418939ccc7b99171b149ad6314f1` | `strategist/SKILL.md`, `composer/SKILL.md`, `strategist/references/quality_standards.md`; root LICENSE | MIT, © 2025 Li Shixiong |
| [Imbad0202/academic-research-skills-codex](https://github.com/Imbad0202/academic-research-skills-codex) | `3c37ef8ab480ba1e9370309c24b99977ad44091f`; package declares 3.22.0 | `skills/academic-research-suite/SKILL.md`; `ars/academic-paper/agents/citation_compliance_agent.md`; `ars/academic-paper/references/writing_judgment_framework.md`; root LICENSE | CC BY-NC 4.0, © 2026 Cheng-I Wu |
| [PaperBanana paper-skills directory](https://paper-banana.org/paper-skills) | Live directory accessed 2026-09-17; no repository revision | Rendered directory and its category/skill descriptions | No reuse license verified for directory content |

Repository references above are default-branch commit SHAs read from branch metadata. Individual blobs were also inspected; source files may continue to change after this snapshot.

## Practices to adopt, adapt and reject

### Master-cai

Adopt its separation of section-specific references, reverse-outline checks, stable terminology, and explicit pairing of major claims with evidence. The method guide makes components intelligible by relating their purpose, operation and expected advantage; the experiments guide links comparisons, ablations and stress tests to paper claims. It explicitly includes failure modes and fair comparison settings.

Adapt module-based guidance for theory, benchmark and analysis papers rather than forcing every contribution into a pipeline. Treat visual polish as communication rather than scientific validation. Replace any broad acceptance recipe with an evidence audit tailored to the actual contribution. Table conventions should defer to the official template.

Evidence: [skill](https://github.com/Master-cai/Research-Paper-Writing-Skills/blob/77e7c2c1ba06f7d71844873147665437a03aac1b/research-paper-writing/SKILL.md), [method](https://github.com/Master-cai/Research-Paper-Writing-Skills/blob/77e7c2c1ba06f7d71844873147665437a03aac1b/research-paper-writing/references/method.md), [experiments](https://github.com/Master-cai/Research-Paper-Writing-Skills/blob/77e7c2c1ba06f7d71844873147665437a03aac1b/research-paper-writing/references/experiments.md).

### SNL-UCSB

Adopt a persistent paper context, an early provisional introduction revised after the evidence is organized, explicit page allocation, and review by an agent that did not draft the text. The semantic checks usefully demand traceability from numbers through analysis to raw results, accurate descriptions of prior work, consistent decompositions across sections, and visual inspection of figures. Keep reviewer findings with locations, severity and concrete remediation.

Adapt compression to remove duplicated explanations and numerical inventories while retaining critical assumptions and uncertainty. Do not impose a universal percentage reduction. Do not universalize the laboratory's sentence-length target, mandatory active voice, claim-only headings, or ban on hedging. Calibrated uncertainty is essential. Avoid an endless loop that claims all scientific risks have disappeared because agents agree.

Evidence: [skill](https://github.com/SNL-UCSB/paper-writing-skill/blob/676f8520bba54208eb4fe1d41620e365d9af6a24/SKILL.md), [semantic checks](https://github.com/SNL-UCSB/paper-writing-skill/blob/676f8520bba54208eb4fe1d41620e365d9af6a24/author_profile/gate_semantic.md), [independent review](https://github.com/SNL-UCSB/paper-writing-skill/blob/676f8520bba54208eb4fe1d41620e365d9af6a24/red_team_protocol.md), [compression](https://github.com/SNL-UCSB/paper-writing-skill/blob/676f8520bba54208eb4fe1d41620e365d9af6a24/author_profile/compression_patterns.md).

### Victor Chen / Deli AutoResearch

Adopt artifact handoffs between literature, drafting, experiments, figures and review; connect each experiment to a claim; separate raw results from presentation; and check citation metadata against primary records.

Reject institutional prestige as a literature-quality feature, fixed recency/acceptance/citation quotas, and verification of only a fraction of citations. Relevant contradictory and foundational work must remain eligible. Treat the page's numerical reviewer scores as unvalidated internal labels, never calibrated acceptance probabilities. Its suggestions to increase trials when significance is absent or select the best iteration need replacement with documented stopping rules, held-out confirmation, and transparent reporting of exploratory analyses. The survey-specific section/figure counts are not a template for an AI conference research paper. Source: [rendered workflow](https://victorchen96.github.io/auto_research/skill/paper-writing.html).

### lishix520

Adopt the separation of planning from composing, a written outline with each section's argumentative role, sample-paper comparison, and cross-section coherence checks. Its reference guide explicitly targets philosophy/interdisciplinary work and preprint platforms, so its word allocations and quality thresholds cannot be transferred as conference requirements.

Replace numeric originality percentages, impact forecasts and citation-count scores with evidence-backed comparison to nearest work. A sparse but complete relevant bibliography is preferable to satisfying a quota. Avoid mandatory confirmation after every chapter when the user has authorized autonomous drafting. Provide meaningful checkpoint artifacts and ask only questions that materially affect the argument or scope.

Evidence: [strategist](https://github.com/lishix520/academic-paper-skills/blob/c325557646e9418939ccc7b99171b149ad6314f1/strategist/SKILL.md), [composer](https://github.com/lishix520/academic-paper-skills/blob/c325557646e9418939ccc7b99171b149ad6314f1/composer/SKILL.md), [quality reference](https://github.com/lishix520/academic-paper-skills/blob/c325557646e9418939ccc7b99171b149ad6314f1/strategist/references/quality_standards.md).

### ARS-Codex

Adopt progressive loading, explicit workflow routing, separation of bibliography validity from claim support, provenance-aware review, and honest reporting of what a verifier actually checked. Its current router distinguishes independent review from shared-context simulation and warns that automated coverage does not establish manuscript correctness. The citation agent supplies useful orphan checks and a correction log, while its judgment reference encourages allocating attention to paragraphs essential to the argument.

Adapt broad disciplinary guidance to ML/CV/NLP conference conventions and official styles. Do not import fixed citation-age, self-citation, or paragraph-density thresholds as hard rules. Keep external service uploads separate from ordinary local writing. Avoid duplicating its large runtime and opaque score machinery. Its noncommercial license means substantial copying requires separate compatibility analysis; the new skill should use original instructions and acknowledge conceptual influence.

Evidence: [router](https://github.com/Imbad0202/academic-research-skills-codex/blob/3c37ef8ab480ba1e9370309c24b99977ad44091f/skills/academic-research-suite/SKILL.md), [citation agent](https://github.com/Imbad0202/academic-research-skills-codex/blob/3c37ef8ab480ba1e9370309c24b99977ad44091f/skills/academic-research-suite/ars/academic-paper/agents/citation_compliance_agent.md), [judgment reference](https://github.com/Imbad0202/academic-research-skills-codex/blob/3c37ef8ab480ba1e9370309c24b99977ad44091f/skills/academic-research-suite/ars/academic-paper/references/writing_judgment_framework.md).

### PaperBanana

Use this as a discovery directory. It groups writing, reading, research and presentation tools and links to implementations. Its stars, editorial summaries and reported scores are not controlled evidence of effectiveness. Inspect the underlying repository and license before adopting anything. Do not replace the user's designated figure skill with a directory-promoted service. Source: [directory](https://paper-banana.org/paper-skills).

## Recommended original skill architecture

1. A concise root router selects intake, evidence planning, writing, figure delegation, revision, reproducibility or submission audit; load only relevant reference modules.
2. A paper brief records venue/year/track, contribution type, scope, audience, strongest defensible claim, key assumptions and unresolved questions.
3. A claim ledger links each material claim to a result/proof/source, scope conditions, contradictory evidence and status. It must distinguish unavailable evidence from disconfirming evidence.
4. A literature ledger records primary URL, identifier/version, verification date, actual reading depth, relevant contribution, precise support and nearest-work differences. Metadata retrieval must never be counted as full-paper reading.
5. An experiment manifest captures dataset version/splits, leakage checks, seeds, hardware, code revision, metric definition, uncertainty unit, baseline parity, selection rule and raw result location.
6. Section references implement rhetorical functions rather than compulsory paragraph counts. The user-preferred abstract/introduction sequence is a useful default; method, benchmark, theory and analysis papers need distinct branches.
7. A figure contract delegates three principal conceptual figures to the designated figure skill, carrying stable terminology, claims, verified inputs and caption requirements. Quantitative plots remain reproducible data outputs.
8. An appendix manifest mirrors main-paper sections, includes complete prompts and operational settings, and marks what is necessary to assess core claims versus supplementary detail.
9. Independent review emits located findings and unresolved scientific concerns. A limited audit loop verifies changes and logs remaining risks, without predicting acceptance.
10. A submission preflight reads current official venue requirements. User preferences for eleven pages, unlimited references, one-column appendices and FAQ length apply only where permitted and useful.

## Licensing and provenance decision

Do not vendor source manuals, examples, snippets or scripts into the new repository. Write original operational guidance, retain this source inventory, and link the consulted materials. MIT copies would require retaining notices if substantial portions were reused. ARS-Codex is noncommercial, and the two web pages did not establish a reuse license during inspection. These observations are practical provenance constraints, not a legal opinion. Keep generated project artifacts and the author's research content separate from third-party source material.
