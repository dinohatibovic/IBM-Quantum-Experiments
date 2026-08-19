# Data Availability Manifest

## Present evidence files

```text
CITATION.cff
LICENSE
README.md
parse_ibm_json.py
data/quantum_results_verified.csv
requirements.txt
stats_report.pdf
```

## Raw JSON currently present

```text
data/results/.gitkeep
```

Raw IBM `job-*-info.json` / `job-*-result.json` exports are not currently included in this repository. `data/results/` is reserved for them.

## Figures currently present

```text
figures/fig1_bell_state_comparison.png
figures/fig2_reproducibility.png
figures/fig3_bb84_d5sd7.png
figures/fig4_bb84_control_group.png
figures/fig5_qrng_8bit.png
figures/fig6_vqc_4qubit.png
figures/fig7_entanglement_metrics.png
figures/fig8_timeline_summary.png
```

## Circuits currently present

```text
data/circuits/.gitkeep
```

QASM / IBM Quantum Composer circuit files are not currently included. `data/circuits/` is reserved for them.

## Calibration currently present

```text
data/calibration/.gitkeep
```

Backend calibration exports (`backend.properties()`) are not currently included — this is why the `T1_avg_us`, `T2_avg_us`, `CZ_error_pct`, and `readout_error_pct` columns in `data/quantum_results_verified.csv` are marked `MISSING`. `data/calibration/` is reserved for them.

## Raw bitarrays currently present

```text
data/raw_bitarrays/.gitkeep
```

Raw decoded `BitArray` dumps are not currently included. `data/raw_bitarrays/` is reserved for them.

## Checksums

```text
data/checksums/release_sha256.txt
```

SHA-256 checksums of the tracked release files above, generated at release time. See `docs/CHECKSUMS.md`.
