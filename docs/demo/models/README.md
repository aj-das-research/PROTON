---
license: apache-2.0
tags: [onnx, ood-detection, medical, retina, flair, proton]
---
# PROTON+ demo model: FLAIR ResNet-50 vision encoder (ONNX)

ONNX export of the vision tower and projection head of **FLAIR** (Silva-Rodríguez et al., Medical Image Analysis 2025,
Apache-2.0, https://github.com/jusiro/FLAIR), used by the in-browser demo of **PROTON+**, the follow-up to PROTON
(test-time online OOD detection for medical vision-language models): https://aj-das-research.github.io/PROTON/demo/

* `flair_vision.onnx`: fp32 (98 MB). Input `image` float32 `[B,3,512,512]` in [0,1] (long side resized to 512,
  zero-padded right/bottom, no mean/std normalisation). Output `embedding` `[B,512]`, l2-normalised.
* `flair_vision_int8.onnx`: weight-only int8 (25 MB): int8 weights with per-channel scales dequantised at load
  (standard DequantizeLinear + Conv ops, runs in onnxruntime-web WASM); embeddings agree with fp32 at cosine >= 0.994
  (mean 0.9985) on ID, ultra-widefield and natural images.
* `text_embeds_ophthalmology.json`: FLAIR text embeddings of the demo's two class prompts ("A fundus photograph of
  normal", "A fundus photograph of diabetic retinopathy") and FLAIR's logit scale, for zero-shot classification.
* `samples/`: the two example images below (long side 512 px).

## Example

The encoder maps a retinal image to a 512-d embedding. Its dot product with each class-prompt embedding, times the
logit scale, gives zero-shot logits; a softmax turns them into a label and a confidence (as in the demo).
Outputs of `flair_vision_int8.onnx` on two real images:

![In-distribution fundus photograph and ultra-widefield image with their zero-shot labels](https://huggingface.co/abhijit2k01/proton-demo/resolve/main/samples/example.jpg)

*Images (resized): FIVES (Jin et al., Scientific Data 2022), CC BY 4.0; DeepDRiD (Liu et al., Patterns 2022), CC BY-SA 4.0. They keep their source licenses.*

| Image | Distribution | Ground truth | Zero-shot label | Softmax confidence |
|---|---|---|---|---|
| `samples/fives_normal.jpg`, FIVES fundus photograph | in-distribution | normal | normal | 0.998 |
| `samples/deepdrid_uwf.jpg`, DeepDRiD ultra-widefield | covariate shift (camera the clinic never saw) | DR grade 0 (no apparent retinopathy) | diabetic retinopathy | 0.989 |

The softmax is confident on both, so it cannot flag the unseen camera; PROTON+ adds a prototype-distance signal built
from the test stream, which does. Try it in the browser: https://aj-das-research.github.io/PROTON/demo/

```python
import json
import numpy as np, onnxruntime as ort
from PIL import Image
from huggingface_hub import hf_hub_download

repo = "abhijit2k01/proton-demo"
sess = ort.InferenceSession(hf_hub_download(repo, "flair_vision_int8.onnx"), providers=["CPUExecutionProvider"])
spec = json.load(open(hf_hub_download(repo, "text_embeds_ophthalmology.json")))

def preprocess(path, size=512):
    """FLAIR input: long side -> 512, zero-pad right/bottom, values in [0,1], no mean/std normalisation."""
    im = Image.open(path).convert("RGB")
    s = max(im.size) / size
    im = im.resize((int(im.width / s), int(im.height / s)), Image.BILINEAR)
    canvas = Image.new("RGB", (size, size))
    canvas.paste(im, (0, 0))
    return (np.asarray(canvas, np.float32) / 255).transpose(2, 0, 1)[None]

emb = sess.run(None, {"image": preprocess(hf_hub_download(repo, "samples/deepdrid_uwf.jpg"))})[0]
print(emb.shape)  # (1, 512)

logits = spec["logit_scale"] * np.array(spec["text_embeds"]) @ emb[0]
p = np.exp(logits - logits.max()); p /= p.sum()
print({c: round(float(v), 3) for c, v in zip(spec["classes"], p)})  # {'normal': 0.011, 'diabetic retinopathy': 0.989}
```

Code and benchmarks: https://github.com/aj-das-research/PROTON. Curated data: https://huggingface.co/datasets/abhijit2k01/proton-benchmarks

## Citation

If you use this model or the demo, please cite PROTON and PROTON+:

```bibtex
@inproceedings{das2026proton,
  title={PROTON: Prototype-Based Test-Time Online OOD Detection for Medical VLMs},
  author={Das, Abhijit and Wasalathilaka, Nichula and Lu, Yifan and Dukre, Adinath and Mahapatra, Dwarikanath and Khan, Shadab and Razzak, Imran},
  booktitle={International Conference on Medical Image Computing and Computer-Assisted Intervention},
  pages={527--537},
  year={2026},
  organization={Springer}
}
@misc{das2026protonplus,
  title  = {PROTON+: Contamination-Robust Prototype Banks for Test-Time Online OOD Detection with Medical VLMs},
  author = {Das, Abhijit and Wasalathilaka, Nichula and Lu, Yifan and Dukre, Adinath and Mahapatra, Dwarikanath and Khan, Shadab and Razzak, Imran},
  year   = {2026},
  note   = {Preprint, https://github.com/aj-das-research/PROTON}
}
```

The weights are FLAIR's, so please also cite FLAIR (Silva-Rodríguez et al., Medical Image Analysis 2025).
