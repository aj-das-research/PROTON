"""FLAIR (Silva-Rodriguez et al., 2025): ResNet-50 + Bio_ClinicalBERT, d=512, 512x512 canvas input.

Vanilla prompts: the class name only (caption template "[CLS]"), as in the PROTON paper and the Ju et al.
benchmark's "naive prompt" setting. Preprocessing follows FLAIRModel.preprocess_image exactly: /255, keep aspect
ratio by resizing the long side to 512, zero-pad right/bottom to 512x512, no mean/std normalisation.
"""
from __future__ import annotations

import os

import numpy as np
import torch
import torchvision.transforms.functional as TF
from PIL import Image

from .base import VLM, l2n

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DEFAULT_WEIGHTS = os.environ.get("FLAIR_WEIGHTS", os.path.join(ROOT, "weights", "flair", "flair_resnet.pth"))


class FLAIR(VLM):
    name = "flair"
    embed_dim = 512

    def __init__(self, weights_path: str | None = None, device: str | None = None, image_size: int = 512,
                 caption: str = "[CLS]"):
        super().__init__(device)
        os.environ.setdefault("TORCH_HOME", os.path.join(ROOT, ".cache", "torch"))
        from flair import FLAIRModel  # third_party/FLAIR installed in the env
        weights_path = weights_path or DEFAULT_WEIGHTS
        # vision_pretrained=False: the FLAIR checkpoint holds the full ResNet-50, so no ImageNet download is needed
        self.model = FLAIRModel(from_checkpoint=True, weights_path=weights_path, caption=caption,
                                image_size=image_size, vision_pretrained=False)
        self.model.eval().to(self.device)
        self.image_size = image_size
        self.caption = caption

    def transform(self, im: Image.Image) -> torch.Tensor:
        x = TF.to_tensor(im)  # float in [0,1], CHW
        h, w = x.shape[-2:]
        scale = max(h, w) / self.image_size
        x = TF.resize(x, [int(h / scale), int(w / scale)], antialias=True)
        x = torch.nn.functional.pad(x, (0, self.image_size - x.shape[-1], 0, self.image_size - x.shape[-2]))
        return x

    @torch.no_grad()
    def image_forward(self, x, local: bool = False):
        vm = self.model.vision_model
        if not local:
            return l2n(vm(x))
        r = vm.model  # torchvision resnet50 with fc=Identity
        f = r.maxpool(r.relu(r.bn1(r.conv1(x))))
        f = r.layer4(r.layer3(r.layer2(r.layer1(f))))          # (B,2048,h,w)
        g = torch.flatten(r.avgpool(f), 1)
        g = l2n(vm.projection_head_vision(g))
        loc = f.flatten(2).transpose(1, 2)                      # (B,P,2048)
        loc = l2n(vm.projection_head_vision(loc))
        return g, loc

    @torch.no_grad()
    def encode_text(self, prompts, joint: bool = True):
        """Encode prompts. joint=True pads them into ONE batch exactly like FLAIRModel.forward does (the FLAIR text
        embedding averages hidden states over all tokens, padding included, so the vector of a short prompt depends
        on the longest prompt in its batch). joint=False encodes each prompt alone (FLAIR.compute_text_embeddings)."""
        tm = self.model.text_model
        prompts = [self.caption.replace("[CLS]", p) for p in prompts]
        if not joint:
            return np.concatenate([self.encode_text([p], joint=True) for p in prompts])
        tok = tm.tokenizer(prompts, truncation=True, padding=True, return_tensors="pt")
        emb = tm(tok["input_ids"].to(self.device), tok["attention_mask"].to(self.device))
        return l2n(emb).float().cpu().numpy()

    @property
    def logit_scale(self) -> float:
        return float(self.model.logit_scale.data.clamp(0, 4.6052).exp())
