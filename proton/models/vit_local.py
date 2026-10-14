"""Patch-token (local) features for CLIP-style VisionTransformers (open_clip and the UniMed fork), used by GL-MCM.
Returns (global (B,d), local (B,P,d)) where local tokens go through the same ln_post + proj as the CLS token."""
from __future__ import annotations

import torch


@torch.no_grad()
def vit_tokens(visual, x: torch.Tensor):
    x = visual.conv1(x)                                   # (B, width, g, g)
    x = x.reshape(x.shape[0], x.shape[1], -1).permute(0, 2, 1)
    cls = visual.class_embedding.to(x.dtype) + torch.zeros(x.shape[0], 1, x.shape[-1], dtype=x.dtype, device=x.device)
    x = torch.cat([cls, x], dim=1) + visual.positional_embedding.to(x.dtype)
    if hasattr(visual, "patch_dropout"):
        x = visual.patch_dropout(x)
    x = visual.ln_pre(x)
    if getattr(visual.transformer, "batch_first", False):
        x = visual.transformer(x)
    else:
        x = x.permute(1, 0, 2)
        x = visual.transformer(x)
        x = x.permute(1, 0, 2)
    x = visual.ln_post(x)
    if getattr(visual, "proj", None) is not None:
        x = x @ visual.proj
    return x[:, 0], x[:, 1:]
