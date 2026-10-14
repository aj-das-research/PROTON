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
* `flair_vision_int8.onnx`: dynamically quantised int8 (25 MB); embeddings agree with fp32 at cosine 0.99.

Code and benchmarks: https://github.com/aj-das-research/PROTON. Curated data: https://huggingface.co/datasets/abhijit2k01/proton-benchmarks
