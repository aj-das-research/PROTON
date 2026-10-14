#!/usr/bin/env bash
# Raw datasets for the three benchmarks (about 12 GB). Kaggle sources need a Kaggle API token (KAGGLE_API_TOKEN or
# ~/.kaggle/kaggle.json) and accepted competition rules for RSNA. Everything lands in data/raw/<source>/.
set -euo pipefail
cd "$(dirname "$0")/.."; R=data/raw; mkdir -p $R
# --- ophthalmology -------------------------------------------------------------------------------------------
mkdir -p $R/fives && [ -d "$R/fives/FIVES A Fundus Image Dataset for AI-based Vessel Segmentation" ] || {
  wget -q --user-agent="Mozilla/5.0" -O $R/fives/FIVES.rar "https://ndownloader.figshare.com/files/34969398"
  (cd $R/fives && 7z x -y FIVES.rar >/dev/null); }
[ -d $R/deepdrid/DeepDRiD ] || { mkdir -p $R/deepdrid && cd $R/deepdrid && git clone --filter=blob:none --sparse https://github.com/deepdrdoc/DeepDRiD.git && cd DeepDRiD && git sparse-checkout set ultra-widefield_images && cd ../../..; }
[ -d $R/imagenette/imagenette2 ] || { mkdir -p $R/imagenette && wget -q -O $R/imagenette/imagenette2.tgz https://s3.amazonaws.com/fast-ai-imageclas/imagenette2.tgz && tar xzf $R/imagenette/imagenette2.tgz -C $R/imagenette; }
# --- radiology -----------------------------------------------------------------------------------------------
[ -d $R/rsna/x ] || { mkdir -p $R/rsna/x && kaggle competitions download -c rsna-pneumonia-detection-challenge -p $R/rsna && unzip -q -o $R/rsna/rsna-pneumonia-detection-challenge.zip -d $R/rsna/x; }
[ -d $R/kermany_cxr/x ] || { mkdir -p $R/kermany_cxr/x && kaggle datasets download -d paultimothymooney/chest-xray-pneumonia -p $R/kermany_cxr && unzip -q -o $R/kermany_cxr/chest-xray-pneumonia.zip "chest_xray/test/*" -d $R/kermany_cxr/x; }
[ -d $R/covid_radiography/x ] || { mkdir -p $R/covid_radiography/x && kaggle datasets download -d tawsifurrahman/covid19-radiography-database -p $R/covid_radiography && unzip -q -o $R/covid_radiography/covid19-radiography-database.zip "COVID-19_Radiography_Dataset/COVID/images/*" -d $R/covid_radiography/x; }
# --- pathology (parquet shards from the Hugging Face hub; exported to PNG by `proton prepare-data`) ----------------
python - <<'PY'
from huggingface_hub import hf_hub_download
for repo, fn in [("1aurent/PatchCamelyon", "data/test-00000-of-00002-bb04e6313f58efa0.parquet"),
                 ("jxie/camelyon17", "data/ood_test-00000-of-00001-4e2cffbdce8ec122.parquet"),
                 ("1aurent/NCT-CRC-HE", "data/CRC_VAL_HE_7K-00000-of-00003-cce1097526b69125.parquet"),
                 ("1aurent/NCT-CRC-HE", "data/CRC_VAL_HE_7K-00001-of-00003-fbb5de8b1164f4ea.parquet"),
                 ("1aurent/NCT-CRC-HE", "data/CRC_VAL_HE_7K-00002-of-00003-2009e87e0c48fccf.parquet")]:
    print(hf_hub_download(repo_id=repo, filename=fn, repo_type="dataset"))
PY
echo "raw data ready under $R"
