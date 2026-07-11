# Contributing

This repository hosts verified IBM Quantum hardware experiment data and the
parser used to derive published metrics. Contributions are welcome, with the
following expectations.

## Reporting issues

Use the GitHub issue templates under `.github/ISSUE_TEMPLATE/`. Please include
the affected job ID(s) (see `docs/JOB_IDS.md`) when reporting a data or metric
discrepancy.

## Proposing changes

1. Fork the repository and create a branch from `main`.
2. Keep changes focused — one logical change per pull request.
3. If you change `parse_ibm_json.py`, run `bash scripts/smoke_test.sh` locally
   before opening a pull request; CI runs the same check.
4. If you add or modify a tracked release file under `data/` or `figures/`,
   regenerate `data/checksums/release_sha256.txt` (`bash scripts/verify_checksums.sh --update`
   is not currently implemented — regenerate manually with `sha256sum` and update
   the file, see `docs/CHECKSUMS.md`).
5. Update `CHANGELOG.md` under an `[Unreleased]` heading.
6. Open a pull request using the template in `.github/PULL_REQUEST_TEMPLATE.md`.

## Scope

This is primarily a single-author verified-results repository tied to a Zenodo
DOI (see `CITATION.cff`). Substantial changes to reported metrics or historical
job data will be reviewed carefully to preserve reproducibility of already-cited
results.

## Code of Conduct

Participation is governed by `CODE_OF_CONDUCT.md`.
