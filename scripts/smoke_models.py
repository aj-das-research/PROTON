"""Smoke test: load one VLM on the given GPU, embed a couple of images + prompts, print shapes and probabilities."""
import glob, os, sys, time
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import numpy as np
from proton.models import load_model
from proton.scores.static import softmax

name = sys.argv[1]
raw = "/mnt/hdd2/Abhijit/projects/PROTON/data/raw"
if name == "flair":
    imgs = sorted(glob.glob(f"{raw}/fives/FIVES*/train/Original/*_N.png"))[:2] + sorted(glob.glob(f"{raw}/fives/FIVES*/train/Original/*_D.png"))[:2]
    prompts = ["normal", "diabetic retinopathy"]
elif name == "unimedclip":
    imgs = sorted(glob.glob(f"{raw}/kermany_cxr/x/chest_xray/test/NORMAL/*.jpeg"))[:2] + sorted(glob.glob(f"{raw}/kermany_cxr/x/chest_xray/test/PNEUMONIA/*.jpeg"))[:2]
    prompts = ["x-ray of normal", "x-ray of pneumonia"]
else:
    imgs = sorted(glob.glob(f"{raw}/lc25000/x/lung_colon_image_set/lung_image_sets/lung_n/*.jpeg"))[:2] + sorted(glob.glob(f"{raw}/lc25000/x/lung_colon_image_set/lung_image_sets/lung_aca/*.jpeg"))[:2]
    prompts = ["histopathology image of benign lung tissue", "histopathology image of lung adenocarcinoma"]
t0 = time.time()
m = load_model(name)
print(name, "loaded in", round(time.time() - t0, 1), "s; logit_scale", m.logit_scale, "dim", m.embed_dim)
g, loc = m.encode_images(imgs, batch_size=4, num_workers=2, local=True, progress=False)
T = m.encode_text(prompts)
print("embeds", g.shape, "local", loc.shape, "text", T.shape, "norms", np.linalg.norm(g, axis=1).round(3))
logits = m.logit_scale * g @ T.T
print("probs (first 2 should be class 0, last 2 class 1):\n", softmax(logits).round(3))
print("local-logit max per image:", (m.logit_scale * loc @ T.T).max(axis=(1, 2)).round(2))
