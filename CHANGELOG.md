# Changelog

All notable changes to this repository are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Fixed

- **`parse_ibm_json.py` — removed the P(11) fidelity override.** Bell fidelity
  was silently redefined as P(11) whenever a job's counts were >80% |11⟩,
  which manufactured the previously reported 96.3% headline from a
  single-basis-state (non-Bell) distribution. Bell fidelity is now always
  P(00)+P(11) from the measured counts (a ZZ-basis upper bound; see
  `docs/REMEDIATION_PLAN.md` §2.2 for the planned XYZ estimator).
- `data/quantum_results_verified.csv` — job `d5sd9mveglic739vatm0` flagged as
  anomalous: fidelity/CI/concurrence/tangle set to N/A (its Shannon entropy of
  0.278 implies ~96% of shots in one basis state, inconsistent with a Bell
  state). The best verified Bell result is now 94.4% (`d5sd2ioubqnc73c4im80`).
- `README.md` — repaired the CI and Docs Lint badge image URLs (they pointed at
  the repository URL instead of `badge.svg` endpoints); headline Bell result
  updated to 94.4% with an anomaly note.
- Citations now use the Zenodo concept DOI `10.5281/zenodo.21427292` (resolves
  to the latest version) in `README.md`, `CITATION.cff`, `latex/main.tex`,
  `latex/statistical_appendix.tex`, `latex/ibm-experiments-paper/bibliography.bib`
  and `notebooks/README.md`; `.zenodo.json` `isNewVersionOf` now points at the
  v1.1.0 deposit (21427293) instead of v1.0.0.
- `data/checksums/release_sha256.txt` regenerated for the corrected
  `parse_ibm_json.py` and `data/quantum_results_verified.csv`.

### Added

- `docs/REMEDIATION_PLAN.md` — full audit findings and step-by-step correction
  plan for the scientific-accuracy issues found in the repository review.
- `scripts/fetch_raw_results.py` — downloads the raw job info/result JSONs
  (and optionally calibration snapshots) from the IBM Quantum account into
  `data/results/`, in the RuntimeEncoder format the parser decodes.
- `data/results/README.md` — how to populate and verify the raw-data
  directory (automated fetch or manual dashboard download).

- `notebooks/` — six Jupyter notebooks: Bell state entanglement, BB84 QKD,
  VQC, and QRNG/reproducibility (QPU reproduction of the verified
  experiments), a QPU benchmarking pipeline over
  `data/quantum_results_verified.csv`, and an extended noise-model analysis.
- `analysis/noise_model_extended.py` — gate-dependent depolarizing + crosstalk
  noise model with bootstrap parameter uncertainty and AIC/BIC comparison.
- `latex/statistical_appendix.tex` — formal write-up of the statistical
  methods used by the dataset (Wilson CI, chi-squared, entropy, concurrence).
- `latex/ibm-experiments-paper/` — full sectioned paper draft for this
  dataset (values mirror the verified CSV).
- `SECURITY.md` — private vulnerability reporting policy.
- `latex/main.tex` — arXiv manuscript scaffold: title/authors, Methods
  section describing the actual parser and hardware, a full Results table
  generated from `data/quantum_results_verified.csv`, and an explicit
  Limitations section. Abstract, Introduction, Results narrative, and
  Discussion are marked `% TODO(author)` and contain no invented claims.
- `latex/bibliography.bib` — two foundational references (Nielsen & Chuang
  2010; Bennett & Brassard 1984), pending expansion.

### Changed

- `latex/main.tex` — all eight `TODO(author)` sections completed (abstract,
  introduction, circuit descriptions, results narrative, discussion,
  sample-size justification, acknowledgments) using only values from
  `data/quantum_results_verified.csv`; the manuscript now compiles as a
  full draft.
- `docs/ARXIV_PREP.md` updated to reflect the `latex/` scaffold's actual
  status (in progress, not done).

## [1.1.1] - 2026-07-18

Metadata-only patch release (no new Zenodo deposit; no experimental data,
parser code, figures, or metrics changed).

### Fixed

- Synchronized version and DOI metadata across `CITATION.cff` and
  `.zenodo.json` after the Zenodo v1.1.0 publication.
- Updated the GitHub repository About description and homepage URL.

## [1.1.0] - 2026-07-11

### Fixed

- Removed 8 duplicate figure PNGs that existed both at repo root and in `data/figures/` (byte-identical, left over from an earlier commit).
- Added the missing `fig1_bell_state_comparison.png` reference to `README.md` and `docs/DATA_AVAILABILITY.md` (present on disk but missing from both docs since it was added).
- Regenerated `docs/REPOSITORY_MAP.md` to match the actual repository layout.
- Removed stray zero-width-space characters preceding 7 of the 8 job IDs in `docs/JOB_IDS.md`.
- Pinned `numpy` and `scipy` versions in `requirements.txt`.
- Fixed `parse_ibm_json.py`'s default output filename (`quantum_results.csv`) to match the file actually committed to this repository (`data/quantum_results_verified.csv`).
- Translated the remaining Croatian text fragment in `docs/IBM_QUANTUM_EXPERIMENTS_AUDIT.md` to English for consistency with the rest of the documentation.

### Changed

- Moved `quantum_results_verified.csv` from the repo root into `data/`.
- Consolidated all experiment figures into a single top-level `figures/` directory (previously duplicated at root and under `data/figures/`).

### Added

- `.zenodo.json` — structured metadata for the next Zenodo release (mirrors `CITATION.cff`).
- `CODE_OF_CONDUCT.md`, `CONTRIBUTING.md`.
- `environment.yml`, `Dockerfile` — reproducible environment definitions.
- `.github/ISSUE_TEMPLATE/`, `.github/PULL_REQUEST_TEMPLATE.md`.
- `.github/workflows/ci.yml`, `.github/workflows/docs.yml`, `.github/workflows/release.yml`.
- `data/checksums/release_sha256.txt` and `scripts/verify_checksums.sh` — release file integrity checking.
- `scripts/smoke_test.sh` — parser compile check and CSV shape validation.
- `docs/RUNTIME_SAFETY.md`, `docs/CHECKSUMS.md`, `docs/ARXIV_PREP.md`, `docs/NATURE_READINESS.md`.
- `release/v1.1.0/RELEASE_NOTES.md`, `release/v1.1.0/MANIFEST.md`, `release/zenodo_deposit.json`.
- Reserved (empty, `.gitkeep`-tracked) directories for future content: `analysis/`, `notebooks/`, `latex/`, `tests/`, `data/raw_bitarrays/`. These are intentionally left without placeholder code — see `docs/NATURE_READINESS.md` for what triggers populating each one.

## [1.0.0] - 2026-06-19

- Initial Zenodo release. DOI: 10.5281/zenodo.20749395.
