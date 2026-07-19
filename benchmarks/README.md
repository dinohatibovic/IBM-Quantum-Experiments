# nisq-hardware-benchmark

Comparison of IBM Heron r2 quantum hardware VQE results against the VQEzy classical dataset.

## Hardware Used

| Backend | Processor    | Qubits |
| ------- | ------------ | ------ |
| ibm_fez | IBM Heron r2 | 156    |

## Key Result

| | Energy (Hartree) | Basis |
| --- | --- | --- |
| IBM Heron r2 (real hardware) | -1.196080 | VQC full |
| VQEzy dataset (sample_8) | -0.886831 | 4-qubit STO-3G |
| Difference | 0.309 Ha = 8.41 eV | — |

Published: Zenodo DOI [10.5281/zenodo.20749395](https://doi.org/10.5281/zenodo.20749395)

## Scripts

| Script | Description |
| --- | --- |
| `inspect_h2.py` | Print full HDF5 dataset key hierarchy |
| `extract_data.py` | Extract bond length, energy, params for any sample |
| `find_target.py` | Find closest VQEzy sample to IBM result, compare energies |

## Dataset Setup

Scripts expect the VQEzy H2 dataset at `./data/h2_4_qubit.h5`:

```bash
mkdir data
# Download from: https://github.com/chizhang24/VQEzy
cp /path/to/h2_4_qubit.h5 data/
```

## Install

```bash
pip install -r requirements.txt
```

## Run

```bash
python inspect_h2.py
python extract_data.py
python find_target.py
```

## Environment

Developed and tested on Android aarch64 (Termux + Ubuntu PRoot)
with Mobile Quantum Labs setup (165 scientific packages).

## About Energy Difference

The difference between IBM hardware and VQEzy results is expected.
VQEzy uses a minimal 4-qubit STO-3G basis with restricted ansatz depth.
The IBM VQC result uses a deeper circuit on real Heron r2 hardware.
Comparing both against FCI (Full Configuration Interaction) ground truth
is the logical next step.

## Author

Dino Hatibovic
ORCID: [0009-0009-5351-6901](https://orcid.org/0009-0009-5351-6901)
