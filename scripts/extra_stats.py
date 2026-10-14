"""Extra statistics the manuscript cites (written to outputs/results/extra_stats.json):
  - running MCM variance and fusion-weight ranges over all streams and five orders (PROTON defaults)
  - gains of PROTON+ over the best static score of each split
  - per-shift t_calib ranges
  - RSNA (ID) vs NIH-sample (semantic) near-duplicate check for the radiology benchmark (64x64 correlation)
"""
import glob, json, os
import numpy as np
from PIL import Image
from proton.data import load_benchmark
from proton.features import load_features
from proton.evaluate import prepare, run_proton_stream, evaluate_static, SHIFTS
from proton.streams import make_stream

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
out = {"variance_alpha": {}, "best_static": {}, "t_calib": {}}
STATIC = ["max_logit", "energy", "gl_mcm", "mcm", "tag_mcm", "hier_l1", "hier_l5"]
for b in ["ophthalmology", "radiology", "pathology"]:
    bench = load_benchmark(b); P = prepare(bench, load_features(b, bench.vlm))
    vmin = amin = 1.0; vmax = amax = 0.0; vmax_all = 0.0
    tc = {}
    for sh in SHIFTS:
        pool, n_id = P.pool(sh); tcs = []
        for seed in range(5):
            order, _ = make_stream(n_id, len(pool) - n_id, seed=seed)
            r = run_proton_stream(P, pool, order); m = r["calibrated"]
            vmin, vmax = min(vmin, r["var"][m].min()), max(vmax, r["var"][m].max()); vmax_all = max(vmax_all, r["var"][5:].max())
            amin, amax = min(amin, r["alpha"][m].min()), max(amax, r["alpha"][m].max()); tcs.append(r["detector"].t_calib)
        tc[sh] = {"mean": float(np.mean(tcs)), "min": int(min(tcs)), "max": int(max(tcs))}
    out["variance_alpha"][b] = {"var_calibrated": [float(vmin), float(vmax)], "var_max_after_5": float(vmax_all), "alpha": [float(amin), float(amax)]}
    out["t_calib"][b] = tc
    st = evaluate_static(P, names=[n for n in STATIC if n in P.base])
    pp = json.load(open(os.path.join(ROOT, "outputs", "results", b, "table_proton_plus.json")))["variants"]["+ domain-anchored prototypes (PROTON+)"]
    out["best_static"][b] = {}
    for sh in SHIFTS:
        best = max(st, key=lambda n: st[n][sh]["auroc"])
        out["best_static"][b][sh] = {"best": best, "auroc": st[best][sh]["auroc"], "proton_plus": pp[sh]["auroc"], "delta": pp[sh]["auroc"] - st[best][sh]["auroc"]}
# radiology duplicate check
bench = load_benchmark("radiology"); df = bench.manifest
def thumbs(paths):
    return np.stack([np.asarray(Image.open(os.path.join(ROOT, p)).convert("L").resize((64, 64)), np.float32).ravel() for p in paths])
A = thumbs(df[df.set == "id"].path); B = thumbs(df[df.set == "semantic"].path)
A = (A - A.mean(1, keepdims=True)) / (A.std(1, keepdims=True) + 1e-6); B = (B - B.mean(1, keepdims=True)) / (B.std(1, keepdims=True) + 1e-6)
C = A @ B.T / A.shape[1]
out["radiology_duplicates"] = {"n_id": int(A.shape[0]), "n_semantic": int(B.shape[0]), "max_corr": float(C.max()),
                               "pairs_corr_gt_0.95": int((C > 0.95).sum()), "pairs_corr_gt_0.9": int((C > 0.9).sum())}
json.dump(out, open(os.path.join(ROOT, "outputs", "results", "extra_stats.json"), "w"), indent=1)
print(json.dumps(out, indent=1))
