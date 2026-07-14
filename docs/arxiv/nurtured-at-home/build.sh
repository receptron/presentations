#!/usr/bin/env bash
# Build the paper PDF with tectonic (self-contained LaTeX engine).
# Install once:  brew install tectonic
#
# Figures are referenced directly from the canonical render location
# (docs/figures/) via \figroot — there is exactly one copy of each figure
# in the repo. Use package.sh to assemble a self-contained arXiv upload.
set -euo pipefail
cd "$(dirname "$0")"
tectonic main.tex
echo "Built: $(pwd)/main.pdf"
