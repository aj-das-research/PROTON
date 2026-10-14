"""Model registry. `load_model("flair")`, `load_model("unimedclip")`, `load_model("quiltnet")`,
or any open_clip id: `load_model("open_clip:hf-hub:org/name")`."""
from __future__ import annotations

from .base import VLM

REGISTRY = {}


def register(name):
    def deco(fn):
        REGISTRY[name] = fn
        return fn
    return deco


@register("flair")
def _flair(**kw):
    from .flair import FLAIR
    return FLAIR(**kw)


@register("unimedclip")
def _unimed(**kw):
    from .unimed import UniMedCLIP
    return UniMedCLIP(**kw)


@register("quiltnet")
def _quilt(**kw):
    from .quilt import QuiltNet
    return QuiltNet(**kw)


def load_model(name: str, **kw) -> VLM:
    if name in REGISTRY:
        return REGISTRY[name](**kw)
    if name.startswith("open_clip:"):
        from .quilt import OpenCLIPModel
        return OpenCLIPModel(name.split(":", 1)[1], name=name, **kw)
    raise KeyError(f"unknown model {name!r}; registered: {sorted(REGISTRY)} or 'open_clip:<id>'")


__all__ = ["load_model", "register", "REGISTRY", "VLM"]
