#!/usr/bin/env bash
# Pretrained VLM weights. FLAIR comes from the authors' Google Drive (same link as the FLAIR repo); the others from
# the Hugging Face hub (HF_HOME is honoured). Needs: wget, python with huggingface_hub.
set -euo pipefail
cd "$(dirname "$0")/.."; mkdir -p weights/flair
if [ ! -f weights/flair/flair_resnet.pth ]; then
  wget -q "https://drive.usercontent.google.com/download?id=1l24_2IzwQdnaa034I0zcyDLs_zMujsbR&export=download&confirm=t" -O weights/flair/weights.zip
  (cd weights/flair && unzip -o weights.zip && rm weights.zip)
fi
python - <<'PY'
from huggingface_hub import hf_hub_download, snapshot_download
hf_hub_download("UzairK/unimed-clip-vit-b16", "unimed-clip-vit-b16.pt")
snapshot_download("wisdomik/QuiltNet-B-32", allow_patterns=["open_clip_pytorch_model.bin", "*.json", "*.txt"])
snapshot_download("microsoft/BiomedNLP-BiomedBERT-base-uncased-abstract")
snapshot_download("emilyalsentzer/Bio_ClinicalBERT")
print("weights ready")
PY
