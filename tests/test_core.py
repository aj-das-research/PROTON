import numpy as np
import pytest

from proton.metrics import ood_metrics, auroc, fpr_at_tpr
from proton.online import PROTON, PROTONConfig, Welford, score_stream
from proton.scores.static import energy, entropy, gl_mcm, hierarchical_mcm, max_logit, mcm, softmax, tag_mcm
from proton.streams import make_stream


def test_metrics_perfect_and_random():
    s = np.array([0.1, 0.2, 0.3, 0.9, 0.8, 0.7]); y = np.array([0, 0, 0, 1, 1, 1])
    m = ood_metrics(s, y)
    assert m["auroc"] == 100 and m["aupr"] == 100 and m["fpr95"] == 0
    rng = np.random.default_rng(0)
    s = rng.random(2000); y = (rng.random(2000) < 0.5).astype(int)
    assert abs(auroc(s, y) - 0.5) < 0.05


def test_welford_matches_numpy():
    rng = np.random.default_rng(1); x = rng.normal(size=500)
    w = Welford()
    for v in x: w.update(float(v))
    assert np.isclose(w.mean, x.mean()) and np.isclose(w.variance, x.var(ddof=1))


def test_static_scores_direction():
    logits = np.array([[10.0, 0.0], [5.0, 4.9]])  # confident vs ambiguous
    for f in (mcm, max_logit, energy, entropy):
        s = f(logits); assert s[1] > s[0], f.__name__  # ambiguous sample is "more OOD"
    assert np.allclose(softmax(logits).sum(1), 1)
    loc = np.stack([logits[:, None, :]] * 3, 1)[:, :, 0, :]
    assert gl_mcm(logits, loc).shape == (2,)
    assert hierarchical_mcm([logits[:, :1], logits[:, 1:]]).shape == (2,)
    assert tag_mcm(np.stack([logits, logits], 1)).shape == (2,)


def _toy_stream(n_id=200, n_ood=100, d=16, seed=0):
    rng = np.random.default_rng(seed)
    T = rng.normal(size=(2, d)); T /= np.linalg.norm(T, axis=1, keepdims=True)
    y = rng.integers(0, 2, n_id)
    E_id = T[y] + 0.3 * rng.normal(size=(n_id, d))
    E_ood = 0.5 * (T[0] + T[1]) + 0.3 * rng.normal(size=(n_ood, d)) + 0.6 * rng.normal(size=d)  # covariate-like
    E = np.concatenate([E_id, E_ood]); E /= np.linalg.norm(E, axis=1, keepdims=True)
    order, is_ood = make_stream(n_id, n_ood, seed=seed)
    return E[order], T, is_ood


def test_proton_runs_and_falls_back_before_calibration():
    E, T, is_ood = _toy_stream()
    out = score_stream(E, T, logit_scale=20.0, k_min=5)
    assert out["score"].shape == (300,)
    assert not out["calibrated"][0] and out["calibrated"][-1]
    assert np.allclose(out["score"][~out["calibrated"]], out["s_base"][~out["calibrated"]])
    det = out["detector"]; assert all(0 < b <= 100 for b in det.bank_sizes())


def test_proton_bank_is_fifo_and_bounded():
    det = PROTON(2, M=3, gate=False, k_min=1)
    rng = np.random.default_rng(0)
    for _ in range(10):
        det.step(rng.normal(size=4), np.array([0.9, 0.1]), -0.9)
    assert det.bank_sizes() == [3, 0]
    mean = np.mean(np.stack(det.banks[0]), 0); mean /= np.linalg.norm(mean)
    assert np.allclose(det.prototypes[0], mean)


def test_alpha_bounds_and_direction():
    det = PROTON(2, alpha_min=0.3, alpha_max=0.7, sigma2_0=0.02)
    assert det.alpha(0.0) > det.alpha(0.1)
    assert 0.3 <= det.alpha(1.0) <= 0.7 and 0.3 <= det.alpha(0.0) <= 0.7


def test_streams_rho():
    order, is_ood = make_stream(300, 150, rho=0.9, seed=0)
    assert abs(1 - is_ood.mean() - 0.9) < 0.01 and len(order) == 333
    order, is_ood = make_stream(300, 150, rho=0.1, seed=0)
    assert abs(1 - is_ood.mean() - 0.1) < 0.02
    o1, _ = make_stream(300, 150, seed=3); o2, _ = make_stream(300, 150, seed=3)
    assert np.array_equal(o1, o2)


def test_domain_anchored_prototype_ignores_shifted_cluster():
    rng = np.random.default_rng(0); d = 32
    a = rng.normal(size=d); a /= np.linalg.norm(a)          # ID mode
    b = rng.normal(size=d); b /= np.linalg.norm(b)          # shifted cluster (nearly orthogonal)
    det = PROTON(2, proto_mode="domain", bandwidth=0.1, gate=False, k_min=1, M=100)
    for _ in range(60):
        e = a + 0.1 * rng.normal(size=d); det.step(e / np.linalg.norm(e), np.array([0.2, 0.8]), -0.8)
    for _ in range(40):
        e = b + 0.1 * rng.normal(size=d); det.step(e / np.linalg.norm(e), np.array([0.2, 0.8]), -0.8)
    assert det.prototypes[1] @ a > 0.95 and det.prototypes[1] @ b < 0.3   # prototype stays on the dominant ID mode
