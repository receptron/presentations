#!/usr/bin/env bash
# Assemble a self-contained arXiv upload tarball.
#
# The working tree keeps a single copy of each figure (docs/figures/,
# referenced via \figroot). arXiv requires a self-contained package, so this
# script copies the referenced figures in, rewrites \figroot to the local
# figures/ directory, verifies the package builds, and tars it up.
set -euo pipefail
cd "$(dirname "$0")"

PKG=arxiv-upload
rm -rf "$PKG" "$PKG.tar.gz"
mkdir -p "$PKG/figures"

sed 's|\\newcommand{\\figroot}{../../figures}|\\newcommand{\\figroot}{figures}|' main.tex > "$PKG/main.tex"
cp refs.bib "$PKG/"
grep -o '\\viewfig{\\figroot/[^}]*}' main.tex | sed 's|.*figroot/||; s|}||' | sort -u | while read -r f; do
  cp -p "../../figures/$f" "$PKG/figures/$f"
  echo "Packaged: figures/$f"
done

(cd "$PKG" && tectonic main.tex && rm -f main.pdf)
tar -czf "$PKG.tar.gz" -C "$PKG" .
echo "Packaged: $(pwd)/$PKG.tar.gz (build verified)"
