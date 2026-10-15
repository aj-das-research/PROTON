---
license: other
license_name: mixed-source-licenses
license_link: https://github.com/aj-das-research/PROTON#citation
task_categories: [image-classification]
tags: [out-of-distribution-detection, medical-imaging, vision-language, retina, chest-x-ray, histopathology, proton]
pretty_name: PROTON / PROTON+ medical OOD benchmarks
size_categories: [1K<n<10K]
---
# PROTON / PROTON+ medical OOD benchmarks

Curated test streams for test-time out-of-distribution detection with medical vision-language models, released with
**PROTON+** (https://github.com/aj-das-research/PROTON, project page https://aj-das-research.github.io/PROTON/),
the follow-up to PROTON (MICCAI 2026, https://arxiv.org/abs/2606.20913).

| File | Content |
|---|---|
| `ophthalmology.parquet`, `radiology.parquet`, `pathology.parquet` | one row per image: `set`, `label` (ID class index or -1), `class_name`, `source`, `path` (as in the repo manifests), `image` (PNG bytes, long side <= 1024 px) |
| `<benchmark>_features_<vlm>.parquet` | the l2-normalised image embedding of every row from the frozen VLM used in the paper (FLAIR, UniMed-CLIP, QuiltNet) |
| `<benchmark>_text_<vlm>.json` | the class-prompt embeddings of every prompt set, the logit scale and the default prompt set |
| `<benchmark>_manifest.csv` | the seeded manifest without images |

`set` is `id` (ID test images), `id_bank` (a disjoint labelled ID split, used only by the privileged baselines and for
prompt selection), `semantic`, `covariate` or `far`. The radiology file also holds `semantic_covid` (COVID-19
radiographs), which is kept for completeness and not used in the paper.

## Preview

The Hub viewer cannot display the image bytes, so here are two images per split of each benchmark, drawn with a fixed
seed (frame colour: blue ID, orange semantic, red covariate, grey far).

![Two images per split of each benchmark](https://huggingface.co/datasets/abhijit2k01/proton-benchmarks/resolve/main/samples/overview.jpg)

Two example rows of `ophthalmology.parquet`, an ID image and a covariate-shifted one:

| set | label | class_name | source | path | image |
|---|---|---|---|---|---|
| `id` | 0 | normal | fives | `data/raw/fives/.../test/Original/151_N.png` | PNG bytes, 1024 x 1024 px |
| `covariate` | -1 | uwf | deepdrid | `data/raw/deepdrid/.../ultra-widefield_images/.../100_l4.jpg` | PNG bytes, 1024 x 807 px |

Load one image (the pathology file is the smallest, 115 MB):
```python
import io, pandas as pd
from huggingface_hub import hf_hub_download
from PIL import Image
df = pd.read_parquet(hf_hub_download("abhijit2k01/proton-benchmarks", "pathology.parquet", repo_type="dataset"))
row = df[df.set == "covariate"].iloc[0]
print(row.set, row.class_name, row.source); Image.open(io.BytesIO(row.image)).save("example.png")
```

## Recompute the results

With the features and text embeddings every number of the paper can be recomputed on a CPU:
```python
import pandas as pd, numpy as np, json
from proton import score_stream, ood_metrics
from proton.online import proton_plus_config
fe = pd.read_parquet("ophthalmology_features_flair.parquet"); tx = json.load(open("ophthalmology_text_flair.json"))
T = np.array([np.mean(tx["text"][tx["default_prompts"]]["embeddings"][c][:k], 0) for c, k in enumerate(tx["text"][tx["default_prompts"]]["counts"])])
stream = fe[fe.set.isin(["id", "covariate"])].sample(frac=1, random_state=0)
out = score_stream(np.stack(stream.embedding), T, tx["logit_scale"], config=proton_plus_config())
print(ood_metrics(out["score"], (stream.set != "id").astype(int)))
```

## Citation

If you use these benchmarks, please cite PROTON and PROTON+, and the original datasets listed below:
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

## Sources and licenses (please cite the original datasets)
* FIVES (Jin et al., Sci. Data 2022), CC BY 4.0. DeepDRiD ultra-widefield (Liu et al., Patterns 2022), CC BY-SA 4.0.
* Imagenette (fast.ai; a subset of ImageNet, Deng et al. 2009), for research use under the ImageNet terms.
* RSNA Pneumonia Detection Challenge (Shih et al., Radiology: AI 2019; images from NIH ChestX-ray14), non-commercial research use.
  NIH ChestX-ray14 sample (Wang et al., CVPR 2017), NIH Clinical Center release. Paediatric chest X-rays (Kermany et al., Cell 2018), CC BY 4.0.
* PatchCamelyon (Veeling et al., MICCAI 2018), CC0. Camelyon17-WILDS (Koh et al., ICML 2021), CC0. NCT-CRC-HE (Kather et al., 2018), CC BY 4.0.

The streams, splits and de-duplication rules are described in the PROTON+ paper and implemented in
`proton/data/manifests.py` of the repository. Images are redistributed only to make the exact test streams
reproducible; the original licenses apply.
