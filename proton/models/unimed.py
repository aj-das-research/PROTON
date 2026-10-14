"""UniMed-CLIP (Khattak et al., 2024): ViT-B/16 (quickGELU, MetaCLIP init) + BiomedBERT text encoder, d=512.

The checkpoint needs the authors' open_clip fork (third_party/UniMed-CLIP/src/open_clip), which we import under
the alias `unimed_open_clip` so it does not clash with the pip `open_clip` package used by QuiltNet.
"""
from __future__ import annotations

import importlib.util
import os
import sys

import torch
from PIL import Image

from .base import VLM, l2n

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
FORK = os.environ.get("UNIMED_CLIP_SRC", os.path.join(ROOT, "third_party", "UniMed-CLIP", "src", "open_clip"))
TEXT_ENCODER = "microsoft/BiomedNLP-BiomedBERT-base-uncased-abstract"


def _load_fork(alias: str = "unimed_open_clip"):
    if alias in sys.modules:
        return sys.modules[alias]
    spec = importlib.util.spec_from_file_location(alias, os.path.join(FORK, "__init__.py"),
                                                  submodule_search_locations=[FORK])
    mod = importlib.util.module_from_spec(spec)
    sys.modules[alias] = mod
    spec.loader.exec_module(mod)
    return mod


class UniMedCLIP(VLM):
    name = "unimedclip"
    embed_dim = 512

    def __init__(self, weights_path: str | None = None, device: str | None = None):
        super().__init__(device)
        oc = _load_fork()
        if weights_path is None:
            from huggingface_hub import hf_hub_download
            weights_path = hf_hub_download("UzairK/unimed-clip-vit-b16", "unimed-clip-vit-b16.pt")
        mean, std = oc.get_mean_std()
        # The released checkpoint stores a few numpy scalars (e.g. the epoch); allow-list exactly that type so the
        # default weights_only=True loader accepts it.
        import numpy as _np
        import numpy.dtypes as _npd
        # Allow-list only numpy scalar/dtype classes (the checkpoint stores e.g. the epoch as a numpy float64).
        # The (object, pickled-name) pair is needed because numpy>=2 moved numpy.core to numpy._core.
        allow = [(_np._core.multiarray.scalar, "numpy.core.multiarray.scalar"), _np.dtype]
        allow += [getattr(_npd, n) for n in dir(_npd) if n.endswith("DType")]
        with torch.serialization.safe_globals(allow):
            self.model, _, self.preprocess = oc.create_model_and_transforms(
                "ViT-B-16-quickgelu", weights_path, precision="fp32", device=self.device, force_quick_gelu=True,
                mean=mean, std=std, inmem=True, text_encoder_name=TEXT_ENCODER)
        self.model.eval()
        self.tokenizer = oc.HFTokenizer(TEXT_ENCODER, context_length=256)

    def transform(self, im: Image.Image) -> torch.Tensor:
        return self.preprocess(im)

    @torch.no_grad()
    def image_forward(self, x, local: bool = False):
        if not local:
            return l2n(self.model.encode_image(x))
        from .vit_local import vit_tokens
        g, loc = vit_tokens(self.model.visual, x)
        return l2n(g), l2n(loc)

    @torch.no_grad()
    def encode_text(self, prompts):
        toks = torch.cat([self.tokenizer(p) for p in prompts]).to(self.device)
        return l2n(self.model.encode_text(toks)).float().cpu().numpy()

    @property
    def logit_scale(self) -> float:
        return float(self.model.logit_scale.exp())
