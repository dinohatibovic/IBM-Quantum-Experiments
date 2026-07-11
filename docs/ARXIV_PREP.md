# arXiv Preparation Checklist

Honest status check against arXiv's submission expectations (topical,
refereeable scientific contribution; TeX/LaTeX or PDF manuscript; figures
included; registered author). This is a checklist, not a claim of readiness.

## Done
- [x] DOI-backed dataset on Zenodo (`CITATION.cff`, `.zenodo.json`).
- [x] Processed results table (`data/quantum_results_verified.csv`) with
      confidence intervals (Wilson CI for fidelity/QBER).
- [x] Statistical report (`stats_report.pdf`).
- [x] Reproducibility test between job pairs (χ²=2.70, p=0.44, see README).
- [x] All 8 figures referenced in the README are present in `figures/`.
- [x] Open-source parser (`parse_ibm_json.py`) with documented function map
      (`docs/PARSER_FUNCTION_MAP.md`).

## Missing
- [ ] No manuscript source exists yet. `latex/` is currently empty — no
      `main.tex`, no abstract, no methods/results/discussion sections have
      been drafted.
- [ ] No bibliography (`bibliography.bib`) has been assembled.
- [ ] Raw IBM JSON exports (`data/results/`), QASM circuits
      (`data/circuits/`), and backend calibration exports
      (`data/calibration/`) are not included — a manuscript would currently
      need to describe this as a data-availability limitation rather than
      point to included raw data.
- [ ] No supplementary materials document has been written.
- [ ] No statistical appendix beyond `stats_report.pdf` exists.

## Before submitting to arXiv
1. Write the manuscript in `latex/main.tex` once the above raw-data gaps are
   either filled or explicitly scoped out of the submission.
2. Add `latex/bibliography.bib`.
3. Re-run `scripts/smoke_test.sh` and update `data/checksums/release_sha256.txt`
   so the arXiv submission cites an exact, verifiable repository state.
4. Tag a Zenodo release matching the manuscript's data description.

This document should be updated as items are completed — do not mark an item
done until the corresponding file actually exists in this repository.
