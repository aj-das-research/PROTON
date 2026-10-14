# PROTON / PROTON+: test-time online OOD detection for (medical) vision-language models

[![Project page](https://img.shields.io/badge/project-page-blue)](https://aj-das-research.github.io/PROTON/)
[![Paper](https://img.shields.io/badge/paper-PROTON-b31b1b)](proton_paper.pdf)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)

`proton-ood` is a small, dependency-light library for **zero-shot and test-time OOD detection with frozen
vision-language models**. It contains

* a faithful implementation of **PROTON** (Das et al.): an online, per-class prototype bank built from confident
  test predictions, a prototype-distance score, and variance-adaptive fusion with any softmax/logit score;
* **PROTON+**: domain-anchored (mean-shift) prototypes, consistency-gated bank admission and scale-free fusion,
  which fix the prototype-contamination failure mode of PROTON (see the paper in `paper/`);
* the standard zero-shot baselines (MCM, Max-Logit, Energy, Entropy, GL-MCM, TAG-MCM, hierarchical-prompt MCM) and
  two privileged feature-bank detectors (kNN-ID, Mahalanobis-ID);
* three ready-made medical benchmarks (ophthalmology / FLAIR, radiology / UniMed-CLIP, pathology / QuiltNet) with
  semantic, covariate and far-OOD splits, reproducible manifests, cached features and every table/figure of the paper;
* a plain `numpy` core: once features are cached nothing below needs a GPU.

```python
from proton import PROTON, score_stream, ood_metrics
from proton.online import proton_plus_config

# embeds: (N,d) l2-normalised image embeddings in stream order, text: (C,d) class-prompt embeddings
out = score_stream(embeds, text, logit_scale=model.logit_scale)                 # PROTON (paper defaults)
plus = score_stream(embeds, text, logit_scale=model.logit_scale, config=proton_plus_config())  # PROTON+
print(ood_metrics(plus["score"], is_ood))                                        # AUROC / AUPR / FPR@95
```

Streaming use (one sample at a time, O(Cd) per step, bank <= C*M*d floats):

```python
det = PROTON(n_classes=2, config=proton_plus_config())
for e, p, s_mcm in stream:            # embedding, softmax over class prompts, any base score (higher = more OOD)
    rec = det.step(e, p, s_mcm)       # rec["score"], rec["s_proto"], rec["alpha"], rec["calibrated"], ...
```

## Install

```bash
git clone https://github.com/aj-das-research/PROTON.git && cd PROTON
pip install -e ".[models,data,plots]"          # core is numpy/scipy/scikit-learn only
# FLAIR (ophthalmology VLM) and the UniMed-CLIP fork are vendored as git clones:
tools/fetch_third_party.sh                     # clones FLAIR, UniMed-CLIP and the Ju et al. benchmark notebooks
pip install -e third_party/FLAIR
```

## Reproduce the paper

```bash
tools/download_data.sh            # FIVES, DeepDRiD UWF, Imagenette, RSNA, Kermany CXR, COVID-19 RDB, PCam, Camelyon17, NCT-CRC
tools/download_weights.sh         # FLAIR ResNet-50, UniMed-CLIP ViT-B/16, QuiltNet-B/32 (+ text encoders)
proton prepare-data               # seeded manifests -> data/benchmarks/<domain>/manifest.csv
CUDA_VISIBLE_DEVICES=0 proton extract --benchmark ophthalmology   # cached features -> outputs/features/*.npz
proton run --benchmark ophthalmology                              # all tables -> outputs/results/ophthalmology/*.md
proton figures                                                    # -> outputs/figures/*.pdf
```

`proton run` writes Markdown + JSON for: the main zero-shot table (Table 2), component / gamma / M ablations
(Table 3), the ID-fraction sweep (Table 1a), PROTON on six base scores (Table 4a), broader baselines incl. the
privileged ones (Table 4b), robustness extras (sigma_0 sweep, forced misrouting, overhead, shift-type triage),
the gamma x M sensitivity grid (Fig. 3b), the PROTON+ comparison and a prompt-sensitivity table. Nothing is ever
copied from the paper; every number is recomputed from the cached features.

## Add your own model or benchmark

* **Model**: subclass `proton.models.base.VLM` (implement `transform`, `image_forward`, `encode_text`,
  `logit_scale`) and register it with `@proton.models.register("name")`, or use any `open_clip` checkpoint directly:
  `load_model("open_clip:hf-hub:org/name")`.
* **Benchmark**: add an entry to `proton/data/benchmarks.yaml` (classes, prompt sets, manifest path) and write a
  manifest CSV with columns `domain,set,label,class_name,source,path` where `set` is one of
  `id, id_bank, semantic, covariate, far` (`id_bank` = optional labelled ID split for the privileged baselines).

## Layout

```
proton/            library: models/ (FLAIR, UniMed-CLIP, QuiltNet/open_clip), data/ (benchmarks, manifests),
                   scores/ (static + feature-bank baselines), online.py (PROTON, PROTON+), evaluate.py, streams.py,
                   features.py, metrics.py, experiments/ (tables, figures), cli.py
tests/             pytest unit tests
data/benchmarks/   committed manifests (the images themselves are downloaded by tools/download_data.sh)
outputs/           features, results, figures (not tracked)
paper/             PROTON+ manuscript (Overleaf-synced), docs/ project page + browser demo
```

## Citation

```bibtex
@article{das2026proton,
  title   = {PROTON: Prototype-Based Test-Time Online OOD Detection for Medical VLMs},
  author  = {Das, Abhijit and Wasalathilaka, Nichula and Lu, Yifan and Dukre, Adinath and Mahapatra, Dwarikanath and Khan, Shadab and Razzak, Imran},
  year    = {2026}
}
```
