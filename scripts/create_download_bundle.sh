#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT_DIR="${ROOT_DIR}/dist"
BUNDLE_NAME="QuantAI-Trad-full-program.zip"

mkdir -p "${OUT_DIR}"
rm -f "${OUT_DIR}/${BUNDLE_NAME}"

cd "${ROOT_DIR}"
zip -r "${OUT_DIR}/${BUNDLE_NAME}" \
  README.md DOWNLOAD.md requirements.txt \
  app ai data database trading dashboard tests scripts \
  -x "*.pyc" "*/__pycache__/*" "dist/*" ".git/*"

echo "Bundle created: ${OUT_DIR}/${BUNDLE_NAME}"
