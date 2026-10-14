# PROTON+ follow-up report

The follow-up report is the preprint **"PROTON+: Contamination-Robust Prototype Banks for Test-Time Online OOD
Detection with Medical VLMs"** (LNCS format): [PDF on the project page](https://aj-das-research.github.io/PROTON/protonplus.pdf).
It is a follow-up to [PROTON](https://arxiv.org/abs/2606.20913) and every number in it is regenerated from
`outputs/results/` by the scripts in this repository.

## What changed from PROTON

| Component | PROTON | PROTON+ |
|---|---|---|
| Class prototype | normalised mean of the FIFO queue | **domain-anchored**: mean-shift mode over the union of all queues, members weighted by proximity to it (h = 0.1) |
| Bank admission | max softmax ≥ γ | max softmax ≥ γ **and** distance to the predicted-class prototype within mean + κ·std of admitted distances (κ = 2) |
| Fusion | α·S_MCM + (1−α)·S_proto on raw scales | the same α on **online z-scores** of both signals |
| Hyper-parameters | γ = 0.7, M = 100, K_min = 5, α ∈ [0.3, 0.7], σ²₀ = 0.02 | identical |
| Cost | 0.02 ms / sample, 0.41 MB | 0.10–0.28 ms / sample, 0.41 MB |

## Headline (AUROC, mean ± SD over five stream orders)

See the results block of the [README](README.md#results) and `outputs/results/<benchmark>/*.md` for every table
(main zero-shot table, ablations, ID-fraction sweeps, base scores, privileged baselines, prompt sensitivity).

## Use PROTON+ instead of PROTON

```python
from proton import PROTON, score_stream
from proton.online import proton_plus_config
out = score_stream(embeds, text_embeds, logit_scale, config=proton_plus_config())   # PROTON+ (recommended)
det = PROTON(n_classes=2, config=proton_plus_config()); rec = det.step(e_t, p_t, s_mcm_t)
```
