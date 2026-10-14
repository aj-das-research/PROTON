#!/usr/bin/env bash
# Clone the third-party repositories the library depends on (not vendored: licenses stay with their authors).
set -euo pipefail
cd "$(dirname "$0")/.."; mkdir -p third_party; cd third_party
[ -d FLAIR ] || git clone --depth 1 https://github.com/jusiro/FLAIR.git
[ -d UniMed-CLIP ] || git clone --depth 1 https://github.com/mbzuai-oryx/UniMed-CLIP.git
[ -d Medical-VLMs-OOD-Detection ] || git clone --depth 1 https://github.com/PyJulie/Medical-VLMs-OOD-Detection.git
echo "third_party ready: $(ls)"
