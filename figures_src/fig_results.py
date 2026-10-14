"""Results figure (house standard: ours = star, arrows on metric axes, ~6 pt labels at \\linewidth).
(a) covariate AUROC against the ID fraction of the stream, (b) PROTON+ covariate AUROC against the gate gamma,
(c) shifted share of the most contaminated class bank on the covariate stream, PROTON vs PROTON+.
All values from outputs/results (table_proton_plus.json, table2_main.json, contamination_stats.json)."""
import json, os, sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..")); R = os.path.join(ROOT, "outputs", "results")
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "paper", "figures", "fig3_results")
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 6, "axes.titlesize": 6.5, "axes.labelsize": 6, "legend.fontsize": 5.3,
                     "xtick.labelsize": 5.5, "ytick.labelsize": 5.5, "pdf.fonttype": 42, "ps.fonttype": 42, "svg.fonttype": "none", "axes.linewidth": 0.6})
B = {"ophthalmology": ("Ophthalmology", "#0072B2"), "radiology": ("Radiology", "#986C00"), "pathology": ("Pathology", "#8E5681")}
fig, axes = plt.subplots(1, 3, figsize=(4.8, 1.6), constrained_layout=True)
ax = axes[0]
for b, (lab, col) in B.items():
    d = json.load(open(f"{R}/{b}/table_proton_plus.json"))["rho"]; rhos = sorted(float(k) for k in d)
    ax.plot([100 * r for r in rhos], [d[str(r)]["proton_plus"]["covariate"]["auroc"] for r in rhos], "-", marker="*", ms=5.5, lw=1.0, color=col, label=f"{lab}: PROTON+ (ours)")
    ax.plot([100 * r for r in rhos], [d[str(r)]["mcm"]["covariate"]["auroc"] for r in rhos], "--", marker="o", ms=2.2, lw=0.8, color=col, alpha=0.75, label=f"{lab}: MCM")
ax.axhline(50, color="#999999", lw=0.5, ls=":"); ax.set_xlabel("ID fraction of the stream (%)"); ax.set_ylabel(r"covariate AUROC (%) $\uparrow$"); ax.set_title("(a) stream composition")
ax.set_xticks([10, 30, 50, 70, 90]); ax.set_ylim(0, 100); ax.legend(loc="lower right", frameon=False, handlelength=1.6, borderpad=0.2, labelspacing=0.15)
ax = axes[1]
for b, (lab, col) in B.items():
    g = json.load(open(f"{R}/{b}/table_proton_plus.json"))["gamma"]; gs = sorted(float(k) for k in g)
    ax.plot(gs, [g[str(x)]["covariate"]["auroc"] for x in gs], "-", marker="*", ms=5.5, lw=1.0, color=col, label=f"{lab}")
    mcm = json.load(open(f"{R}/{b}/table2_main.json"))["static"]["mcm"]["covariate"]["auroc"]
    ax.axhline(mcm, color=col, lw=0.7, ls="--", alpha=0.75)
    ax.plot([0.7], [g["0.7"]["covariate"]["auroc"]], marker="*", ms=8.5, color=col, mec="black", mew=0.4)
ax.set_xlabel(r"confidence gate $\gamma$ (large star: default)"); ax.set_ylabel(r"covariate AUROC (%) $\uparrow$"); ax.set_title("(b) gate; dashed: MCM")
ax.set_xticks([0.5, 0.6, 0.7, 0.8, 0.9]); ax.set_ylim(40, 100)
ax = axes[2]
cs = json.load(open(f"{R}/contamination_stats.json")); x = np.arange(len(B)); w = 0.36
pro = [100 * max(cs[b]["covariate"]["bank_ood_frac"]) for b in B]; plus = [100 * max(cs[b]["covariate"]["bank_ood_frac_plus"]) for b in B]
ax.bar(x - w / 2, pro, w, color="#5F6368", label="PROTON"); ax.bar(x + w / 2, plus, w, color="#D55E00", label="PROTON+ (ours)")
for xi, (a, c) in enumerate(zip(pro, plus)):
    ax.text(xi - w / 2, a + 1.5, f"{a:.0f}", ha="center", fontsize=5); ax.text(xi + w / 2, c + 1.5, f"{c:.0f}", ha="center", fontsize=5)
ax.set_xticks(x); ax.set_xticklabels([B[b][0] for b in B]); ax.set_ylabel(r"shifted share of class bank (%) $\downarrow$"); ax.set_title("(c) contamination, covariate stream")
ax.set_ylim(0, 80); ax.legend(frameon=False, loc="upper right", borderpad=0.2)
for a in axes:
    a.spines[["top", "right"]].set_visible(False)
for ext in ("pdf", "svg", "png"):
    fig.savefig(OUT + "." + ext, dpi=300 if ext == "png" else None, bbox_inches="tight", pad_inches=0.01)
print("written", OUT)
