"""PROTON: PROtotype-based Test-time ONline OOD detection (Algorithm 1 of the paper).

The detector is model-agnostic: it only needs, per test sample, an l2-normalised image embedding `e_t`, the
softmax probabilities `p_t` over the ID class prompts (for the confidence gate and the class assignment) and a
scalar base OOD score `s_base` (MCM by default, but any score from `proton.scores.static` works). It keeps

* an online prototype bank: one FIFO queue of at most M embeddings per class, filled with high-confidence
  predictions (max_c p_t >= gamma), prototype = l2-normalised mean of the queue;
* a prototype distance score  S_proto = 1 - max_c <e_t, mu_c>;
* an adaptive fusion weight   alpha_t = alpha_max - sigmoid(100 (var_t - var_0)) (alpha_max - alpha_min),
  where var_t is the running variance of the base score (Welford);
* a pure-base-score fallback until every class has at least K_min prototypes.

Ablation switches reproduce Table 3(a): `gate=False` (no confidence gate), `adaptive=False` with `fixed_alpha`
(constant fusion weight), `use_proto=False` (plain base score).
"""
from __future__ import annotations

from collections import deque
from dataclasses import dataclass

import numpy as np

from .scores.static import softmax


def _sigmoid(x: float) -> float:
    return float(1.0 / (1.0 + np.exp(-x)))


@dataclass
class Welford:
    """Exact single-pass running mean/variance (O(1) memory)."""
    n: int = 0
    mean: float = 0.0
    m2: float = 0.0

    def update(self, x: float) -> float:
        self.n += 1
        delta = x - self.mean
        self.mean += delta / self.n
        self.m2 += delta * (x - self.mean)
        return self.variance

    @property
    def variance(self) -> float:
        return self.m2 / (self.n - 1) if self.n > 1 else 0.0


@dataclass
class PROTONConfig:
    gamma: float = 0.7        # confidence gate
    M: int = 100              # per-class FIFO bank size
    k_min: int = 5            # min samples per class before calibration
    alpha_min: float = 0.3
    alpha_max: float = 0.7
    sigma2_0: float = 0.02    # reference base-score variance
    slope: float = 100.0      # sigmoid slope in Eq. (4)
    adaptive: bool = True     # variance-driven alpha (False -> fixed_alpha)
    fixed_alpha: float = 0.5
    gate: bool = True         # confidence gate on bank updates
    use_proto: bool = True    # False -> returns the base score (pure baseline)
    normalize: str = "none"   # "none" (paper) | "zscore" (online z-scoring of both signals; PROTON+ option)
    proto_metric: str = "cos"  # "cos" (paper) | "knn" (PROTON+ option: 1 - max sim to bank members)
    # ---- PROTON+ options (all off = the paper's algorithm) ----
    admission: str = "confidence"  # "confidence" (paper) | "consistency": also require the sample to lie within the
                                   # typical radius of its predicted-class prototype (mean + kappa*std of the
                                   # prototype distances of previously admitted samples)
    kappa: float = 2.0
    robust_proto: bool = False     # trimmed-mean prototype: drop the `trim` fraction of bank members farthest from
                                   # the plain mean before averaging (limits the pull of admitted outliers)
    trim: float = 0.2
    proto_mode: str = "mean"       # "mean" (paper) | "domain": domain-anchored prototypes. A mean-shift step over
                                   # ALL bank members (every class) finds the dominant imaging-domain mode mu_dom;
                                   # each class prototype is the mean of its members weighted by
                                   # exp((e·mu_dom - 1)/h), so a confidently-classified but covariate-shifted
                                   # cluster inside a class bank gets almost no weight.
    bandwidth: float = 0.1
    ms_iters: int = 3
    fusion: str = "sum"            # "sum": alpha*S_base + (1-alpha)*S_proto (paper) | "max": max of the two
                                   # online z-scores (parameter-free; implies normalize="zscore")
    alpha_mode: str = "variance"   # "variance": Eq. (4), driven by the running variance of the base score (paper)
                                   # | "rejection": driven by the running fraction of confident samples rejected by
                                   # the consistency admission (a direct, label-free symptom of domain shift)
    rej_ref: float = 0.1           # reference rejection rate (alpha = midpoint there)
    rej_slope: float = 20.0


def proton_plus_config(**overrides) -> PROTONConfig:
    """PROTON+ preset: domain-anchored prototypes + consistency admission + online z-scored fusion (paper
    hyper-parameters otherwise)."""
    cfg = PROTONConfig(proto_mode="domain", bandwidth=0.1, admission="consistency", kappa=2.0, normalize="zscore")
    for k, v in overrides.items():
        setattr(cfg, k, v)
    return cfg


class PROTON:
    """Online detector. Call `step` per sample (streaming) or `score_stream` for arrays."""

    def __init__(self, n_classes: int, config: PROTONConfig | None = None, **overrides):
        self.cfg = config or PROTONConfig()
        for k, v in overrides.items():
            if not hasattr(self.cfg, k):
                raise TypeError(f"unknown PROTON option {k!r}")
            setattr(self.cfg, k, v)
        self.C = int(n_classes)
        self.reset()

    # ------------------------------------------------------------------ state
    def reset(self):
        self.banks = [deque(maxlen=self.cfg.M) for _ in range(self.C)]
        self._sums = [None] * self.C           # running sums for O(1) prototype updates
        self.prototypes = [None] * self.C      # l2-normalised means
        self.welford = Welford()
        self._base_stats = Welford()
        self._proto_stats = Welford()
        self._adm_stats = Welford()            # prototype distances of admitted samples (consistency admission)
        self.mu_dom = None
        self._rej = Welford()                  # indicator of consistency-admission rejections (alpha_mode="rejection")
        self.t = 0
        self.history = []                      # per-step diagnostics (alpha, var, calibrated, ...)

    @property
    def calibrated(self) -> bool:
        return all(len(b) >= self.cfg.k_min for b in self.banks)

    def bank_sizes(self):
        return [len(b) for b in self.banks]

    def prototype_matrix(self):
        if any(p is None for p in self.prototypes):
            return None
        return np.stack(self.prototypes)

    # ------------------------------------------------------------------ core
    def _enqueue(self, c: int, e: np.ndarray):
        bank = self.banks[c]
        if self._sums[c] is None:
            self._sums[c] = np.zeros_like(e, dtype=np.float64)
        if len(bank) == bank.maxlen:               # evict oldest (FIFO)
            self._sums[c] -= bank[0]
        bank.append(e)
        self._sums[c] += e
        mean = self._sums[c] / len(bank)
        if self.cfg.robust_proto and len(bank) >= 3:
            B = np.stack(bank)
            d = 1.0 - B @ (mean / (np.linalg.norm(mean) + 1e-12))
            keep = d <= np.quantile(d, 1.0 - self.cfg.trim)
            mean = B[keep].mean(0)
        self.prototypes[c] = mean / (np.linalg.norm(mean) + 1e-12)
        if self.cfg.proto_mode == "domain":
            self._domain_anchored_prototypes()

    def _domain_anchored_prototypes(self):
        """Mean-shift on the union of all banks -> mu_dom; class prototypes = domain-weighted member means."""
        cfg = self.cfg
        members = [np.stack(b) for b in self.banks if len(b)]
        if not members:
            return
        A = np.concatenate(members)
        mu = A.mean(0); mu /= (np.linalg.norm(mu) + 1e-12)
        for _ in range(cfg.ms_iters):
            w = np.exp((A @ mu - 1.0) / cfg.bandwidth)
            mu = w @ A; mu /= (np.linalg.norm(mu) + 1e-12)
        self.mu_dom = mu
        for c, bank in enumerate(self.banks):
            if len(bank) == 0:
                continue
            B = np.stack(bank)
            w = np.exp((B @ mu - 1.0) / cfg.bandwidth)
            p = w @ B
            self.prototypes[c] = p / (np.linalg.norm(p) + 1e-12)

    def proto_score(self, e: np.ndarray) -> float:
        if self.cfg.proto_metric == "knn":
            best = -1.0
            for bank in self.banks:
                if len(bank):
                    best = max(best, float(np.max(np.stack(bank) @ e)))
            return 1.0 - best
        P = self.prototype_matrix()
        return float(1.0 - np.max(P @ e))

    def alpha(self, var_t: float) -> float:
        cfg = self.cfg
        if not cfg.adaptive:
            return cfg.fixed_alpha
        if cfg.alpha_mode == "rejection":
            rej = self._rej.mean if self._rej.n > 0 else 0.0
            return cfg.alpha_max - _sigmoid(cfg.rej_slope * (rej - cfg.rej_ref)) * (cfg.alpha_max - cfg.alpha_min)
        return cfg.alpha_max - _sigmoid(cfg.slope * (var_t - cfg.sigma2_0)) * (cfg.alpha_max - cfg.alpha_min)

    def step(self, e: np.ndarray, p: np.ndarray, s_base: float) -> dict:
        """Score one sample and then (maybe) update the bank. Returns a dict with the fused score and diagnostics."""
        cfg = self.cfg
        e = np.asarray(e, dtype=np.float64)
        p = np.asarray(p, dtype=np.float64)
        s_base = float(s_base)
        self.t += 1
        var_t = self.welford.update(s_base)
        calibrated = cfg.use_proto and self.calibrated
        if calibrated:
            s_proto = self.proto_score(e)
            a = self.alpha(var_t)
            if cfg.normalize == "zscore" or cfg.fusion == "max":
                self._base_stats.update(s_base)
                self._proto_stats.update(s_proto)
                zb = (s_base - self._base_stats.mean) / (np.sqrt(self._base_stats.variance) + 1e-6)
                zp = (s_proto - self._proto_stats.mean) / (np.sqrt(self._proto_stats.variance) + 1e-6)
                s = max(zb, zp) if cfg.fusion == "max" else a * zb + (1 - a) * zp
            else:
                s = a * s_base + (1 - a) * s_proto
        else:
            s_proto, a, s = float("nan"), 1.0, s_base
        # confidence-gated bank update (after scoring, Alg. 1 lines 11-12)
        conf = float(p.max())
        c_hat = int(p.argmax())
        updated = (not cfg.gate) or conf >= cfg.gamma
        if updated and cfg.admission == "consistency" and self.prototypes[c_hat] is not None and calibrated:
            d_hat = float(1.0 - e @ self.prototypes[c_hat])
            if self._adm_stats.n >= cfg.k_min:
                thr = self._adm_stats.mean + cfg.kappa * np.sqrt(self._adm_stats.variance)
                updated = d_hat <= thr
                self._rej.update(0.0 if updated else 1.0)
            if updated:
                self._adm_stats.update(d_hat)
        if cfg.use_proto and updated:
            self._enqueue(c_hat, e)
        rec = {"score": float(s), "s_base": s_base, "s_proto": s_proto, "alpha": a, "var": var_t,
               "calibrated": calibrated, "updated": updated, "pred": c_hat, "conf": conf}
        self.history.append(rec)
        return rec

    def score_stream(self, embeds: np.ndarray, probs: np.ndarray, base_scores: np.ndarray) -> dict:
        """Convenience wrapper: runs `step` over a whole stream in order. Returns dict of arrays."""
        self.reset()
        out = [self.step(e, p, s) for e, p, s in zip(embeds, probs, base_scores)]
        keys = out[0].keys()
        return {k: np.array([o[k] for o in out]) for k in keys}


def score_stream(embeds: np.ndarray, text_embeds: np.ndarray, logit_scale: float, base: str = "mcm",
                 config: PROTONConfig | None = None, base_scores: np.ndarray | None = None, **overrides) -> dict:
    """One-call PROTON: embeddings (N,d) + class text embeddings (C,d) + logit scale -> fused scores.

    `base_scores` lets you pass any precomputed base score (shape (N,), higher = more OOD); otherwise `base`
    is looked up in proton.scores.static.BASE_SCORES and computed from the logits.
    """
    from .scores.static import BASE_SCORES
    logits = logit_scale * (embeds @ text_embeds.T)
    probs = softmax(logits)
    if base_scores is None:
        base_scores = BASE_SCORES[base](logits)
    det = PROTON(text_embeds.shape[0], config, **overrides)
    out = det.score_stream(embeds, probs, base_scores)
    out["detector"] = det
    return out
