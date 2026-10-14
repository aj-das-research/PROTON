"""Turn outputs/results/<benchmark>/*.json into LaTeX table bodies under paper/tables/ (booktabs, no copying of
paper numbers: everything comes from the JSON written by `proton run`)."""
import json, os
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
RES = os.path.join(ROOT, "outputs", "results"); OUT = os.path.join(ROOT, "paper", "tables"); os.makedirs(OUT, exist_ok=True)
SH = ("semantic", "covariate", "far")
PRETTY = {"max_logit": "Max-Logits", "energy": "Energy", "gl_mcm": "GL-MCM", "mcm": "MCM", "entropy": "Entropy", "tag_mcm": "TAG-MCM",
          "hier_l1": "MCM (L=1)$^\\dagger$", "hier_l5": "MCM (L=5)$^\\dagger$", "knn_id": "kNN-ID$^\\ddagger$", "mahalanobis_id": "Mahalanobis-ID$^\\ddagger$",
          "proton": "PROTON", "hier_l5+proton": "MCM (L=5) + PROTON"}
BENCH = {"ophthalmology": "Ophthalmology (FLAIR)", "radiology": "Radiology (UniMed-CLIP)", "pathology": "Pathology (QuiltNet)"}

def load(b, name):
    p = os.path.join(RES, b, name + ".json")
    return json.load(open(p)) if os.path.exists(p) else None

def f1(x): return f"{x:.1f}"
def fpm(r, sh, m):
    """value ± SD when the record carries a std (online detectors), else the value (static scores)."""
    return f"{r[sh][m]:.1f}" + (f"\\,$\\pm$\\,{r[sh][m + '_std']:.1f}" if (m + "_std") in r[sh] else "")

def bold_best(vals, higher=True):
    order = sorted(range(len(vals)), key=lambda i: (-vals[i] if higher else vals[i]))
    out = [f1(v) for v in vals]
    if len(order) > 0: out[order[0]] = "\\best{" + out[order[0]] + "}"
    if len(order) > 1: out[order[1]] = "\\second{" + out[order[1]] + "}"
    return out

def main_table(b, pm=True):
    d = load(b, "table2_main"); pp = load(b, "table_proton_plus")
    if d is None: return
    rows = []
    for name in ["max_logit", "energy", "gl_mcm", "mcm", "tag_mcm", "hier_l1", "hier_l5"]:
        if name in d["static"]: rows.append((PRETTY[name], d["static"][name]))
    rows.append(("PROTON~\\cite{das2026proton}", d["proton"]))
    if pp: rows.append(("\\protonp (ours)", pp["variants"]["+ domain-anchored prototypes (PROTON+)"] if "+ domain-anchored prototypes (PROTON+)" in pp["variants"] else pp["variants"][list(pp["variants"])[-1]]))
    cols = []
    for sh in SH:
        for m, hi in (("auroc", True), ("aupr", True), ("fpr95", False)):
            col = bold_best([r[1][sh][m] for r in rows], hi)
            if pm:
                col = [c + (f"\\,$\\pm$\\,{r[1][sh][m + '_std']:.1f}" if m + "_std" in r[1][sh] else "") for c, r in zip(col, rows)]
            cols.append(col)
    lines = ["\\begin{tabular}{l" + "ccc" * 3 + "}", "\\toprule",
             " & \\multicolumn{3}{c}{Semantic} & \\multicolumn{3}{c}{Covariate} & \\multicolumn{3}{c}{Far-OOD} \\\\",
             "\\cmidrule(lr){2-4}\\cmidrule(lr){5-7}\\cmidrule(lr){8-10}",
             "Method & AUC$\\uparrow$ & APR$\\uparrow$ & FPR$\\downarrow$ & AUC$\\uparrow$ & APR$\\uparrow$ & FPR$\\downarrow$ & AUC$\\uparrow$ & APR$\\uparrow$ & FPR$\\downarrow$ \\\\", "\\midrule"]
    for i, (name, _) in enumerate(rows):
        if name.startswith("PROTON~"): lines.append("\\midrule")
        lines.append(name + " & " + " & ".join(c[i] for c in cols) + " \\\\")
    mcm = d["static"]["mcm"]; last = rows[-1][1]
    delta = []
    for sh in SH:
        for m in ("auroc", "aupr", "fpr95"):
            v = last[sh][m] - mcm[sh][m]
            better = (v >= 0) == (m != "fpr95")
            delta.append(("\\dpos{" if better else "\\dneg{") + f"{v:+.1f}" + "}")
    lines += ["\\midrule", "$\\Delta$ \\protonp vs.\\ MCM & " + " & ".join(delta) + " \\\\", "\\bottomrule", "\\end{tabular}"]
    open(os.path.join(OUT, f"main_{b}{'' if pm else '_nopm'}.tex"), "w").write("\n".join(lines) + "\n")

def cross_domain():
    lines = ["\\begin{tabular}{llrrr|rrr|rrr}", "\\toprule",
             " & & \\multicolumn{3}{c|}{Semantic} & \\multicolumn{3}{c|}{Covariate} & \\multicolumn{3}{c}{Far-OOD} \\\\",
             "Domain (VLM) & Method & AUROC & AUPR & FPR@95 & AUROC & AUPR & FPR@95 & AUROC & AUPR & FPR@95 \\\\", "\\midrule"]
    for b in BENCH:
        d = load(b, "table2_main"); pp = load(b, "table_proton_plus")
        if d is None: continue
        rs = [("MCM", d["static"]["mcm"]), ("PROTON", d["proton"])]
        if pp: rs.append(("\\protonp", pp["variants"]["+ domain-anchored prototypes (PROTON+)"]))
        for k, (n, r) in enumerate(rs):
            lead = ("\\multirow{%d}{*}{%s}" % (len(rs), BENCH[b])) if k == 0 else ""
            lines.append(lead + " & " + n + " & " + " & ".join(fpm(r, sh, m) for sh in SH for m in ("auroc", "aupr", "fpr95")) + " \\\\")
        lines.append("\\midrule")
    lines[-1] = "\\bottomrule"; lines.append("\\end{tabular}")
    open(os.path.join(OUT, "cross_domain.tex"), "w").write("\n".join(lines) + "\n")

def ablation(b):
    d = load(b, "table3_ablation"); pp = load(b, "table_proton_plus")
    if d is None: return
    lines = ["\\begin{tabular}{lccc}", "\\toprule", "Variant & Sem & Cov & Far \\\\", "\\midrule"]
    for k, r in d["components"].items():
        lines.append(k.replace("alpha", "$\\alpha$").replace("Proto.", "Proto.") + " & " + " & ".join(f1(r[sh]["auroc"]) for sh in SH) + " \\\\")
    if pp:
        lines.append("\\midrule")
        for k in ["+ z-scored fusion", "+ consistency admission", "+ domain-anchored prototypes (PROTON+)"]:
            if k in pp["variants"]:
                lab = {"+ z-scored fusion": "PROTON + z-scored fusion", "+ consistency admission": "~~+ consistency admission",
                       "+ domain-anchored prototypes (PROTON+)": "~~+ domain-anchored prototypes (\\protonp)"}[k]
                lines.append(lab + " & " + " & ".join(f1(pp["variants"][k][sh]["auroc"]) for sh in SH) + " \\\\")
    lines += ["\\bottomrule", "\\end{tabular}"]
    open(os.path.join(OUT, f"ablation_{b}.tex"), "w").write("\n".join(lines) + "\n")
    # gamma / M
    lines = ["\\begin{tabular}{lccc|lccc}", "\\toprule", "$\\gamma$ & AUC & APR & F95 & $M$ & AUC & APR & F95 \\\\", "\\midrule"]
    gs, Ms = list(d["gamma"].items()), list(d["M"].items())
    for i in range(max(len(gs), len(Ms))):
        g = gs[i] if i < len(gs) else None; M = Ms[i] if i < len(Ms) else None
        lines.append((f"{g[0]} & " + " & ".join(f1(g[1][m]) for m in ("auroc", "aupr", "fpr95")) if g else " & & & ") + " & " +
                      (f"{M[0]} & " + " & ".join(f1(M[1][m]) for m in ("auroc", "aupr", "fpr95")) if M else " & & & ") + " \\\\")
    lines += ["\\bottomrule", "\\end{tabular}"]
    open(os.path.join(OUT, f"sensitivity_{b}.tex"), "w").write("\n".join(lines) + "\n")

def rho(b):
    d = load(b, "table_proton_plus")
    if d is None: return
    lines = ["\\begin{tabular}{lccc|ccc|ccc}", "\\toprule", " & \\multicolumn{3}{c|}{MCM} & \\multicolumn{3}{c|}{PROTON} & \\multicolumn{3}{c}{\\protonp} \\\\",
             "$\\rho$ & Sem & Cov & Far & Sem & Cov & Far & Sem & Cov & Far \\\\", "\\midrule"]
    for r_, r in d["rho"].items():
        lines.append(f"{100*float(r_):.0f}\\% & " + " & ".join(f1(r[k][sh]["auroc"]) for k in ("mcm", "proton", "proton_plus") for sh in SH) + " \\\\")
    lines += ["\\bottomrule", "\\end{tabular}"]
    open(os.path.join(OUT, f"rho_{b}.tex"), "w").write("\n".join(lines) + "\n")

def base_scores(b):
    d = load(b, "table4a_base_scores"); pp = load(b, "table_proton_plus")
    if d is None: return
    lines = ["\\begin{tabular}{lccc|ccc|ccc}", "\\toprule", " & \\multicolumn{3}{c|}{Base} & \\multicolumn{3}{c|}{+PROTON} & \\multicolumn{3}{c}{+\\protonp} \\\\",
             "Base score & Sem & Cov & Far & Sem & Cov & Far & Sem & Cov & Far \\\\", "\\midrule"]
    for k, r in d.items():
        if k == "entropy":   # identical to MCM for C=2
            continue
        plus = pp["bases"][k]["proton_plus"] if pp and k in pp.get("bases", {}) else None
        lines.append(PRETTY[k] + " & " + " & ".join(f1(r["base"][sh]["auroc"]) for sh in SH) + " & " + " & ".join(f1(r["proton"][sh]["auroc"]) for sh in SH) +
                     " & " + (" & ".join(f1(plus[sh]["auroc"]) for sh in SH) if plus else "-- & -- & --") + " \\\\")
    lines += ["\\bottomrule", "\\end{tabular}"]
    open(os.path.join(OUT, f"base_scores_{b}.tex"), "w").write("\n".join(lines) + "\n")

def broader(b):
    d = load(b, "table4b_broader"); pp = load(b, "table_proton_plus")
    if d is None: return
    lines = ["\\begin{tabular}{lccc}", "\\toprule", "Method & Sem & Cov & Far \\\\", "\\midrule"]
    for k, r in d.items():
        lines.append(PRETTY.get(k, k) + " & " + " & ".join(f1(r[sh]["auroc"]) for sh in SH) + " \\\\")
    if pp: lines.append("\\protonp (ours) & " + " & ".join(f1(pp["variants"]["+ domain-anchored prototypes (PROTON+)"][sh]["auroc"]) for sh in SH) + " \\\\")
    lines += ["\\bottomrule", "\\end{tabular}"]
    open(os.path.join(OUT, f"broader_{b}.tex"), "w").write("\n".join(lines) + "\n")

def ladder():
    """S_proto alone, PROTON+ and PROTON+ with oracle admission, per modality, with ± over stream orders."""
    rows = [("\\protonp", "+ domain-anchored prototypes (PROTON+)"), ("$\\sproto$ only (\\protonp bank)", "S_proto only (PROTON+ bank)"),
            ("\\protonp, oracle admission", "PROTON+, oracle ID-only bank")]
    short = {"ophthalmology": "Ophth.", "radiology": "Radio.", "pathology": "Patho."}
    lines = ["\\begin{tabular}{llrrr}", "\\toprule", "Modality & Variant & Sem & Cov & Far \\\\", "\\midrule"]
    for b in BENCH:
        pp = load(b, "table_proton_plus")
        if pp is None: continue
        for k, (lab, key) in enumerate(rows):
            lead = ("\\multirow{%d}{*}{%s}" % (len(rows), short[b])) if k == 0 else ""
            lines.append(lead + " & " + lab + " & " + " & ".join(fpm(pp["variants"][key], sh, "auroc") for sh in SH) + " \\\\")
        lines.append("\\midrule")
    lines[-1] = "\\bottomrule"; lines.append("\\end{tabular}")
    open(os.path.join(OUT, "ladder.tex"), "w").write("\n".join(lines) + "\n")


def prompts(b):
    d = load(b, "table_prompt_sensitivity")
    if d is None: return
    lines = ["\\begin{tabular}{lcccc}", "\\toprule", "Prompt set & ID acc. & MCM (Sem/Cov/Far) & PROTON & \\protonp \\\\", "\\midrule"]
    for ps, r in d.items():
        lines.append(ps.replace("_", "\\_") + f" & {100*r['id_acc']:.1f} & " + " / ".join(f1(r["mcm"][sh]["auroc"]) for sh in SH) + " & " +
                     " / ".join(f1(r["proton"][sh]["auroc"]) for sh in SH) + " & " + " / ".join(f1(r["proton_plus"][sh]["auroc"]) for sh in SH) + " \\\\")
    lines += ["\\bottomrule", "\\end{tabular}"]
    open(os.path.join(OUT, f"prompts_{b}.tex"), "w").write("\n".join(lines) + "\n")

if __name__ == "__main__":
    for b in BENCH:
        main_table(b); main_table(b, pm=False); ablation(b); rho(b); base_scores(b); broader(b); prompts(b)
    cross_domain(); ladder()
    print("tables written:", sorted(os.listdir(OUT)))
