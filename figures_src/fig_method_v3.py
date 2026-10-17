"""PROTON+ method figure built on REAL data: the FLAIR embedding space of the ophthalmology covariate stream (PCA of
ID + ultra-widefield embeddings), the actual end-of-stream prototypes of PROTON (contaminated mean) and PROTON+
(domain-anchored), and one real shifted image with its real softmax confidence and prototype distance.
Layout: stream + frozen VLM (left) -> embedding space with the three PROTON+ changes placed where they act (centre,
hero panel) -> verdict card for the highlighted image (right)."""
import glob, json, os, sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Rectangle, Ellipse
from PIL import Image
sys.path.insert(0, "/mnt/hdd2/Abhijit/projects/PROTON")
from proton.data import load_benchmark
from proton.features import load_features
from proton.evaluate import prepare, run_proton_stream
from proton.streams import make_stream
from proton.online import proton_plus_config

ROOT = "/mnt/hdd2/Abhijit/projects/PROTON"
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "paper", "figures", "fig2_method_v3")
ACC, ID0, ID1, SHIFT, GREY, INK, PALE, PEACH = "#D55E00", "#0072B2", "#2CA02C", "#D62728", "#6B7280", "#1F2328", "#F3F4F6", "#FFF3E8"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 6.5, "pdf.fonttype": 42, "ps.fonttype": 42, "svg.fonttype": "none", "mathtext.fontset": "dejavusans"})

# ------------------------------------------------------------------ real data
b = load_benchmark("ophthalmology"); P = prepare(b, load_features("ophthalmology", b.vlm))
pool, n_id = P.pool("covariate"); order, is_ood = make_stream(n_id, len(pool) - n_id, seed=0); idx = pool[order]
r0 = run_proton_stream(P, pool, order); r1 = run_proton_stream(P, pool, order, config=proton_plus_config())
E = P.embeds; lab = P.labels; sets = P.sets
from sklearn.decomposition import PCA
pca = PCA(2, random_state=0).fit(E[pool]); Z = pca.transform(E[pool])
proto0 = pca.transform(np.stack(r0["detector"].prototypes)); proto1 = pca.transform(np.stack(r1["detector"].prototypes))
# one real shifted image: a late, confidently-classified ultra-widefield sample
late = [t for t in range(len(idx)) if is_ood[t] == 1 and r1["calibrated"][t] and r1["conf"][t] > 0.9][-3]
i_sample = idx[late]; z_sample = pca.transform(E[i_sample:i_sample + 1])[0]
conf, sproto, pred = r1["conf"][late], r1["s_proto"][late], r1["pred"][late]
bank_ood = json.load(open(f"{ROOT}/outputs/results/contamination_stats.json"))["ophthalmology"]["covariate"]
print(f"sample t={late} conf={conf:.3f} S_proto={sproto:.3f} pred={b.classes[pred]}; bank OOD share PROTON {bank_ood['bank_ood_frac'][1]:.2f} vs PROTON+ {bank_ood['bank_ood_frac_plus'][1]:.2f}")

# ------------------------------------------------------------------ canvas
W, H = 7.0, 3.5
fig = plt.figure(figsize=(W, H))
def panel(x0, y0, w, h): ax = fig.add_axes([x0, y0, w, h]); ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off"); return ax
def rbox(ax, x0, y0, x1, y1, fc, ec, lw=0.9, r=0.03, z=1):
    ax.add_patch(FancyBboxPatch((x0, y0), x1 - x0, y1 - y0, boxstyle=f"round,pad=0,rounding_size={r}", fc=fc, ec=ec, lw=lw, zorder=z))
def arrow(ax, p0, p1, color=GREY, lw=1.0, style="-|>", ls="-", rad=0.0, z=3, ms=8):
    ax.add_patch(FancyArrowPatch(p0, p1, arrowstyle=style, mutation_scale=ms, color=color, lw=lw, ls=ls, connectionstyle=f"arc3,rad={rad}", zorder=z))
def badge(ax, x, y, n, r=0.028):
    ax.add_patch(Circle((x, y), r, fc=ACC, ec="white", lw=0.6, zorder=9, transform=ax.transAxes)); ax.text(x, y - 0.002, str(n), ha="center", va="center", fontsize=6.5, color="white", weight="bold", zorder=10)

# ---- left: stream and frozen VLM --------------------------------------------------------------------------
L = panel(0.005, 0.07, 0.27, 0.90)
L.text(0.03, 0.97, "Unlabelled test stream", fontsize=7.2, weight="bold", va="top", color=INK)
thumbs = [("id_", ID0, "fundus, normal"), ("id_", ID1, "fundus, DR"), ("covariate_", SHIFT, "ultra-widefield camera")]
files = {"id_": sorted(glob.glob(f"{ROOT}/docs/demo/assets/examples/id_*.jpg")), "covariate_": sorted(glob.glob(f"{ROOT}/docs/demo/assets/examples/covariate_*.jpg"))}
for k, ((pref, col, cap), y) in enumerate(zip(thumbs, [0.80, 0.56, 0.32])):
    f = files[pref][k if pref == "id_" else 0]
    im = np.asarray(Image.open(f).convert("RGB").resize((120, 120)))
    L.imshow(im, extent=(0.04, 0.30, y - 0.11, y + 0.11), zorder=3, aspect="auto")
    L.add_patch(Rectangle((0.04, y - 0.11), 0.26, 0.22, fc="none", ec=col, lw=1.4, zorder=4))
    L.text(0.17, y - 0.145, cap, ha="center", va="top", fontsize=5.6, color=col)
    arrow(L, (0.31, y), (0.45, 0.56), color=GREY, lw=0.8, rad=0.0)
L.text(0.17, 0.10, r"$x_t$, one at a time, no labels", ha="center", fontsize=5.8, color=GREY)
rbox(L, 0.46, 0.30, 0.98, 0.82, "white", GREY, lw=1.0, r=0.04)
L.text(0.72, 0.76, "Frozen VLM", ha="center", fontsize=7.2, weight="bold", color=INK)
L.text(0.72, 0.70, "FLAIR, no weight update", ha="center", fontsize=5.4, color=GREY)
rbox(L, 0.50, 0.50, 0.94, 0.64, PALE, GREY, lw=0.6, r=0.02); L.text(0.72, 0.57, "image tower $\\rightarrow e_t$", ha="center", fontsize=6.2, color=INK)
rbox(L, 0.50, 0.34, 0.94, 0.48, PALE, GREY, lw=0.6, r=0.02); L.text(0.72, 0.41, "text prompts $\\rightarrow T$ (cached)", ha="center", fontsize=6.2, color=INK)
L.text(0.72, 0.24, r"$p_t=\mathrm{softmax}(e_t^{\top}T/\tau)$", ha="center", fontsize=6.2, color=INK)
L.text(0.72, 0.17, "softmax: what MCM reads", ha="center", fontsize=5.4, color=GREY)
L.text(0.72, 0.88, "embedding: what the bank reads", ha="center", fontsize=5.4, color=GREY)

# ---- centre: embedding space (hero) -----------------------------------------------------------------------
C = fig.add_axes([0.285, 0.10, 0.44, 0.84]); C.set_xticks([]); C.set_yticks([])
for s in C.spines.values(): s.set_edgecolor(ACC); s.set_linewidth(1.2)
C.set_title("Embedding space of the stream (FLAIR, PCA of real embeddings)", fontsize=7, color=INK, pad=4)
m0, m1, mc = (lab[pool] == 0) & (sets[pool] == "id"), (lab[pool] == 1) & (sets[pool] == "id"), sets[pool] == "covariate"
C.scatter(Z[m0, 0], Z[m0, 1], s=7, c=ID0, alpha=.55, lw=0, label="normal (ID)")
C.scatter(Z[m1, 0], Z[m1, 1], s=7, c=ID1, alpha=.55, lw=0, label="diabetic retinopathy (ID)")
C.scatter(Z[mc, 0], Z[mc, 1], s=7, c=SHIFT, alpha=.55, lw=0, label="ultra-widefield (shifted, confidently labelled DR)")
# prototypes of class DR (index 1)
C.scatter(*proto0[1], s=70, marker="X", c=GREY, ec="white", lw=.5, zorder=6)
C.scatter(*proto1[1], s=180, marker="*", c=ACC, ec="white", lw=.6, zorder=7)
C.scatter(*proto1[0], s=120, marker="*", c=ACC, ec="white", lw=.6, zorder=7)
# the highlighted real sample and its distance to the anchored prototype
C.scatter(*z_sample, s=60, facecolors="none", edgecolors=INK, lw=1.3, zorder=8)
C.plot([z_sample[0], proto1[1][0]], [z_sample[1], proto1[1][1]], ls=":", lw=1.0, c=INK, zorder=5)
xmid, ymid = (z_sample + proto1[1]) / 2
# admission radius (illustrative in the projection) around the DR anchor
rad = 0.45 * np.linalg.norm(Z[m1].std(0))
C.add_patch(Circle(proto1[1], rad * 2.2, fc="none", ec=ACC, lw=0.9, ls=(0, (3, 2)), zorder=5))
xr = C.get_xlim(); yr = C.get_ylim(); dx = xr[1] - xr[0]; dy = yr[1] - yr[0]
def ann(text, xy, xytext, color, size=5.8, weight="normal", ha="left", arrowc=None):
    C.annotate(text, xy=xy, xytext=xytext, fontsize=size, color=color, weight=weight, ha=ha, va="center", zorder=10,
               arrowprops=dict(arrowstyle="-", color=arrowc or color, lw=0.6, shrinkA=0, shrinkB=2), bbox=dict(boxstyle="round,pad=0.25", fc="white", ec="none", alpha=.9))
ann("PROTON prototype of “DR”: the plain mean,\n%d%% of its queue is shifted, so it drifts\nbetween the two clusters" % round(100 * bank_ood["bank_ood_frac"][1]),
    proto0[1], (proto0[1][0] + 0.02 * dx, proto0[1][1] - 0.30 * dy), GREY)
ann("①  PROTON+ prototype: anchored to the\ndominant mode of the whole bank (mean shift),\nshifted members weighted ≈ 0",
    proto1[1], (proto1[1][0] - 0.62 * dx, proto1[1][1] + 0.30 * dy), ACC, weight="bold")
ann("②  consistency admission: an image joins the\nbank only inside the typical radius of its class",
    (proto1[1][0] + rad * 2.2 * 0.7, proto1[1][1] + rad * 2.2 * 0.7), (proto1[1][0] - 0.62 * dx, proto1[1][1] - 0.40 * dy), ACC, weight="bold")
ann(f"this image: softmax {conf:.2f} “DR”, yet\n$S_{{proto}}$ = {sproto:.2f} from every prototype",
    z_sample, (z_sample[0] + 0.04 * dx, z_sample[1] + 0.22 * dy), INK)
C.legend(loc="lower right", fontsize=5.2, frameon=True, framealpha=.9, edgecolor="none", markerscale=1.6, handletextpad=0.3)

# ---- right: verdict card ------------------------------------------------------------------------------------
Rp = panel(0.735, 0.07, 0.26, 0.90)
rbox(Rp, 0.02, 0.02, 0.98, 0.98, PEACH, ACC, lw=1.1, r=0.05)
badge(Rp, 0.09, 0.925, 3); Rp.text(0.16, 0.925, "scale-free fusion, one verdict", fontsize=6.8, weight="bold", color=ACC, va="center")
im = np.asarray(Image.open(b.paths()[i_sample]).convert("RGB").resize((140, 140)))
Rp.imshow(im, extent=(0.06, 0.40, 0.56, 0.86), zorder=3, aspect="auto"); Rp.add_patch(Rectangle((0.06, 0.56), 0.34, 0.30, fc="none", ec=SHIFT, lw=1.3, zorder=4))
Rp.text(0.23, 0.53, "real ultra-widefield image", ha="center", va="top", fontsize=5.2, color=SHIFT)
def gauge(y, label, val, frac, col, note):
    Rp.text(0.46, y + 0.075, label, fontsize=5.6, color=INK, va="center")
    Rp.add_patch(Rectangle((0.46, y), 0.48, 0.045, fc="#E5E7EB", ec="none", zorder=2)); Rp.add_patch(Rectangle((0.46, y), 0.48 * frac, 0.045, fc=col, ec="none", zorder=3))
    Rp.text(0.95, y + 0.022, f"{val:.2f}", fontsize=6.2, weight="bold", color=INK, ha="right", va="center", zorder=4)
    Rp.text(0.46, y - 0.035, note, fontsize=5.0, color=GREY, va="center")
gauge(0.74, "softmax confidence (MCM)", conf, conf, ID0, "looks in-distribution to MCM")
gauge(0.58, "prototype distance $S_{proto}$ (PROTON+)", sproto, min(1, sproto / 0.9), ACC, "far from every class prototype")
Rp.text(0.50, 0.43, r"$S_t=\alpha_t\,z(S_{\mathrm{MCM}})+(1-\alpha_t)\,z(S_{\mathrm{proto}})$", ha="center", fontsize=6.0, color=INK)
Rp.text(0.50, 0.37, "online z-scores, variance-driven $\\alpha_t$ as in PROTON", ha="center", fontsize=5.0, color=GREY)
rbox(Rp, 0.14, 0.17, 0.86, 0.30, "#FDE2E2", "#FDE2E2", r=0.03); Rp.text(0.50, 0.235, "flagged out-of-distribution", ha="center", va="center", fontsize=7.0, weight="bold", color="#9F1239")
Rp.text(0.50, 0.10, "the softmax alone would have accepted it", ha="center", fontsize=5.2, color=GREY)
# connectors between panels
arrow(L, (0.98, 0.57), (1.08, 0.57), color=ACC, lw=1.1)
fig.text(0.283, 0.60, "$e_t$", fontsize=6.5, color=ACC, ha="left")
fig.text(0.283, 0.27, r"$p_t$", fontsize=6.5, color=ID0, ha="left")
arrow(L, (0.98, 0.41), (1.08, 0.24), color=ID0, lw=1.0, rad=0.2)
fig.text(0.005, 0.015, "orange: what PROTON+ changes   grey ×: PROTON's prototype   dashed circle: admission radius (illustrative in the projection)   open circle: one real stream image", fontsize=5.2, color=GREY)
for ext in ("pdf", "svg", "png"):
    fig.savefig(OUT + "." + ext, dpi=300 if ext == "png" else None, bbox_inches="tight", pad_inches=0.02)
print("written", OUT)
