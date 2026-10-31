#!/usr/bin/env bash
# Build the site with a pinned Hugo version, whatever Hugo the host has.
# Cloudflare Pages build command: bash build.sh   (output directory: site/public)
set -euo pipefail

HUGO_VERSION="${HUGO_VERSION:-0.168.0}"
ROOT="$(cd "$(dirname "$0")" && pwd)"
BIN="$ROOT/.hugo/$HUGO_VERSION"

if [ ! -x "$BIN/hugo" ]; then
  case "$(uname -s)-$(uname -m)" in
    Linux-x86_64)  asset="linux-amd64.tar.gz" ;;
    Linux-aarch64) asset="linux-arm64.tar.gz" ;;
    Darwin-*)      asset="darwin-universal.tar.gz" ;;
    *) echo "No Hugo download for $(uname -s)-$(uname -m); install Hugo $HUGO_VERSION extended yourself." >&2; exit 1 ;;
  esac
  url="https://github.com/gohugoio/hugo/releases/download/v${HUGO_VERSION}/hugo_extended_${HUGO_VERSION}_${asset}"
  echo "Downloading Hugo $HUGO_VERSION extended from $url"
  mkdir -p "$BIN"
  curl -fsSL "$url" | tar -xz -C "$BIN" hugo
fi

"$BIN/hugo" version
exec "$BIN/hugo" --source "$ROOT/site" --minify "$@"
