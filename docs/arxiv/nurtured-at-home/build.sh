#!/usr/bin/env bash
# Build the paper PDF with tectonic (self-contained LaTeX engine).
# Install once:  brew install tectonic
set -euo pipefail
cd "$(dirname "$0")"

# Sync figures from the canonical render location (docs/figures/) so the
# self-contained arXiv package never falls behind a re-rendered source.
for f in fig1-architecture.png fig3a-desktop-map-view.png fig3b-relay-mobile-view.png; do
  src="../../figures/$f"
  if [ -f "$src" ] && ! cmp -s "$src" "figures/$f"; then
    cp -p "$src" "figures/$f"
    echo "Synced: figures/$f"
  fi
done

tectonic main.tex
echo "Built: $(pwd)/main.pdf"
