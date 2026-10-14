"""How much do FLAIR's MCM numbers depend on the prompt wording? Encodes prompt variants and reports MCM AUROC."""
import numpy as np, sys
from proton.data import load_benchmark
from proton.features import load_features
from proton.models import load_model
from proton.scores.static import mcm, softmax
from proton.metrics import ood_metrics
b = load_benchmark("ophthalmology"); f = load_features("ophthalmology", "flair")
m = load_model("flair")
E, s = f["embeds"], f["logit_scale"]
sets = b.manifest["set"].to_numpy(); labels = b.manifest["label"].to_numpy()
variants = {
 "vanilla": ["normal", "diabetic retinopathy"],
 "A fundus photograph of X": ["A fundus photograph of normal", "A fundus photograph of diabetic retinopathy"],
 "A fundus photograph of X.": ["A fundus photograph of normal.", "A fundus photograph of diabetic retinopathy."],
 "a photo of X": ["a photo of normal", "a photo of diabetic retinopathy"],
 "X fundus": ["normal fundus", "diabetic retinopathy fundus"],
 "no DR / DR": ["no diabetic retinopathy", "diabetic retinopathy"],
 "healthy / DR": ["healthy", "diabetic retinopathy"],
}
id_idx = np.where(sets == "id")[0]
for name, prompts in variants.items():
    T = m.encode_text(prompts); logits = s * E @ T.T; p = softmax(logits); sc = mcm(logits)
    acc = (p[id_idx].argmax(1) == labels[id_idx]).mean()
    res = []
    for sh in ("semantic", "covariate", "far"):
        j = np.where(sets == sh)[0]; pool = np.concatenate([id_idx, j]); y = np.r_[np.zeros(len(id_idx)), np.ones(len(j))]
        res.append(f"{ood_metrics(sc[pool], y)['auroc']:.1f}")
    conf = {sh: p[sets == sh].max(1).mean() for sh in ("id", "semantic", "covariate", "far")}
    print(f"{name:28s} acc {acc:.2f} | MCM AUROC sem/cov/far {' / '.join(res)} | mean conf id {conf['id']:.2f} sem {conf['semantic']:.2f} cov {conf['covariate']:.2f} far {conf['far']:.2f}")
