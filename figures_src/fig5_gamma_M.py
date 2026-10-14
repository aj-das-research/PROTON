"""Fig. 5 (output name fig3b_gamma_M): change in covariate AUROC over MCM against the gate gamma and the per-class bank
size M, PROTON (top row) and PROTON+ (bottom row), one column per modality, ONE shared symmetric diverging scale
(orange = gain over MCM, blue = loss). Real data only, same protocol for both rows (covariate shift, 3 stream orders):
  PROTON : outputs/results/<benchmark>/fig3b_gamma_M.json       (proton.experiments.tables.gamma_M_grid)
  PROTON+: outputs/results/<benchmark>/fig5_gamma_M_plus.json   (computed here with proton_plus_config if missing;
                                                                 pass --recompute to rebuild)
Run:  HF_HOME=/mnt/hdd2/Abhijit/.cache/huggingface /mnt/hdd2/Abhijit/envs/proton/bin/python figures_src/fig5_gamma_M.py"""
import json, os, sys, time
sys.path.insert(0, "/mnt/hdd2/Abhijit/projects/PROTON/figures_src")
from paper_style import *                      # noqa: F401,F403  (rcParams, palette, FULL_W, save, preview)
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, to_rgb
from matplotlib.patches import Rectangle

sys.path.insert(0, ROOT)
RES = os.path.join(ROOT, "outputs", "results")
BENCH = [("ophthalmology", "Ophthalmology", "FLAIR"), ("radiology", "Radiology", "UniMed-CLIP"),
         ("pathology", "Pathology", "QuiltNet")]
G_DEF, M_DEF, N_PERM = 0.7, 100, 3


# ---------------------------------------------------------------------------------------------- PROTON+ grid (cached)
def plus_grid(key, gammas, Ms, mcm_ref, recompute=False):
    """Delta covariate AUROC of PROTON+ over MCM on the same gamma x M grid and protocol as gamma_M_grid (PROTON)."""
    path = os.path.join(RES, key, "fig5_gamma_M_plus.json")
    if os.path.exists(path) and not recompute:
        d = json.load(open(path))
        if d["gammas"] == list(gammas) and d["Ms"] == list(Ms):
            return d
    os.environ.setdefault("HF_HOME", "/mnt/hdd2/Abhijit/.cache/huggingface")
    from dataclasses import asdict
    from proton.data import load_benchmark
    from proton.features import load_features
    from proton.evaluate import prepare, evaluate_proton, evaluate_static
    from proton.online import proton_plus_config
    b = load_benchmark(key)
    P = prepare(b, load_features(key, b.vlm))
    mcm = evaluate_static(P, shifts=("covariate",), names=["mcm"])["mcm"]["covariate"]["auroc"]
    assert abs(mcm - mcm_ref) < 1e-9, f"MCM differs from the PROTON grid's ({mcm} vs {mcm_ref})"
    chk = evaluate_proton(P, shifts=("covariate",), n_perm=N_PERM, gamma=G_DEF, M=M_DEF)["covariate"]["auroc"] - mcm
    t0, grid, std = time.time(), np.zeros((len(gammas), len(Ms))), np.zeros((len(gammas), len(Ms)))
    for i, g in enumerate(gammas):
        for j, M in enumerate(Ms):
            r = evaluate_proton(P, shifts=("covariate",), n_perm=N_PERM, config=proton_plus_config(gamma=g, M=M))
            grid[i, j], std[i, j] = r["covariate"]["auroc"] - mcm, r["covariate"]["auroc_std"]
    d = {"method": "PROTON+", "shift": "covariate", "n_perm": N_PERM, "gammas": list(gammas), "Ms": list(Ms),
         "delta_auroc": grid.tolist(), "auroc_std": std.tolist(), "mcm_cov_auroc": mcm,
         "config": {k: v for k, v in asdict(proton_plus_config()).items() if k not in ("gamma", "M")},
         "proton_default_delta_check": chk, "seconds": round(time.time() - t0, 1)}
    json.dump(d, open(path, "w"), indent=1)
    print(f"computed {path} in {d['seconds']} s (PROTON default re-run: {chk:+.3f})")
    return d


# ---------------------------------------------------------------------------------------------------------- data
cols = []
for key, name, vlm in BENCH:
    d = json.load(open(os.path.join(RES, key, "fig3b_gamma_M.json")))
    q = plus_grid(key, d["gammas"], d["Ms"], d["mcm_cov_auroc"], recompute="--recompute" in sys.argv)
    cols.append(dict(name=name, vlm=vlm, gammas=d["gammas"], Ms=d["Ms"], mcm=d["mcm_cov_auroc"],
                     rows=[np.array(d["delta_auroc"], float), np.array(q["delta_auroc"], float)]))
gammas, Ms = cols[0]["gammas"], cols[0]["Ms"]
assert all(c["gammas"] == gammas and c["Ms"] == Ms for c in cols), "grids must share gamma and M"
gi, mj = gammas.index(G_DEF), Ms.index(M_DEF)
VMAX = 10 * np.ceil(max(np.abs(g).max() for c in cols for g in c["rows"]) / 10)   # symmetric, shared by all six
ROWS = [("PROTON", C_PROTON), ("PROTON+ (ours)", ACC)]

# numbers quoted in the caption / text (printed so they can be checked)
for c in cols:
    for (lab, _), g in zip(ROWS, c["rows"]):
        same_low = [gm for r, gm in enumerate(gammas) if np.allclose(g[r], g[0])]
        print(f"{c['name']:13s} {lab:15s} MCM={c['mcm']:5.1f}  range {g.min():+6.1f}..{g.max():+6.1f}  "
              f"default {g[gi, mj]:+5.1f}  cells<0: {int((g < 0).sum()):2d}/{g.size}  max spread over M: "
              f"{np.ptp(g, 1).max():4.1f}  spread over gamma at M={M_DEF}: {np.ptp(g[:, mj]):4.1f}  "
              f"gamma=0.9,M={M_DEF}: {g[-1, mj]:+.1f}  rows equal to gamma={gammas[0]}: {same_low}")
    d = c["rows"][1] - c["rows"][0]
    print(f"{c['name']:13s} PROTON+ minus PROTON: {d.min():+.1f}..{d.max():+.1f}, at default {d[gi, mj]:+.1f}, "
          f"cells where PROTON+ > PROTON: {int((d > 0).sum())}/{d.size}")
    neg = [(gammas[i], Ms[j], round(float(c["rows"][1][i, j]), 1)) for i, j in zip(*np.where(c["rows"][1] < 0))]
    if neg:
        print(f"{c['name']:13s} PROTON+ cells below MCM (gamma, M, delta): {neg}")
allp = np.concatenate([c["rows"][1].ravel() for c in cols]); allo = np.concatenate([c["rows"][0].ravel() for c in cols])
print(f"PROTON+ above MCM in {int((allp > 0).sum())}/{allp.size} cells, above PROTON in "
      f"{sum(int((c['rows'][1] > c['rows'][0]).sum()) for c in cols)}/{allp.size}")
print(f"PROTON+ min over all grids {allp.min():+.2f} (cells < 0: {int((allp < 0).sum())}), "
      f"PROTON min {allo.min():+.1f} (cells < 0: {int((allo < 0).sum())}); shared colour scale +-{VMAX:.0f} points")

# ------------------------------------------------------------------------------------------------------- colours
# muted blue (loss vs MCM) - warm white - muted vermillion (gain, the paper's accent family); the ends are light enough
# (luminance > 0.21) that ink text keeps the higher contrast on every cell, so all numbers share one colour
CMAP = LinearSegmentedColormap.from_list(
    "proton_div", [(0.0, "#5F8BC0"), (0.25, "#A9C4E2"), (0.5, "#F2F1EE"), (0.75, "#F5BF98"), (1.0, "#DA6C2E")])


def lum(rgb):
    c = np.array(rgb[:3]); c = np.where(c <= 0.03928, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


def text_on(rgb):
    """White or ink text, whichever has the higher WCAG contrast against the cell colour."""
    L, Li = lum(rgb), lum(to_rgb(INK))
    return "white" if 1.05 / (L + 0.05) > (L + 0.05) / (Li + 0.05) else INK


def fmt(v, plus=False):
    r = int(np.round(v))
    return "0" if r == 0 else ((f"+{r}" if plus else f"{r}") if r > 0 else "−" + str(-r))


# -------------------------------------------------------------------------------------------------------- layout
W, H = FULL_W, 2.66                                 # final size; margins are fitted so the tight bbox is exactly W x H
GAP, RGAP, CB_GAP, CB_W = 0.07, 0.08, 0.09, 0.07    # inches: between columns, between rows, to colour bar, bar width


def title(ax, k, name, vlm, ph):
    """'(a) Name' in the semibold title style, ' · VLM' in regular muted text right after it."""
    t = ax.text(0, 1 + 3.0 / 72 / ph, f"({'abc'[k]}) {name}", transform=ax.transAxes, ha="left", va="bottom",
                fontsize=7, fontweight="semibold", color=INK)                  # 3 pt above the heatmap
    ax.annotate(f" · {vlm}", xy=(1, 0), xycoords=t, ha="left", va="bottom", fontsize=6.5, color=MUTE)


def heat(ax, g, first_col, last_row):
    im = ax.pcolormesh(np.arange(len(Ms) + 1) - 0.5, np.arange(len(gammas) + 1) - 0.5, g, cmap=CMAP,
                       vmin=-VMAX, vmax=VMAX, edgecolors="white", linewidth=0.6)
    ax.set_xlim(-0.5, len(Ms) - 0.5); ax.set_ylim(len(gammas) - 0.5, -0.5)
    ax.grid(False)
    for sp in ax.spines.values():
        sp.set_visible(False)
    for i in range(len(gammas)):
        for j in range(len(Ms)):
            ax.text(j, i, fmt(g[i, j]), ha="center", va="center", fontsize=5.6,
                    color=text_on(CMAP((g[i, j] + VMAX) / (2 * VMAX))))
    ax.add_patch(Rectangle((mj - 0.5, gi - 0.5), 1, 1, fill=False, ec=INK, lw=0.9, zorder=5))
    ax.set_xticks(range(len(Ms))); ax.set_xticklabels([str(m) for m in Ms] if last_row else [])
    ax.set_yticks(range(len(gammas))); ax.set_yticklabels([f"{x:.1f}" for x in gammas] if first_col else [])
    ax.tick_params(axis="both", length=0, pad=1.5)
    for t, v in zip(ax.get_xticklabels(), Ms):
        if v == M_DEF: t.set_color(INK); t.set_fontweight("bold")
    for t, v in zip(ax.get_yticklabels(), gammas):
        if v == G_DEF: t.set_color(INK); t.set_fontweight("bold")
    if last_row:
        ax.set_xlabel(r"bank size $M$", labelpad=1.5)
    if first_col:
        ax.set_ylabel(r"gate $\gamma$", labelpad=2)
    return im


def draw(L, R, B, T):
    pw = (W - L - 2 * GAP - CB_GAP - CB_W - R) / 3
    ph = (H - B - T - RGAP) / 2
    fig = plt.figure(figsize=(W, H))
    for r, ((lab, col), last) in enumerate(zip(ROWS, (False, True))):
        y0 = B + (1 - r) * (ph + RGAP)
        for k, c in enumerate(cols):
            ax = fig.add_axes([(L + k * (pw + GAP)) / W, y0 / H, pw / W, ph / H])
            im = heat(ax, c["rows"][r], k == 0, last)
            if r == 0:
                title(ax, k, c["name"], c["vlm"], ph)
            if k == 0:   # row label, left of the gamma axis label
                ax.annotate(lab, xy=(0, 0.5), xycoords=ax.yaxis.label, xytext=(-2.5, 0), textcoords="offset points",
                            rotation=90, ha="right", va="center", fontsize=7, fontweight="semibold", color=col)
    cax = fig.add_axes([(L + 3 * pw + 2 * GAP + CB_GAP) / W, B / H, CB_W / W, (2 * ph + RGAP) / H])
    ticks = np.arange(-VMAX + 10, VMAX, 10) if VMAX <= 30 else np.arange(-VMAX + 10, VMAX - 5, 20)
    cb = fig.colorbar(im, cax=cax, ticks=ticks)
    cb.ax.set_yticklabels([fmt(v, plus=True) for v in ticks])
    cb.outline.set_visible(False)
    cb.ax.tick_params(length=1.8, width=0.5, pad=1.2, color=LINE)
    cb.set_label("ΔAUROC vs MCM (points)", labelpad=2)
    return fig


PAD = 0.01                                           # save() adds pad_inches=0.01 around the tight bbox
# fit: draw with a guess, measure the tight bbox, move the margins so the content fills W x H, redraw
L, R, B, T = 0.40, 0.30, 0.30, 0.18
for _ in range(3):
    fig = draw(L, R, B, T)
    bb = fig.get_tightbbox(fig.canvas.get_renderer())                 # inches
    L, R, B, T = L - bb.x0 + PAD, R - (W - bb.x1) + PAD, B - bb.y0 + PAD, T - (H - bb.y1) + PAD
    plt.close(fig)
fig = draw(L, R, B, T)
# audit: smallest font, overlapping text boxes, widest cell number against the cell width
rend = fig.canvas.get_renderer()
texts = [t for t in fig.findobj(plt.Text) if t.get_visible() and t.get_text().strip()]
print(f"audit: smallest font {min(t.get_fontsize() for t in texts):.1f} pt over {len(texts)} text objects")
boxes = [(t.get_text(), t.get_window_extent(rend)) for t in texts]
over = [(a, b) for i, (a, ba) in enumerate(boxes) for (b, bb) in boxes[i + 1:] if ba.overlaps(bb)
        and ba.intersection(ba, bb).width > 0.5 and ba.intersection(ba, bb).height > 0.5]
print(f"audit: {len(over)} overlapping text pairs", over[:5])
hm = fig.axes[:6]
cw = hm[0].get_window_extent(rend).width / len(Ms); ch = hm[0].get_window_extent(rend).height / len(gammas)
widest = max(t.get_window_extent(rend).width for a in hm for t in a.texts if len(t.get_text()) <= 3)
print(f"audit: cell {cw / fig.dpi:.3f} x {ch / fig.dpi:.3f} in, widest number {widest / fig.dpi:.3f} in")

save(fig, "fig3b_gamma_M")
p, size = preview("fig3b_gamma_M")
print("preview:", p, "size (in):", size)
