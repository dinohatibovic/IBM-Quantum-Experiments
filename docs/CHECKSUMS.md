# Release Checksums

`data/checksums/release_sha256.txt` records SHA-256 checksums of the files
that make up a tagged release, so a downloaded copy (or a Zenodo deposit) can
be verified against what was actually released.

## Verifying

From the repository root:

```bash
bash scripts/verify_checksums.sh
```

This runs `sha256sum -c data/checksums/release_sha256.txt` and reports any
file that is missing or whose hash no longer matches.

## Regenerating (maintainers)

After changing any tracked file listed in the checksum manifest, regenerate it
from the repository root:

```bash
sha256sum \
  data/quantum_results_verified.csv \
  figures/*.png \
  stats_report.pdf \
  parse_ibm_json.py \
  > data/checksums/release_sha256.txt
```

Commit the updated `data/checksums/release_sha256.txt` alongside the file
change. `.github/workflows/release.yml` verifies this file matches the
repository contents whenever a GitHub Release is published.

## Scope

Only files with fixed content across the current release are checksummed
(processed CSV, figures, PDF report, parser script). Reserved-but-empty
directories (`data/results/`, `data/circuits/`, `data/calibration/`,
`data/raw_bitarrays/`) are not checksummed since they currently contain no
tracked data.
