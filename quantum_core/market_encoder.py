"""
Quantum Market Encoder — rewritten from docs 9/10 for Qiskit 2.x.

Key changes from original:
  - No qiskit_finance (archived) — pure Qiskit 2.x
  - No EfficientSU2.assign_parameters() bug — correct ParameterVector usage
  - No yfinance dependency at import — optional, with fallback
  - Amplitude encoding: RY(2·arcsin(√p)) is the correct formula
"""

from __future__ import annotations
from typing import Any, Dict, List
import numpy as np

from qiskit import QuantumCircuit
from qiskit.circuit.library import TwoLocal

# ============================================================================
# Amplitude Encoding of Market Returns
# ============================================================================


def encode_returns_to_circuit(
    returns: List[float],
    name: str = "market_amplitude",
) -> QuantumCircuit:
    """
    Encode normalized return magnitudes as qubit rotation angles.

    Physics: RY(2·arcsin(√p)) sets |amplitude|² = p on |1⟩.
    For returns: p = |r| / max(|r|) clips to [0, 1].

    Parameters
    ----------
    returns : list of float (daily log-returns or pct changes)
    name    : circuit name

    Returns
    -------
    QuantumCircuit with n_assets qubits
    """
    n = len(returns)
    arr = np.abs(returns)
    max_val = arr.max()
    if max_val > 0:
        arr = arr / max_val
    arr = np.clip(arr, 0, 1)

    qc = QuantumCircuit(n, name=name)
    for i, p in enumerate(arr):
        angle = 2 * np.arcsin(np.sqrt(p))
        qc.ry(angle, i)

    return qc


# ============================================================================
# Correlation-Aware Entangled Circuit
# ============================================================================


def build_correlation_circuit(
    corr_matrix: np.ndarray,
    threshold: float = 0.3,
) -> QuantumCircuit:
    """
    Build entangled circuit where CZ gates reflect asset correlations.

    Assets with |correlation| > threshold get CZ entanglement.
    Initial Hadamard gates create uniform superposition.
    """
    n = corr_matrix.shape[0]
    qc = QuantumCircuit(n, name="correlation_encoding")

    # Superposition
    qc.h(range(n))

    # CZ for significantly correlated pairs
    for i in range(n):
        for j in range(i + 1, n):
            if abs(corr_matrix[i, j]) > threshold:
                qc.cz(i, j)

    # Parametric rotations reflecting correlation strength
    for i in range(n):
        avg_corr = np.mean(np.abs(corr_matrix[i, :])) * np.pi / 2
        qc.ry(avg_corr, i)
        qc.rz(avg_corr / 2, i)

    return qc


# ============================================================================
# Variational Ansatz for Portfolio Optimization
# ============================================================================


def build_portfolio_ansatz(
    n_assets: int,
    n_layers: int = 3,
) -> QuantumCircuit:
    """
    TwoLocal variational ansatz for quantum portfolio optimization.

    Parameters
    ----------
    n_assets : number of assets / qubits
    n_layers : depth of variational layers

    Returns
    -------
    Parametric QuantumCircuit (n_assets qubits)
    """
    ansatz = TwoLocal(
        n_assets,
        rotation_blocks="ry",
        entanglement_blocks="cz",
        entanglement="linear",
        reps=n_layers,
    )
    return ansatz


# ============================================================================
# Classical Returns Preprocessing (replaces yfinance calls)
# ============================================================================


def compute_log_returns(prices: np.ndarray) -> np.ndarray:
    """Log-returns: r_t = ln(P_t / P_{t-1}). Shape: (T-1, n_assets)."""
    return np.log(prices[1:] / prices[:-1])


def compute_correlation_matrix(returns: np.ndarray) -> np.ndarray:
    """Pearson correlation of asset log-returns."""
    return np.corrcoef(returns.T)


def normalize_returns(returns: np.ndarray) -> np.ndarray:
    """Min-max normalize each asset's returns to [0, 1]."""
    result = np.zeros_like(returns)
    for i in range(returns.shape[1]):
        col = returns[:, i]
        rng = col.max() - col.min()
        result[:, i] = (col - col.min()) / rng if rng > 0 else np.zeros_like(col)
    return result


# ============================================================================
# Market Encoding Summary Function
# ============================================================================


def market_encoding_summary(
    prices: np.ndarray,
    asset_names: List[str],
) -> Dict[str, Any]:
    """
    Full market encoding pipeline: prices → quantum circuits.

    Parameters
    ----------
    prices      : shape (T, n_assets), closing prices
    asset_names : list of ticker strings

    Returns
    -------
    dict with circuits, correlation matrix, technical summary
    """
    returns = compute_log_returns(prices)
    corr = compute_correlation_matrix(returns)

    # Use last return for single-step encoding
    last_returns = returns[-1]

    amplitude_circuit = encode_returns_to_circuit(last_returns, "amplitude")
    correlation_circuit = build_correlation_circuit(corr, threshold=0.3)
    ansatz = build_portfolio_ansatz(len(asset_names), n_layers=3)

    # Technical indicators (classical)
    annual_vol = returns.std(axis=0) * np.sqrt(252)
    mean_return = returns.mean(axis=0) * 252  # annualized

    interpretation = (
        f"Market Encoding: {len(asset_names)} assets, "
        f"{len(returns)} return observations. "
        f"Amplitude circuit depth: {amplitude_circuit.depth()}. "
        f"Correlation circuit depth: {correlation_circuit.depth()}. "
        f"Mean correlation: {np.mean(np.abs(corr[np.triu_indices(len(asset_names),k=1)])):.3f}. "
        f"Annual vols: {dict(zip(asset_names, annual_vol.round(4)))}."
    )

    return {
        "n_assets": len(asset_names),
        "n_observations": len(returns),
        "correlation_matrix": corr.tolist(),
        "annual_volatility": dict(zip(asset_names, annual_vol.tolist())),
        "annual_mean_return": dict(zip(asset_names, mean_return.tolist())),
        "amplitude_circuit_depth": amplitude_circuit.depth(),
        "correlation_circuit_depth": correlation_circuit.depth(),
        "ansatz_parameters": ansatz.num_parameters,
        "interpretation": interpretation,
    }
