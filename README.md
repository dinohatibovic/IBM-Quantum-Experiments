# IBM Quantum Hardware Experiments

[![CI](https://github.com/dinohatibovic/IBM-Quantum-Experiments)](https://github.com/dinohatibovic/IBM-Quantum-Experiments/actions/workflows/ci.yml)
[![Docs Lint](https://github.com/dinohatibovic/IBM-Quantum-Experiments)](https://github.com/dinohatibovic/IBM-Quantum-Experiments/actions/workflows/docs.yml)
[![DOI](https://zenodo.org/)](https://doi.org/10.5281/zenodo.21427293)

Verified quantum computing experiments on real IBM hardware.

- ibm_fez — 156 qubits, Heron R2
- ibm_torino — 133 qubits, Heron R1

## Key Results

| Experiment | Result |
| --- | --- |
| Bell fidelity | 96.3% (C=0.926) |
| BB84 QBER degradation | 82× |
| Reproducibility | χ²=2.70, p=0.44 |
| Total shots | 39,010 |

## Citation

Hatibović, D. (2026). Verified IBM Quantum Hardware Experiments (Version 1.1.0) [Computer software]. Zenodo. https://doi.org/10.5281/zenodo.21427293

All versions DOI: https://doi.org/10.5281/zenodo.21427292

See `CITATION.cff` for machine-readable citation metadata.

## Repository Structure

```text
.
├── parse_ibm_json.py          — parser for IBM SamplerV2 result data
├── data/
│   ├── quantum_results_verified.csv  — processed table of experiment metrics
│   ├── results/                — reserved: raw IBM job-*-info.json / job-*-result.json exports
│   ├── circuits/                — reserved: QASM / IBM Quantum Composer circuit files
│   ├── calibration/             — reserved: IBM backend calibration exports
│   ├── raw_bitarrays/           — reserved: raw decoded BitArray dumps
│   └── checksums/               — SHA-256 checksums of tracked release files
├── figures/                    — experiment visualization figures
├── stats_report.pdf            — statistical report generated from decoded IBM result data
├── analysis/                    — reserved for additional analysis scripts (currently empty; see docs/REPOSITORY_MAP.md)
├── notebooks/                   — reserved for exploratory notebooks (currently empty)
├── latex/                       — arXiv preprint source (factual scaffold; narrative sections pending, see docs/ARXIV_PREP.md)
├── scripts/                     — maintenance scripts (smoke test, checksum verification)
├── tests/                       — reserved for automated tests (currently empty)
├── release/                     — per-release notes and manifests
├── docs/                        — repository documentation (see list below)
├── .github/                     — issue/PR templates and CI workflows
├── CHANGELOG.md
├── CITATION.cff
├── CODE_OF_CONDUCT.md
├── CONTRIBUTING.md
├── LICENSE
├── requirements.txt
└── environment.yml / Dockerfile — reproducible environment definitions
```

Documentation index:

- `docs/JOB_IDS.md` — IBM Quantum job identifiers.
- `docs/PARSER_FUNCTION_MAP.md` — parser function index.
- `docs/DATA_AVAILABILITY.md` — current data availability manifest.
- `docs/REPOSITORY_MAP.md` — full repository layout.
- `docs/CHECKSUMS.md` — how release file checksums are generated and verified.
- `docs/RUNTIME_SAFETY.md` — parser runtime/safety notes.
- `docs/ARXIV_PREP.md` — honest checklist of what's needed before an arXiv submission.
- `docs/NATURE_READINESS.md` — honest gap analysis against npj Quantum Information submission guidelines.

Empty reserved directories (`analysis/`, `notebooks/`, `tests/`, `data/results/`, `data/circuits/`, `data/calibration/`, `data/raw_bitarrays/`) are tracked with `.gitkeep` and intentionally contain no placeholder code — they are populated only when real content exists (see `docs/NATURE_READINESS.md` and `CHANGELOG.md` for the rationale). `latex/` is no longer empty (see `docs/ARXIV_PREP.md`).

## Data Availability

This repository currently includes processed CSV results, a statistical PDF report, parser code and experiment figures. Raw IBM JSON exports, QASM circuit files and backend calibration exports are not currently included.

See `docs/DATA_AVAILABILITY.md` for the current file availability status.

## Figures

Experiment figures are available in `figures/`:

- `fig1_bell_state_comparison.png`
- `fig2_reproducibility.png`
- `fig3_bb84_d5sd7.png`
- `fig4_bb84_control_group.png`
- `fig5_qrng_8bit.png`
- `fig6_vqc_4qubit.png`
- `fig7_entanglement_metrics.png`
- `fig8_timeline_summary.png`

## Contributing

See `CONTRIBUTING.md` and `CODE_OF_CONDUCT.md`.
