# PROTON+: a follow-up report on prototype-based test-time OOD detection for medical VLMs

*Abhijit Das et al., MBZUAI. Follow-up to PROTON ([arXiv:2606.20913](https://arxiv.org/abs/2606.20913)). All numbers below are
regenerated from `outputs/results/` by `scripts/build_report.py`; nothing is copied from the original paper.*

## 1. Why a follow-up

PROTON adds an online bank of class prototypes on top of a frozen medical vision-language model (VLM) and fuses the
distance to the nearest prototype with the maximum-concept-matching (MCM) score, so that covariate-shifted inputs
that look confident to the softmax can still be flagged. We re-implemented PROTON from scratch as a library, built three
benchmarks (ophthalmology, radiology, pathology; semantic / covariate / far-OOD splits each) and found two things:

1. **The gain over MCM reported in the PROTON paper does not transfer.** On the ultra-widefield covariate split
   PROTON scores 46.7 AUROC against 68.9 for MCM. The absolute PROTON number is close
   to the original paper's (66.3 with the original prompt), but the MCM baseline is far stronger than the 42.4 reported.
2. **The cause is bank contamination.** The confidence gate can only exclude low-confidence inputs, which MCM already
   detects. A covariate-shifted input is confidently misclassified by definition, so it enters the bank of the class it
   was assigned to. On the ultra-widefield stream 97% of the shifted images pass the gate
   (mean confidence 0.955 vs 0.970 for ID), 148 of 150 are assigned to the
   diabetic-retinopathy class, and that class bank ends with 63% shifted members (means over 5 stream
   orders). The prototype then sits between the ID and the shifted cluster and separates neither.

PROTON+ keeps the bank and the fusion of PROTON and changes how prototypes are estimated and which samples may enter.

## 2. What changed from PROTON

| Component | PROTON | PROTON+ |
|---|---|---|
| Class prototype | normalised mean of the FIFO queue | **domain-anchored**: a mean-shift step over the union of all queues finds the dominant imaging-domain mode μ_dom; each class prototype is the mean of its queue weighted by exp((e·μ_dom − 1)/h), h = 0.1, 3 iterations |
| Bank admission | max softmax ≥ γ | max softmax ≥ γ **and** distance to the predicted-class prototype ≤ mean + κ·std of previously admitted distances (κ = 2, active after K_min admissions post-calibration) |
| Fusion | α·S_MCM + (1−α)·S_proto on raw scales | same weight α (variance-driven, unchanged) on **online z-scores** of both signals; z-scored MCM before calibration so the score keeps one scale |
| Hyper-parameters | γ = 0.7, M = 100, K_min = 5, α ∈ [0.3, 0.7], σ²₀ = 0.02 | identical, plus h and κ fixed a priori |
| Cost / state | 0.02 ms per sample, 0.41 MB | 0.10–0.28 ms per sample (anchor update after each admission), 0.41 MB |

Everything else (frozen VLM, prompts, no labels, no training, single pass over the stream) is unchanged. Two variants are
evaluated alongside: the maximum of the two z-scores instead of the weighted sum, and a fusion weight driven by the
rejection rate of the admission rule instead of the MCM variance.

## 3. Results

Mean ± SD over five random stream orders; each stream = all ID test images + all images of one OOD split.

### 3.1 Headline (AUROC and FPR@95)

| Benchmark | Method | Sem AUROC | Cov AUROC | Far AUROC | Sem FPR@95 | Cov FPR@95 | Far FPR@95 |
|---|---|---|---|---|---|---|---|
| Ophthalmology | MCM | 75.8 | 68.9 | 78.5 | 86.0 | 69.7 | 75.0 |
| Ophthalmology | PROTON (paper algorithm) | 68.0 ± 0.9 | 46.7 ± 1.8 | 86.8 ± 3.6 | 92.7 ± 2.3 | 83.6 ± 6.1 | 55.0 ± 26.0 |
| Ophthalmology | **PROTON+** | 67.3 ± 0.7 | 85.3 ± 7.8 | 93.4 ± 0.5 | 75.8 ± 1.7 | 31.5 ± 26.5 | 15.4 ± 1.8 |
| Radiology | MCM | 54.2 | 46.6 | 27.6 | 89.7 | 87.3 | 99.7 |
| Radiology | PROTON (paper algorithm) | 55.3 ± 0.9 | 61.2 ± 1.7 | 93.9 ± 2.3 | 95.2 ± 1.2 | 67.6 ± 3.7 | 33.5 ± 33.5 |
| Radiology | **PROTON+** | 61.4 ± 0.7 | 93.9 ± 0.6 | 91.5 ± 1.4 | 88.1 ± 1.4 | 26.7 ± 5.4 | 35.7 ± 31.5 |
| Pathology | MCM | 59.8 | 66.1 | 67.1 | 90.3 | 85.2 | 77.2 |
| Pathology | PROTON (paper algorithm) | 64.9 ± 1.3 | 73.0 ± 3.7 | 75.2 ± 3.7 | 92.8 ± 1.2 | 87.2 ± 8.7 | 80.4 ± 12.5 |
| Pathology | **PROTON+** | 82.4 ± 0.3 | 85.6 ± 0.9 | 92.1 ± 0.7 | 67.7 ± 5.4 | 50.7 ± 4.1 | 35.0 ± 4.3 |

PROTON+ beats MCM on every covariate and far stream on all five orders in all three modalities. On semantic shift it
loses to MCM in ophthalmology (67.3 vs 75.8), where glaucoma and AMD images lie inside the ID imaging
domain, and wins in radiology and pathology. Against the *best* static score of each split (not only MCM) the margins
are: covariate 1.1, 15.5, 18.4; far 9.4, 7.0, 24.9;
semantic -8.4, -8.8, 22.5 (ophthalmology, radiology, pathology).

### 3.2 All zero-shot scores

**Ophthalmology (FLAIR)**

| Method | Sem AUROC | Sem AUPR | Sem FPR | Cov AUROC | Cov AUPR | Cov FPR | Far AUROC | Far AUPR | Far FPR |
|---|---|---|---|---|---|---|---|---|---|
| Max-Logits | 54.0 | 54.1 | 79.3 | 27.9 | 23.3 | 88.0 | 83.9 | 76.4 | 63.0 |
| Energy | 51.8 | 51.5 | 79.7 | 27.2 | 23.2 | 88.0 | 83.9 | 76.5 | 62.7 |
| GL-MCM | 75.8 | 75.6 | 86.0 | 68.9 | 45.3 | 69.3 | 78.5 | 62.4 | 75.0 |
| MCM | 75.8 | 75.6 | 86.0 | 68.9 | 45.2 | 69.7 | 78.5 | 62.4 | 75.0 |
| TAG-MCM | 68.4 | 70.5 | 88.7 | 30.1 | 23.8 | 93.7 | 72.2 | 47.2 | 60.3 |
| MCM (L=1) | 66.5 | 65.0 | 84.7 | 84.2 | 66.3 | 47.3 | 51.8 | 38.4 | 98.3 |
| MCM (L=5) | 58.3 | 56.5 | 87.0 | 66.5 | 42.5 | 65.7 | 54.4 | 33.5 | 74.3 |
| PROTON | 68.0 | 72.5 | 92.7 | 46.7 | 29.4 | 83.6 | 86.8 | 76.2 | 55.0 |
| **PROTON+** | 67.3 | 69.0 | 75.8 | 85.3 | 63.9 | 31.5 | 93.4 | 81.8 | 15.4 |

**Radiology (UniMed-CLIP)**

| Method | Sem AUROC | Sem AUPR | Sem FPR | Cov AUROC | Cov AUPR | Cov FPR | Far AUROC | Far AUPR | Far FPR |
|---|---|---|---|---|---|---|---|---|---|
| Max-Logits | 69.4 | 56.1 | 82.3 | 0.4 | 10.8 | 100.0 | 75.7 | 64.6 | 90.2 |
| Energy | 70.2 | 57.4 | 84.8 | 0.4 | 10.8 | 100.0 | 77.0 | 67.4 | 90.5 |
| GL-MCM | 54.3 | 35.7 | 89.7 | 46.7 | 18.1 | 87.3 | 29.2 | 14.2 | 98.0 |
| MCM | 54.2 | 35.2 | 89.7 | 46.6 | 18.1 | 87.3 | 27.6 | 14.0 | 99.7 |
| TAG-MCM | 57.4 | 36.8 | 87.8 | 48.1 | 19.3 | 85.5 | 41.3 | 16.0 | 87.5 |
| MCM (L=1) | 54.2 | 35.2 | 89.7 | 46.6 | 18.1 | 87.3 | 27.6 | 14.0 | 99.7 |
| MCM (L=5) | 54.2 | 32.0 | 77.5 | 78.4 | 38.2 | 46.3 | 84.6 | 52.3 | 39.5 |
| PROTON | 55.3 | 38.3 | 95.2 | 61.2 | 31.0 | 67.6 | 93.9 | 92.5 | 33.5 |
| **PROTON+** | 61.4 | 42.4 | 88.1 | 93.9 | 82.1 | 26.7 | 91.5 | 74.6 | 35.7 |

**Pathology (QuiltNet)**

| Method | Sem AUROC | Sem AUPR | Sem FPR | Cov AUROC | Cov AUPR | Cov FPR | Far AUROC | Far AUPR | Far FPR |
|---|---|---|---|---|---|---|---|---|---|
| Max-Logits | 2.1 | 19.1 | 100.0 | 21.3 | 12.4 | 97.7 | 25.0 | 15.3 | 99.3 |
| Energy | 1.7 | 19.1 | 100.0 | 19.4 | 12.2 | 99.0 | 23.3 | 15.0 | 99.7 |
| GL-MCM | 56.7 | 40.5 | 94.0 | 67.2 | 30.9 | 77.7 | 67.2 | 29.1 | 75.2 |
| MCM | 59.8 | 42.4 | 90.3 | 66.1 | 29.8 | 85.2 | 67.1 | 31.5 | 77.2 |
| TAG-MCM | 48.7 | 33.1 | 97.2 | 48.0 | 19.4 | 92.0 | 45.1 | 18.7 | 95.0 |
| MCM (L=1) | 59.8 | 42.4 | 90.3 | 66.1 | 29.8 | 85.2 | 67.1 | 31.5 | 77.2 |
| MCM (L=5) | 15.3 | 20.4 | 99.8 | 64.6 | 30.7 | 77.3 | 61.1 | 26.3 | 87.3 |
| PROTON | 64.9 | 54.9 | 92.8 | 73.0 | 47.3 | 87.2 | 75.2 | 50.4 | 80.4 |
| **PROTON+** | 82.4 | 72.5 | 67.7 | 85.6 | 64.6 | 50.7 | 92.1 | 81.6 | 35.0 |

### 3.3 Which change matters (AUROC)

| Benchmark | Variant | Sem | Cov | Far |
|---|---|---|---|---|
| Ophthalmology | PROTON (paper) | 68.0 ± 0.9 | 46.7 ± 1.8 | 86.8 ± 3.6 |
| Ophthalmology | + z-scored fusion | 69.4 ± 1.1 | 50.7 ± 0.4 | 89.0 ± 1.5 |
| Ophthalmology | + consistency admission | 70.6 ± 2.9 | 40.1 ± 2.8 | 92.6 ± 1.7 |
| Ophthalmology | + domain-anchored prototypes = PROTON+ | 67.3 ± 0.7 | 85.3 ± 7.8 | 93.4 ± 0.5 |
| Ophthalmology | S_proto alone (PROTON+ bank) | 57.0 ± 1.0 | 90.4 ± 12.6 | 97.9 ± 0.8 |
| Ophthalmology | PROTON+ with oracle admission | 73.6 ± 2.9 | 90.4 ± 1.1 | 93.5 ± 0.6 |
| Ophthalmology | PROTON+, max-fusion | 65.7 ± 0.6 | 86.6 ± 6.5 | 93.2 ± 0.7 |
| Ophthalmology | PROTON+, rejection-driven α | 64.4 ± 2.4 | 86.9 ± 9.0 | 93.6 ± 1.9 |
| Radiology | PROTON (paper) | 55.3 ± 0.9 | 61.2 ± 1.7 | 93.9 ± 2.3 |
| Radiology | + z-scored fusion | 61.6 ± 0.8 | 78.1 ± 0.8 | 90.5 ± 1.3 |
| Radiology | + consistency admission | 61.9 ± 0.7 | 78.4 ± 12.1 | 92.8 ± 1.4 |
| Radiology | + domain-anchored prototypes = PROTON+ | 61.4 ± 0.7 | 93.9 ± 0.6 | 91.5 ± 1.4 |
| Radiology | S_proto alone (PROTON+ bank) | 62.6 ± 0.5 | 98.8 ± 0.5 | 96.2 ± 2.2 |
| Radiology | PROTON+ with oracle admission | 64.9 ± 0.9 | 92.4 ± 1.5 | 91.3 ± 1.6 |
| Radiology | PROTON+, max-fusion | 56.0 ± 0.7 | 92.2 ± 1.2 | 90.8 ± 1.9 |
| Radiology | PROTON+, rejection-driven α | 60.8 ± 0.8 | 95.8 ± 2.3 | 93.8 ± 2.1 |
| Pathology | PROTON (paper) | 64.9 ± 1.3 | 73.0 ± 3.7 | 75.2 ± 3.7 |
| Pathology | + z-scored fusion | 77.7 ± 0.6 | 84.7 ± 0.8 | 82.8 ± 2.5 |
| Pathology | + consistency admission | 82.1 ± 0.7 | 85.6 ± 1.0 | 88.2 ± 7.9 |
| Pathology | + domain-anchored prototypes = PROTON+ | 82.4 ± 0.3 | 85.6 ± 0.9 | 92.1 ± 0.7 |
| Pathology | S_proto alone (PROTON+ bank) | 94.9 ± 0.7 | 93.7 ± 0.9 | 98.7 ± 0.4 |
| Pathology | PROTON+ with oracle admission | 82.1 ± 0.6 | 85.8 ± 0.8 | 91.4 ± 1.1 |
| Pathology | PROTON+, max-fusion | 84.8 ± 0.5 | 87.9 ± 1.5 | 95.2 ± 1.4 |
| Pathology | PROTON+, rejection-driven α | 88.3 ± 3.5 | 88.0 ± 3.5 | 96.6 ± 1.7 |

The prototype distance *alone*, computed from the PROTON+ bank, is the strongest single detector on every covariate and
far shift (90–99 AUROC). Fusion with MCM only pays where MCM carries information the embedding lacks (ophthalmology
semantic shift). The oracle row (shifted samples never admitted) is a reference, not a bound: PROTON+ exceeds it on three
pairs because the oracle calibrates later.

### 3.4 Stream composition (AUROC, Sem / Cov / Far)

| Benchmark | ID fraction | MCM (Sem/Cov/Far) | PROTON | PROTON+ |
|---|---|---|---|---|
| Ophthalmology | 90% | 76.2 / 67.7 / 75.5 | 73.1 / 85.5 / 90.4 | 70.6 / 88.5 / 90.9 |
| Ophthalmology | 70% | 74.8 / 69.0 / 79.0 | 71.2 / 47.7 / 87.4 | 68.7 / 74.7 / 92.9 |
| Ophthalmology | 50% | 75.8 / 69.1 / 78.4 | 68.2 / 34.0 / 55.3 | 67.4 / 22.3 / 36.7 |
| Ophthalmology | 30% | 76.2 / 68.3 / 78.0 | 60.3 / 28.0 / 26.4 | 64.5 / 28.8 / 27.8 |
| Ophthalmology | 10% | 75.9 / 69.2 / 78.1 | 50.0 / 41.3 / 16.7 | 56.8 / 41.4 / 20.5 |
| Radiology | 90% | 53.7 / 46.8 / 27.5 | 57.8 / 71.0 / 94.1 | 64.8 / 96.4 / 94.1 |
| Radiology | 70% | 54.4 / 47.2 / 27.9 | 54.9 / 54.3 / 81.8 | 62.0 / 89.5 / 81.0 |
| Radiology | 50% | 54.5 / 47.9 / 28.5 | 54.5 / 49.9 / 58.8 | 58.8 / 69.0 / 73.0 |
| Radiology | 30% | 54.5 / 46.7 / 27.7 | 54.0 / 38.8 / 37.1 | 55.6 / 12.2 / 14.2 |
| Radiology | 10% | 53.5 / 47.5 / 27.5 | 53.8 / 23.7 / 21.4 | 52.5 / 12.7 / 13.1 |
| Pathology | 90% | 60.0 / 66.6 / 67.1 | 73.0 / 74.6 / 81.9 | 87.0 / 87.5 / 93.8 |
| Pathology | 70% | 59.9 / 65.8 / 66.8 | 64.1 / 65.4 / 68.4 | 81.6 / 79.8 / 81.7 |
| Pathology | 50% | 60.2 / 65.4 / 66.5 | 60.1 / 61.7 / 64.3 | 73.9 / 71.5 / 73.5 |
| Pathology | 30% | 59.6 / 67.6 / 68.7 | 55.6 / 67.6 / 63.9 | 45.2 / 67.5 / 68.8 |
| Pathology | 10% | 63.0 / 61.2 / 61.9 | 51.8 / 61.2 / 54.4 | 44.7 / 61.6 / 50.3 |

Both detectors assume that ID inputs are the majority of the stream. Once the shifted cluster dominates the bank, the
prototype score inverts; MCM is order-free and does not.

### 3.5 Prompt sensitivity

The main tables use one policy: the modality-prefixed class prompt of the public benchmark code ("A fundus photograph
of …", "x-ray of …", "histopathology image of …"). Prompt wording moves MCM by up to 28 AUROC points between
single-prompt wordings; PROTON+ is far less sensitive on covariate and far shifts.

| Benchmark | Prompt set | ID acc. | MCM (Sem/Cov/Far) | PROTON | PROTON+ |
|---|---|---|---|---|---|
| Ophthalmology | flair_default | 84.0 | 75.8 / 68.9 / 78.5 | 68.0 / 46.7 / 86.8 | 67.3 / 85.3 / 93.4 |
| Ophthalmology | vanilla | 86.0 | 65.6 / 64.9 / 83.5 | 58.5 / 46.7 / 94.4 | 58.2 / 87.9 / 97.0 |
| Ophthalmology | l1 | 83.7 | 66.5 / 84.2 / 51.8 | 65.0 / 66.6 / 78.2 | 64.6 / 94.0 / 88.1 |
| Ophthalmology | l5 | 57.3 | 58.3 / 66.5 / 54.4 | 41.2 / 24.0 / 25.3 | 56.2 / 50.8 / 58.8 |
| Radiology | vanilla | 73.2 | 41.8 / 57.5 / 55.5 | 44.9 / 78.9 / 94.7 | 53.2 / 95.5 / 96.2 |
| Radiology | l1 | 69.2 | 54.2 / 46.6 / 27.6 | 55.3 / 61.2 / 93.9 | 61.4 / 93.9 / 91.5 |
| Radiology | l5 | 55.3 | 54.2 / 78.4 / 84.6 | 50.3 / 79.1 / 88.3 | 49.9 / 88.5 / 96.8 |
| Pathology | l1 | 59.3 | 59.8 / 66.1 / 67.1 | 64.9 / 73.0 / 75.2 | 82.4 / 85.6 / 92.1 |
| Pathology | id_acc | 72.7 | 48.8 / 48.0 / 45.1 | 52.9 / 55.6 / 58.2 | 72.5 / 70.1 / 81.1 |
| Pathology | vanilla | 64.5 | 64.3 / 53.4 / 72.5 | 66.7 / 58.9 / 82.2 | 75.8 / 72.9 / 92.5 |
| Pathology | l5 | 65.5 | 15.3 / 64.6 / 61.1 | 32.6 / 61.5 / 65.7 | 15.4 / 73.4 / 81.5 |

## 4. What we understand now

* **Softmax erases the shift, the embedding keeps it.** Oracle prototypes separate covariate and far shifts at 97–100 AUROC
  in every modality; the whole difficulty is estimating prototypes from an unlabelled, contaminated stream.
* **Confidence is the wrong admission criterion for covariate shift.** The samples a detector must catch are exactly the
  confident ones. Geometry of the bank (dominant mode, typical radius) is a usable label-free substitute.
* **Scale matters.** A probability-based score and a cosine distance cannot be mixed with a fixed weight; z-scoring alone
  recovers 4–17 AUROC points on covariate shift.
* **The variance-driven weight is effectively constant** (0.42–0.65 on every stream), and no label-free statistic we tried
  picks the better signal on all nine streams. Choosing the fusion weight online remains open.
* **Benchmarks of different datasets measure dataset identity.** Privileged detectors with labelled ID features reach
  99–100 AUROC on covariate and far shifts. Splits drawn from the same acquisition pipeline (our radiology semantic split)
  are harder and more informative.

## 5. Limitations and next steps

* ID-minority streams (ρ ≤ 0.5) invert both detectors; a deployment that cannot guarantee an ID majority needs a small
  labelled seed set.
* Test-time prompt learners (TTL, TINS, STAR) were not run; the released streams make that comparison direct.
* One VLM per modality; FLAIR's text encoder averages over padding tokens, so prompts must be encoded as the benchmark
  code does (jointly), and this is documented and implemented.

## 6. Use PROTON+ instead of PROTON

```python
from proton import PROTON, score_stream, ood_metrics
from proton.online import proton_plus_config

out = score_stream(embeds, text_embeds, logit_scale, config=proton_plus_config())   # PROTON+
det = PROTON(n_classes=2, config=proton_plus_config())                              # or step-by-step
rec = det.step(e_t, p_t, s_mcm_t)                                                   # rec["score"], rec["s_proto"], ...
```

`proton_plus_config()` returns PROTON's hyper-parameters with `proto_mode="domain"`, `admission="consistency"` and
`normalize="zscore"`; passing no config gives the original PROTON algorithm. The benchmarks, baselines, streams,
metrics and the `proton make-benchmark` / `proton extract` / `proton run` pipeline work for any registered VLM and any
folder-based dataset (see README).

## 7. Reproduce this report

```
tools/download_data.sh && tools/download_weights.sh && proton prepare-data
for b in ophthalmology radiology pathology; do proton extract --benchmark $b && proton run --benchmark $b; done
python scripts/contamination_stats.py && python scripts/extra_stats.py && python scripts/build_report.py
```
