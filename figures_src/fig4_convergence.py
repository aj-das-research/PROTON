"""Fig. 4 (output name fig3a_convergence), compact redesign in the shared paper style.

Replays the covariate stream (ID test images + shifted images, five stream orders = seeds 0-4) with
proton.online.PROTON (paper defaults) and with PROTON+ (proton.online.proton_plus_config), records every class
prototype right after each admission to its bank, and plots
(a) cosine of the PROTON prototype after k admissions to its final value, one hue per modality, solid = normal or
    benign class, dashed = disease class, mean over five stream orders, dashed reference at 0.99 and a marker where
    each modality stays above it;
(b) per-admission drift ||mu_k - mu_{k-1}|| of the PROTON prototypes on a log axis, reference at 0.01 and the bank
    size M = 100;
(c) cosine of the prototype of the most contaminated class bank (largest shifted share under PROTON) to the clean class
    mean (mean embedding of the held-out labelled ID split `id_bank`, never seen by the detectors), averaged over the
    admissions after the first ten and over the five orders, PROTON (circle) -> PROTON+ (star).
PROTON+ is left out of (a, b) on purpose: its domain-anchored prototype of the ophthalmology DR bank switches mean-shift
mode during the stream (single-update jumps up to 1.26 after 50 admissions), see the report in the stats json.
Level: full (recomputed from the cached features in outputs/features). Series cache and caption numbers:
outputs/results/fig4_convergence_series.pkl and outputs/results/fig4_convergence_stats.json.
Run: HF_HOME=/mnt/hdd2/Abhijit/.cache/huggingface /mnt/hdd2/Abhijit/envs/proton/bin/python figures_src/fig4_convergence.py
     (add --recompute to replay the streams again).
"""
import json
import os
import pickle
import sys

sys.path.insert(0, "/mnt/hdd2/Abhijit/projects/PROTON/figures_src")
sys.path.insert(0, "/mnt/hdd2/Abhijit/projects/PROTON")
from paper_style import *  # noqa: F401,F403  (rcParams, palette, encodings, save, preview)
from paper_style import ROOT, FULL_W, INK, MUTE, LINE, GRID, MOD_COL, C_PROTON, ACC, style_proton_plus, style_proton, save, preview

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from matplotlib.ticker import FuncFormatter, NullFormatter

R = os.path.join(ROOT, "outputs", "results")
CACHE = os.path.join(R, "fig4_convergence_series.pkl")
STATS = os.path.join(R, "fig4_convergence_stats.json")
MODS = ["ophthalmology", "radiology", "pathology"]
NAME = {"ophthalmology": "Ophthalmology", "radiology": "Radiology", "pathology": "Pathology"}
SEEDS = range(5)
THR_COS, THR_DRIFT, M_BANK = 0.99, 0.01, 100
ANN = 5.6  # annotation font size (pt)


# ---------------------------------------------------------------- data (full replay, cached)
def replay():
    from proton.data import load_benchmark
    from proton.evaluate import prepare
    from proton.features import load_features
    from proton.online import PROTON, proton_plus_config
    from proton.streams import make_stream
    out = {}
    for b in MODS:
        bench = load_benchmark(b)
        P = prepare(bench, load_features(b, bench.vlm))
        pool, n_id = P.pool("covariate")
        C = P.T.shape[0]
        bank = P.idx("id_bank")
        ref = np.stack([P.embeds[bank][P.labels[bank] == c].mean(0) for c in range(C)])
        ref /= np.linalg.norm(ref, axis=1, keepdims=True)
        out[b] = {"classes": list(bench.classes), "runs": {}}
        for meth in ("proton", "plus"):
            for seed in SEEDS:
                order, is_ood = make_stream(n_id, len(pool) - n_id, seed=seed)
                det = PROTON(C) if meth == "proton" else PROTON(C, proton_plus_config())
                protos, t_adm, ood = [[] for _ in range(C)], [[] for _ in range(C)], [[] for _ in range(C)]
                for t, i in enumerate(pool[order]):
                    r = det.step(P.embeds[i], P.probs[i], P.base["mcm"][i])
                    if r["updated"]:
                        c = r["pred"]
                        protos[c].append(det.prototypes[c].copy()); t_adm[c].append(t + 1); ood[c].append(int(is_ood[t]))
                run = {"t_calib": det.t_calib, "cls": []}
                for c in range(C):
                    Pk = np.stack(protos[c])
                    fin = det.prototypes[c]                      # prototype at the end of the stream
                    run["cls"].append({
                        "cos_final": Pk @ fin,                    # cos(mu_k, mu_final), k = 1..n_c admissions
                        "drift": np.linalg.norm(np.diff(Pk, axis=0), axis=1),   # ||mu_k - mu_{k-1}||, k = 2..n_c
                        "cos_ref": Pk @ ref[c],                   # cos(mu_k, clean class mean)
                        "cos_ref_final": float(fin @ ref[c]),
                        "t_adm": np.array(t_adm[c]), "ood": np.array(ood[c]),
                        "bank_ood_frac": float(np.mean(ood[c][-M_BANK:])),
                    })
                out[b]["runs"][(meth, seed)] = run
    return out


if "--recompute" in sys.argv or not os.path.exists(CACHE):
    data = replay()
    with open(CACHE, "wb") as f:
        pickle.dump(data, f)
else:
    with open(CACHE, "rb") as f:
        data = pickle.load(f)


def stack(b, meth, c, key):
    """(seeds, n) array of a per-admission series; NaN-padded to the longest run."""
    rows = [data[b]["runs"][(meth, s)]["cls"][c][key] for s in SEEDS]
    n = max(len(r) for r in rows)
    A = np.full((len(rows), n), np.nan)
    for i, r in enumerate(rows):
        A[i, :len(r)] = r
    return A


def settle(cs, thr=THR_COS):
    """First admission count k after which the series stays >= thr (1-based)."""
    bad = np.where(~(cs >= thr))[0]
    return int(bad[-1] + 2) if len(bad) else 1


# ---------------------------------------------------------------- numbers for the caption
stats = {}
for b in MODS:
    cl = data[b]["classes"]
    st = {"classes": cl}
    for meth in ("proton", "plus"):
        runs = [data[b]["runs"][(meth, s)] for s in SEEDS]
        d = {"admissions": [[len(r["cls"][c]["cos_final"]) for r in runs] for c in range(len(cl))],
             "settle_per_run": [[settle(r["cls"][c]["cos_final"]) for r in runs] for c in range(len(cl))],
             "settle_mean_curve": [settle(np.nanmean(stack(b, meth, c, "cos_final"), 0)) for c in range(len(cl))],
             "cos_ref_final_mean": [float(np.mean([r["cls"][c]["cos_ref_final"] for r in runs])) for c in range(len(cl))],
             "cos_ref_final_sd": [float(np.std([r["cls"][c]["cos_ref_final"] for r in runs])) for c in range(len(cl))],
             "bank_ood_frac": [float(np.mean([r["cls"][c]["bank_ood_frac"] for r in runs])) for c in range(len(cl))],
             "t_calib": [r["t_calib"] for r in runs]}
        dm = [np.nanmean(stack(b, meth, c, "drift"), 0) for c in range(len(cl))]
        d["drift_below_thr_at"] = [int(np.where(~(x < THR_DRIFT))[0][-1] + 3) if np.any(~(x < THR_DRIFT)) else 2 for x in dm]
        d["drift_median_after_M"] = [float(np.nanmedian(stack(b, meth, c, "drift")[:, M_BANK:])) if stack(b, meth, c, "drift").shape[1] > M_BANK else None for c in range(len(cl))]
        st[meth] = d
    st["worst_class"] = int(np.argmax(st["proton"]["bank_ood_frac"]))
    stats[b] = st
with open(STATS, "w") as f:
    json.dump(stats, f, indent=1)
for b in MODS:
    s = stats[b]
    print(b, s["classes"])
    for meth in ("proton", "plus"):
        d = s[meth]
        print(f"  {meth:6s} adm {d['admissions']}\n         settle/run {d['settle_per_run']} mean-curve {d['settle_mean_curve']}"
              f"\n         drift<0.01 from {d['drift_below_thr_at']} drift med after M {d['drift_median_after_M']}"
              f"\n         cos_ref_final {np.round(d['cos_ref_final_mean'], 3)} +- {np.round(d['cos_ref_final_sd'], 3)} bank_ood {np.round(d['bank_ood_frac'], 2)}")


# ---------------------------------------------------------------- display helpers
def log_binned(A, n_bins=36):
    """Geometric mean of a (seeds, n) positive series inside log-spaced admission bins (k = 2..n+1)."""
    k = np.arange(2, A.shape[1] + 2)
    edges = np.unique(np.round(np.geomspace(2, k[-1] + 1, n_bins)).astype(int))
    xs, ys = [], []
    for lo, hi in zip(edges[:-1], edges[1:]):
        sel = (k >= lo) & (k < hi)
        v = A[:, sel]
        v = v[np.isfinite(v) & (v > 0)]
        if v.size:
            xs.append(np.exp(np.mean(np.log(k[sel])))); ys.append(np.exp(np.mean(np.log(v))))
    return np.array(xs), np.array(ys)


CLS_LS = {0: "-", 1: (0, (2.6, 1.4))}       # solid = normal / benign class, dashed = disease class
K_WARM = 10                                 # (c) averages the prototype over admissions after the first ten
for b in MODS:                              # (c) numbers: most contaminated bank, mean over admissions > K_WARM
    c = stats[b]["worst_class"]
    for meth in ("proton", "plus"):
        v = [data[b]["runs"][(meth, s)]["cls"][c]["cos_ref"][K_WARM:].mean() for s in SEEDS]
        stats[b][meth]["cos_ref_stream_worst"] = [float(np.mean(v)), float(np.std(v))]
    print(f"(c) {b:13s} class {stats[b]['classes'][c]!r}: PROTON {stats[b]['proton']['cos_ref_stream_worst']}, "
          f"PROTON+ {stats[b]['plus']['cos_ref_stream_worst']}")
with open(STATS, "w") as f:
    json.dump(stats, f, indent=1)


def plain_log(ax, axis="x"):
    fmt = FuncFormatter(lambda v, _: f"{v:g}")
    (ax.xaxis if axis == "x" else ax.yaxis).set_major_formatter(fmt)
    (ax.xaxis if axis == "x" else ax.yaxis).set_minor_formatter(NullFormatter())


# ---------------------------------------------------------------- layout (inches)
W, H = FULL_W, 1.74
L, GAP, RM = 0.37, 0.44, 0.04
BOT, PH = 0.30, 1.10
PW = (W - L - 2 * GAP - RM) / 3
fig = plt.figure(figsize=(W, H))
x0 = [L + i * (PW + GAP) for i in range(3)]
ax_a, ax_b, ax_c = [fig.add_axes([x / W, BOT / H, PW / W, PH / H]) for x in x0]

# ---------------------------------------------------------------- (a) cosine to the final prototype (PROTON)
ax = ax_a
ax.axhline(THR_COS, color=INK, lw=0.6, ls=(0, (3, 2)), zorder=1)
ax.text(430, THR_COS - 0.004, "0.99", fontsize=ANN, color=MUTE, ha="right", va="top")
for b in MODS:
    col = MOD_COL[b]
    for c in (0, 1):
        A = stack(b, "proton", c, "cos_final")
        ax.plot(np.arange(1, A.shape[1] + 1), np.nanmean(A, 0), color=col, lw=0.9, ls=CLS_LS[c], zorder=3)
    ks = max(stats[b]["proton"]["settle_mean_curve"])
    ax.plot([ks], [THR_COS], marker="o", ms=3.4, color=col, mec="white", mew=0.5, zorder=5)
    ax.text(ks, 1.0035, f"{ks}", color=col, fontsize=ANN, ha="center", va="bottom", zorder=6)
ax.set_xscale("log"); ax.set_xlim(1, 450); ax.set_ylim(0.85, 1.016)
ax.set_yticks([0.85, 0.90, 0.95, 1.00]); plain_log(ax, "x")
ax.set_xlabel("Bank admissions (log)"); ax.set_ylabel("Cosine to final value")
ax.set_title("(a) PROTON convergence")

# ---------------------------------------------------------------- (b) drift per update (PROTON)
ax = ax_b
ax.axhline(THR_DRIFT, color=INK, lw=0.6, ls=(0, (3, 2)), zorder=1)
ax.axvline(M_BANK, color=LINE, lw=0.6, ls=(0, (1, 1.5)), zorder=1)
ax.text(M_BANK * 1.12, 0.55, "bank full", fontsize=ANN, color=MUTE, ha="left", va="center")
for b in MODS:
    col = MOD_COL[b]
    for c in (0, 1):
        xs, ys = log_binned(stack(b, "proton", c, "drift"))
        ax.plot(xs, ys, color=col, lw=0.9, ls=CLS_LS[c], zorder=3)
ax.set_xscale("log"); ax.set_yscale("log"); ax.set_xlim(1, 450); ax.set_ylim(0.003, 1)
plain_log(ax, "x"); plain_log(ax, "y")
ax.set_xlabel("Bank admissions (log)"); ax.set_ylabel("Prototype change (log)")
ax.set_title("(b) PROTON drift")

# ---------------------------------------------------------------- (c) most contaminated bank vs clean class mean
ax = ax_c
DX = 0.16
for i, b in enumerate(MODS):
    col = MOD_COL[b]
    p = stats[b]["proton"]["cos_ref_stream_worst"][0]; q = stats[b]["plus"]["cos_ref_stream_worst"][0]
    xp, xq = i - DX, i + DX                 # PROTON left, PROTON+ right (as in the slope chart of Fig. 3c)
    ax.plot([xp, xq], [p, q], color=col, lw=1.2, zorder=2)
    ax.plot([xp], [p], **{**style_proton(), "ms": 3.8})
    ax.plot([xq], [q], **{**style_proton_plus(), "ms": 6.5, "lw": 0})
    for x, v, is_plus in ((xp, p, False), (xq, q, True)):
        top = v >= (q if not is_plus else p)
        ax.text(x, v + (0.028 if top else -0.028), f"{v:.2f}", fontsize=ANN, ha="center", va="bottom" if top else "top",
                color=ACC if is_plus else C_PROTON)
ax.set_xlim(-0.55, 2.55); ax.set_xticks(range(3)); ax.set_xticklabels(["Ophth.", "Radio.", "Patho."])
for t, b in zip(ax.get_xticklabels(), MODS):
    t.set_color(MOD_COL[b])
ax.set_ylim(0.45, 1.06); ax.set_yticks([0.5, 0.75, 1.0])
ax.set_ylabel("Cosine to clean mean ↑")
ax.set_title("(c) contaminated bank")

for ax in (ax_a, ax_b):
    ax.tick_params(axis="both", which="minor", size=1.2, width=0.4, color=LINE)

# ---------------------------------------------------------------- shared legend
h = [Line2D([], [], color=MOD_COL[b], lw=1.2) for b in MODS] + \
    [Line2D([], [], color=MUTE, lw=0.9, ls=CLS_LS[0]), Line2D([], [], color=MUTE, lw=0.9, ls=CLS_LS[1]),
     Line2D([], [], ls="none", **{**style_proton(), "ms": 3.8}), Line2D([], [], ls="none", **{**style_proton_plus(), "ms": 6.5})]
lab = [NAME[b] for b in MODS] + ["normal/benign", "disease", "PROTON", "PROTON+ (ours)"]
fig.legend(h, lab, loc="upper center", bbox_to_anchor=(0.5, 1.0), ncol=len(h), handlelength=1.5, columnspacing=0.9,
           handletextpad=0.4, borderaxespad=0.0)

save(fig, "fig3a_convergence")
p, size = preview("fig3a_convergence")
print("preview", p, size)
