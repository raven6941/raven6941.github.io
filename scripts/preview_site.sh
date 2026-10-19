#!/usr/bin/env sh
set -eu

ROOT="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
cd "$ROOT"

python3 scripts/build_site.py

case "$(uname -s)" in
  Darwin) open "$ROOT/_site/index.html" ;;
  Linux) xdg-open "$ROOT/_site/index.html" ;;
  *) printf 'Built %s/_site/index.html\n' "$ROOT" ;;
esac
