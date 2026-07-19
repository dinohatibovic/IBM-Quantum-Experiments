# Notebooks

Jupyter notebooks accompanying the verified experiments in this repository
(Zenodo DOI 10.5281/zenodo.20749395).

| Notebook | Purpose | Runs where |
| --- | --- | --- |
| `01_Bell_State_Entanglement.ipynb` | Reproduce the Bell state experiment (ibm_fez vs ibm_torino) | IBM QPU (credentials required) |
| `02_BB84_QKD.ipynb` | Reproduce BB84 with Alice/Eve/Bob and QBER measurement | IBM QPU (credentials required) |
| `03_VQC.ipynb` | Reproduce the variational quantum circuit experiment | IBM QPU (credentials required) |
| `04_QRNG_Reproducibility.ipynb` | Reproduce QRNG and the chi-squared reproducibility test | IBM QPU (credentials required) |
| `05_QPU_Benchmarking.ipynb` | Benchmarking pipeline over `data/quantum_results_verified.csv` | Local |
| `06_QPU_Noise_Model_Analysis.ipynb` | Extended noise model fit (see `analysis/noise_model_extended.py`) | Local |

## Dependencies

The repository's core `requirements.txt` stays minimal (numpy, scipy). The
notebooks additionally need:

```bash
pip install matplotlib pandas seaborn statsmodels jupyter
pip install qiskit qiskit-ibm-runtime   # only for notebooks 01-04 (QPU execution)
```

Notebooks 01–04 submit real jobs to IBM Quantum and require a configured
`QiskitRuntimeService` account. Notebooks 05–06 run fully offline against the
committed dataset.
