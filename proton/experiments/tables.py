"""Reproduce every table of the paper from cached features. Each function returns plain dicts and writes
JSON + Markdown under outputs/results/<benchmark>/. Run everything with `proton run --benchmark ophthalmology`.
"""
from __future__ import annotations

import json
import os
import time

import numpy as np
import pandas as pd

from ..data import load_benchmark
from ..evaluate import (SHIFTS, Prepared, evaluate_base_over_streams, evaluate_privileged, evaluate_proton,
                        evaluate_static, prepare, run_proton_stream)
from ..features import extract_features
from ..metrics import ood_metrics
from ..online import PROTONConfig, proton_plus_config
from ..streams import make_stream

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
RES_DIR = os.path.join(ROOT, "outputs", "results")

STATIC_ORDER = ["max_logit", "energy", "gl_mcm", "mcm", "entropy", "tag_mcm", "hier_l1", "hier_l5"]
PRETTY = {"max_logit": "Max-Logits", "energy": "Energy", "gl_mcm": "GL-MCM", "mcm": "MCM", "entropy": "Entropy",
          "tag_mcm": "TAG-MCM", "hier_l1": "MCM (L=1)", "hier_l5": "MCM (L=5)", "hier_vanilla": "MCM (vanilla)",
          "knn_id": "kNN-ID", "mahalanobis_id": "Mahalanobis-ID", "proton": "PROTON"}


def _save(bench_name, name, obj, md=None):
    d = os.path.join(RES_DIR, bench_name)
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, f"{name}.json"), "w") as f:
        json.dump(obj, f, indent=1, default=float)
    if md is not None:
        with open(os.path.join(d, f"{name}.md"), "w") as f:
            f.write(md)
    return obj


def _fmt(m, keys=("auroc", "aupr", "fpr95")):
    return " | ".join(f"{m[k]:.1f}" for k in keys)


# ----------------------------------------------------------------------------------------------- Table 2
def table2_main(P: Prepared, n_perm: int = 5) -> dict:
    static = evaluate_static(P)
    pro = evaluate_proton(P, n_perm=n_perm)
    rows = []
    for name in STATIC_ORDER:
        if name in static:
            rows.append((PRETTY[name], static[name]))
    rows.append(("PROTON (ours)", pro))
    md = ["| Method | Sem AUC | Sem APR | Sem FPR | Cov AUC | Cov APR | Cov FPR | Far AUC | Far APR | Far FPR |",
          "|---|---|---|---|---|---|---|---|---|---|"]
    for name, r in rows:
        md.append(f"| {name} | " + " | ".join(_fmt(r[s]) for s in SHIFTS) + " |")
    delta = {s: {m: pro[s][m] - static["mcm"][s][m] for m in ("auroc", "aupr", "fpr95")} for s in SHIFTS}
    md.append("| Δ vs MCM | " + " | ".join(_fmt(delta[s]) for s in SHIFTS) + " |")
    md.append("")
    md.append("PROTON mean ± std over %d stream orders: " % n_perm + ", ".join(
        f"{s}: {pro[s]['auroc']:.1f}±{pro[s]['auroc_std']:.1f}" for s in SHIFTS))
    return _save(P.bench.name, "table2_main", {"static": static, "proton": pro, "delta_vs_mcm": delta}, "\n".join(md))


# ----------------------------------------------------------------------------------------------- Table 3
def table3_ablation(P: Prepared, n_perm: int = 5) -> dict:
    variants = {
        "MCM baseline": dict(use_proto=False),
        "+ Proto. (alpha=.5)": dict(adaptive=False, fixed_alpha=0.5, gate=False),
        "+ Adapt. fusion": dict(adaptive=True, gate=False),
        "+ Conf. gate (Full)": dict(adaptive=True, gate=True),
    }
    res = {k: evaluate_proton(P, n_perm=n_perm, **v) for k, v in variants.items()}
    md = ["| Variant | Cov | Sem | Far |", "|---|---|---|---|"]
    for k, r in res.items():
        md.append(f"| {k} | {r['covariate']['auroc']:.1f} | {r['semantic']['auroc']:.1f} | {r['far']['auroc']:.1f} |")
    gam = {g: evaluate_proton(P, shifts=("covariate",), n_perm=n_perm, gamma=g)["covariate"] for g in
           (0.5, 0.6, 0.7, 0.8, 0.9)}
    md += ["", "| gamma | AUC | APR | F95 |", "|---|---|---|---|"] + [f"| {g} | {_fmt(r)} |" for g, r in gam.items()]
    Ms = {M: evaluate_proton(P, shifts=("covariate",), n_perm=n_perm, M=M)["covariate"] for M in (10, 25, 50, 100, 200)}
    md += ["", "| M | AUC | APR | F95 |", "|---|---|---|---|"] + [f"| {M} | {_fmt(r)} |" for M, r in Ms.items()]
    return _save(P.bench.name, "table3_ablation", {"components": res, "gamma": gam, "M": Ms}, "\n".join(md))


# ----------------------------------------------------------------------------------------------- Table 1(a)
def table1a_rho(P: Prepared, n_perm: int = 5, rhos=(0.9, 0.7, 0.3, 0.1)) -> dict:
    res = {}
    for rho in rhos:
        res[str(rho)] = {"proton": evaluate_proton(P, n_perm=n_perm, rho=rho),
                         "mcm": evaluate_base_over_streams(P, "mcm", n_perm=n_perm, rho=rho)}
    md = ["| rho | Sem | Cov | Far | (MCM: Sem | Cov | Far) |", "|---|---|---|---|---|"]
    for rho, r in res.items():
        md.append(f"| {float(rho):.0%} | " + " | ".join(f"{r['proton'][s]['auroc']:.1f}" for s in SHIFTS) +
                  " | " + " | ".join(f"{r['mcm'][s]['auroc']:.1f}" for s in SHIFTS) + " |")
    return _save(P.bench.name, "table1a_rho", res, "\n".join(md))


# ----------------------------------------------------------------------------------------------- Table 4(a)
def table4a_base_scores(P: Prepared, n_perm: int = 5) -> dict:
    res = {}
    for b in ("max_logit", "energy", "gl_mcm", "mcm", "entropy", "tag_mcm"):
        if b not in P.base:
            continue
        base = evaluate_static(P, names=[b])[b]
        pro = evaluate_proton(P, n_perm=n_perm, base=b)
        res[b] = {"base": base, "proton": pro}
    md = ["| Base score | Base (Cov) | +PROTON (Cov) | Δ | Base (Sem) | +PROTON (Sem) | Base (Far) | +PROTON (Far) |",
          "|---|---|---|---|---|---|---|---|"]
    for b, r in res.items():
        c0, c1 = r["base"]["covariate"]["auroc"], r["proton"]["covariate"]["auroc"]
        md.append(f"| {PRETTY[b]} | {c0:.1f} | {c1:.1f} | {c1 - c0:+.1f} | {r['base']['semantic']['auroc']:.1f} | "
                  f"{r['proton']['semantic']['auroc']:.1f} | {r['base']['far']['auroc']:.1f} | {r['proton']['far']['auroc']:.1f} |")
    return _save(P.bench.name, "table4a_base_scores", res, "\n".join(md))


# ----------------------------------------------------------------------------------------------- Table 4(b)
def table4b_broader(P: Prepared, n_perm: int = 5) -> dict:
    res = {}
    st = evaluate_static(P)
    for n in ("tag_mcm", "hier_l5"):
        if n in st:
            res[n] = st[n]
    res.update(evaluate_privileged(P))
    res["proton"] = evaluate_proton(P, n_perm=n_perm)
    # Hier.MCM(L=5) + PROTON: hierarchical logits give both the base score and the gate probabilities
    if "hier_l5" in P.base:
        res["hier_l5+proton"] = evaluate_proton(P, n_perm=n_perm, base="hier_l5", probs=P.hier_probs["l5"])
    md = ["| Method | Cov AUC | Sem AUC | Far AUC |", "|---|---|---|---|"]
    for n, r in res.items():
        md.append(f"| {PRETTY.get(n, n)} | {r['covariate']['auroc']:.1f} | {r['semantic']['auroc']:.1f} | {r['far']['auroc']:.1f} |")
    return _save(P.bench.name, "table4b_broader", res, "\n".join(md))


# ----------------------------------------------------------------------------------------------- robustness extras
def robustness_extras(P: Prepared, n_perm: int = 5) -> dict:
    out = {}
    # sigma2_0 sweep (mean AUROC over shifts)
    out["sigma2_0"] = {}
    for s0 in (0.005, 0.01, 0.02, 0.04, 0.08):
        r = evaluate_proton(P, n_perm=n_perm, sigma2_0=s0)
        out["sigma2_0"][str(s0)] = {"mean_auroc": float(np.mean([r[s]["auroc"] for s in SHIFTS])), "per_shift": r}
    # forced misrouting: a fraction q of gated bank updates goes to a random wrong class
    out["misrouting"] = {}
    for q in (0.0, 0.1, 0.2, 0.3):
        vals = []
        pool, n_id = P.pool("covariate")
        for k in range(n_perm):
            order, is_ood = make_stream(n_id, len(pool) - n_id, seed=k)
            rng = np.random.default_rng(100 + k)
            probs = P.probs.copy()
            flip = rng.random(len(probs)) < q
            probs[flip] = probs[flip][:, ::-1]        # swap class probabilities -> wrong argmax, same confidence
            r = run_proton_stream(P, pool, order, probs=probs)
            vals.append(ood_metrics(r["score"], is_ood)["auroc"])
        out["misrouting"][str(q)] = {"auroc": float(np.mean(vals)), "std": float(np.std(vals))}
    # per-sample overhead (CPU, numpy)
    pool, n_id = P.pool("covariate")
    order, _ = make_stream(n_id, len(pool) - n_id, seed=0)
    t0 = time.perf_counter()
    r = run_proton_stream(P, pool, order)
    dt = (time.perf_counter() - t0) / len(order)
    d = P.embeds.shape[1]
    out["overhead"] = {"ms_per_sample": 1000 * dt,
                       "bank_mb": P.T.shape[0] * r["detector"].cfg.M * d * 4 / 1e6}
    # shift-type triage from (S_base, S_proto): 3-way macro-F1 with 5-fold CV logistic regression
    try:
        from sklearn.linear_model import LogisticRegression
        from sklearn.model_selection import cross_val_predict
        from sklearn.metrics import f1_score
        X, y = [], []
        for ci, sh in enumerate(SHIFTS):
            pool, n_id = P.pool(sh)
            order, is_ood = make_stream(n_id, len(pool) - n_id, seed=0)
            r = run_proton_stream(P, pool, order)
            m = (is_ood == 1) & r["calibrated"]
            X.append(np.stack([r["s_base"][m], r["s_proto"][m]], 1)); y.append(np.full(m.sum(), ci))
        X, y = np.concatenate(X), np.concatenate(y)
        pred = cross_val_predict(LogisticRegression(max_iter=1000, class_weight="balanced"), X, y, cv=5)
        out["triage_macro_f1"] = float(f1_score(y, pred, average="macro"))
    except Exception as e:  # pragma: no cover
        out["triage_macro_f1"] = f"failed: {e}"
    md = [f"sigma2_0 sweep mean AUROC: " + ", ".join(f"{k}: {v['mean_auroc']:.1f}" for k, v in out["sigma2_0"].items()),
          "misrouting (cov AUROC): " + ", ".join(f"{k}: {v['auroc']:.1f}" for k, v in out["misrouting"].items()),
          f"overhead: {out['overhead']['ms_per_sample']:.3f} ms/sample, bank {out['overhead']['bank_mb']:.2f} MB",
          f"triage macro-F1: {out['triage_macro_f1']}"]
    return _save(P.bench.name, "robustness_extras", out, "\n".join(md))


# ----------------------------------------------------------------------------------------------- Fig 3(b) grid
def gamma_M_grid(P: Prepared, n_perm: int = 3, gammas=(0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9),
                 Ms=(10, 25, 50, 75, 100, 150, 200, 500)) -> dict:
    mcm = evaluate_static(P, shifts=("covariate",), names=["mcm"])["mcm"]["covariate"]["auroc"]
    grid = np.zeros((len(gammas), len(Ms)))
    for i, g in enumerate(gammas):
        for j, M in enumerate(Ms):
            grid[i, j] = evaluate_proton(P, shifts=("covariate",), n_perm=n_perm, gamma=g, M=M)["covariate"]["auroc"] - mcm
    out = {"gammas": list(gammas), "Ms": list(Ms), "delta_auroc": grid.tolist(), "mcm_cov_auroc": mcm}
    df = pd.DataFrame(grid, index=[f"g={g}" for g in gammas], columns=[f"M={M}" for M in Ms]).round(1)
    return _save(P.bench.name, "fig3b_gamma_M", out, df.to_markdown())


# ----------------------------------------------------------------------------------------------- PROTON+
def table_proton_plus(P: Prepared, n_perm: int = 5, rhos=(0.9, 0.7, 0.5, 0.3, 0.1)) -> dict:
    """PROTON+ vs PROTON vs MCM: main shifts, component ablation, ID-fraction sweep and gamma sensitivity."""
    mcm = evaluate_static(P, names=["mcm"])["mcm"]
    variants = {
        "MCM": None,
        "PROTON (paper)": dict(),
        "+ z-scored fusion": dict(normalize="zscore"),
        "+ consistency admission": dict(normalize="zscore", admission="consistency"),
        "+ trimmed prototypes (PROTON+)": dict(normalize="zscore", admission="consistency", robust_proto=True),
        "consistency only": dict(admission="consistency"),
        "trimmed only": dict(robust_proto=True),
    }
    res = {}
    for k, v in variants.items():
        res[k] = mcm if v is None else evaluate_proton(P, n_perm=n_perm, **v)
    md = ["| Variant | Sem AUC | Cov AUC | Far AUC | Sem FPR | Cov FPR | Far FPR |", "|---|---|---|---|---|---|---|"]
    for k, r in res.items():
        md.append(f"| {k} | " + " | ".join(f"{r[s]['auroc']:.1f}" for s in SHIFTS) + " | " +
                  " | ".join(f"{r[s]['fpr95']:.1f}" for s in SHIFTS) + " |")
    plus = proton_plus_config()
    rho = {}
    for r_ in rhos:
        rho[str(r_)] = {"proton_plus": evaluate_proton(P, n_perm=n_perm, rho=r_, config=proton_plus_config()),
                        "proton": evaluate_proton(P, n_perm=n_perm, rho=r_),
                        "mcm": evaluate_base_over_streams(P, "mcm", n_perm=n_perm, rho=r_)}
    md += ["", "| rho | PROTON+ Sem/Cov/Far | PROTON Sem/Cov/Far | MCM Sem/Cov/Far |", "|---|---|---|---|"]
    for r_, r in rho.items():
        md.append(f"| {float(r_):.0%} | " + " / ".join(f"{r['proton_plus'][s]['auroc']:.1f}" for s in SHIFTS) + " | " +
                  " / ".join(f"{r['proton'][s]['auroc']:.1f}" for s in SHIFTS) + " | " +
                  " / ".join(f"{r['mcm'][s]['auroc']:.1f}" for s in SHIFTS) + " |")
    gam = {g: evaluate_proton(P, n_perm=n_perm, config=proton_plus_config(gamma=g)) for g in (0.5, 0.6, 0.7, 0.8, 0.9)}
    kap = {k: evaluate_proton(P, n_perm=n_perm, config=proton_plus_config(kappa=k)) for k in (1.0, 1.5, 2.0, 3.0, 4.0)}
    md += ["", "| gamma (PROTON+) | Sem | Cov | Far |", "|---|---|---|---|"] + \
          [f"| {g} | " + " | ".join(f"{r[s]['auroc']:.1f}" for s in SHIFTS) + " |" for g, r in gam.items()]
    md += ["", "| kappa (PROTON+) | Sem | Cov | Far |", "|---|---|---|---|"] + \
          [f"| {k} | " + " | ".join(f"{r[s]['auroc']:.1f}" for s in SHIFTS) + " |" for k, r in kap.items()]
    # PROTON+ on every base score
    bases = {}
    for b in ("max_logit", "energy", "gl_mcm", "mcm", "entropy", "tag_mcm"):
        if b in P.base:
            bases[b] = {"base": evaluate_static(P, names=[b])[b], "proton_plus": evaluate_proton(P, n_perm=n_perm, base=b, config=proton_plus_config())}
    md += ["", "| Base score | Base Sem/Cov/Far | +PROTON+ Sem/Cov/Far |", "|---|---|---|"]
    for b, r in bases.items():
        md.append(f"| {PRETTY[b]} | " + " / ".join(f"{r['base'][s]['auroc']:.1f}" for s in SHIFTS) + " | " +
                  " / ".join(f"{r['proton_plus'][s]['auroc']:.1f}" for s in SHIFTS) + " |")
    return _save(P.bench.name, "table_proton_plus", {"variants": res, "rho": rho, "gamma": gam, "kappa": kap, "bases": bases}, "\n".join(md))


# ----------------------------------------------------------------------------------------------- prompt sensitivity
def table_prompt_sensitivity(bench, feats, n_perm: int = 5) -> dict:
    """Every prompt set of the benchmark: zero-shot ID accuracy, MCM, PROTON and PROTON+ AUROC per shift."""
    res = {}
    for ps in bench.prompts:
        P = prepare(bench, feats, prompt_set=ps)
        i = P.idx("id")
        acc = float((P.probs[i].argmax(1) == P.labels[i]).mean())
        res[ps] = {"id_acc": acc, "mcm": evaluate_static(P, names=["mcm"])["mcm"],
                   "proton": evaluate_proton(P, n_perm=n_perm),
                   "proton_plus": evaluate_proton(P, n_perm=n_perm, config=proton_plus_config())}
    md = ["| Prompt set | ID acc | MCM Sem/Cov/Far | PROTON Sem/Cov/Far | PROTON+ Sem/Cov/Far |", "|---|---|---|---|---|"]
    for ps, r in res.items():
        md.append(f"| {ps}{' (default)' if ps == bench.default_prompts else ''} | {100 * r['id_acc']:.1f} | " +
                  " / ".join(f"{r['mcm'][s]['auroc']:.1f}" for s in SHIFTS) + " | " +
                  " / ".join(f"{r['proton'][s]['auroc']:.1f}" for s in SHIFTS) + " | " +
                  " / ".join(f"{r['proton_plus'][s]['auroc']:.1f}" for s in SHIFTS) + " |")
    return _save(bench.name, "table_prompt_sensitivity", res, "\n".join(md))


# ----------------------------------------------------------------------------------------------- driver
def run_benchmark(name: str, n_perm: int = 5, prompt_set: str | None = None, device=None, grid: bool = True) -> dict:
    bench = load_benchmark(name)
    feats = extract_features(bench, device=device)
    P = prepare(bench, feats, prompt_set=prompt_set)
    out = {"table2": table2_main(P, n_perm), "table3": table3_ablation(P, n_perm), "table1a": table1a_rho(P, n_perm),
           "table4a": table4a_base_scores(P, n_perm), "table4b": table4b_broader(P, n_perm),
           "extras": robustness_extras(P, n_perm), "proton_plus": table_proton_plus(P, n_perm),
           "prompts": table_prompt_sensitivity(bench, feats, n_perm)}
    if grid:
        out["fig3b"] = gamma_M_grid(P)
    return out
