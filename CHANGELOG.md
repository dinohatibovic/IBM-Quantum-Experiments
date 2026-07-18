# Changelog

All notable changes to this repository are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added

- `latex/main.tex` — arXiv manuscript scaffold: title/authors, Methods
  section describing the actual parser and hardware, a full Results table
  generated from `data/quantum_results_verified.csv`, and an explicit
  Limitations section. Abstract, Introduction, Results narrative, and
  Discussion are marked `% TODO(author)` and contain no invented claims.
- `latex/bibliography.bib` — two foundational references (Nielsen & Chuang
  2010; Bennett & Brassard 1984), pending expansion.

### Changed

- `docs/ARXIV_PREP.md` updated to reflect the `latex/` scaffold's actual
  status (in progress, not done).

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
