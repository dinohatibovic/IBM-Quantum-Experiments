# v1.1.0 Release Notes

Professional repository restructuring. No experimental results changed -
this release is documentation, structure, and tooling only.

See `CHANGELOG.md` for the full itemized list. Summary:

- Fixed duplicate figure files, stale documentation, missing `fig1` references,
  stale repository map entries, zero-width-space characters in `docs/JOB_IDS.md`,
  unpinned dependency versions, a parser default-filename mismatch, and a
  leftover non-English documentation fragment.
- Restructured repository paths: figures are consolidated into `figures/`, and
  `quantum_results_verified.csv` moved into `data/`.
- Added `.zenodo.json`, `CHANGELOG.md`, `CODE_OF_CONDUCT.md`,
  `CONTRIBUTING.md`, `environment.yml`, `Dockerfile`, GitHub issue and pull
  request templates, CI workflows, release checksums, and additional
  documentation files.
- Added LaTeX manuscript scaffold in `latex/main.tex` and
  `latex/bibliography.bib`.
- Reserved empty directories (`analysis/`, `notebooks/`, `tests/`,
  `data/raw_bitarrays/`) were added for future milestones and intentionally
  contain no placeholder code.

## Upgrade notes

If you have scripts or notebooks referencing the old paths, update them:

- `quantum_results_verified.csv` -> `data/quantum_results_verified.csv`
- `data/figures/*.png` -> `figures/*.png`
