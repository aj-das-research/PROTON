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
def _encode(p):
    im = Image.open(p).convert("RGB"); w, h = im.size; s = 1024 / max(w, h)
    if s < 1: im = im.resize((round(w * s), round(h * s)), Image.LANCZOS)
    buf = io.BytesIO(); im.save(buf, format="PNG", compress_level=4); return buf.getvalue(), im.size


from proton.data import load_benchmark, load_specs
from proton.features import load_features
specs = load_specs()
for b in ["ophthalmology", "radiology", "pathology"]:
    bench = load_benchmark(b); df = bench.manifest.copy(); paths = bench.paths()
    # images: re-encode as PNG bytes (lossless) with the long side capped at 1024 px, in parallel
    from concurrent.futures import ProcessPoolExecutor
    with ProcessPoolExecutor(16) as ex:
        enc = list(ex.map(_encode, paths, chunksize=8))
    blobs, sizes = [b for b, _ in enc], [sz for _, sz in enc]
    print(b, "encoded", len(blobs), "images", flush=True)
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
card = open(os.path.join(ROOT, "scripts", "hf_dataset_card.md")).read()  # card text lives in scripts/hf_dataset_card.md
open(os.path.join(a.out, "README.md"), "w").write(card)
print("total MB:", round(sum(os.path.getsize(os.path.join(a.out, f)) for f in os.listdir(a.out)) / 1e6, 1))
if not a.no_upload:
    from huggingface_hub import HfApi
    api = HfApi(); api.create_repo(a.repo, repo_type="dataset", exist_ok=True, private=False)
    api.upload_folder(folder_path=a.out, repo_id=a.repo, repo_type="dataset", commit_message="PROTON+ curated benchmarks: images, embeddings, prompts, manifests")
    print("uploaded to https://huggingface.co/datasets/" + a.repo)
