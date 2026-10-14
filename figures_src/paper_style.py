"""Shared visual style for every data figure of the PROTON+ preprint, matched to the TikZ method figure (Fig. 1).

Import first:  from paper_style import *   (adds rcParams, palette, and helpers)
Rules
* Final width = LNCS text width: FULL_W = 4.80 in (12.2 cm). Choose the height for the content; multi-panel rows are
  typically 1.45-1.9 in tall (aspect 2.5-3.3 : 1). Never taller than 3.0 in.
* Font: Liberation Sans (metric clone of Helvetica, as in Fig. 1). Sizes at final width: ticks 6, labels 6.5,
  panel titles 7 (semibold), annotations >= 5.6. Nothing below 5.5 pt.
* Encodings (identical in every figure): PROTON+ = accent orange solid line + filled star; PROTON = dark grey solid line +
  circle; MCM = light grey dashed line (no markers); oracle / reference = thin black dotted. Shift types: normal blue,
  DR green, ultra-widefield red, semantic amber, far grey.
* Axes: left/bottom spines only (0.6 pt, LINE colour), light horizontal grid, outward ticks, better-direction arrow in
  metric labels ("AUROC (%) ↑", "FPR@95 ↓"). Panel titles "(a) short title" left-aligned. Frameless legends, shared once.
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
FULL_W = 4.80
INK, MUTE, LINE, GRID = "#1F2328", "#6B7280", "#9AA1AB", "#E8EAEE"
ACC, ACC_SOFT = "#D55E00", "#FDF0E6"
C_NORMAL, C_DR, C_UWF, C_SEM, C_FAR = "#3B7DD8", "#2E9E5B", "#D64545", "#E69F00", "#8A9099"
C_PROTON, C_MCM = "#4B5563", "#A3A9B2"
MOD_COL = {"ophthalmology": "#3B7DD8", "radiology": "#B07A00", "pathology": "#8E5681"}   # per-modality hues (if needed)
SHIFT_COL = {"semantic": C_SEM, "covariate": C_UWF, "far": C_FAR}

import glob as _glob
for _f in _glob.glob(os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts", "LiberationSans-*.ttf")):
    try: font_manager.fontManager.addfont(_f)
    except Exception: pass

def _font():
    names = {f.name for f in font_manager.fontManager.ttflist}
    for n in ("Liberation Sans", "Arial", "Helvetica", "DejaVu Sans"):
        if n in names:
            return n
    return "DejaVu Sans"

plt.rcParams.update({
    "font.family": _font(), "font.size": 6.5, "axes.titlesize": 7, "axes.titleweight": "semibold", "axes.titlelocation": "left",
    "axes.titlepad": 4, "axes.labelsize": 6.5, "axes.labelcolor": INK, "xtick.labelsize": 6, "ytick.labelsize": 6,
    "xtick.color": MUTE, "ytick.color": MUTE, "axes.edgecolor": LINE, "axes.linewidth": 0.6, "axes.spines.top": False,
    "axes.spines.right": False, "axes.grid": True, "axes.grid.axis": "y", "grid.color": GRID, "grid.linewidth": 0.5,
    "axes.axisbelow": True, "xtick.major.size": 2, "ytick.major.size": 2, "xtick.major.width": 0.6, "ytick.major.width": 0.6,
    "xtick.direction": "out", "ytick.direction": "out", "legend.fontsize": 6, "legend.frameon": False, "legend.handlelength": 1.6,
    "legend.borderaxespad": 0.2, "lines.linewidth": 1.1, "lines.markersize": 4, "pdf.fonttype": 42, "ps.fonttype": 42,
    "svg.fonttype": "none", "mathtext.fontset": "custom", "mathtext.rm": _font(), "mathtext.it": _font() + ":italic",
    "mathtext.bf": _font() + ":bold", "figure.dpi": 150, "savefig.dpi": 300, "text.color": INK,
})

def style_proton_plus(**kw): return dict(color=ACC, lw=1.3, marker="*", ms=6.5, mec="white", mew=0.4, zorder=4, **kw)
def style_proton(**kw): return dict(color=C_PROTON, lw=1.0, marker="o", ms=3, mec="white", mew=0.3, zorder=3, **kw)
def style_mcm(**kw): return dict(color=C_MCM, lw=1.0, ls=(0, (3, 2)), zorder=2, **kw)

def save(fig, name, docs=True):
    """Write paper/figures/<name>.pdf|png|svg (+ docs/figures/<name>.png|svg)."""
    out = os.path.join(ROOT, "paper", "figures", name)
    os.makedirs(os.path.dirname(out), exist_ok=True); os.makedirs(os.path.join(ROOT, "docs", "figures"), exist_ok=True)
    for ext in ("pdf", "svg", "png"):
        fig.savefig(f"{out}.{ext}", bbox_inches="tight", pad_inches=0.01)
    if docs:
        for ext in ("png", "svg"):
            fig.savefig(os.path.join(ROOT, "docs", "figures", f"{name}.{ext}"), bbox_inches="tight", pad_inches=0.01)
    return out

def preview(name, dpi=330):
    """Render the saved PDF at print size to outputs/fig_preview/<name>.png for visual QA; returns the path and size."""
    import fitz
    d = fitz.open(os.path.join(ROOT, "paper", "figures", f"{name}.pdf")); r = d[0].rect
    os.makedirs(os.path.join(ROOT, "outputs", "fig_preview"), exist_ok=True)
    p = os.path.join(ROOT, "outputs", "fig_preview", f"{name}.png"); d[0].get_pixmap(dpi=dpi).save(p)
    return p, (round(r.width / 72, 2), round(r.height / 72, 2))
