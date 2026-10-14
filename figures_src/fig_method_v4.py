"""PROTON+ method figure, built at the LNCS text width (4.8 in) from REAL data.
Top strip: the pipeline (stream -> frozen VLM -> softmax score | prototype bank -> z-score fusion -> OOD score), with the
three PROTON+ changes as orange badges. Bottom: "inside the bank" for the DR class on the ultra-widefield stream (seed 0):
(b) PROTON's plain-mean prototype vs (c) PROTON+'s domain-anchored prototype, drawn in a 2-D linear projection of the real
FLAIR embeddings (x: ID -> ultra-widefield mean direction, y: normal -> DR direction), with one real ultra-widefield image
and its real prototype distance under each method."""
import os, sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Rectangle
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from PIL import Image
sys.path.insert(0, "/mnt/hdd2/Abhijit/projects/PROTON")
from proton.data import load_benchmark
from proton.features import load_features
from proton.evaluate import prepare, run_proton_stream
from proton.streams import make_stream
from proton.online import proton_plus_config

ROOT = "/mnt/hdd2/Abhijit/projects/PROTON"
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "paper", "figures", "fig2_method")
ACC, ACC_SOFT, NORM, DR, UWF, GREY, INK, MUTED, PANEL = "#D55E00", "#FDF0E6", "#3B7DD8", "#2E9E5B", "#D64545", "#8A9099", "#1F2328", "#6B7280", "#F7F8FA"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 6, "pdf.fonttype": 42, "ps.fonttype": 42, "svg.fonttype": "none", "mathtext.fontset": "dejavusans", "axes.linewidth": 0.6})

# ------------------------------------------------------------------ real data
b = load_benchmark("ophthalmology"); P = prepare(b, load_features("ophthalmology", b.vlm))
pool, n_id = P.pool("covariate"); order, is_ood = make_stream(n_id, len(pool) - n_id, seed=0); idx = pool[order]
r0 = run_proton_stream(P, pool, order); r1 = run_proton_stream(P, pool, order, config=proton_plus_config())
det0, det1 = r0["detector"], r1["detector"]
E, lab, sets = P.embeds, P.labels, P.sets
T_SAMPLE = 413
i_s = idx[T_SAMPLE]; conf_s = r1["conf"][T_SAMPLE]; sp0, sp1 = r0["s_proto"][T_SAMPLE], r1["s_proto"][T_SAMPLE]
idm = (sets == "id"); cov = (sets == "covariate")
c = E[idm].mean(0)
d1 = E[cov].mean(0) - c; d1 /= np.linalg.norm(d1)
d2 = E[idm & (lab == 1)].mean(0) - E[idm & (lab == 0)].mean(0); d2 -= (d2 @ d1) * d1; d2 /= np.linalg.norm(d2)
proj = lambda X: np.c_[(np.atleast_2d(X) - c) @ d1, (np.atleast_2d(X) - c) @ d2]
Zall = proj(E[pool]); Zs = proj(E[i_s])[0]
# bank members of the DR queue (class 1) at the end of the stream, with their true group
def members(det, cls):
    M = np.stack(det.banks[cls]); key = {E[i].round(5).tobytes(): i for i in pool}
    ids = [key.get(np.asarray(m, dtype=np.float32).round(5).tobytes()) for m in M]
    shifted = np.array([sets[i] == "covariate" if i is not None else False for i in ids])
    return M, shifted
M0, sh0 = members(det0, 1); M1, sh1 = members(det1, 1)
w1 = np.exp((M1 @ det1.mu_dom - 1.0) / det1.cfg.bandwidth); w1n = w1 / w1.max()
share_w_shifted = w1[sh1].sum() / w1.sum()
rejected = np.array([h["calibrated"] and (h["conf"] >= det1.cfg.gamma) and not h["updated"] for h in det1.history])
Zrej = proj(E[idx[rejected & (is_ood == 1)]])
print(f"PROTON DR queue: {sh0.mean():.0%} shifted | PROTON+ DR queue: {sh1.mean():.0%} shifted members holding {share_w_shifted:.1%} of the anchor weight | rejected shifted: {int((rejected & (is_ood == 1)).sum())}")
print(f"sample t={T_SAMPLE}: conf {conf_s:.3f}, S_proto PROTON {sp0:.3f}, PROTON+ {sp1:.3f}")

# ------------------------------------------------------------------ canvas (inches)
W, H = 4.8, 3.0
fig = plt.figure(figsize=(W, H)); ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, W); ax.set_ylim(0, H); ax.axis("off")
def rbox(x0, y0, x1, y1, fc="white", ec=GREY, lw=0.7, r=0.06, z=2, ls="-"):
    ax.add_patch(FancyBboxPatch((x0, y0), x1 - x0, y1 - y0, boxstyle=f"round,pad=0,rounding_size={r}", fc=fc, ec=ec, lw=lw, ls=ls, zorder=z))
def txt(x, y, s, size=6, color=INK, ha="center", va="center", weight="normal", z=6, **kw):
    return ax.text(x, y, s, fontsize=size, color=color, ha=ha, va=va, fontweight=weight, zorder=z, **kw)
def arrow(p0, p1, color=GREY, lw=0.8, rad=0.0, style="-|>", ls="-", z=3, ms=6):
    ax.add_patch(FancyArrowPatch(p0, p1, arrowstyle=style, mutation_scale=ms, color=color, lw=lw, ls=ls, connectionstyle=f"arc3,rad={rad}", zorder=z, shrinkA=0, shrinkB=0))
def badge(x, y, n, r=0.062):
    ax.add_patch(Circle((x, y), r, fc=ACC, ec="white", lw=0.5, zorder=8)); txt(x, y - 0.004, str(n), size=5.6, color="white", weight="bold", z=9)

# ---- top strip: pipeline ---------------------------------------------------------------------------------------
yT = 2.53
thumbs = [(b.paths()[np.where(idm & (lab == 0))[0][3]], NORM), (b.paths()[np.where(idm & (lab == 1))[0][5]], DR), (b.paths()[i_s], UWF), (b.paths()[np.where(idm & (lab == 1))[0][9]], DR)]
for k, (p, col) in enumerate(thumbs):
    x0, y0, s = 0.05 + 0.105 * k, yT - 0.21 + 0.035 * k, 0.32
    im = np.asarray(Image.open(p).convert("RGB").resize((96, 96)))
    ax.imshow(im, extent=(x0, x0 + s, y0, y0 + s), zorder=3 + k, aspect="auto")
    ax.add_patch(Rectangle((x0, y0), s, s, fc="none", ec=col, lw=1.0, zorder=3 + k))
txt(0.35, yT - 0.33, "test stream, no labels", size=5.3, color=MUTED)
arrow((0.72, yT), (0.86, yT), lw=0.9)
rbox(0.86, yT - 0.25, 1.46, yT + 0.25, fc=PANEL, ec=GREY)
txt(1.16, yT + 0.08, "frozen VLM", size=6.3, weight="bold"); txt(1.16, yT - 0.10, "FLAIR", size=5.3, color=MUTED)
# lane 1: softmax score (unchanged PROTON machinery)
rbox(1.66, yT + 0.10, 2.86, yT + 0.46, fc="white", ec=GREY)
txt(2.26, yT + 0.36, "softmax score (MCM)", size=5.8, weight="bold", color="#4B5563")
txt(2.26, yT + 0.20, r"$S_{\mathrm{MCM}}=-\max_c\,p_{t,c}$", size=5.6)
arrow((1.46, yT + 0.12), (1.66, yT + 0.28), lw=0.8); txt(1.53, yT + 0.27, "$p_t$", size=5.6, color=MUTED, ha="right")
# lane 2: prototype bank (PROTON+ changes 1 and 2)
rbox(1.66, yT - 0.46, 2.86, yT - 0.10, fc=ACC_SOFT, ec=ACC, lw=0.9)
txt(2.26, yT - 0.20, "online prototype bank", size=5.8, weight="bold", color=ACC)
txt(2.26, yT - 0.36, r"$S_{\mathrm{proto}}=1-\max_c\,e_t^{\top}\mu_c$", size=5.6)
badge(2.70, yT - 0.10, 1); badge(2.84, yT - 0.10, 2)
arrow((1.46, yT - 0.12), (1.66, yT - 0.28), lw=0.8, color=ACC); txt(1.53, yT - 0.29, "$e_t$", size=5.6, color=ACC, ha="right")
# fusion (PROTON+ change 3) and output
arrow((2.86, yT + 0.28), (3.04, yT + 0.12), lw=0.8); arrow((2.86, yT - 0.28), (3.04, yT - 0.12), lw=0.8, color=ACC)
rbox(3.04, yT - 0.25, 4.18, yT + 0.25, fc=ACC_SOFT, ec=ACC, lw=0.9)
badge(4.16, yT + 0.25, 3)
txt(3.61, yT + 0.10, "z-score fusion", size=5.8, weight="bold", color=ACC)
txt(3.61, yT - 0.08, r"$\alpha_t\,z(S_{\mathrm{MCM}})+(1{-}\alpha_t)\,z(S_{\mathrm{proto}})$", size=5.1)
arrow((4.18, yT), (4.30, yT), lw=0.9)
rbox(4.30, yT - 0.15, 4.76, yT + 0.15, fc=INK, ec=INK, r=0.08); txt(4.53, yT + 0.01, "OOD\nscore", size=5.6, color="white", weight="bold", linespacing=1.0)
# what the badges mean (in place, under the bank) and the zoom into the bank
txt(2.26, yT - 0.585, "① domain-anchored prototypes    ② consistency admission    ③ scale-free fusion", size=5.3, color=ACC)
txt(W / 2, yT - 0.735, f"zoom into the “DR” bank on the ultra-widefield stream   ·   ◯ a real ultra-widefield image, softmax {conf_s:.2f} “DR”",
    size=5.3, color=MUTED, z=7, bbox=dict(boxstyle="round,pad=0.28", fc="white", ec=ACC, lw=0.6))

# ---- bottom panels: PROTON vs PROTON+ (compact, no text inside the plots) ---------------------------------------
Zdr, Zcv = proj(E[idm & (lab == 1)]), proj(E[cov])
xlo, xhi = np.percentile(Zdr[:, 0], 1), np.percentile(Zcv[:, 0], 99.5)
ylo, yhi = min(np.percentile(Zcv[:, 1], 0.5), np.percentile(Zdr[:, 1], 3)), np.percentile(Zdr[:, 1], 99.5)
padx, pady = 0.05 * (xhi - xlo), 0.10 * (yhi - ylo)
P0 = proj(np.stack(det0.prototypes)); P1 = proj(np.stack(det1.prototypes))
thumb = np.asarray(Image.open(b.paths()[i_s]).convert("RGB").resize((64, 64)))
gap = 0.10; pw = (W - 0.10 - gap) / 2; ph = 0.98; y0p = 0.42
def embed_panel(x0, title, note, tcol, members_Z, member_alpha, member_shifted, proto_Z, proto_marker, proto_col, sp, verdict, vcol):
    a = fig.add_axes([x0 / W, y0p / H, pw / W, ph / H]); a.set_xlim(xlo - padx, xhi + padx); a.set_ylim(ylo - pady, yhi + pady)
    a.set_xticks([]); a.set_yticks([]); a.set_facecolor(PANEL)
    for sp_ in a.spines.values(): sp_.set_edgecolor(tcol); sp_.set_linewidth(0.9 if tcol == ACC else 0.6)
    for m, col in [(idm & (lab == 0), NORM), (idm & (lab == 1), DR), (cov, UWF)]:
        Z = proj(E[m]); a.scatter(Z[:, 0], Z[:, 1], s=2.0, c=col, alpha=0.14, lw=0, zorder=1)
    for z, al, shf in zip(members_Z, member_alpha, member_shifted):
        col = UWF if shf else DR
        if al < 0: a.scatter(*z, s=9, facecolors="white", edgecolors=col, lw=0.55, alpha=0.95, zorder=3)
        else: a.scatter(*z, s=9, c=col, alpha=min(1, 0.45 + 0.55 * al), lw=0.25, edgecolors="white", zorder=3)
    a.scatter(*proto_Z, s=95 if proto_marker == "*" else 44, marker=proto_marker, c=proto_col, edgecolors="white", lw=0.6, zorder=6)
    a.plot([Zs[0], proto_Z[0]], [Zs[1], proto_Z[1]], ls=(0, (1.2, 1.2)), lw=0.85, c=INK, zorder=5)
    a.scatter(*Zs, s=34, facecolors="none", edgecolors=INK, lw=1.0, zorder=7)
    ab = AnnotationBbox(OffsetImage(thumb, zoom=0.19), Zs, xybox=(0.915, 0.78), boxcoords="axes fraction", frameon=True,
                        bboxprops=dict(ec=UWF, lw=0.9, boxstyle="square,pad=0.05"), arrowprops=dict(arrowstyle="-", color=UWF, lw=0.6), zorder=8)
    a.add_artist(ab)
    # title and one-line note above the panel, verdict below it (all outside the plot)
    txt(x0, y0p + ph + 0.20, title, size=6.1, weight="bold", color=tcol, ha="left")
    txt(x0, y0p + ph + 0.075, note, size=5.25, color=tcol if tcol == ACC else MUTED, ha="left")
    t = txt(x0, y0p - 0.115, verdict, size=5.6, weight="bold", color="white", ha="left", bbox=dict(boxstyle="round,pad=0.26", fc=vcol, ec="none"))
    fig.canvas.draw(); wv = t.get_window_extent().width / fig.dpi
    txt(x0 + wv + 0.08, y0p - 0.115, f"prototype distance $S_{{\\mathrm{{proto}}}}$ = {sp:.2f}", size=5.5, color=INK, ha="left")
    return a
med_id = np.median(w1[~sh1]); alpha1 = np.where(w1 < 0.15 * med_id, -1.0, np.clip(w1 / w1[~sh1].max(), 0, 1))
embed_panel(0.05, "PROTON: plain-mean prototype", f"{sh0.mean():.0%} of the queue is shifted, the mean (✕) drifts toward it", "#4B5563",
            proj(M0), np.ones(len(M0)), sh0, P0[1], "X", "#4B5563", sp0, "missed", "#6B7280")
embed_panel(0.05 + pw + gap, "PROTON+: domain-anchored prototype", f"① shifted members keep {share_w_shifted:.0%} of the weight, ★ stays on DR", ACC,
            proj(M1), alpha1, sh1, P1[1], "*", ACC, sp1, "flagged as OOD", "#B42318")
# legend row
items = [("o", NORM, "normal (ID)"), ("o", DR, "DR (ID)"), ("o", UWF, "ultra-widefield (shifted)"), ("X", "#4B5563", "PROTON prototype"), ("*", ACC, "PROTON+ prototype"), ("hollow", UWF, "≈0 anchor weight")]
x = 0.08
for mk, col, name in items:
    if mk == "hollow": ax.scatter(x, 0.07, s=12, marker="o", facecolors="white", edgecolors=col, lw=0.6, zorder=9)
    else: ax.scatter(x, 0.07, s=12 if mk != "*" else 30, marker=mk, c=col, edgecolors="white", lw=0.6, zorder=9)
    t = txt(x + 0.055, 0.07, name, size=5.2, color=MUTED, ha="left"); fig.canvas.draw()
    x += 0.055 + t.get_window_extent().width / fig.dpi + 0.13
for ext in ("pdf", "svg", "png"):
    fig.savefig(OUT + "." + ext, dpi=400 if ext == "png" else None, bbox_inches="tight", pad_inches=0.01)
print("written", OUT)
