"""OOD detection metrics.

Convention (same as Ming et al. 2022 / Ju et al. 2025 notebooks): the OOD set is the positive class and a
higher score means "more OOD". AUPR is therefore AUPR-Out; FPR@95 is the false-positive rate on ID samples at the
threshold where 95% of OOD samples are detected (tpr=0.95), picked as the ROC operating point closest to 0.95.
"""
from __future__ import annotations

import numpy as np
from sklearn.metrics import average_precision_score, roc_auc_score, roc_curve


def _check(scores, is_ood):
    scores = np.asarray(scores, dtype=np.float64).ravel()
    is_ood = np.asarray(is_ood).astype(int).ravel()
    if scores.shape != is_ood.shape:
        raise ValueError(f"scores {scores.shape} and labels {is_ood.shape} differ")
    if is_ood.min() == is_ood.max():
        raise ValueError("need both ID (0) and OOD (1) samples")
    return scores, is_ood


def auroc(scores, is_ood) -> float:
    s, y = _check(scores, is_ood)
    return float(roc_auc_score(y, s))


def aupr(scores, is_ood) -> float:
    """Average precision with OOD as the positive class (AUPR-Out)."""
    s, y = _check(scores, is_ood)
    return float(average_precision_score(y, s))


def fpr_at_tpr(scores, is_ood, tpr_target: float = 0.95) -> float:
    """FPR on ID at the ROC point whose TPR (OOD recall) is closest to `tpr_target`."""
    s, y = _check(scores, is_ood)
    fpr, tpr, _ = roc_curve(y, s)
    idx = int(np.argmin(np.abs(tpr - tpr_target)))
    return float(fpr[idx])


def ood_metrics(scores, is_ood, as_percent: bool = True) -> dict:
    """Return {'auroc', 'aupr', 'fpr95'} (in percent by default)."""
    m = {"auroc": auroc(scores, is_ood), "aupr": aupr(scores, is_ood), "fpr95": fpr_at_tpr(scores, is_ood, 0.95)}
    if as_percent:
        m = {k: 100.0 * v for k, v in m.items()}
    return m


def bootstrap_ci(scores, is_ood, metric=auroc, n_boot: int = 1000, seed: int = 0, alpha: float = 0.05):
    """Percentile bootstrap CI of a metric (stratified over ID/OOD)."""
    s, y = _check(scores, is_ood)
    rng = np.random.default_rng(seed)
    id_idx, ood_idx = np.where(y == 0)[0], np.where(y == 1)[0]
    vals = []
    for _ in range(n_boot):
        bi = np.concatenate([rng.choice(id_idx, len(id_idx)), rng.choice(ood_idx, len(ood_idx))])
        vals.append(metric(s[bi], y[bi]))
    vals = np.sort(vals)
    return float(np.mean(vals)), float(vals[int(alpha / 2 * n_boot)]), float(vals[int((1 - alpha / 2) * n_boot) - 1])
