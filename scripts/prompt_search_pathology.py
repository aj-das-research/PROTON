"""Pick QuiltNet prompts for PCam by ID zero-shot accuracy ONLY (no OOD information is used)."""
import numpy as np
from proton.data import load_benchmark
from proton.features import load_features
from proton.models import load_model
from proton.scores.static import softmax
b = load_benchmark("pathology"); f = load_features("pathology", "quiltnet"); m = load_model("quiltnet")
E, s = f["embeds"], f["logit_scale"]; sets = b.manifest["set"].to_numpy(); labels = b.manifest["label"].to_numpy()
i = np.where(sets == "id")[0]
cands = {
 "benign/malignant": ["benign", "malignant"],
 "normal/tumor": ["normal", "tumor"],
 "normal tissue/tumor tissue": ["normal tissue", "tumor tissue"],
 "lymph node: normal/metastasis": ["normal lymph node tissue", "lymph node metastasis"],
 "H&E normal lymph/metastatic carcinoma": ["an H&E image of normal lymph node tissue", "an H&E image of metastatic carcinoma in a lymph node"],
 "histopathology benign/malignant": ["histopathology image of benign tissue", "histopathology image of malignant tissue"],
 "no tumor/tumor": ["a histopathology patch with no tumor cells", "a histopathology patch with tumor cells"],
 "lymphocytes/breast cancer cells": ["lymphocytes", "breast cancer cells"],
 "benign lymph node/breast cancer metastasis": ["benign lymph node", "breast cancer metastasis"],
 "normal/cancer": ["normal", "cancer"],
 "non-cancerous/cancerous": ["non-cancerous tissue", "cancerous tissue"],
 "lymph: healthy/metastatic": ["healthy lymph node tissue", "metastatic tumor tissue in lymph node"],
}
for name, pr in cands.items():
    T = m.encode_text(pr); p = softmax(s * E @ T.T)
    acc = (p[i].argmax(1) == labels[i]).mean(); bal = np.bincount(p[i].argmax(1), minlength=2)
    print(f"{name:42s} acc {acc:.3f} pred hist {bal} mean conf {p[i].max(1).mean():.2f}")
