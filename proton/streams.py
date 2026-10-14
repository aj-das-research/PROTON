"""Reproducible unlabelled test streams.

A stream is an ordered list of indices into the concatenation [ID pool (n_id) | OOD pool (n_ood)].
`make_stream` controls the ID fraction rho and the random order (seed).
"""
from __future__ import annotations

import numpy as np


def make_stream(n_id: int, n_ood: int, rho: float | None = None, seed: int = 0):
    """Return (order, is_ood). rho = desired ID fraction. If None, all ID and all OOD samples are used. Otherwise
    the OOD count is set to round(n_id (1-rho)/rho) when that many OOD samples exist, else the ID count is reduced
    to round(n_ood rho/(1-rho)); subsets are drawn uniformly at random with `seed`, then the stream is shuffled."""
    rng = np.random.default_rng(seed)
    id_idx = np.arange(n_id)
    ood_idx = n_id + np.arange(n_ood)
    if rho is not None:
        want_ood = int(round(n_id * (1 - rho) / rho))
        if want_ood <= n_ood:
            ood_idx = rng.choice(ood_idx, want_ood, replace=False)
        else:
            want_id = int(round(n_ood * rho / (1 - rho)))
            id_idx = rng.choice(id_idx, want_id, replace=False)
    order = np.concatenate([id_idx, ood_idx])
    rng.shuffle(order)
    is_ood = (order >= n_id).astype(int)
    return order, is_ood


def permutations(n_id: int, n_ood: int, n_perm: int = 5, seed0: int = 0, rho: float | None = None):
    """Yield (seed, order, is_ood) for `n_perm` stream orders."""
    for k in range(n_perm):
        order, is_ood = make_stream(n_id, n_ood, rho=rho, seed=seed0 + k)
        yield seed0 + k, order, is_ood
