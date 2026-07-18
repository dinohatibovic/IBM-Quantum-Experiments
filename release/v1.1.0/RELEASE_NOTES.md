# v1.1.0 Release Notes

Professional repository restructuring. No experimental results changed —
this release is documentation, structure, and tooling only.

See `CHANGELOG.md` for the full itemized list. Summary:

- Fixed: duplicate figure files, stale documentation (missing fig1 reference,
  stale repository map), zero-width-space characters in `docs/JOB_IDS.md`,
  unpinned dependency versions, a parser default-filename mismatch, and a
  leftover non-English documentation fragment.
- Restructured: figures consolidated into `figures/`; `quantum_results_verified.csv`
  moved into `data/`.
- Added: `.zenodo.json`, `CHANGELOG.md`, `CODE_OF_CONDUCT.md`, `CONTRIBUTING.md`,
  `environment.yml`, `Dockerfile`, GitHub issue/PR templates, three CI
  workflows (smoke test, markdown lint, release checksum verification),
  release checksums, and four new documentation files (`RUNTIME_SAFETY.md`,
  `CHECKSUMS.md`, `ARXIV_PREP.md`, `NATURE_READINESS.md`).
- Reserved empty directories (`analysis/`, `notebooks/`, `latex/`, `tests/`,
  `data/raw_bitarrays/`) were added for future milestones but intentionally
  contain no placeholder code — see `docs/NATURE_READINESS.md` for what
  triggers populating each one.

## Upgrade notes

If you have scripts or notebooks referencing the old paths, update them:

- `quantum_results_verified.csv` → `data/quantum_results_verified.csv`
- `data/figures/*.png` → `figures/*.png`
