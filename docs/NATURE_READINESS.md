# Nature / npj Quantum Information Readiness — Gap Analysis

This is an honest gap analysis against npj Quantum Information's published
submission guidelines (online submission, manuscript files, data availability,
computer code, supplementary information, statistical guidelines), not a
claim that this repository is ready for submission. Nothing below should be
read as "Nature-ready" — several items require experimental work (re-running
hardware jobs, exporting calibration data) that cannot be done by editing this
repository alone.

## Data availability
- Processed results (`data/quantum_results_verified.csv`) and figures are
  present and DOI-backed.
- Raw IBM JSON exports, QASM circuits, and backend calibration snapshots are
  **not** included (`data/results/`, `data/circuits/`, `data/calibration/` are
  empty). This is the single largest gap: four calibration-derived columns in
  the results CSV (`T1_avg_us`, `T2_avg_us`, `CZ_error_pct`,
  `readout_error_pct`) are currently marked `MISSING` for all 8 jobs.

## Code availability
- `parse_ibm_json.py` is open-source and documented (`docs/PARSER_FUNCTION_MAP.md`,
  `docs/RUNTIME_SAFETY.md`).
- No automated test suite exists yet (`tests/` is empty) — code availability
  is satisfied, but reviewers may reasonably ask for regression tests once the
  parser's calibration-handling path is exercised with real calibration data.

## Statistical guidelines
- `stats_report.pdf` and the Wilson confidence intervals / χ² reproducibility
  test in `data/quantum_results_verified.csv` cover the current 8-job dataset.
- No dedicated statistical appendix beyond `stats_report.pdf` exists.
- Sample size (8 jobs) is small; a submission would need to either justify
  this scope explicitly or expand the dataset.

## Supplementary information
- Not yet assembled. Would need to be authored once a manuscript exists
  (see `docs/ARXIV_PREP.md`).

## Manuscript
- No manuscript draft exists (`latex/` is empty).
- No target-journal decision has been made.

## What would actually move this forward
1. Export raw job JSON, QASM circuits, and calibration snapshots for the 8
   existing jobs (or re-run and capture them going forward) into
   `data/results/`, `data/circuits/`, `data/calibration/`.
2. Backfill the `MISSING` calibration columns in
   `data/quantum_results_verified.csv` using `parse_ibm_json.py --calib`.
3. Only after (1)–(2): draft a manuscript (see `docs/ARXIV_PREP.md`) and
   revisit this document with a concrete journal target.

This document should be revised whenever a gap above is actually closed —
not have items checked off in anticipation of future work.
