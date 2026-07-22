#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
noise_model_extended.py
Extended QPU noise model for IBM-Quantum-Experiments.

Models:
  - gate-dependent depolarizing (separate errors for 1q and 2q gates)
  - readout error (single per-qubit misassignment rate)
  - crosstalk factor
  - thermal decay (T1/T2, fixed from calibration — not fitted)
  - bootstrap uncertainty on fitted parameters
  - AIC/BIC comparison (simple vs extended model)

IMPORTANT (read before using in a paper):
  The extended model fits 4 parameters (p_1q, p_2q, r, alpha_xtalk). With few
  Bell measurements (e.g. 3-4 points) it will OVERFIT — a good in-sample fit
  that is not statistically significant. Use the AIC/BIC comparison to check
  whether the extended model is REALLY better than the 2-parameter simple
  model. If AIC/BIC is not lower for the extended model, report the simple
  model. Reliable identification of the extended model needs >= 10 Bell
  circuits of varying depth.

Note on readout: an earlier revision exposed r0 (P(0->1)) and r1 (P(1->0))
separately but used only their average (r0+r1)/2, so the two were
non-identifiable from fidelity data alone (the optimizer returned r0 == r1).
This version fits a single readout rate r. True asymmetric readout requires
per-qubit assignment-matrix calibration data, not Bell fidelity, and is left
for a future revision once data/calibration/ is populated.

Dependencies:
  pip install numpy pandas scipy
"""

import numpy as np
import pandas as pd
from scipy.optimize import minimize


# ---------------------------------------------------------
# 1. Noise model components
# ---------------------------------------------------------

def depolarizing_fidelity_gate_dependent(p_1q, p_2q, n_1q, n_2q):
    """Depolarizing with separate error for 1q and 2q gates.
    Fidelity factor = (1-p_1q)^n_1q * (1-p_2q)^n_2q"""
    return (1 - p_1q) ** n_1q * (1 - p_2q) ** n_2q


def crosstalk_factor(alpha_xtalk, n_pairs):
    """Crosstalk: exp(-alpha * n_pairs).
    n_pairs ~ number of simultaneously active qubit pairs."""
    return np.exp(-alpha_xtalk * n_pairs)


def readout_fidelity(r, n_qubits):
    """Readout error: single per-qubit misassignment rate r.
    Fidelity factor = (1-r)^n_qubits."""
    return (1 - r) ** n_qubits


def thermal_decay_factor(t, t1, t2):
    """Thermal decay from T1/T2. t, t1, t2 in the same units (s)."""
    if t1 <= 0 or t2 <= 0:
        return 1.0
    amp = np.exp(-t / t1)      # amplitude damping (T1)
    deph = np.exp(-t / t2)     # dephasing (T2)
    return np.sqrt(amp * deph)


def combined_model_extended(params, row):
    """Combined extended model (4 fitted params; T1/T2 fixed from calibration).
    row needs: n_1q, n_2q, n_pairs, n_qubits, t1, t2, duration_s"""
    p_1q = params["p_1q"]
    p_2q = params["p_2q"]
    r = params["r"]
    alpha_xtalk = params["alpha_xtalk"]

    n_1q = row.get("n_1q", row.get("depth_1q", 0))
    n_2q = row.get("n_2q", row.get("depth_2q", 0))
    n_pairs = row.get("n_pairs", 1)
    n_qubits = row.get("n_qubits", 2)
    t1 = row.get("t1", 1e9)
    t2 = row.get("t2", 1e9)
    duration = row.get("duration_s", (n_1q + n_2q) * 50e-9)

    f_dep = depolarizing_fidelity_gate_dependent(p_1q, p_2q, n_1q, n_2q)
    f_ro = readout_fidelity(r, n_qubits)
    f_xt = crosstalk_factor(alpha_xtalk, n_pairs)
    f_th = thermal_decay_factor(duration, t1, t2)
    return f_dep * f_ro * f_xt * f_th


# Number of fitted parameters in the extended model (p_1q, p_2q, r, alpha_xtalk).
N_PARAMS_EXTENDED = 4
# Number of fitted parameters in the simple model (p_gate, r).
N_PARAMS_SIMPLE = 2


# ---------------------------------------------------------
# 2. Fitting the extended model to Bell data
# ---------------------------------------------------------

def fit_extended_model(bell_df):
    """Fits p_1q, p_2q, r, alpha_xtalk to Bell fidelity.
    bell_df columns: fidelity, n_1q, n_2q, n_pairs, n_qubits, t1, t2, duration_s"""
    x0 = np.array([0.005, 0.02, 0.01, 0.05])
    bounds = [(1e-6, 0.1), (1e-6, 0.3), (0.0, 0.1), (0.0, 0.5)]

    def loss(x):
        params = {"p_1q": float(x[0]), "p_2q": float(x[1]),
                  "r": float(x[2]), "alpha_xtalk": float(x[3])}
        preds = bell_df.apply(lambda r: combined_model_extended(params, r), axis=1)
        meas = bell_df["fidelity"].values
        return np.sum((preds - meas) ** 2)

    res = minimize(loss, x0, bounds=bounds, method="L-BFGS-B")
    params_hat = {"p_1q": float(res.x[0]), "p_2q": float(res.x[1]),
                  "r": float(res.x[2]), "alpha_xtalk": float(res.x[3])}
    bell_df = bell_df.copy()
    bell_df["predicted_fidelity_ext"] = bell_df.apply(
        lambda r: combined_model_extended(params_hat, r), axis=1)
    return params_hat, bell_df, res.fun


def fit_simple_model(bell_df):
    """Fits the 2-parameter simple model: single gate error p and readout r.
    F = (1-p)^(n_1q+n_2q) * (1-r)^n_qubits. Returns (params_hat, sse)."""
    def loss(x):
        p, r = x
        preds = bell_df.apply(
            lambda row: (1 - p) ** (row["n_1q"] + row["n_2q"])
            * (1 - r) ** row["n_qubits"], axis=1)
        return np.sum((preds - bell_df["fidelity"].values) ** 2)

    res = minimize(loss, [0.01, 0.01],
                   bounds=[(1e-6, 0.2), (0.0, 0.1)], method="L-BFGS-B")
    return {"p_gate": float(res.x[0]), "r": float(res.x[1])}, res.fun


# ---------------------------------------------------------
# 3. Bootstrap uncertainty on the parameters
# ---------------------------------------------------------

def bootstrap_params(bell_df, n_boot=1000):
    """Bootstrap over Bell rows to estimate parameter uncertainty."""
    param_samples = []
    for _ in range(n_boot):
        sample = bell_df.sample(frac=1.0, replace=True)
        try:
            params_hat, _, _ = fit_extended_model(sample)
            param_samples.append(params_hat)
        except Exception:
            continue
    if not param_samples:
        return {}
    keys = param_samples[0].keys()
    stats = {}
    for k in keys:
        vals = np.array([p[k] for p in param_samples])
        stats[k] = {"mean": float(vals.mean()), "std": float(vals.std()),
                    "min": float(vals.min()), "max": float(vals.max())}
    return stats


# ---------------------------------------------------------
# 4. AIC / BIC comparison (simple vs extended)
# ---------------------------------------------------------

def aic_bic_from_sse(sse, n_params, n_points):
    """AIC/BIC from the sum of squared errors (Gaussian assumption)."""
    sigma2 = sse / n_points
    if sigma2 <= 0:
        sigma2 = 1e-12
    loglik = -0.5 * n_points * (np.log(2 * np.pi * sigma2) + 1)
    aic = 2 * n_params - 2 * loglik
    bic = n_params * np.log(n_points) - 2 * loglik
    return aic, bic


def compare_models(simple_sse, ext_sse, n_points,
                   n_params_simple=N_PARAMS_SIMPLE,
                   n_params_ext=N_PARAMS_EXTENDED):
    """Compares simple vs extended model via AIC/BIC.
    LOWER AIC/BIC = better model. If simple has a lower AIC, use simple!"""
    aic_s, bic_s = aic_bic_from_sse(simple_sse, n_params_simple, n_points)
    aic_e, bic_e = aic_bic_from_sse(ext_sse, n_params_ext, n_points)
    verdict = "extended" if aic_e < aic_s else "simple"
    return {"simple": {"AIC": aic_s, "BIC": bic_s},
            "extended": {"AIC": aic_e, "BIC": bic_e},
            "preferred_by_AIC": verdict}


# ---------------------------------------------------------
# DEMO / self-test on the verified Bell fidelities
# ---------------------------------------------------------

if __name__ == "__main__":
    # Genuine Bell fidelities from data/quantum_results_verified.csv (Z-basis
    # P(00)+P(11)). Job d5sd9mveglic739vatm0 (formerly 0.9630) is EXCLUDED: it
    # is flagged anomalous (single-basis-state distribution, not a Bell state)
    # in the CSV and docs/REMEDIATION_PLAN.md, so its fidelity is N/A.
    # T1/T2 are placeholders pending data/calibration/ (see the note above);
    # they are fixed, not fitted, so they do not affect the parameter count.
    bell_rows = pd.DataFrame([
        # backend    fidelity  n_1q n_2q n_pairs n_qubits t1(s)     t2(s)     duration_s
        {"backend": "ibm_torino", "fidelity": 0.859, "n_1q": 2, "n_2q": 1,
         "n_pairs": 1, "n_qubits": 2, "t1": 195.91e-6, "t2": 209.75e-6,
         "duration_s": 3 * 50e-9},
        {"backend": "ibm_fez", "fidelity": 0.940, "n_1q": 2, "n_2q": 1,
         "n_pairs": 1, "n_qubits": 2, "t1": 195.91e-6, "t2": 209.75e-6,
         "duration_s": 3 * 50e-9},
        {"backend": "ibm_fez", "fidelity": 0.944, "n_1q": 2, "n_2q": 1,
         "n_pairs": 1, "n_qubits": 2, "t1": 176.01e-6, "t2": 102.07e-6,
         "duration_s": 3 * 50e-9},
    ])

    print("=" * 64)
    print("  EXTENDED NOISE MODEL — self-test on verified Bell data")
    print("=" * 64)
    print(f"\n  Number of measurements: {len(bell_rows)}")
    print(f"  Extended-model parameters: {N_PARAMS_EXTENDED}")
    if len(bell_rows) <= N_PARAMS_EXTENDED:
        print(f"  WARNING: {N_PARAMS_EXTENDED} parameters on {len(bell_rows)}"
              " points = OVERFITTING.")
        print("     Not statistically significant. See AIC/BIC below;"
              " use >= 10 Bell circuits for the extended fit.")

    params_ext, bell_ext, sse_ext = fit_extended_model(bell_rows)
    print(f"\n  Fitted parameters (extended):")
    for k, v in params_ext.items():
        print(f"    {k:14s} = {v:.6f}")
    print(f"  SSE (extended) = {sse_ext:.2e}")

    print(f"\n  Predictions vs measured:")
    for _, r in bell_ext.iterrows():
        print(f"    {r['backend']:11s}  measured={r['fidelity']:.4f}  "
              f"predicted={r['predicted_fidelity_ext']:.4f}")

    params_simple, simple_sse = fit_simple_model(bell_rows)
    print(f"\n  Fitted parameters (simple):")
    for k, v in params_simple.items():
        print(f"    {k:14s} = {v:.6f}")
    print(f"  SSE (simple)   = {simple_sse:.2e}")

    print(f"\n  Model comparison (LOWER AIC = better):")
    cmp = compare_models(simple_sse, sse_ext, len(bell_rows))
    print(f"    simple   AIC={cmp['simple']['AIC']:.2f}  "
          f"BIC={cmp['simple']['BIC']:.2f}")
    print(f"    extended AIC={cmp['extended']['AIC']:.2f}  "
          f"BIC={cmp['extended']['BIC']:.2f}")
    print(f"    -> preferred by AIC: {cmp['preferred_by_AIC'].upper()}")

    print("\n  CONCLUSION:")
    if cmp["preferred_by_AIC"] == "simple":
        print("  The simple model is preferred for this data. The extended")
        print("  model overfits with so few points — do NOT report it as")
        print("  justified. Acquire more Bell measurements (10+).")
    else:
        print("  The extended model is preferred — but verify with the")
        print("  bootstrap std before reporting.")
    print("=" * 64)
