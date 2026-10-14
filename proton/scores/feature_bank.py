"""Privileged feature-bank detectors that consume LABELLED in-distribution image features (used only as an upper
bound in Table 4(b) of the paper; PROTON itself never sees these)."""
from __future__ import annotations

import numpy as np


def _l2n(x):
    return x / (np.linalg.norm(x, axis=-1, keepdims=True) + 1e-12)


def knn_id_score(test_feats: np.ndarray, id_feats: np.ndarray, k: int = 10) -> np.ndarray:
    """kNN distance (Sun et al., 2022): negative cosine similarity to the k-th nearest labelled ID feature."""
    t, b = _l2n(test_feats), _l2n(id_feats)
    sims = t @ b.T
    k = min(k, b.shape[0])
    kth = -np.partition(-sims, k - 1, axis=1)[:, k - 1]
    return -kth


def mahalanobis_id_score(test_feats: np.ndarray, id_feats: np.ndarray, id_labels: np.ndarray, shrink: float = 1e-3):
    """Class-conditional Mahalanobis distance with a shared (shrunk) covariance (Lee et al., 2018). Higher = more OOD."""
    t, b = _l2n(test_feats), _l2n(id_feats)
    classes = np.unique(id_labels)
    mus = np.stack([b[id_labels == c].mean(0) for c in classes])
    centered = np.concatenate([b[id_labels == c] - mus[i] for i, c in enumerate(classes)])
    cov = centered.T @ centered / max(len(centered) - 1, 1)
    cov += shrink * np.trace(cov) / cov.shape[0] * np.eye(cov.shape[0])
    prec = np.linalg.pinv(cov)
    d = []
    for mu in mus:
        diff = t - mu
        d.append(np.einsum("nd,de,ne->n", diff, prec, diff))
    return np.min(np.stack(d, axis=1), axis=1)
