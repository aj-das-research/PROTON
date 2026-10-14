"""PROTON+ method figure (editable vector: PDF/SVG/PNG), faithful to proton/online.py. See fig_method.md.
Text is measured with the renderer and shrunk to fit its box, so nothing overflows at paper width."""
import glob, os, sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Rectangle
from PIL import Image
import numpy as np

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "paper", "figures", "fig2_method")
ACC, ID0, ID1, SHIFT, FAR, GREY, PALE, TXT, PEACH = "#D55E00", "#0072B2", "#2CA02C", "#D62728", "#7F7F7F", "#5F6368", "#F3F4F6", "#1F2328", "#FFF3E8"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 7, "pdf.fonttype": 42, "ps.fonttype": 42, "svg.fonttype": "none", "mathtext.fontset": "dejavusans"})

W, H = 7.0, 3.1
fig = plt.figure(figsize=(W, H)); ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 100); ax.set_ylim(0, 44.3); ax.axis("off")
fig.canvas.draw(); R = fig.canvas.get_renderer()
def u2px(): return fig.get_figwidth() * fig.dpi / 100.0          # pixels per x-unit
def box(x0, y0, x1, y1, fc=PALE, ec=GREY, lw=0.8, r=0.9, ls="-", z=2):
    ax.add_patch(FancyBboxPatch((x0, y0), x1 - x0, y1 - y0, boxstyle=f"round,pad=0,rounding_size={r}", fc=fc, ec=ec, lw=lw, ls=ls, zorder=z))
def txt(x, y, s, size=7, ha="center", va="center", color=TXT, weight="normal", z=5, maxw=None):
    """Place text; if maxw (x-units) is given, shrink the font until the rendered width fits."""
    t = ax.text(x, y, s, fontsize=size, ha=ha, va=va, color=color, fontweight=weight, zorder=z)
    if maxw is not None:
        for _ in range(12):
            w = t.get_window_extent(R).width / u2px()
            if w <= maxw: break
            t.set_fontsize(t.get_fontsize() * 0.94)
    return t
def arrow(p0, p1, color=GREY, lw=0.9, style="-|>", ls="-", rad=0.0, z=3, ms=7):
    ax.add_patch(FancyArrowPatch(p0, p1, arrowstyle=style, mutation_scale=ms, color=color, lw=lw, ls=ls, connectionstyle=f"arc3,rad={rad}", zorder=z))
def badge(x, y, n):
    ax.add_patch(Circle((x, y), 1.3, fc=ACC, ec="white", lw=0.5, zorder=6)); txt(x, y - 0.1, str(n), size=6.5, color="white", weight="bold", z=7)

# ---------------- column A: stream with real thumbnails (FIVES CC-BY, DeepDRiD, Imagenette)
txt(7.0, 42.2, "Unlabelled test stream", size=7, weight="bold", maxw=13.5)
for (pref, col, lab), y in zip([("id_", ID0, "fundus (ID)"), ("covariate_", SHIFT, "ultra-widefield"), ("far_", FAR, "natural image")], [32.0, 21.5, 11.0]):
    f = sorted(glob.glob(os.path.join(ROOT, "docs/demo/assets/examples", pref + "*.jpg")))[0]
    ax.imshow(np.asarray(Image.open(f).convert("RGB").resize((96, 96))), extent=(2.6, 9.4, y - 3.4, y + 3.4), zorder=3, aspect="auto")
    ax.add_patch(Rectangle((2.6, y - 3.4), 6.8, 6.8, fc="none", ec=col, lw=1.3, zorder=4))
    txt(6.0, y - 4.5, lab, size=5.6, color=col, maxw=12)
txt(6.0, 3.6, r"$x_t$, one at a time", size=6, color=GREY, maxw=12)
arrow((9.8, 21.5), (13.6, 21.5), lw=1.0)

# ---------------- column B: frozen VLM
box(13.8, 8.0, 28.2, 36.0, fc="white", ec=GREY)
txt(21.0, 34.0, "Frozen VLM", size=7.2, weight="bold", maxw=13); txt(21.0, 31.8, "no weight update", size=5.6, color=GREY, maxw=13)
box(15.0, 22.5, 27.0, 29.5, fc=PALE); txt(21.0, 27.5, "image tower", size=6.5, maxw=11.5); txt(21.0, 24.6, r"$e_t\in\mathbb{R}^d$, unit norm", size=5.8, maxw=11.5)
box(15.0, 13.0, 27.0, 20.0, fc=PALE); txt(21.0, 18.0, "text tower (cached)", size=6.5, maxw=11.5); txt(21.0, 15.1, r"$T=[t_1,\ldots,t_C]$", size=5.8, maxw=11.5)
txt(21.0, 10.4, r"$p_t=\mathrm{softmax}(e_t^{\top}T/\tau)$", size=5.8, maxw=13.5)

# ---------------- column C top: softmax score (unchanged)
box(31.5, 36.3, 50.5, 43.8, fc="white", ec=GREY)
txt(41.0, 41.6, "Softmax score (what MCM reads)", size=6.4, weight="bold", maxw=18)
txt(41.0, 38.6, r"$S_{\mathrm{MCM}}=-\max_c\, p_{t,c}$", size=6.6, maxw=18)
arrow((28.4, 27.0), (31.3, 39.5), rad=-0.3, lw=1.0); txt(29.1, 36.3, r"$p_t$", size=6, color=GREY)

# ---------------- column C: prototype bank (proposal)
box(31.5, 1.6, 68.5, 34.0, fc="white", ec=ACC, lw=1.1)
txt(50.0, 32.2, "Online prototype bank: per-class FIFO of M embeddings", size=6.4, weight="bold", maxw=35)
for row, (y, col, name) in enumerate([(27.6, ID0, r"$\mathcal{D}_1$"), (23.2, ID1, r"$\mathcal{D}_2$")]):
    txt(34.3, y, name, size=6.5)
    for k in range(9):
        c = SHIFT if (row == 1 and k in (2, 4, 7)) else col
        ax.add_patch(Rectangle((36.4 + 2.15 * k, y - 1.35), 1.8, 2.7, fc=c, ec="white", lw=0.4, zorder=3))
    txt(56.4, y, "oldest", size=5.2, color=GREY, ha="left")
txt(44.0, 20.3, "red: confidently misclassified shifted inputs that passed the gate", size=5.3, color=SHIFT, maxw=30)
arrow((28.4, 25.0), (36.0, 25.4), lw=1.0); txt(31.8, 26.6, r"$e_t$", size=6, color=GREY)
# (1) domain-anchored prototypes
box(33.0, 3.0, 52.0, 17.5, fc=PEACH, ec=ACC, lw=0.9)
badge(34.6, 16.0, 1); txt(43.6, 15.9, "domain-anchored prototypes", size=6.3, weight="bold", color=ACC, maxw=15.5)
txt(42.5, 13.0, r"$\mu_{\mathrm{dom}}$: mean-shift mode of all queues", size=5.6, maxw=17.5)
txt(42.5, 10.3, r"$w(e)=\exp\big((e^{\top}\mu_{\mathrm{dom}}-1)/h\big)$", size=5.6, maxw=17.5)
txt(42.5, 7.6, r"$\mu_c=\sum_{e\in\mathcal{D}_c} w(e)\,e\;/\;\|\cdot\|$", size=5.6, maxw=17.5)
txt(42.5, 4.7, r"$S_{\mathrm{proto}}=1-\max_c\, e_t^{\top}\mu_c$", size=6.2, maxw=17.5)
arrow((45.0, 21.6), (45.0, 17.7), lw=0.9)
# inset (illustrative)
ix0, iy0, ix1, iy1 = 54.0, 3.0, 67.3, 17.5
box(ix0, iy0, ix1, iy1, fc="white", ec=GREY, lw=0.6, r=0.4)
rng = np.random.default_rng(3)
idp = np.c_[rng.normal(57.8, 0.85, 26), rng.normal(11.6, 1.2, 26)]; shp = np.c_[rng.normal(64.2, 0.75, 14), rng.normal(6.4, 1.0, 14)]
ax.scatter(idp[:, 0], idp[:, 1], s=4, c=ID1, zorder=4, lw=0); ax.scatter(shp[:, 0], shp[:, 1], s=4, c=SHIFT, zorder=4, lw=0)
mean_all = np.r_[idp, shp].mean(0); ax.scatter(*mean_all, s=30, marker="x", c=GREY, zorder=5, lw=1.2)
ax.scatter(*idp.mean(0), s=60, marker="*", c=ACC, ec="white", lw=0.4, zorder=6)
ax.add_patch(Circle(idp.mean(0), 2.7, fc="none", ec=ACC, lw=0.6, ls=(0, (2, 1.5)), zorder=4))
txt(60.6, 16.4, "illustrative embedding space", size=5.0, color=GREY, maxw=12.5)
txt(mean_all[0] + 0.5, mean_all[1] - 0.2, "mean (PROTON)", size=4.9, color=GREY, ha="left", maxw=6.5)
txt(idp.mean(0)[0] - 3.3, idp.mean(0)[1] + 2.4, "anchored (PROTON+)", size=4.9, color=ACC, ha="left", weight="bold", maxw=9)
txt(58.0, 4.0, r"admission radius $m_t+\kappa s_t$", size=4.8, color=ACC, maxw=9)

# ---------------- column D top: fusion (3) and output
box(71.5, 24.0, 99.0, 37.5, fc=PEACH, ec=ACC, lw=0.9)
badge(73.1, 36.0, 3); txt(86.2, 35.9, "scale-free adaptive fusion", size=6.3, weight="bold", color=ACC, maxw=23)
txt(85.2, 32.4, r"$S_t=\alpha_t\, z(S_{\mathrm{MCM}})+(1-\alpha_t)\, z(S_{\mathrm{proto}})$", size=6.3, maxw=26)
txt(85.2, 29.4, r"$z$: online z-score;  $\alpha_t$ from the running variance of $S_{\mathrm{MCM}}$", size=5.3, maxw=26)
txt(85.2, 26.4, r"before calibration ($|\mathcal{D}_c|<K_{\min}$): $S_t=z(S_{\mathrm{MCM}})$", size=5.3, color=GREY, maxw=26)
arrow((50.7, 40.0), (71.3, 33.5), rad=0.15, lw=1.0)
arrow((68.7, 10.0), (71.3, 27.5), rad=-0.3, lw=1.0); txt(69.4, 20.0, r"$S_{\mathrm{proto}}$", size=6, color=GREY, ha="right")
box(84.5, 39.2, 99.0, 44.0, fc=ACC, ec=ACC); txt(91.7, 41.5, r"OOD score $S_t$", size=6.8, color="white", weight="bold", maxw=13)
arrow((91.7, 37.7), (91.7, 39.0), lw=1.0)

# ---------------- column D bottom: consistency admission (2), feedback into the bank
box(71.5, 3.0, 99.0, 14.5, fc=PEACH, ec=ACC, lw=0.9)
badge(73.1, 13.0, 2); txt(86.2, 12.9, "consistency admission (after scoring)", size=6.3, weight="bold", color=ACC, maxw=23)
txt(85.2, 9.8, r"admit $e_t$ to $\mathcal{D}_{\hat c}$ iff $\max_c p_{t,c}\geq\gamma$ and", size=5.6, maxw=26)
txt(85.2, 6.6, r"$d_t=1-e_t^{\top}\mu_{\hat c}\;\leq\; m_t+\kappa\, s_t$", size=5.8, maxw=26)
txt(85.2, 4.1, r"($m_t, s_t$: running mean/std of admitted $d$)", size=4.9, color=GREY, maxw=26)
arrow((71.3, 8.7), (68.7, 8.7), color=ACC, lw=1.0, ls=(0, (3, 2)))
arrow((68.7, 8.7), (68.7, 1.0), color=ACC, lw=1.0, style="-", ls=(0, (3, 2)))
arrow((68.7, 1.0), (45.0, 1.0), color=ACC, lw=1.0, style="-", ls=(0, (3, 2)))
arrow((45.0, 1.0), (45.0, 2.8), color=ACC, lw=1.0, ls=(0, (3, 2)))
txt(57.0, 0.0, "bank update (dashed)", size=4.9, color=ACC, va="bottom", maxw=14)
txt(1.0, 0.1, "orange: changed by PROTON+   grey: unchanged PROTON machinery   solid arrows: data flow", size=5.2, color=GREY, ha="left", va="bottom", maxw=60)

for ext in ("pdf", "svg", "png"):
    fig.savefig(OUT + "." + ext, dpi=300 if ext == "png" else None, bbox_inches="tight", pad_inches=0.02)
print("written", OUT)
