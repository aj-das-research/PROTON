"""Extract and cache everything the experiments need from a frozen VLM for one benchmark:

    outputs/features/<benchmark>__<model>.npz with
        embeds      (N, d)   l2-normalised image embeddings, manifest order
        local       (N, P, d) patch embeddings (optional, for GL-MCM)
        text/<set>  (C, K_c_max, d) prompt-set embeddings (padded; see text_counts)
        tag         (C, T, d) TAG template embeddings
        logit_scale scalar
Everything downstream (PROTON, baselines, figures) is CPU-only numpy on these caches.
"""
from __future__ import annotations

import json
import os

import numpy as np

from .data import Benchmark, load_benchmark
from .models import load_model

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
FEAT_DIR = os.path.join(ROOT, "outputs", "features")


def feature_path(benchmark: str, model: str, feat_dir: str = FEAT_DIR) -> str:
    return os.path.join(feat_dir, f"{benchmark}__{model}.npz")


def extract_features(benchmark: str | Benchmark, model_name: str | None = None, local: bool = True,
                     batch_size: int = 32, num_workers: int = 8, feat_dir: str = FEAT_DIR, device=None,
                     force: bool = False) -> dict:
    bench = load_benchmark(benchmark) if isinstance(benchmark, str) else benchmark
    model_name = model_name or bench.vlm
    out = feature_path(bench.name, model_name, feat_dir)
    if os.path.exists(out) and not force:
        return load_features(bench.name, model_name, feat_dir)
    os.makedirs(feat_dir, exist_ok=True)
    vlm = load_model(model_name, device=device)
    paths = bench.paths()
    res = vlm.encode_images(paths, batch_size=batch_size, num_workers=num_workers, local=local)
    store = {"logit_scale": np.float32(vlm.logit_scale)}
    if local:
        store["embeds"], store["local"] = res
    else:
        store["embeds"] = res
    counts = {}
    for pname, per_class in bench.prompts.items():
        kmax = max(len(x) for x in per_class)
        arr = np.zeros((len(per_class), kmax, vlm.embed_dim), np.float32)
        if kmax == 1:   # benchmark protocol (Ju et al.): the C class prompts form one batch
            arr[:, 0] = vlm.encode_text([plist[0] for plist in per_class])
        else:           # hierarchical sets: each class's description list is one batch
            for c, plist in enumerate(per_class):
                arr[c, :len(plist)] = vlm.encode_text(list(plist))
        store[f"text/{pname}"] = arr
        counts[pname] = [len(x) for x in per_class]
    # TAG (Liu & Zach, 2024): K random word shuffles of each class prompt (the default prompt set), plus the original
    K = 10
    rng = np.random.default_rng(0)
    base_prompts = [plist[0] for plist in bench.prompts[bench.default_prompts]]
    tag = np.zeros((len(bench.classes), K + 1, vlm.embed_dim), np.float32)
    for c, prompt in enumerate(base_prompts):
        words = prompt.split()
        variants = [prompt] + [" ".join(rng.permutation(words).tolist()) for _ in range(K)]
        tag[c] = vlm.encode_text(variants)
    store["tag"] = tag
    store["text_counts"] = np.frombuffer(json.dumps(counts).encode(), dtype=np.uint8)
    np.savez_compressed(out, **store)
    return load_features(bench.name, model_name, feat_dir)


def load_features(benchmark: str, model: str, feat_dir: str = FEAT_DIR) -> dict:
    z = np.load(feature_path(benchmark, model, feat_dir))
    d = {k: z[k] for k in z.files}
    d["text_counts"] = json.loads(d["text_counts"].tobytes().decode())
    d["logit_scale"] = float(d["logit_scale"])
    return d


def class_text_embeds(feats: dict, prompt_set: str) -> np.ndarray:
    """(C, d) per-class text embedding. Single prompt -> that embedding. Multi-prompt (hierarchical) sets -> the plain
    mean of the prompt embeddings, so that logits are the mean of the per-prompt logits exactly as in Ju et al.'s
    hierarchical MCM (no re-normalisation)."""
    arr = feats[f"text/{prompt_set}"]
    counts = feats["text_counts"][prompt_set]
    return np.stack([arr[c, :k].mean(0) for c, k in enumerate(counts)]).astype(np.float32)


def level_logits(feats: dict, prompt_set: str) -> list:
    """For hierarchical MCM: list over classes of (N, K_c) logits of every prompt of that class."""
    arr, counts, s = feats[f"text/{prompt_set}"], feats["text_counts"][prompt_set], feats["logit_scale"]
    return [s * feats["embeds"] @ arr[c, :k].T for c, k in enumerate(counts)]
