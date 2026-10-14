"""Refresh the results block of README.md (between the RESULTS markers) from outputs/results."""
import json, os, re
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..")); R = os.path.join(ROOT, "outputs", "results")
SH = ("semantic", "covariate", "far"); B = {"ophthalmology": "Ophthalmology · FLAIR", "radiology": "Radiology · UniMed-CLIP", "pathology": "Pathology · QuiltNet"}
PLUS = "+ domain-anchored prototypes (PROTON+)"
lines = ["| Benchmark (VLM) | Method | Semantic | Covariate | Far-OOD |", "|---|---|---|---|---|"]
for b, n in B.items():
    t2 = json.load(open(f"{R}/{b}/table2_main.json")); pp = json.load(open(f"{R}/{b}/table_proton_plus.json"))["variants"]
    for name, r in [("MCM", t2["static"]["mcm"]), ("PROTON", t2["proton"]), ("**PROTON+**", pp[PLUS])]:
        cells = [f"{r[s]['auroc']:.1f}" + (f" ± {r[s]['auroc_std']:.1f}" if "auroc_std" in r[s] else "") for s in SH]
        lines.append(f"| {n} | {name} | " + " | ".join(("**" + c + "**") if name.startswith("**") else c for c in cells) + " |")
block = "\n".join(lines)
p = os.path.join(ROOT, "README.md"); s = open(p).read()
s = re.sub(r"<!-- RESULTS:START -->.*?<!-- RESULTS:END -->", "<!-- RESULTS:START -->\n" + block + "\n<!-- RESULTS:END -->", s, flags=re.S)
open(p, "w").write(s); print("README results block refreshed")
