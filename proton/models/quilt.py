"""QuiltNet-B/32 (Ikezogwo et al., 2023): CLIP ViT-B/32 fine-tuned on Quilt-1M histopathology image-text pairs.
Loaded with the pip `open_clip` package from the Hugging Face hub (`hf-hub:wisdomik/QuiltNet-B-32`).
Also serves as the generic wrapper for any `open_clip` model via `OpenCLIPModel(model_id)`."""
from __future__ import annotations

import torch
from PIL import Image

from .base import VLM, l2n


class OpenCLIPModel(VLM):
    name = "open_clip"

    def __init__(self, model_id: str = "hf-hub:wisdomik/QuiltNet-B-32", device: str | None = None, name=None):
        super().__init__(device)
        import open_clip
        self.model, self.preprocess = open_clip.create_model_from_pretrained(model_id, device=self.device)
        self.tokenizer = open_clip.get_tokenizer(model_id)
        self.model.eval()
        tp = getattr(self.model, "text_projection", None)
        self.embed_dim = int(tp.shape[-1]) if tp is not None and hasattr(tp, "shape") else 512
        if name:
            self.name = name

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
        toks = self.tokenizer(prompts).to(self.device)
        return l2n(self.model.encode_text(toks)).float().cpu().numpy()

    @property
    def logit_scale(self) -> float:
        return float(self.model.logit_scale.exp())


class QuiltNet(OpenCLIPModel):
    name = "quiltnet"
    embed_dim = 512

    def __init__(self, device: str | None = None):
        super().__init__("hf-hub:wisdomik/QuiltNet-B-32", device=device, name="quiltnet")
