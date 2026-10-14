"""Export everything the in-browser demo needs (docs/demo/):
  models/flair_vision.onnx      FLAIR ResNet-50 + projection (input 1x3x512x512 float in [0,1], output 512-d l2-normalised)
  assets/ophthalmology.json     class prompts, their FLAIR text embeddings (joint-encoded), logit scale, PROTON(+) defaults
  assets/examples/*.jpg         a few FIVES / UWF / ImageNet thumbnails (CC-BY sources) + their precomputed embeddings
Run: CUDA_VISIBLE_DEVICES=5 python scripts/export_demo_assets.py
"""
import json, os, sys
import numpy as np, torch
from PIL import Image
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from proton.models import load_model
from proton.data import load_benchmark
from proton.features import load_features, class_text_embeds

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUT = os.path.join(ROOT, "docs", "demo"); os.makedirs(os.path.join(OUT, "models"), exist_ok=True)
os.makedirs(os.path.join(OUT, "assets", "examples"), exist_ok=True)

m = load_model("flair", device="cpu")
vm = m.model.vision_model

class Wrapped(torch.nn.Module):
    def __init__(self, vm): super().__init__(); self.vm = vm
    def forward(self, x):
        e = self.vm(x); return e / e.norm(dim=-1, keepdim=True)

w = Wrapped(vm).eval()
x = torch.zeros(1, 3, 512, 512)
onnx_path = os.path.join(OUT, "models", "flair_vision.onnx")
torch.onnx.export(w, x, onnx_path, input_names=["image"], output_names=["embedding"], opset_version=17, dynamo=False,
                  dynamic_axes={"image": {0: "batch"}, "embedding": {0: "batch"}})
print("onnx written", os.path.getsize(onnx_path) / 1e6, "MB")
# sanity: onnxruntime vs torch
import onnxruntime as ort
sess = ort.InferenceSession(onnx_path, providers=["CPUExecutionProvider"])
bench = load_benchmark("ophthalmology")
paths = bench.paths("id")[:2] + bench.paths("covariate")[:2] + bench.paths("far")[:2] + bench.paths("semantic")[:2]
xs = torch.stack([m.transform(Image.open(p).convert("RGB")) for p in paths])
ref = w(xs).detach().numpy(); got = sess.run(None, {"image": xs.numpy()})[0]
print("onnx max abs diff vs torch:", float(np.abs(ref - got).max()))

feats = load_features("ophthalmology", "flair")
T = class_text_embeds(feats, bench.default_prompts)
spec = {"benchmark": "ophthalmology", "vlm": "FLAIR (ResNet-50 + Bio_ClinicalBERT)", "image_size": 512,
        "classes": bench.classes, "prompts": [p[0] for p in bench.prompts[bench.default_prompts]],
        "text_embeds": T.round(6).tolist(), "logit_scale": feats["logit_scale"],
        "proton": {"gamma": 0.7, "M": 100, "k_min": 5, "alpha_min": 0.3, "alpha_max": 0.7, "sigma2_0": 0.02},
        "proton_plus": {"bandwidth": 0.1, "kappa": 2.0, "ms_iters": 3}}
# example gallery: 6 per set, thumbnails + embeddings (so the demo can stream them without the model)
ex = []
rng = np.random.default_rng(0)
for s, n in [("id", 8), ("semantic", 6), ("covariate", 6), ("far", 6)]:
    df = bench.subset(s); idx = rng.choice(len(df), n, replace=False)
    for i in idx:
        row = df.iloc[i]; p = os.path.join(ROOT, row["path"])
        name = f"{s}_{i}.jpg"; Image.open(p).convert("RGB").resize((256, 256)).save(os.path.join(OUT, "assets", "examples", name), quality=85)
        gi = int(np.where((bench.manifest["path"] == row["path"]).to_numpy())[0][0])
        ex.append({"file": "assets/examples/" + name, "set": s, "class_name": row["class_name"], "embedding": feats["embeds"][gi].round(5).tolist()})
spec["examples"] = ex
json.dump(spec, open(os.path.join(OUT, "assets", "ophthalmology.json"), "w"))
print("assets written:", len(ex), "examples")
