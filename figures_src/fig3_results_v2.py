"""Fig. 3 (fig3_results), compact redesign in the shared paper style.

(a) Covariate AUROC against the ID fraction of the stream: PROTON+ (solid, stars, +-1 SD band) and MCM (dashed), one hue
    per modality, chance line, shaded region without an ID majority.
(b) Covariate AUROC of PROTON+ against the gate gamma, MCM as dashed reference, default gamma = 0.7 marked once.
(c) Shifted share of the most contaminated class bank on the covariate stream, PROTON -> PROTON+ (slope chart).
Shared y scale for (a) and (b), equal plot areas, one shared legend row.
Data (render level): outputs/results/<benchmark>/table_proton_plus.json ("rho", "gamma"),
outputs/results/<benchmark>/table2_main.json (static MCM), outputs/results/contamination_stats.json.
"""
import json
import os
import sys

sys.path.insert(0, "/mnt/hdd2/Abhijit/projects/PROTON/figures_src")
from paper_style import *  # noqa: F401,F403  (rcParams, palette, encodings, save, preview)
from paper_style import ROOT, FULL_W, INK, MUTE, LINE, GRID, MOD_COL, C_PROTON, style_proton_plus, style_proton, save, preview

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch, Rectangle
from matplotlib.legend_handler import HandlerPatch

R = os.path.join(ROOT, "outputs", "results")
MODS = ["ophthalmology", "radiology", "pathology"]
NAME = {"ophthalmology": "Ophthalmology", "radiology": "Radiology", "pathology": "Pathology"}
ANN = 5.6  # annotation font size (pt)


def load(p):
    with open(p) as f:
        return json.load(f)


# ---------------------------------------------------------------- data
rho, gam, mcm_static, bank = {}, {}, {}, {}
cs = load(os.path.join(R, "contamination_stats.json"))
for b in MODS:
    t = load(os.path.join(R, b, "table_proton_plus.json"))
    rs = sorted(float(k) for k in t["rho"])
    rho[b] = dict(x=np.array([100 * r for r in rs]),
                  pp=np.array([t["rho"][str(r)]["proton_plus"]["covariate"]["auroc"] for r in rs]),
                  pp_sd=np.array([t["rho"][str(r)]["proton_plus"]["covariate"]["auroc_std"] for r in rs]),
                  mcm=np.array([t["rho"][str(r)]["mcm"]["covariate"]["auroc"] for r in rs]),
                  mcm_sd=np.array([t["rho"][str(r)]["mcm"]["covariate"]["auroc_std"] for r in rs]))
    gs = sorted(float(k) for k in t["gamma"])
    gam[b] = dict(x=np.array(gs),
                  pp=np.array([t["gamma"][str(g)]["covariate"]["auroc"] for g in gs]),
                  pp_sd=np.array([t["gamma"][str(g)]["covariate"]["auroc_std"] for g in gs]))
    mcm_static[b] = load(os.path.join(R, b, "table2_main.json"))["static"]["mcm"]["covariate"]["auroc"]
    bank[b] = (100 * max(cs[b]["covariate"]["bank_ood_frac"]), 100 * max(cs[b]["covariate"]["bank_ood_frac_plus"]))
G_DEF = 0.7  # default gate (experiments.tex: gamma = 0.7)

# ---------------------------------------------------------------- numbers for the caption
print("(a) PROTON+ - MCM covariate AUROC per ID fraction:")
for b in MODS:
    d = rho[b]
    print(f"   {b:13s}", "  ".join(f"{x:.0f}%: {p:5.1f}-{m:5.1f}={p - m:+5.1f}" for x, p, m in zip(d["x"], d["pp"], d["mcm"])))
print("   max SD PROTON+ %.1f, max SD MCM %.1f" % (max(rho[b]["pp_sd"].max() for b in MODS), max(rho[b]["mcm_sd"].max() for b in MODS)))
print("(b) PROTON+ covariate AUROC over gamma; static MCM:")
for b in MODS:
    d = gam[b]; lo = d["x"] <= G_DEF
    print(f"   {b:13s}", "  ".join(f"{x:.1f}: {v:5.1f}+-{s:4.1f}" for x, v, s in zip(d["x"], d["pp"], d["pp_sd"])),
          f"| range on [0.5,0.7] = {np.ptp(d['pp'][lo]):.1f} | MCM {mcm_static[b]:.1f}")
lead90 = [rho[b]["pp"][-1] - rho[b]["mcm"][-1] for b in MODS]
print("   caption: PROTON+ lead over MCM at ID fraction %.0f%%: %.1f to %.1f points" % (rho[MODS[0]]["x"][-1], min(lead90), max(lead90)))
print("   caption: below chance (AUROC < 50) at some ID fraction <= 50%:",
      [b for b in MODS if (rho[b]["pp"][rho[b]["x"] <= 50] < 50).any()])
print("   caption: max PROTON+ range over gamma <= %.1f: %.1f points" % (G_DEF, max(np.ptp(gam[b]["pp"][gam[b]["x"] <= G_DEF]) for b in MODS)))
print("(c) shifted share of most contaminated bank, PROTON -> PROTON+:")
for b in MODS:
    print(f"   {b:13s} {bank[b][0]:.1f} -> {bank[b][1]:.1f}")

# ---------------------------------------------------------------- layout (inches)
W, H = FULL_W, 1.64
L, GAP_AB, GAP_BC, RM = 0.36, 0.13, 0.36, 0.02    # left margin, gaps, right margin
BOT, PH = 0.30, 1.04                               # bottom margin, plot height
PW = (W - L - GAP_AB - GAP_BC - RM) / 3            # equal plot width
fig = plt.figure(figsize=(W, H))
x0 = [L, L + PW + GAP_AB, L + 2 * PW + GAP_AB + GAP_BC]
axes = [fig.add_axes([x / W, BOT / H, PW / W, PH / H]) for x in x0]
ax_a, ax_b, ax_c = axes

YLAB = "Covariate AUROC (%) ↑"
BAND = 0.13

# ---------------------------------------------------------------- (a) ID fraction
ax = ax_a
ax.axvspan(0, 50, color=GRID, alpha=0.55, lw=0, zorder=0)
ax.text(7, 97, "no ID majority", fontsize=ANN, color=MUTE, ha="left", va="top")
ax.axhline(50, color=LINE, lw=0.6, ls=(0, (1, 1.5)), zorder=1)
ax.text(93, 51.5, "chance", fontsize=ANN, color=MUTE, ha="right", va="bottom")
for b in MODS:
    d, c = rho[b], MOD_COL[b]
    ax.fill_between(d["x"], d["pp"] - d["pp_sd"], np.minimum(d["pp"] + d["pp_sd"], 100), color=c, alpha=BAND, lw=0, zorder=2)
    ax.plot(d["x"], d["mcm"], color=c, lw=0.9, ls=(0, (3, 2)), alpha=0.85, zorder=3)
    ax.plot(d["x"], d["pp"], **{**style_proton_plus(), "color": c, "ms": 5.5})
ax.set_xlim(5, 95); ax.set_xticks([10, 30, 50, 70, 90])
ax.set_xlabel("ID fraction of the stream (%)")
ax.set_ylabel(YLAB)
ax.set_title("(a) stream composition")

# ---------------------------------------------------------------- (b) gate gamma
ax = ax_b
ax.axvline(G_DEF, color=LINE, lw=0.6, ls=(0, (1, 1.5)), zorder=1)
ax.text(G_DEF + 0.012, 3, "default", fontsize=ANN, color=MUTE, ha="left", va="bottom")
for b in MODS:
    d, c = gam[b], MOD_COL[b]
    ax.axhline(mcm_static[b], color=c, lw=0.9, ls=(0, (3, 2)), alpha=0.85, zorder=3)
    ax.fill_between(d["x"], d["pp"] - d["pp_sd"], np.minimum(d["pp"] + d["pp_sd"], 100), color=c, alpha=BAND, lw=0, zorder=2)
    ax.plot(d["x"], d["pp"], **{**style_proton_plus(), "color": c, "ms": 5.5})
ax.set_xlim(0.47, 0.93); ax.set_xticks([0.5, 0.6, 0.7, 0.8, 0.9])
ax.set_xlabel("Gate γ")
ax.tick_params(axis="y", labelleft=False)
ax.set_title("(b) confidence gate")

for ax in (ax_a, ax_b):
    ax.set_ylim(0, 102); ax.set_yticks([0, 25, 50, 75, 100])

# ---------------------------------------------------------------- (c) bank contamination (slope chart)
ax = ax_c
for b in MODS:
    p0, p1 = bank[b]; c = MOD_COL[b]
    ax.plot([0, 1], [p0, p1], color=c, lw=1.1, zorder=2)
    ax.plot([0], [p0], **{**style_proton(), "ms": 4.2})
    ax.plot([1], [p1], **{**style_proton_plus(), "color": c, "ms": 6.5})
# value labels, nudged apart where they would touch
def place(vals, gap):
    order = np.argsort(vals); out = np.array(vals, float)
    for i in range(1, len(order)):
        if out[order[i]] - out[order[i - 1]] < gap:
            out[order[i]] = out[order[i - 1]] + gap
    return out
left = place([bank[b][0] for b in MODS], 6.0); right = place([bank[b][1] for b in MODS], 6.0)
for b, yl, yr in zip(MODS, left, right):
    ax.text(-0.13, yl, f"{bank[b][0]:.0f}", fontsize=ANN, color=C_PROTON, ha="right", va="center")
    ax.text(1.13, yr, f"{bank[b][1]:.0f}", fontsize=ANN, color=MOD_COL[b], ha="left", va="center")
ax.set_xlim(-0.5, 1.5); ax.set_xticks([0, 1]); ax.set_xticklabels(["PROTON", "PROTON+"])
ax.tick_params(axis="x", length=0)
ax.set_ylim(-4, 70); ax.set_yticks([0, 20, 40, 60])
ax.set_ylabel("Shifted share (%) ↓")
ax.set_title("(c) bank contamination")

# ---------------------------------------------------------------- shared legend row
h = [Line2D([], [], **{**style_proton_plus(), "color": INK, "ms": 5.5}),
     Line2D([], [], color=INK, lw=0.9, ls=(0, (3, 2))),
     Line2D([], [], **{**style_proton(), "ms": 4.2}),
     Patch(color=MOD_COL["ophthalmology"], lw=0), Patch(color=MOD_COL["radiology"], lw=0), Patch(color=MOD_COL["pathology"], lw=0)]
lab = ["PROTON+ (ours)", "MCM", "PROTON", NAME["ophthalmology"], NAME["radiology"], NAME["pathology"]]
def _square(legend, orig_handle, xdescent, ydescent, width, height, fontsize):   # modality key: a small square next to its label, not a wide bar
    s, xd, yd, w, h = 0.8 * fontsize, xdescent, ydescent, width, height
    return Rectangle((-xd + w - s, -yd + (h - s) / 2), s, s)
fig.legend(h, lab, loc="upper center", bbox_to_anchor=(0.5, 1.0), ncol=6, handlelength=1.8, columnspacing=1.0,
           handletextpad=0.45, borderaxespad=0, handler_map={Patch: HandlerPatch(patch_func=_square)})

save(fig, "fig3_results")
try:
    p, size = preview("fig3_results")
except ModuleNotFoundError:  # PyMuPDF missing in this env: same rasterisation through another interpreter
    import subprocess
    code = ("import fitz,os,sys; r=sys.argv[1]; d=fitz.open(os.path.join(r,'paper','figures','fig3_results.pdf')); q=d[0].rect;"
            "o=os.path.join(r,'outputs','fig_preview'); os.makedirs(o,exist_ok=True); p=os.path.join(o,'fig3_results.png');"
            "d[0].get_pixmap(dpi=330).save(p); print(p, round(q.width/72,2), round(q.height/72,2))")
    out = subprocess.run([os.environ.get("FITZ_PY", "/home/mbz-imran/miniconda3/bin/python"), "-c", code, ROOT],
                         capture_output=True, text=True, check=True).stdout.split()
    p, size = out[0], (float(out[1]), float(out[2]))
print("preview", p, size)
