"""Effect of FLAIR's text-encoding protocol (joint padded batch vs each prompt alone) on MCM, per prompt set."""
import json, numpy as np
from proton.data import load_benchmark
from proton.features import load_features
from proton.models import load_model
from proton.scores.static import mcm
from proton.metrics import ood_metrics
b = load_benchmark("ophthalmology"); f = load_features("ophthalmology", "flair"); m = load_model("flair")
E, s = f["embeds"], f["logit_scale"]; sets = b.manifest["set"].to_numpy(); idx_id = np.where(sets == "id")[0]
out = {}
for ps in ["flair_default", "vanilla", "l1"]:
    prompts = [p[0] for p in b.prompts[ps]]
    for joint in (True, False):
        T = m.encode_text(prompts, joint=joint); sc = mcm(s * E @ T.T); res = {}
        for sh in ("semantic", "covariate", "far"):
            j = np.where(sets == sh)[0]; pool = np.concatenate([idx_id, j]); y = np.r_[np.zeros(len(idx_id)), np.ones(len(j))]
            res[sh] = ood_metrics(sc[pool], y)["auroc"]
        out[f"{ps}/{'joint' if joint else 'separate'}"] = res
        print(ps, "joint" if joint else "separate", {k: round(v, 1) for k, v in res.items()})
json.dump(out, open("outputs/results/flair_text_encoding.json", "w"), indent=1)
