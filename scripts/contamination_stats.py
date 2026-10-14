"""Bank-contamination statistics under the default protocol, averaged over five stream orders -> outputs/results/contamination_stats.json"""
import json, numpy as np
from proton.data import load_benchmark
from proton.features import load_features
from proton.evaluate import prepare, run_proton_stream, SHIFTS
from proton.streams import make_stream
from proton.online import proton_plus_config
out = {}
for bname in ["ophthalmology", "radiology", "pathology"]:
    b = load_benchmark(bname); P = prepare(b, load_features(bname, b.vlm)); o = {}
    for sh in SHIFTS:
        pool, n_id = P.pool(sh); vals = []
        for seed in range(5):
            order, is_ood = make_stream(n_id, len(pool) - n_id, seed=seed); idx = pool[order]
            r = run_proton_stream(P, pool, order); rp = run_proton_stream(P, pool, order, config=proton_plus_config())
            def comp(run):
                return [float(is_ood[np.where(run["updated"] & (run["pred"] == c))[0][-100:]].mean()) if (run["updated"] & (run["pred"] == c)).any() else 0.0 for c in range(2)]
            alpha = r["alpha"][r["calibrated"]]
            vals.append(dict(bank_ood_frac=comp(r), bank_ood_frac_plus=comp(rp), gate_pass_ood=float(np.mean(P.probs[idx][is_ood == 1].max(1) >= 0.7)),
                             conf_ood=float(P.probs[idx][is_ood == 1].max(1).mean()), conf_id=float(P.probs[idx][is_ood == 0].max(1).mean()),
                             alpha_min=float(alpha.min()), alpha_max=float(alpha.max()), pred_hist_ood=np.bincount(r["pred"][is_ood == 1], minlength=2).tolist()))
        o[sh] = {k: (np.mean([v[k] for v in vals], axis=0).round(3).tolist() if isinstance(vals[0][k], list) else round(float(np.mean([v[k] for v in vals])), 3)) for k in vals[0]}
        print(bname, sh, o[sh])
    out[bname] = o
out["_note"] = "means over five stream orders (seeds 0-4); bank_ood_frac = OOD share among the last 100 admissions per class"
json.dump(out, open("outputs/results/contamination_stats.json", "w"), indent=1)
