"""Print every quantity the manuscript prose cites, computed from outputs/results (run after `proton run`)."""
import json, os
import numpy as np
R = "outputs/results"; SH = ("semantic", "covariate", "far"); B = ["ophthalmology", "radiology", "pathology"]
def L(b, n): return json.load(open(f"{R}/{b}/{n}.json"))
print("== main deltas (raw values) ==")
for b in B:
    t2 = L(b, "table2_main"); pp = L(b, "table_proton_plus")["variants"]
    mcm, pro, plus = t2["static"]["mcm"], t2["proton"], pp["+ domain-anchored prototypes (PROTON+)"]
    print(b, "MCM", [round(mcm[s]["auroc"], 2) for s in SH], "| PROTON", [f"{pro[s]['auroc']:.2f}±{pro[s]['auroc_std']:.2f}" for s in SH],
          "| PROTON+", [f"{plus[s]['auroc']:.2f}±{plus[s]['auroc_std']:.2f}" for s in SH])
    print("   dPROTON-MCM", [round(pro[s]["auroc"] - mcm[s]["auroc"], 2) for s in SH], " dPLUS-MCM", [round(plus[s]["auroc"] - mcm[s]["auroc"], 2) for s in SH],
          " dPLUS-PROTON", [round(plus[s]["auroc"] - pro[s]["auroc"], 2) for s in SH])
    print("   FPR MCM/PROTON/PLUS", [(round(mcm[s]["fpr95"], 1), round(pro[s]["fpr95"], 1), f"{plus[s]['fpr95']:.1f}±{plus[s]['fpr95_std']:.1f}") for s in SH])
    print("   per-seed PROTON auroc range", [(round(min(r["auroc"] for r in pro[s]["per_seed"]), 1), round(max(r["auroc"] for r in pro[s]["per_seed"]), 1)) for s in SH])
    for k in ["+ z-scored fusion", "+ consistency admission", "S_proto only (PROTON+ bank)", "PROTON+, oracle ID-only bank", "PROTON, oracle ID-only bank", "PROTON+ max-fusion", "PROTON+ rejection-driven alpha"]:
        print(f"   {k:32s}", [f"{pp[k][s]['auroc']:.1f}±{pp[k][s]['auroc_std']:.1f}" for s in SH], "t_calib", pp[k]["covariate"].get("t_calib"))
    ex = L(b, "robustness_extras"); print("   cost ms PROTON/PLUS", round(ex["overhead"]["ms_per_sample"], 3), round(ex["overhead"]["ms_per_sample_plus"], 3), "wins", ex["wins_vs_mcm"], "triage", round(ex["triage_macro_f1"], 2) if isinstance(ex["triage_macro_f1"], float) else ex["triage_macro_f1"])
    print("   sigma sweep", {k: round(v["mean_auroc"], 1) for k, v in ex["sigma2_0"].items()})
    t3 = L(b, "table3_ablation"); c = t3["components"]; print("   ablation cov: adapt-nogate vs full", round(c["+ Adapt. fusion"]["covariate"]["auroc"] - c["+ Conf. gate (Full)"]["covariate"]["auroc"], 2))
    g = L(b, "table_proton_plus"); print("   gamma PLUS", {k: [round(v[s]["auroc"], 1) for s in SH] for k, v in g["gamma"].items()}); print("   kappa PLUS", {k: [round(v[s]["auroc"], 1) for s in SH] for k, v in g["kappa"].items()})
    print("   t_calib per shift (PROTON)", {s: round(t2["proton"][s]["t_calib"], 1) for s in SH})
    ps = L(b, "table_prompt_sensitivity"); print("   prompts:", {k: (round(100 * v["id_acc"], 1), [round(v["mcm"][s]["auroc"], 1) for s in SH], [round(v["proton"][s]["auroc"], 1) for s in SH], [round(v["proton_plus"][s]["auroc"], 1) for s in SH]) for k, v in ps.items()})
e = json.load(open(f"{R}/extra_stats.json")); print("== extra ==", json.dumps(e["best_static"]), json.dumps(e["variance_alpha"]), json.dumps(e["t_calib"]))
bw = json.load(open(f"{R}/bandwidth_sweep.json")); print("== bandwidth ==", {b: {h: [round(v[s], 1) for s in SH] for h, v in bw[b].items()} for b in bw})
