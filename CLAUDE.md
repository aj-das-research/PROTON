# PROTON: reproduction + PROTON+ (Abhijit Das, MBZUAI)

Paper: "PROTON: Prototype-Based Test-Time Online OOD Detection for Medical VLMs" (Das et al.; `proton_paper.pdf`,
text dump in `notes/proton_paper.txt`). Goal: faithful reproduction of every table/figure, then an improved
PROTON+ write-up, a reusable OOD toolkit, a project page with a live demo.

## Layout

| Path | What | Tracked |
|---|---|---|
| `proton/` | the library (`pip install -e .`): models, data, scores, online detector, evaluate, experiments, cli | yes |
| `tests/` | pytest unit tests (`python -m pytest -q tests`) | yes |
| `scripts/` | one-off helpers (smoke tests, exports) | yes |
| `data/benchmarks/*/manifest.csv` | exact image lists per benchmark (seeded) | yes (manifests only) |
| `data/raw/`, `data/benchmarks/*/` images, `weights/`, `third_party/`, `outputs/` | raw downloads, exported PNGs, checkpoints, results | no |
| `paper/` | git clone of the Overleaf project (PROTON+ paper, arXiv style) | own repo, not tracked here |
| `docs/` | GitHub Pages project page + in-browser demo | yes |
| `.claude/skills/a-star-paper-writing` | project-local writing skill (do NOT install globally; `tools/install_skills.sh`) | yes |

## Environment and compute

- Python env: `/mnt/hdd2/Abhijit/envs/proton/bin/python` (uv, py3.11, torch 2.11 cu128, open_clip, transformers,
  FLAIR installed editable from `third_party/FLAIR`). Always export `HF_HOME=/mnt/hdd2/Abhijit/.cache/huggingface`.
- Use `/usr/bin/curl` or `/usr/bin/wget` for downloads (the miniconda curl fails TLS on figshare).
- GPUs: pick a GPU with 0 MiB in `nvidia-smi`, set `CUDA_VISIBLE_DEVICES`; never touch `slurmlite` processes.
  Abhijit (2026-10-14): use idle GPUs freely, yield when someone is queued, never leave work idle.
- Feature extraction is the only GPU step (`proton extract`); everything else is numpy on cached `.npz` files.

## Reproduction pipeline

```
proton prepare-data                       # manifests from data/raw (seed 0)
CUDA_VISIBLE_DEVICES=5 proton extract --benchmark ophthalmology   # -> outputs/features/<bench>__<vlm>.npz
proton run --benchmark ophthalmology      # -> outputs/results/<bench>/table*.json|md, fig3b grid
proton figures                            # -> outputs/figures/*.pdf|png
```
Benchmarks (`proton/data/benchmarks.yaml`): ophthalmology = Ju et al. (FIVES N/D vs G+A, DeepDRiD UWF, ImageNet);
radiology = RSNA normal/opacity vs COVID-19, paediatric CXR (Kermany), ImageNet; pathology = PCam vs NCT-CRC
tissues, Camelyon17-WILDS other hospital, ImageNet. `id_bank` rows are a disjoint labelled ID set used only by the
privileged kNN/Mahalanobis baselines.

## Conventions

- Metrics: OOD positive, higher score = more OOD; AUROC/AUPR-out/FPR@95 as in Ju et al. notebooks.
- PROTON defaults (paper): gamma=0.7, M=100, K_min=5, alpha in [0.3,0.7], sigma2_0=0.02; 5 stream permutations.
- Never copy numbers from the paper into results; everything in `outputs/results` is computed.
- Git identity is repo-local (Abhijit Das). Push code to `origin` (github.com/aj-das-research/PROTON) and the paper
  to Overleaf via `git -C paper push` (pull first).

## Paper and site (status 2026-10-14)

- `paper/` holds the PROTON+ preprint in LNCS format (`main.tex` + `lncs_sections/*.tex`, llncs.cls/splncs04.bst).
  Compile with `~/.local/bin/tectonic -X compile --keep-logs main.tex` (the conda `tex` env is broken); check
  `grep -c Overfull main.log` is 0 and render pages with PyMuPDF. Tables: `python scripts/make_paper_tables.py`.
  Copy `main.pdf` to `docs/protonplus.pdf` after each build. Figures 2-5 (matplotlib, shared style
  `figures_src/paper_style.py`, Liberation Sans in `figures_src/fonts/`, 4.80 in wide = LNCS text width):
  `figures_src/fig2_embedding.py` -> fig1_blind_spot, `fig3_results_v2.py` -> fig3_results,
  `fig4_convergence.py` -> fig3a_convergence, `fig5_gamma_M.py` -> fig3b_gamma_M (PROTON+ grid cached in
  `outputs/results/<benchmark>/fig5_gamma_M_plus.json`, `--recompute` rebuilds). Each script's `save()` writes
  `paper/figures/` and `docs/figures/`. Run with the proton env and `HF_HOME=/mnt/hdd2/Abhijit/.cache/huggingface`.
  The older `proton figures` / `figures_src/fig_results.py` / `fig_method*.py` routes are superseded.
- Abhijit removed the "AI assistance" paragraph from the conclusion on Overleaf (2026-10-14): do not re-add it.
- `docs/` is the project page, live at https://aj-das-research.github.io/PROTON/ (Pages source main:/docs), with the
  guided browser demo in `docs/demo/` (weight-only int8 ONNX of FLAIR's vision tower, tracked in git, mirrored on HF
  `abhijit2k01/proton-demo`; `scripts/export_demo_assets.py` regenerates it). Visual QA: `scripts/screenshot.py URL OUT.png`.
  Curated benchmarks are on HF `abhijit2k01/proton-benchmarks` (`scripts/push_hf_dataset.py`).
- Prompt policy (2026-10-14, Abhijit's decision): one uniform rule, the modality-prefixed class prompt of the benchmark
  code (`flair_default`, radiology `l1`, pathology `l1`); all other prompt sets go to the appendix prompt-sensitivity table.

- Method figure (Fig. 1 of the preprint, README, project page): TikZ, `figures_src/tikz_method/fig_method.tex` with real data from `make_data.py` -> `data.tex` (FLAIR embeddings, ultra-widefield stream seed 0, image t=413). Build: `cd figures_src/tikz_method && ~/.local/bin/tectonic -X compile fig_method.tex`, then copy the PDF to `paper/figures/fig2_method.pdf` and export PNG/SVG (PyMuPDF) to `docs/figures/`. Final design = variant A (chosen by Abhijit); variant B and the earlier matplotlib versions are kept for reference only.
