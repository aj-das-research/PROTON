"""Static (per-sample, stateless) zero-shot OOD scores for CLIP-like VLMs.

All functions take `logits` of shape (N, C): cosine similarities between the image embedding and the C
in-distribution class text embeddings, already multiplied by the VLM's logit scale (1/tau). They return a
1-D array where HIGHER = MORE OOD, so every score can be plugged into `proton.online.PROTON` as the base signal.
"""
from __future__ import annotations

import numpy as np
from scipy.special import logsumexp

_EPS = 1e-12


def softmax(logits: np.ndarray, axis: int = -1) -> np.ndarray:
    z = logits - logits.max(axis=axis, keepdims=True)
    e = np.exp(z)
    return e / e.sum(axis=axis, keepdims=True)


def mcm(logits: np.ndarray) -> np.ndarray:
    """Maximum Concept Matching (Ming et al., 2022): S = -max_c softmax(logits)_c."""
    return -softmax(logits).max(axis=-1)


def max_logit(logits: np.ndarray) -> np.ndarray:
    """S = -max_c logit_c (Hendrycks et al., 2022)."""
    return -logits.max(axis=-1)


def energy(logits: np.ndarray, T: float = 1.0) -> np.ndarray:
    """Energy score (Liu et al., 2020): S = -T * logsumexp(logits / T)."""
    return -T * logsumexp(logits / T, axis=-1)


def entropy(logits: np.ndarray) -> np.ndarray:
    """Predictive entropy of the softmax: higher entropy = more OOD."""
    p = softmax(logits)
    return -(p * np.log(p + _EPS)).sum(axis=-1)


def gl_mcm(global_logits: np.ndarray, local_logits: np.ndarray, lam: float = 1.0) -> np.ndarray:
    """GL-MCM (Miyai et al., 2025): S = -(max softmax(global) + lam * max over patches & classes softmax(local)).

    `local_logits` has shape (N, P, C): per-patch cosine similarities (times logit scale) to the class embeddings.
    The local softmax is over classes for each patch; the maximum over patches and classes is used.
    """
    g = softmax(global_logits).max(axis=-1)
    l = softmax(local_logits, axis=-1).max(axis=(-1, -2))
    return -(g + lam * l)


def hierarchical_mcm(level_logits: list[np.ndarray]) -> np.ndarray:
    """Hierarchical-prompt MCM of Ju et al. (2025): for each class c the logits of its prompt descriptions are averaged,
    then MCM is applied to the resulting (N, C) logits. `level_logits[c]` has shape (N, K_c)."""
    cls = np.stack([ll.mean(axis=-1) for ll in level_logits], axis=-1)
    return mcm(cls)


def tag_mcm(template_logits: np.ndarray) -> np.ndarray:
    """TAG-style text-prompt augmentation (Liu & Zach, 2024) with MCM read-out.

    `template_logits` has shape (N, K, C): logits of the image against the K augmented variants (TAG: random word
    shuffles of the prompt) of every class. TAG scores S = (1/K) sum_k max_c softmax(logits_k)_c, i.e. the mean
    over augmentations of the per-augmentation maximum softmax probability. Returned negated (higher = more OOD).
    """
    return -softmax(template_logits, axis=-1).max(axis=-1).mean(axis=1)


BASE_SCORES = {
    "mcm": mcm,
    "max_logit": max_logit,
    "energy": energy,
    "entropy": entropy,
}


def compute_base_score(name: str, logits: np.ndarray, **extra) -> np.ndarray:
    """Dispatch a base score by name. GL-MCM needs `local_logits`, TAG-MCM needs `template_logits`,
    hierarchical MCM needs `level_logits`."""
    if name in BASE_SCORES:
        return BASE_SCORES[name](logits)
    if name == "gl_mcm":
        return gl_mcm(logits, extra["local_logits"])
    if name == "tag_mcm":
        return tag_mcm(extra["template_logits"])
    if name.startswith("hier_mcm"):
        return hierarchical_mcm(extra["level_logits"])
    raise KeyError(f"unknown base score {name!r}; known: {sorted(BASE_SCORES) + ['gl_mcm', 'tag_mcm', 'hier_mcm']}")
