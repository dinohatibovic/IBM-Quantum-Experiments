# Analysis

- `noise_model_extended.py` — extended QPU noise model: gate-dependent depolarizing
  (separate 1q/2q errors), asymmetric readout, crosstalk factor, bootstrap parameter
  uncertainty, and AIC/BIC model comparison. Used from
  `notebooks/06_QPU_Noise_Model_Analysis.ipynb`.

## Dependencies

In addition to the MVP `requirements.txt` (numpy, scipy), the benchmarking notebooks
also need:

```bash
pip install pandas seaborn statsmodels matplotlib
```
