"""Embedding-vs-softmax figure (paper Fig. 2, file name fig1_blind_spot), house style of paper_style.py.

(a) share of OOD MCM scores inside the 5th-95th percentile range of the ID scores, all modalities in one chart
    (dotted line: the same share for the ID scores themselves, 90% by construction);
(b) MCM confidence against the PROTON+ prototype distance S_proto on the covariate stream (seed-0 order, samples after
    calibration), dashed line = 95th percentile of the ID S_proto, grey band = ID 5th-95th percentile of MCM confidence;
(c) t-SNE of the image embeddings (perplexity 30, PCA init, random_state 0), fitted on every sample.
Columns of (b) and (c): ophthalmology (FLAIR), radiology (UniMed-CLIP), pathology (QuiltNet).
The data pipeline is that of proton.experiments.figures.fig1_blind_spot. Every number comes from the cached features.

Run:  HF_HOME=... /mnt/hdd2/Abhijit/envs/proton/bin/python figures_src/fig2_embedding.py
Set FIG_CACHE=<file.pkl> to reuse the computed data between renders (layout iteration only).
"""
import json, os, pickle, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paper_style import *  # noqa: F401,F403  (rcParams, palette, save, preview)
from paper_style import ROOT, FULL_W, INK, MUTE, LINE, GRID, C_NORMAL, C_DR, C_UWF, C_SEM, C_FAR, save, preview
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

sys.path.insert(0, ROOT)
MODS = [("ophthalmology", "Ophthalmology", "Ophth."), ("radiology", "Radiology", "Radio."), ("pathology", "Pathology", "Patho.")]
SHIFTS = ("semantic", "covariate", "far")
COL = {"id0": C_NORMAL, "id1": C_DR, "semantic": C_SEM, "covariate": C_UWF, "far": C_FAR}


def overlap_fraction(s_id, s_ood):
    """Fraction of OOD scores inside the [5th, 95th] percentile range of the ID scores (as in figures.py)."""
    lo, hi = np.percentile(s_id, 5), np.percentile(s_id, 95)
    return float(np.mean((s_ood >= lo) & (s_ood <= hi)))


def compute():
    from proton.data import load_benchmark
    from proton.features import load_features
    from proton.evaluate import prepare, run_proton_stream
    from proton.streams import make_stream
    from proton.online import proton_plus_config
    from sklearn.manifold import TSNE
    D = {}
    for bname, _, _ in MODS:
        bench = load_benchmark(bname)
        P = prepare(bench, load_features(bname, bench.vlm))
        id_idx, mcm = P.idx("id"), P.base["mcm"]
        d = {"vlm": bench.vlm, "classes": list(bench.classes)}
        d["overlap"] = {sh: overlap_fraction(mcm[id_idx], mcm[P.idx(sh)]) for sh in SHIFTS}
        d["overlap_id_self"] = overlap_fraction(mcm[id_idx], mcm[id_idx])
        d["mcm_conf_id_range"] = (float(np.percentile(-mcm[id_idx], 5)), float(np.percentile(-mcm[id_idx], 95)))
        # (b) covariate stream, seed-0 order, PROTON+ (identical to fig1_blind_spot)
        pool, n_id = P.pool("covariate")
        order, is_ood = make_stream(n_id, len(pool) - n_id, seed=0)
        run = run_proton_stream(P, pool, order, config=proton_plus_config())
        m = run["calibrated"]
        cls = P.labels[run["idx"]]
        d["sc_conf"], d["sc_sproto"] = -run["s_base"][m], run["s_proto"][m]
        d["sc_ood"], d["sc_cls"] = is_ood[m].astype(int), cls[m]
        thr = float(np.percentile(d["sc_sproto"][d["sc_ood"] == 0], 95))
        d["thr"] = thr
        d["caught"] = float(np.mean(d["sc_sproto"][d["sc_ood"] == 1] > thr))
        d["n_cov_calibrated"] = int((d["sc_ood"] == 1).sum()); d["n_id_calibrated"] = int((d["sc_ood"] == 0).sum())
        # (c) t-SNE over ID (two classes) + the three OOD sets (identical to fig1_blind_spot)
        sel, lab = [], []
        for name, idx in [("id0", id_idx[P.labels[id_idx] == 0]), ("id1", id_idx[P.labels[id_idx] == 1]),
                          ("semantic", P.idx("semantic")), ("covariate", P.idx("covariate")), ("far", P.idx("far"))]:
            sel.append(idx); lab += [name] * len(idx)
        sel = np.concatenate(sel)
        d["tsne"] = TSNE(n_components=2, init="pca", perplexity=30, random_state=0).fit_transform(P.embeds[sel])
        d["tsne_lab"] = np.array(lab)
        D[bname] = d
    return D


def load_data():
    cache = os.environ.get("FIG_CACHE")
    if cache and os.path.exists(cache):
        return pickle.load(open(cache, "rb"))
    D = compute()
    if cache:
        pickle.dump(D, open(cache, "wb"))
    return D


# ----------------------------------------------------------------------------------------------- layout (inches)
W, H = FULL_W, 2.40
X0, AW = 0.29, 0.80              # (a) column: left edge and width of the axes
XS, SG = 1.52, 0.26              # small multiples: first left edge, gap (room for y tick labels)
SW = (W - 0.03 - XS - 2 * SG) / 3
Y_B, HB = 1.30, 0.80             # row (b): bottom, height
Y_C, HC = 0.00, 0.82             # row (c): bottom, height
Y_TB = Y_B + HB + 0.165          # baseline of the (a)/(b) titles
Y_TC = Y_C + HC + 0.055          # baseline of the (c) title
TITLE = dict(fontsize=7, fontweight="semibold", ha="left", va="bottom", color=INK)


def axes_in(fig, x, y, w, h):
    return fig.add_axes([x / W, y / H, w / W, h / H])


def render(D):
    fig = plt.figure(figsize=(W, H))
    ms_pts = 1.6                      # scatter marker area (pt^2)
    fmt = plt.FuncFormatter(lambda v, _: f"{v:g}")

    # (a) overlap chart, all modalities ---------------------------------------------------------------------------
    ax = axes_in(fig, X0, Y_B, AW, HB)
    bh, step, gap = 0.58, 0.80, 0.50
    yt, y = [], 0.0
    for bname, _, short in MODS:
        ys = []
        for sh in SHIFTS:
            v = 100 * D[bname]["overlap"][sh]
            ax.barh(y, v, height=bh, color=COL[sh], lw=0)
            ax.text(116, y, f"{v:.0f}", va="center", ha="right", fontsize=5.8, color=INK)
            ys.append(y); y += step
        yt.append(np.mean(ys)); y += gap
    selfov = 100 * np.mean([D[b]["overlap_id_self"] for b, _, _ in MODS])
    ax.axvline(selfov, color=INK, lw=0.6, ls=(0, (1, 1.2)), zorder=5)
    ax.text(selfov, 1.0, "ID", transform=ax.get_xaxis_transform(), ha="center", va="bottom", fontsize=5.8, color=INK)
    ax.set_ylim(y - gap - step + 0.5, -0.5)
    ax.set_yticks(yt); ax.set_yticklabels([s for _, _, s in MODS]); ax.tick_params(axis="y", length=0, pad=2)
    ax.set_xlim(0, 116); ax.set_xticks([0, 50, 100]); ax.spines["bottom"].set_bounds(0, 100)
    ax.spines["left"].set_visible(False)
    ax.grid(False)
    ax.set_xlabel(r"OOD in ID range (%) $\downarrow$", labelpad=2)
    fig.text(0.01 / W, Y_TB / H, "(a) MCM score overlap", **TITLE)

    # (b) scatter per modality -------------------------------------------------------------------------------------
    for j, (bname, full, _) in enumerate(MODS):
        d = D[bname]
        ax = axes_in(fig, XS + j * (SW + SG), Y_B, SW, HB)
        lo, hi = d["mcm_conf_id_range"]
        ax.axvspan(lo, hi, color=GRID, lw=0, zorder=0)
        for k, c in ((0, "id0"), (1, "id1")):
            mm = (d["sc_ood"] == 0) & (d["sc_cls"] == k)
            ax.scatter(d["sc_conf"][mm], d["sc_sproto"][mm], s=ms_pts, c=COL[c], lw=0, alpha=0.6, rasterized=True, zorder=2)
        mm = d["sc_ood"] == 1
        ax.scatter(d["sc_conf"][mm], d["sc_sproto"][mm], s=ms_pts, c=COL["covariate"], lw=0, alpha=0.8, rasterized=True, zorder=3)
        ax.axhline(d["thr"], color=INK, lw=0.6, ls=(0, (3, 2)), zorder=4)
        ax.set_ylim(0, float(d["sc_sproto"].max()) * 1.28)
        ax.set_xlim(0.48, 1.02); ax.set_xticks([0.5, 0.75, 1.0]); ax.set_xticklabels(["0.5", "0.75", "1"])
        ax.yaxis.set_major_locator(plt.MaxNLocator(3)); ax.yaxis.set_major_formatter(fmt)
        ax.tick_params(axis="y", pad=1.5)
        ax.text(0.03, 0.97, f"{100 * d['caught']:.0f}% above", transform=ax.transAxes, ha="left", va="top",
                fontsize=5.8, color=C_UWF, fontweight="semibold")
        ax.set_title(full, loc="center", fontsize=6.5, fontweight="normal", pad=2.5)
        if j == 0:
            ax.set_ylabel("prototype distance", labelpad=1.5)
        if j == 1:
            ax.set_xlabel("MCM confidence", labelpad=1.5)
    fig.text((XS - 0.30) / W, Y_TB / H, "(b) covariate stream: MCM confidence vs. prototype distance", **TITLE)

    # (c) t-SNE per modality ---------------------------------------------------------------------------------------
    for j, (bname, _, _) in enumerate(MODS):
        d = D[bname]
        ax = axes_in(fig, XS + j * (SW + SG), Y_C, SW, HC)
        Z, lab = d["tsne"], d["tsne_lab"]
        for name in ["id0", "id1", "semantic", "covariate", "far"]:
            mm = lab == name
            ax.scatter(Z[mm, 0], Z[mm, 1], s=ms_pts * 0.8, c=COL[name], lw=0, alpha=0.65, rasterized=True)
        ax.set_xticks([]); ax.set_yticks([]); ax.grid(False)
        for s in ax.spines.values():
            s.set_visible(True); s.set_color(LINE); s.set_linewidth(0.5)
        pad = 0.06
        for setlim, v in ((ax.set_xlim, Z[:, 0]), (ax.set_ylim, Z[:, 1])):
            r = v.max() - v.min(); setlim(v.min() - pad * r, v.max() + pad * r)
    fig.text((XS - 0.30) / W, Y_TC / H, "(c) t-SNE of the image embeddings", **TITLE)

    # shared legend in the free cell under (a) -----------------------------------------------------------------------
    lax = axes_in(fig, 0.01, Y_C, XS - 0.35, HC); lax.axis("off")
    dot = lambda c, l: Line2D([], [], ls="none", marker="o", ms=3.2, mfc=c, mec="none", label=l)
    handles = [dot(C_NORMAL, "ID normal / benign"), dot(C_DR, "ID disease"), dot(C_SEM, "semantic OOD"),
               dot(C_UWF, "covariate OOD"), dot(C_FAR, "far OOD"),
               Line2D([], [], color=INK, lw=0.6, ls=(0, (3, 2)), label="95th pct. of ID distance"),
               plt.Rectangle((0, 0), 1, 1, fc=GRID, ec="none", label="5–95th pct. of ID MCM")]
    lax.legend(handles=handles, loc="center left", bbox_to_anchor=(0.0, 0.5), handlelength=1.4, handletextpad=0.5,
               labelspacing=0.32, borderaxespad=0, fontsize=6)
    return fig


def main():
    D = load_data()
    stats = {b: {"vlm": D[b]["vlm"], "overlap_pct": {s: round(100 * D[b]["overlap"][s], 1) for s in SHIFTS},
                 "id_self_overlap_pct": round(100 * D[b]["overlap_id_self"], 1),
                 "cov_above_id95_sproto_pct": round(100 * D[b]["caught"], 1),
                 "n_cov_calibrated": D[b]["n_cov_calibrated"], "n_id_calibrated": D[b]["n_id_calibrated"],
                 "n_tsne": int(len(D[b]["tsne_lab"]))} for b, _, _ in MODS}
    print(json.dumps(stats, indent=1))
    fig = render(D)
    out = save(fig, "fig1_blind_spot")
    plt.close(fig)
    try:
        p, size = preview("fig1_blind_spot")
    except ImportError:   # PyMuPDF is not in the proton env: run the same preview with an interpreter that has it
        import subprocess
        py = os.environ.get("PREVIEW_PY", os.path.expanduser("~/miniconda3/bin/python"))
        p, size = eval(subprocess.run([py, "-c", "import sys; sys.path.insert(0, sys.argv[1]); from paper_style import preview; "
                                       "print(repr(preview('fig1_blind_spot')))", os.path.dirname(os.path.abspath(__file__))],
                                      capture_output=True, text=True, check=True).stdout.strip().splitlines()[-1])
    print("saved", out, "preview", p, "size (in)", size)


if __name__ == "__main__":
    main()
