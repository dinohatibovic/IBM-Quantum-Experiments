import numpy as np
import pandas as pd
from scipy.optimize import minimize
from scipy.stats import chisquare

# ---------------------------------------------------------
# 1. Gate-dependent + crosstalk noise model
# ---------------------------------------------------------

def depolarizing_fidelity_gate_dependent(p_1q, p_2q, n_1q, n_2q):
    """
    Depolarizing model with separate error per 1q and 2q gate.
    Fidelity factor = (1 - p_1q)^{n_1q} * (1 - p_2q)^{n_2q}
    """
    return (1 - p_1q) ** n_1q * (1 - p_2q) ** n_2q


def crosstalk_factor(alpha_xtalk, n_pairs):
    """
    Simple crosstalk factor: exp(-alpha_xtalk * n_pairs)
    n_pairs ~ number of simultaneously active qubit pairs.
    """
    return np.exp(-alpha_xtalk * n_pairs)


def readout_fidelity_asym(r0, r1, n_qubits):
    """
    Asymmetric readout error (approximate factor).
    r0: P(0 -> 1), r1: P(1 -> 0)
    For simplicity, use average error per qubit.
    """
    r_avg = (r0 + r1) / 2.0
    return (1 - r_avg) ** n_qubits


def thermal_decay_factor(t, t1, t2):
    if t1 <= 0 or t2 <= 0:
        return 1.0
    amp = np.exp(-t / t1)
    deph = np.exp(-t / t2)
    return np.sqrt(amp * deph)


def combined_model_extended(params, row):
    """
    Extended model:
    - gate-dependent depolarizing (p_1q, p_2q)
    - asymmetric readout (r0, r1)
    - crosstalk (alpha_xtalk)
    - thermal decay (t1, t2, duration)
    row must contain: n_1q, n_2q, n_pairs, n_qubits, t1, t2, duration_s
    """
    p_1q = params["p_1q"]
    p_2q = params["p_2q"]
    r0 = params["r0"]
    r1 = params["r1"]
    alpha_xtalk = params["alpha_xtalk"]

    n_1q = row.get("n_1q", row.get("depth_1q", 0))
    n_2q = row.get("n_2q", row.get("depth_2q", 0))
    n_pairs = row.get("n_pairs", 1)
    n_qubits = row.get("n_qubits", 2)
    t1 = row.get("t1", 1e9)
    t2 = row.get("t2", 1e9)
    duration = row.get("duration_s", (n_1q + n_2q) * 50e-9)

    f_dep = depolarizing_fidelity_gate_dependent(p_1q, p_2q, n_1q, n_2q)
    f_ro = readout_fidelity_asym(r0, r1, n_qubits)
    f_xt = crosstalk_factor(alpha_xtalk, n_pairs)
    f_th = thermal_decay_factor(duration, t1, t2)

    return f_dep * f_ro * f_xt * f_th

# ---------------------------------------------------------
# 2. Fitting extended model to Bell rows
# ---------------------------------------------------------

def fit_extended_model(bell_df):
    """
    Fit p_1q, p_2q, r0, r1, alpha_xtalk to Bell fidelity data.
    bell_df must have columns: fidelity, n_1q, n_2q, n_pairs, n_qubits, t1, t2, duration_s
    """
    x0 = np.array([0.005, 0.02, 0.01, 0.01, 0.05])  # initial guess
    bounds = [(1e-6, 0.1), (1e-6, 0.3), (0.0, 0.1), (0.0, 0.1), (0.0, 0.5)]

    def loss(x):
        params = {
            "p_1q": float(x[0]),
            "p_2q": float(x[1]),
            "r0": float(x[2]),
            "r1": float(x[3]),
            "alpha_xtalk": float(x[4]),
        }
        preds = bell_df.apply(lambda r: combined_model_extended(params, r), axis=1)
        meas = bell_df["fidelity"].values
        return np.sum((preds - meas) ** 2)

    res = minimize(loss, x0, bounds=bounds, method="L-BFGS-B")
    params_hat = {
        "p_1q": float(res.x[0]),
        "p_2q": float(res.x[1]),
        "r0": float(res.x[2]),
        "r1": float(res.x[3]),
        "alpha_xtalk": float(res.x[4]),
    }
    bell_df = bell_df.copy()
    bell_df["predicted_fidelity_ext"] = bell_df.apply(
        lambda r: combined_model_extended(params_hat, r), axis=1
    )
    return params_hat, bell_df, res.fun

# ---------------------------------------------------------
# 3. Bootstrap uncertainty on parameters
# ---------------------------------------------------------

def bootstrap_params(bell_df, n_boot=1000):
    """
    Bootstrap over Bell rows to estimate parameter uncertainty.
    Returns: dict with mean, std for each parameter.
    """
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
        stats[k] = {
            "mean": float(vals.mean()),
            "std": float(vals.std()),
            "min": float(vals.min()),
            "max": float(vals.max()),
        }
    return stats

# ---------------------------------------------------------
# 4. AIC / BIC comparison (simple vs extended model)
# ---------------------------------------------------------

def aic_bic_from_sse(sse, n_params, n_points):
    """
    AIC/BIC from sum of squared errors (Gaussian assumption).
    """
    sigma2 = sse / n_points
    loglik = -0.5 * n_points * (np.log(2 * np.pi * sigma2) + 1)
    aic = 2 * n_params - 2 * loglik
    bic = n_params * np.log(n_points) - 2 * loglik
    return aic, bic

def compare_models(simple_sse, ext_sse, n_points):
    """
    Compare simple vs extended model via AIC/BIC.
    simple: 2 params (p_gate, r_readout)
    extended: 5 params (p_1q, p_2q, r0, r1, alpha_xtalk)
    """
    aic_simple, bic_simple = aic_bic_from_sse(simple_sse, 2, n_points)
    aic_ext, bic_ext = aic_bic_from_sse(ext_sse, 5, n_points)
    return {
        "simple": {"AIC": aic_simple, "BIC": bic_simple},
        "extended": {"AIC": aic_ext, "BIC": bic_ext},
    }
