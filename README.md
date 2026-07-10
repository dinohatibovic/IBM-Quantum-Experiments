# IBM Quantum Hardware Experiments

[

![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20749395.svg)

](https://doi.org/10.5281/zenodo.20749395)

Verified quantum computing experiments on real IBM hardware.
- ibm_fez — 156 qubits, Heron R2
- ibm_torino — 133 qubits, Heron R1

## Key Results
| Experiment | Result |
|---|---|
| Bell fidelity | 96.3% (C=0.926) |
| BB84 QBER degradation | 82× |
| Reproducibility | χ²=2.70, p=0.44 |
| Total shots | 39,010 |

## Citation
Hatibović, D. (2026). Verified IBM Quantum Hardware Experiments.
Zenodo. https://doi.org/10.5281/zenodo.20749395

## Repository Structure

- `parse_ibm_json.py` — parser for IBM SamplerV2 result data.
- `quantum_results_verified.csv` — processed table of experiment metrics.
- `stats_report.pdf` — statistical report generated from decoded IBM result data.
- `data/figures/` — experiment visualization figures.
- `data/results/` — reserved location for raw IBM `job-*-info.json` and `job-*-result.json` exports.
- `data/circuits/` — reserved location for QASM / IBM Quantum Composer circuit files.
- `data/calibration/` — reserved location for IBM backend calibration exports or screenshots.
- `docs/JOB_IDS.md` — IBM Quantum job identifiers.
- `docs/PARSER_FUNCTION_MAP.md` — parser function index.
- `docs/DATA_AVAILABILITY.md` — current data availability manifest.
- `docs/REPOSITORY_MAP.md` — repository layout.

## Data Availability

This repository currently includes processed CSV results, a statistical PDF report, parser code and experiment figures. Raw IBM JSON exports, QASM circuit files and backend calibration exports are not currently included.

See `docs/DATA_AVAILABILITY.md` for the current file availability status.

## Figures

Experiment figures are available in `data/figures/`:

- `fig2_reproducibility.png`
- `fig3_bb84_d5sd7.png`
- `fig4_bb84_control_group.png`
- `fig5_qrng_8bit.png`
- `fig6_vqc_4qubit.png`
- `fig7_entanglement_metrics.png`
- `fig8_timeline_summary.png`

## Repository Structure

- `parse_ibm_json.py` — parser for IBM SamplerV2 result data.
- `quantum_results_verified.csv` — processed table of experiment metrics.
- `stats_report.pdf` — statistical report generated from decoded IBM result data.
- `data/figures/` — experiment visualization figures.
- `data/results/` — reserved location for raw IBM `job-*-info.json` and `job-*-result.json` exports.
- `data/circuits/` — reserved location for QASM / IBM Quantum Composer circuit files.
- `data/calibration/` — reserved location for IBM backend calibration exports or screenshots.
- `docs/JOB_IDS.md` — IBM Quantum job identifiers.
- `docs/PARSER_FUNCTION_MAP.md` — parser function index.
- `docs/DATA_AVAILABILITY.md` — current data availability manifest.
- `docs/REPOSITORY_MAP.md` — repository layout.

## Data Availability

This repository currently includes processed CSV results, a statistical PDF report, parser code and experiment figures. Raw IBM JSON exports, QASM circuit files and backend calibration exports are not currently included.

See `docs/DATA_AVAILABILITY.md` for the current file availability status.

## Figures

Experiment figures are available in `data/figures/`:

- `fig2_reproducibility.png`
- `fig3_bb84_d5sd7.png`
- `fig4_bb84_control_group.png`
- `fig5_qrng_8bit.png`
- `fig6_vqc_4qubit.png`
- `fig7_entanglement_metrics.png`
- `fig8_timeline_summary.png`
