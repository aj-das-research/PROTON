"""Paper figures from cached features + the saved results (all matplotlib, vector PDF + PNG).

fig1  MCM blind spot: (a) ID/OOD MCM-score overlap per shift, (b) MCM vs prototype distance scatter,
      (c) t-SNE of embeddings; one row per benchmark.
fig3a prototype convergence (cosine to final prototype, drift, PCA trajectory).
fig3b gamma x M sensitivity heatmaps (delta AUROC over MCM, covariate shift).
"""
from __future__ import annotations

import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from ..data import load_benchmark
from ..evaluate import SHIFTS, prepare, run_proton_stream
from ..features import load_features
from ..streams import make_stream

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
FIG_DIR = os.path.join(ROOT, "outputs", "figures")
RES_DIR = os.path.join(ROOT, "outputs", "results")
COL = {"id0": "#1f77b4", "id1": "#2ca02c", "semantic": "#ff7f0e", "covariate": "#d62728", "far": "#7f7f7f"}
plt.rcParams.update({"font.size": 7, "axes.titlesize": 8, "axes.labelsize": 7, "legend.fontsize": 6,
                     "pdf.fonttype": 42, "ps.fonttype": 42})


def _save(fig, name):
    os.makedirs(FIG_DIR, exist_ok=True)
    fig.savefig(os.path.join(FIG_DIR, name + ".pdf"), bbox_inches="tight")
    fig.savefig(os.path.join(FIG_DIR, name + ".png"), bbox_inches="tight", dpi=200)
    plt.close(fig)


def overlap_fraction(s_id, s_ood):
    """Fraction of OOD scores falling inside the [5th, 95th] percentile range of ID scores."""
    lo, hi = np.percentile(s_id, 5), np.percentile(s_id, 95)
    return float(np.mean((s_ood >= lo) & (s_ood <= hi)))


def fig1_blind_spot(benchmarks=("ophthalmology", "radiology", "pathology")):
    rows = [b for b in benchmarks if os.path.exists(os.path.join(ROOT, "outputs", "features",
                                                                  f"{b}__{load_benchmark(b).vlm}.npz"))]
    fig, axes = plt.subplots(len(rows), 3, figsize=(7.2, 2.3 * len(rows)), squeeze=False, constrained_layout=True)
    stats = {}
    for r, bname in enumerate(rows):
        bench = load_benchmark(bname)
        P = prepare(bench, load_features(bname, bench.vlm))
        id_idx = P.idx("id")
        mcm = P.base["mcm"]
        # (a) overlap bars
        ax = axes[r, 0]
        ov = {sh: overlap_fraction(mcm[id_idx], mcm[P.idx(sh)]) for sh in SHIFTS}
        ax.bar([s[:3].title() + "." for s in SHIFTS], [100 * v for v in ov.values()], color=[COL[s] for s in SHIFTS])
        for i, v in enumerate(ov.values()):
            ax.text(i, 100 * v + 1, f"{100 * v:.0f}%", ha="center", fontsize=6)
        ax.set_ylim(0, 110); ax.set_ylabel("ID/OOD MCM overlap (%)")
        ax.set_title(f"({'abc'[0]}) MCM score overlap" if r == 0 else "")
        # (b) scatter MCM vs proto distance over the covariate stream (calibrated part)
        ax = axes[r, 1]
        pool, n_id = P.pool("covariate")
        order, is_ood = make_stream(n_id, len(pool) - n_id, seed=0)
        from ..online import proton_plus_config
        run = run_proton_stream(P, pool, order, config=proton_plus_config())
        m = run["calibrated"]
        ax.scatter(-run["s_base"][m & (is_ood == 0)], run["s_proto"][m & (is_ood == 0)], s=4, c=COL["id0"], label="ID", alpha=.6)
        ax.scatter(-run["s_base"][m & (is_ood == 1)], run["s_proto"][m & (is_ood == 1)], s=4, c=COL["covariate"], label="Covariate OOD", alpha=.6)
        thr = np.percentile(run["s_proto"][m & (is_ood == 0)], 95)
        caught = float(np.mean(run["s_proto"][m & (is_ood == 1)] > thr))
        ax.axhline(thr, ls="--", lw=.6, c="k")
        ax.text(0.02, 0.95, f"{100 * caught:.0f}% cov. caught\n(at 95% ID TNR on $S_{{proto}}$)", transform=ax.transAxes, va="top", fontsize=6)
        ax.set_xlabel("max softmax (MCM)"); ax.set_ylabel("$S_{proto}$ (PROTON+ bank)")
        ax.set_title("(b) MCM vs prototype dist." if r == 0 else "")
        if r == 0: ax.legend(loc="upper left", bbox_to_anchor=(0.0, 0.78), frameon=False)
        # (c) t-SNE
        ax = axes[r, 2]
        try:
            from sklearn.manifold import TSNE
            sel, lab = [], []
            for name, idx in [("id0", id_idx[P.labels[id_idx] == 0]), ("id1", id_idx[P.labels[id_idx] == 1]),
                              ("semantic", P.idx("semantic")), ("covariate", P.idx("covariate")), ("far", P.idx("far"))]:
                sel.append(idx); lab += [name] * len(idx)
            sel = np.concatenate(sel); lab = np.array(lab)
            Z = TSNE(n_components=2, init="pca", perplexity=30, random_state=0).fit_transform(P.embeds[sel])
            names = {"id0": f"ID: {bench.classes[0]}", "id1": f"ID: {bench.classes[1]}", "semantic": "Semantic OOD",
                     "covariate": "Covariate OOD", "far": "Far-OOD"}
            for name in ["id0", "id1", "semantic", "covariate", "far"]:
                mm = lab == name
                ax.scatter(Z[mm, 0], Z[mm, 1], s=3, c=COL[name], label=names[name], alpha=.7)
            ax.set_xticks([]); ax.set_yticks([])
            if r == 0: ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.02), ncol=3, markerscale=2, frameon=False, fontsize=5.5)
        except Exception as e:  # pragma: no cover
            ax.text(.5, .5, f"t-SNE failed: {e}", ha="center")
        ax.set_title("(c) t-SNE embeddings" if r == 0 else "")
        ax.text(1.02, 0.5, f"{bname.title()}\n({ {'flair': 'FLAIR', 'unimedclip': 'UniMed-CLIP', 'quiltnet': 'QuiltNet'}[bench.vlm] })", transform=ax.transAxes, rotation=270, va="center", fontsize=7)
        stats[bname] = {"overlap": ov, "cov_caught_at_95tnr": caught}
    _save(fig, "fig1_blind_spot")
    os.makedirs(RES_DIR, exist_ok=True)
    with open(os.path.join(RES_DIR, "fig1_stats.json"), "w") as f:
        json.dump(stats, f, indent=1)
    return stats


def fig3a_convergence(benchmarks=("ophthalmology", "radiology", "pathology")):
    rows = [b for b in benchmarks if os.path.exists(os.path.join(ROOT, "outputs", "features",
                                                                  f"{b}__{load_benchmark(b).vlm}.npz"))]
    fig, axes = plt.subplots(len(rows), 3, figsize=(7.2, 2.0 * len(rows)), squeeze=False, constrained_layout=True)
    stats = {}
    for r, bname in enumerate(rows):
        bench = load_benchmark(bname)
        P = prepare(bench, load_features(bname, bench.vlm))
        pool, n_id = P.pool("covariate")
        order, is_ood = make_stream(n_id, len(pool) - n_id, seed=0)
        # replay the stream while recording prototypes after every update
        from ..online import PROTON
        det = PROTON(P.T.shape[0])
        idx = pool[order]
        traj = {c: [] for c in range(P.T.shape[0])}
        tpos = {c: [] for c in range(P.T.shape[0])}
        kmin_t = None
        for t, i in enumerate(idx):
            det.step(P.embeds[i], P.probs[i], P.base["mcm"][i])
            if kmin_t is None and det.calibrated:
                kmin_t = t + 1
            for c in range(P.T.shape[0]):
                if det.prototypes[c] is not None and (not traj[c] or not np.array_equal(traj[c][-1], det.prototypes[c])):
                    traj[c].append(det.prototypes[c].copy()); tpos[c].append(t + 1)
        final = {c: traj[c][-1] for c in traj}
        ax = axes[r, 0]
        for c in traj:
            cs = [float(p @ final[c]) for p in traj[c]]
            ax.plot(tpos[c], cs, lw=1, label=bench.classes[c])
        if kmin_t: ax.axvline(kmin_t, ls="--", lw=.6, c="k"); ax.text(kmin_t, 0.93, f"$K_{{min}}$={kmin_t}", fontsize=6)
        ax.set_ylim(0.9, 1.001); ax.set_xlabel("Stream position t"); ax.set_ylabel(r"cos($\mu_t$, $\mu_T$)")
        if r == 0: ax.set_title("Convergence"); ax.legend()
        ax = axes[r, 1]
        for c in traj:
            d = [float(np.linalg.norm(traj[c][k] - traj[c][k - 1])) for k in range(1, len(traj[c]))]
            ax.plot(range(1, len(d) + 1), d, lw=1)
        ax.axhline(0.01, ls="--", lw=.6, c="k"); ax.set_xlabel("Update step"); ax.set_ylabel(r"$\|\Delta\mu_t\|$")
        if r == 0: ax.set_title("Drift rate")
        ax = axes[r, 2]
        from sklearn.decomposition import PCA
        allp = np.concatenate([np.stack(traj[c]) for c in traj])
        pca = PCA(2).fit(allp)
        for c in traj:
            Z = pca.transform(np.stack(traj[c]))
            ax.plot(Z[:, 0], Z[:, 1], lw=.8, alpha=.8); ax.scatter(Z[-1, 0], Z[-1, 1], marker="*", s=40, c="k", zorder=5)
        ax.set_xlabel("PC1"); ax.set_ylabel("PC2")
        if r == 0: ax.set_title("Prototype trajectory")
        ax.text(1.02, 0.5, bname.title(), transform=ax.transAxes, rotation=270, va="center", fontsize=7)
        n99 = {bench.classes[c]: next((tpos[c][k] for k in range(len(traj[c])) if traj[c][k] @ final[c] > 0.99), None) for c in traj}
        stats[bname] = {"kmin_reached_at": kmin_t, "cos_gt_0.99_at": n99}
    _save(fig, "fig3a_convergence")
    with open(os.path.join(RES_DIR, "fig3a_stats.json"), "w") as f:
        json.dump(stats, f, indent=1)
    return stats


def fig3b_grid(benchmarks=("ophthalmology", "radiology", "pathology")):
    rows = [(b, os.path.join(RES_DIR, b, "fig3b_gamma_M.json")) for b in benchmarks]
    rows = [(b, p) for b, p in rows if os.path.exists(p)]
    fig, axes = plt.subplots(1, len(rows), figsize=(2.6 * len(rows), 2.3), squeeze=False, constrained_layout=True)
    for ax, (b, p) in zip(axes[0], rows):
        d = json.load(open(p))
        g = np.array(d["delta_auroc"])
        v = np.abs(g).max()
        im = ax.imshow(g, cmap="RdBu_r", vmin=-v, vmax=v, aspect="auto")
        ax.set_xticks(range(len(d["Ms"]))); ax.set_xticklabels(d["Ms"], fontsize=6)
        ax.set_yticks(range(len(d["gammas"]))); ax.set_yticklabels(d["gammas"], fontsize=6)
        for i in range(g.shape[0]):
            for j in range(g.shape[1]):
                ax.text(j, i, f"{g[i, j]:+.0f}", ha="center", va="center", fontsize=5)
        gi = d["gammas"].index(0.7) if 0.7 in d["gammas"] else None
        mj = d["Ms"].index(100) if 100 in d["Ms"] else None
        if gi is not None and mj is not None:
            ax.scatter(mj, gi, marker="*", s=60, c="gold", edgecolor="k", lw=.4)
        ax.set_xlabel("M"); ax.set_ylabel(r"$\gamma$")
        ax.set_title(f"{b.title()} ({ {'flair': 'FLAIR', 'unimedclip': 'UniMed-CLIP', 'quiltnet': 'QuiltNet'}[load_benchmark(b).vlm] })")
        plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04).set_label(r"$\Delta$AUROC vs MCM", fontsize=6)
    _save(fig, "fig3b_gamma_M")


def make_all(benchmark=None):
    out = {"fig1": fig1_blind_spot(), "fig3a": fig3a_convergence()}
    fig3b_grid()
    return out
