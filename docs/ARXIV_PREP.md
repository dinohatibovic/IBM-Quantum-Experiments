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

## In progress

- [~] `latex/main.tex` exists as a **factual scaffold only**: title/authors,
      a Methods section describing the actual parser and hardware, a full
      Results table generated directly from
      `data/quantum_results_verified.csv`, and an explicit Limitations
      section documenting the missing calibration/raw-data gaps below. The
      Abstract, Introduction, Results narrative, and Discussion are marked
      `% TODO(author)` and contain no invented claims or interpretation —
      those sections require the author's own scientific writing.
- [~] `latex/bibliography.bib` exists with two well-established foundational
      references (Nielsen & Chuang 2010; Bennett & Brassard 1984). It needs
      expansion with actual related work once the Introduction/Discussion
      are written.

## Missing

- [ ] Raw IBM JSON exports (`data/results/`), QASM circuits
      (`data/circuits/`), and backend calibration exports
      (`data/calibration/`) are not included — the manuscript currently
      describes this as a data-availability limitation (see
      `latex/main.tex`, Limitations section) rather than pointing to
      included raw data. The author has these files locally and intends to
      add them in a follow-up commit.
- [ ] No supplementary materials document has been written.
- [ ] No statistical appendix beyond `stats_report.pdf` exists.
- [ ] Abstract, Introduction, Results narrative, and Discussion in
      `latex/main.tex` are unwritten (`% TODO(author)` markers).

## Before submitting to arXiv

1. Backfill raw data (`data/results/`, `data/circuits/`, `data/calibration/`)
   and re-run `parse_ibm_json.py --calib` to fill the `MISSING` CSV columns.
2. Write the `% TODO(author)` sections of `latex/main.tex` — this cannot be
   automated; it requires the author's own scientific framing and
   interpretation.
3. Expand `latex/bibliography.bib` with real related-work citations.
4. Re-run `scripts/smoke_test.sh` and update `data/checksums/release_sha256.txt`
   so the arXiv submission cites an exact, verifiable repository state.
5. Tag a Zenodo release matching the manuscript's data description.

This document should be updated as items are completed — do not mark an item
done until the corresponding file actually exists in this repository.
