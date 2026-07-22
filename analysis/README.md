# Analysis

- `noise_model_extended.py` — extended QPU noise model for the Bell-state
  fidelity data in this repository: gate-dependent depolarizing errors
  (separate 1q/2q), a single-rate readout error, a crosstalk factor, thermal
  T1/T2 decay (fixed from calibration), bootstrap parameter-uncertainty
  estimation, and an AIC/BIC comparison against a 2-parameter simple model.
  The extended model has **4 fitted parameters** (p_1q, p_2q, r, alpha_xtalk).
  Run `python analysis/noise_model_extended.py` for a self-test on the three
  verified Bell fidelities (0.859, 0.940, 0.944); the anomalous job
  `d5sd9mveglic739vatm0` is excluded (see `docs/REMEDIATION_PLAN.md` §2.1,
  §3.3). With only three points the self-test correctly prefers the simple
  model — the extended fit needs >= 10 Bell circuits to be identifiable.
  Demonstrated in `notebooks/06_QPU_Noise_Model_Analysis.ipynb`.

## Dependencies

```bash
pip install numpy scipy pandas
```
