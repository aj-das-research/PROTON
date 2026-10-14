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
