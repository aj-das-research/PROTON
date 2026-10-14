"""Common interface for frozen vision-language models.

Every wrapper exposes:
    name, embed_dim, logit_scale (float, = 1/tau as learned by the VLM)
    encode_images(paths, batch_size, num_workers, local=False) -> (N, d) l2-normalised float32 (and (N, P, d) local)
    encode_text(prompts) -> (K, d) l2-normalised float32
"""
from __future__ import annotations

import numpy as np
import torch
from PIL import Image
from torch.utils.data import DataLoader, Dataset


def l2n(x: torch.Tensor) -> torch.Tensor:
    return x / x.norm(dim=-1, keepdim=True).clamp_min(1e-12)


class _PathDataset(Dataset):
    def __init__(self, paths, transform):
        self.paths, self.transform = list(paths), transform

    def __len__(self):
        return len(self.paths)

    def __getitem__(self, i):
        with Image.open(self.paths[i]) as im:
            im = im.convert("RGB")
            return self.transform(im), i


class VLM:
    name: str = "base"
    embed_dim: int = 512

    def __init__(self, device: str | None = None):
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")

    def transform(self, pil_image: Image.Image) -> torch.Tensor:
        raise NotImplementedError

    @torch.no_grad()
    def image_forward(self, x: torch.Tensor, local: bool = False):
        """x: (B,3,H,W) on device -> global (B,d) [, local (B,P,d)] l2-normalised."""
        raise NotImplementedError

    @torch.no_grad()
    def encode_text(self, prompts: list[str]) -> np.ndarray:
        raise NotImplementedError

    @property
    def logit_scale(self) -> float:
        raise NotImplementedError

    @torch.no_grad()
    def encode_images(self, paths, batch_size: int = 32, num_workers: int = 8, local: bool = False,
                      progress: bool = True):
        ds = _PathDataset(paths, self.transform)
        dl = DataLoader(ds, batch_size=batch_size, num_workers=num_workers, shuffle=False, pin_memory=True)
        if progress:
            from tqdm import tqdm
            dl = tqdm(dl, desc=f"{self.name} images", leave=False)
        g_all, l_all = [], []
        for x, _ in dl:
            out = self.image_forward(x.to(self.device, non_blocking=True), local=local)
            if local:
                g, l = out
                l_all.append(l.float().cpu().numpy())
            else:
                g = out
            g_all.append(g.float().cpu().numpy())
        g_all = np.concatenate(g_all).astype(np.float32)
        if local:
            return g_all, np.concatenate(l_all).astype(np.float32)
        return g_all
