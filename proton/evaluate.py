"""Glue between cached features and detectors: builds logits/probabilities for a prompt set, computes every
static baseline, runs PROTON over reproducible streams and returns metrics per shift type.

Typical use:
    bench = load_benchmark("ophthalmology"); feats = extract_features(bench)
    prep  = prepare(bench, feats)                      # logits, probs, base scores for the default prompts
    res   = evaluate_proton(prep, shifts=("semantic","covariate","far"), n_perm=5)
"""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from .data import Benchmark
from .features import class_text_embeds, level_logits
from .metrics import ood_metrics
from .online import PROTON, PROTONConfig
from .scores.feature_bank import knn_id_score, mahalanobis_id_score
from .scores.static import energy, entropy, gl_mcm, hierarchical_mcm, max_logit, mcm, softmax, tag_mcm
from .streams import make_stream

SHIFTS = ("semantic", "covariate", "far")


@dataclass
class Prepared:
    bench: Benchmark
    feats: dict
    prompt_set: str
    T: np.ndarray                       # (C,d) class text embeddings
    logits: np.ndarray                  # (N,C)
    probs: np.ndarray                   # (N,C)
    sets: np.ndarray                    # (N,) set name per manifest row
    labels: np.ndarray                  # (N,) class index (ID) or -1
    base: dict = field(default_factory=dict)   # name -> (N,) static score (higher = more OOD)
    hier_probs: dict = field(default_factory=dict)  # prompt_set -> (N,C) probs from averaged logits

    @property
    def embeds(self):
        return self.feats["embeds"]

    def idx(self, set_name):
        return np.where(self.sets == set_name)[0]

    def pool(self, shift):
        """Indices of [ID test set | OOD(shift)] in that order, plus n_id."""
        id_idx, ood_idx = self.idx("id"), self.idx(shift)
        return np.concatenate([id_idx, ood_idx]), len(id_idx)


def prepare(bench: Benchmark, feats: dict, prompt_set: str | None = None, with_baselines: bool = True) -> Prepared:
    prompt_set = prompt_set or bench.default_prompts
    s = feats["logit_scale"]
    E = feats["embeds"]
    T = class_text_embeds(feats, prompt_set)
    logits = s * E @ T.T
    sets = bench.manifest["set"].to_numpy()
    labels = bench.manifest["label"].to_numpy()
    P = Prepared(bench, feats, prompt_set, T, logits, softmax(logits), sets, labels)
    if with_baselines:
        P.base["mcm"] = mcm(logits)
        P.base["max_logit"] = max_logit(logits)
        P.base["energy"] = energy(logits)
        P.base["entropy"] = entropy(logits)
        if "local" in feats:
            local_logits = s * np.einsum("npd,cd->npc", feats["local"], T)
            P.base["gl_mcm"] = gl_mcm(logits, local_logits)
        if "tag" in feats:
            tag_logits = s * np.einsum("nd,ctd->ntc", E, feats["tag"])
            P.base["tag_mcm"] = tag_mcm(tag_logits)
        for ps in bench.prompts:
            ll = level_logits(feats, ps)
            P.base[f"hier_{ps}"] = hierarchical_mcm(ll)
            P.hier_probs[ps] = softmax(np.stack([x.mean(-1) for x in ll], -1))
    return P


# ----------------------------------------------------------------------------------------------- static evaluation
def evaluate_static(P: Prepared, shifts=SHIFTS, names=None) -> dict:
    """{score_name: {shift: metrics}} for stateless scores (order-independent)."""
    names = names or list(P.base)
    out = {}
    for name in names:
        out[name] = {}
        for sh in shifts:
            pool, n_id = P.pool(sh)
            is_ood = (np.arange(len(pool)) >= n_id).astype(int)
            out[name][sh] = ood_metrics(P.base[name][pool], is_ood)
    return out


def evaluate_privileged(P: Prepared, shifts=SHIFTS, k: int = 10) -> dict:
    """kNN-ID and Mahalanobis-ID using the labelled, disjoint `id_bank` split."""
    bank = P.idx("id_bank")
    if len(bank) == 0:
        return {}
    Eb, yb = P.embeds[bank], P.labels[bank]
    out = {"knn_id": {}, "mahalanobis_id": {}}
    for sh in shifts:
        pool, n_id = P.pool(sh)
        is_ood = (np.arange(len(pool)) >= n_id).astype(int)
        out["knn_id"][sh] = ood_metrics(knn_id_score(P.embeds[pool], Eb, k=k), is_ood)
        out["mahalanobis_id"][sh] = ood_metrics(mahalanobis_id_score(P.embeds[pool], Eb, yb), is_ood)
    return out


# ----------------------------------------------------------------------------------------------- PROTON
def run_proton_stream(P: Prepared, pool: np.ndarray, order: np.ndarray, base: str = "mcm",
                      config: PROTONConfig | None = None, probs: np.ndarray | None = None, **overrides) -> dict:
    """Run PROTON over pool[order]; returns dict of per-step arrays in stream order plus the detector."""
    idx = pool[order]
    probs = P.probs if probs is None else probs
    det = PROTON(P.T.shape[0], config, **overrides)
    out = det.score_stream(P.embeds[idx], probs[idx], P.base[base][idx])
    out["detector"] = det
    out["idx"] = idx
    return out


def evaluate_proton(P: Prepared, shifts=SHIFTS, n_perm: int = 5, seed0: int = 0, base: str = "mcm",
                    config: PROTONConfig | None = None, rho: float | None = None, probs=None, **overrides) -> dict:
    """{shift: {'auroc': mean, 'auroc_std': std, 'aupr':..., 'fpr95':..., 'per_seed': [...]}}"""
    out = {}
    for sh in shifts:
        pool, n_id = P.pool(sh)
        n_ood = len(pool) - n_id
        runs = []
        for k in range(n_perm):
            order, is_ood = make_stream(n_id, n_ood, rho=rho, seed=seed0 + k)
            r = run_proton_stream(P, pool, order, base=base, config=config, probs=probs, **overrides)
            runs.append(ood_metrics(r["score"], is_ood))
        agg = {}
        for m in ("auroc", "aupr", "fpr95"):
            v = np.array([r[m] for r in runs])
            agg[m], agg[m + "_std"] = float(v.mean()), float(v.std())
        agg["per_seed"] = runs
        out[sh] = agg
    return out


def evaluate_base_over_streams(P: Prepared, base: str, shifts=SHIFTS, n_perm: int = 5, seed0: int = 0,
                               rho: float | None = None) -> dict:
    """Static score evaluated on exactly the same (sub-sampled) streams as PROTON (needed when rho != None)."""
    out = {}
    for sh in shifts:
        pool, n_id = P.pool(sh)
        n_ood = len(pool) - n_id
        runs = []
        for k in range(n_perm):
            order, is_ood = make_stream(n_id, n_ood, rho=rho, seed=seed0 + k)
            runs.append(ood_metrics(P.base[base][pool[order]], is_ood))
        agg = {m: float(np.mean([r[m] for r in runs])) for m in ("auroc", "aupr", "fpr95")}
        agg.update({m + "_std": float(np.std([r[m] for r in runs])) for m in ("auroc", "aupr", "fpr95")})
        out[sh] = agg
    return out
