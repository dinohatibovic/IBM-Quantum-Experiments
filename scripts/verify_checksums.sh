#!/usr/bin/env bash
# Verifies tracked release files against data/checksums/release_sha256.txt.
set -euo pipefail
cd "$(dirname "$0")/.."

if [ ! -s data/checksums/release_sha256.txt ]; then
    echo "data/checksums/release_sha256.txt is missing or empty" >&2
    exit 1
fi

sha256sum -c data/checksums/release_sha256.txt
