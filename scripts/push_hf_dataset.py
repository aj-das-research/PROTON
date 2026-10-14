"""Publish the curated benchmarks to the Hugging Face Hub as parquet: images + metadata per benchmark, the cached
VLM embeddings (so the full evaluation runs without any image download), text-prompt embeddings and the manifests.
Usage: HF_HOME=... python scripts/push_hf_dataset.py [--repo abhijit2k01/proton-benchmarks] [--no-upload]"""
import argparse, io, json, os
import numpy as np, pandas as pd, pyarrow as pa, pyarrow.parquet as pq
from PIL import Image
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ap = argparse.ArgumentParser(); ap.add_argument("--repo", default="abhijit2k01/proton-benchmarks"); ap.add_argument("--no-upload", action="store_true")
ap.add_argument("--out", default=os.path.join(ROOT, "outputs", "hf_dataset")); a = ap.parse_args()
os.makedirs(a.out, exist_ok=True)
from proton.data import load_benchmark, load_specs
from proton.features import load_features
specs = load_specs()
for b in ["ophthalmology", "radiology", "pathology"]:
    bench = load_benchmark(b); df = bench.manifest.copy(); paths = bench.paths()
    # images: re-encode as PNG bytes (lossless) with the long side capped at 1024 px to keep the parquet shards small
    blobs, sizes = [], []
    for p in paths:
        im = Image.open(p).convert("RGB"); w, h = im.size; s = 1024 / max(w, h)
        if s < 1: im = im.resize((round(w * s), round(h * s)), Image.LANCZOS)
        buf = io.BytesIO(); im.save(buf, format="PNG", optimize=True); blobs.append(buf.getvalue()); sizes.append(im.size)
    df["image"] = blobs; df["width"] = [s[0] for s in sizes]; df["height"] = [s[1] for s in sizes]; df["row_id"] = range(len(df))
    t = pa.Table.from_pandas(df[["row_id", "domain", "set", "label", "class_name", "source", "path", "width", "height", "image"]], preserve_index=False)
    pq.write_table(t, os.path.join(a.out, f"{b}.parquet"), compression="zstd"); print(b, "images parquet", len(df), "rows")
    f = load_features(b, bench.vlm)
    fe = pd.DataFrame({"row_id": range(len(df)), "set": df["set"], "label": df["label"], "class_name": df["class_name"], "path": df["path"],
                       "embedding": [e.astype(np.float32).tolist() for e in f["embeds"]]})
    pq.write_table(pa.Table.from_pandas(fe, preserve_index=False), os.path.join(a.out, f"{b}_features_{bench.vlm}.parquet"), compression="zstd")
    text = {ps: {"prompts": specs[b]["prompts"][ps], "embeddings": f[f"text/{ps}"].tolist(), "counts": f["text_counts"][ps]} for ps in specs[b]["prompts"]}
    json.dump({"vlm": bench.vlm, "logit_scale": f["logit_scale"], "classes": bench.classes, "default_prompts": bench.default_prompts, "text": text},
              open(os.path.join(a.out, f"{b}_text_{bench.vlm}.json"), "w"))
    df.drop(columns=["image"]).to_csv(os.path.join(a.out, f"{b}_manifest.csv"), index=False)
card = """---
license: other
license_name: mixed-source-licenses
license_link: https://github.com/aj-das-research/PROTON#citation
task_categories: [image-classification]
tags: [out-of-distribution-detection, medical-imaging, vision-language, retina, chest-x-ray, histopathology, proton]
pretty_name: PROTON / PROTON+ medical OOD benchmarks
size_categories: [1K<n<10K]
---
# PROTON / PROTON+ medical OOD benchmarks

Curated test streams for test-time out-of-distribution detection with medical vision-language models, released with
**PROTON+** (https://github.com/aj-das-research/PROTON, project page https://aj-das-research.github.io/PROTON/),
the follow-up to PROTON (https://arxiv.org/abs/2606.20913).

| File | Content |
|---|---|
| `ophthalmology.parquet`, `radiology.parquet`, `pathology.parquet` | one row per image: `set` (id / id_bank / semantic / covariate / far), `label` (ID class index or -1), `class_name`, `source`, `path` (as in the repo manifests), `image` (PNG bytes, long side <= 1024 px) |
| `<benchmark>_features_<vlm>.parquet` | the l2-normalised image embedding of every row from the frozen VLM used in the paper (FLAIR, UniMed-CLIP, QuiltNet) |
| `<benchmark>_text_<vlm>.json` | the class-prompt embeddings of every prompt set, the logit scale and the default prompt set |
| `<benchmark>_manifest.csv` | the seeded manifest without images |

With the features and text embeddings every number of the paper can be recomputed on a CPU:
```python
import pandas as pd, numpy as np, json
from proton import score_stream, ood_metrics
from proton.online import proton_plus_config
fe = pd.read_parquet("ophthalmology_features_flair.parquet"); tx = json.load(open("ophthalmology_text_flair.json"))
T = np.array([np.mean(tx["text"][tx["default_prompts"]]["embeddings"][c][:k], 0) for c, k in enumerate(tx["text"][tx["default_prompts"]]["counts"])])
stream = fe[fe.set.isin(["id", "covariate"])].sample(frac=1, random_state=0)
out = score_stream(np.stack(stream.embedding), T, tx["logit_scale"], config=proton_plus_config())
print(ood_metrics(out["score"], (stream.set != "id").astype(int)))
```

## Sources and licenses (please cite the original datasets)
* FIVES (Jin et al., Sci. Data 2022), CC BY 4.0. DeepDRiD ultra-widefield (Liu et al., Patterns 2022), CC BY-SA 4.0.
* Imagenette (fast.ai; a subset of ImageNet, Deng et al. 2009), for research use under the ImageNet terms.
* RSNA Pneumonia Detection Challenge (Shih et al., Radiology: AI 2019; images from NIH ChestX-ray14), non-commercial research use.
  NIH ChestX-ray14 sample (Wang et al., CVPR 2017), NIH Clinical Center release. Paediatric chest X-rays (Kermany et al., Cell 2018), CC BY 4.0.
* PatchCamelyon (Veeling et al., MICCAI 2018), CC0. Camelyon17-WILDS (Koh et al., ICML 2021), CC0. NCT-CRC-HE (Kather et al., 2018), CC BY 4.0.

The streams, splits and de-duplication rules are described in the PROTON+ paper and implemented in
`proton/data/manifests.py` of the repository. Images are redistributed only to make the exact test streams
reproducible; the original licenses apply.
"""
open(os.path.join(a.out, "README.md"), "w").write(card)
print("total MB:", round(sum(os.path.getsize(os.path.join(a.out, f)) for f in os.listdir(a.out)) / 1e6, 1))
if not a.no_upload:
    from huggingface_hub import HfApi
    api = HfApi(); api.create_repo(a.repo, repo_type="dataset", exist_ok=True, private=False)
    api.upload_folder(folder_path=a.out, repo_id=a.repo, repo_type="dataset", commit_message="PROTON+ curated benchmarks: images, embeddings, prompts, manifests")
    print("uploaded to https://huggingface.co/datasets/" + a.repo)
