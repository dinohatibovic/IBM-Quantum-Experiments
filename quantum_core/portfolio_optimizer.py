"""
Quantum Portfolio Optimization via QUBO/QAOA — rewritten from docs 9/10.

Key corrections vs. original:
  - No qiskit_optimization (separate package with breaking changes)
  - QUBO formulation done manually (no QuadraticProgram)
  - QAOA via qiskit_algorithms (separate pip install) OR
    classical COBYLA fallback (always works)
  - No fabricated performance numbers
"""

from __future__ import annotations
from typing import Any, Dict, Optional
import numpy as np
from scipy.optimize import minimize

from qiskit import QuantumCircuit
from .backend import QuantumBackend

# ============================================================================
# QUBO Formulation
# ============================================================================


def portfolio_qubo(
    expected_returns: np.ndarray,
    cov_matrix: np.ndarray,
    risk_aversion: float = 0.5,
    budget: Optional[int] = None,
    penalty: float = 5.0,
) -> np.ndarray:
    """
    Build QUBO matrix for portfolio selection.

    Objective: min  −Σ_i r_i·x_i  +  λ·Σ_{ij} σ_{ij}·x_i·x_j
    Constraint: Σ_i x_i = budget  (added as quadratic penalty)

    Parameters
    ----------
    expected_returns : shape (n,)
    cov_matrix       : shape (n, n)
    risk_aversion    : λ (trade-off return vs risk)
    budget           : number of assets to select (None = n//2)
    penalty          : Lagrange multiplier for budget constraint

    Returns
    -------
    Q : QUBO matrix shape (n, n)
    """
    n = len(expected_returns)
    if budget is None:
        budget = n // 2

    Q = np.zeros((n, n))

    # Linear terms on diagonal
    for i in range(n):
        Q[i, i] -= expected_returns[i]

    # Quadratic risk terms
    Q += risk_aversion * cov_matrix

    # Budget constraint penalty: P*(Σ x_i - K)² = P*(Σ x_i² + 2Σ_{i<j} x_i·x_j - 2K·Σ x_i + K²)
    for i in range(n):
        Q[i, i] += penalty * (1 - 2 * budget)
    for i in range(n):
        for j in range(i + 1, n):
            Q[i, j] += 2 * penalty

    return Q


# ============================================================================
# Classical Brute-Force Solver (baseline / verification)
# ============================================================================


def solve_portfolio_classical(
    expected_returns: np.ndarray,
    cov_matrix: np.ndarray,
    risk_aversion: float = 0.5,
    budget: Optional[int] = None,
) -> Dict[str, Any]:
    """
    Brute-force optimal portfolio (exact for small n).
    Classical baseline for comparison with quantum results.
    """
    n = len(expected_returns)
    if budget is None:
        budget = n // 2

    best_val = np.inf
    best_selection = None

    for mask in range(2**n):
        bits = [(mask >> i) & 1 for i in range(n)]
        if sum(bits) != budget:
            continue
        x = np.array(bits, dtype=float)
        val = -x @ expected_returns + risk_aversion * x @ cov_matrix @ x
        if val < best_val:
            best_val = val
            best_selection = bits[:]

    selected = [i for i, b in enumerate(best_selection) if b]
    ret = sum(expected_returns[i] for i in selected)
    risk = np.array(best_selection) @ cov_matrix @ np.array(best_selection)
    sharpe = ret / np.sqrt(risk) if risk > 0 else 0.0

    return {
        "selected_assets": selected,
        "objective_value": float(best_val),
        "expected_return": float(ret),
        "portfolio_risk": float(risk),
        "sharpe_ratio": float(sharpe),
        "method": "brute_force",
    }


# ============================================================================
# QAOA-Style Ansatz (manual, no qiskit_algorithms dependency)
# ============================================================================


def _qaoa_circuit(
    n: int, gammas: np.ndarray, betas: np.ndarray, Q: np.ndarray
) -> QuantumCircuit:
    """Build p-layer QAOA circuit for QUBO minimization."""
    p = len(gammas)
    qc = QuantumCircuit(n, n, name=f"QAOA_p{p}")

    # Initial superposition
    qc.h(range(n))

    for layer in range(p):
        # Problem unitary: e^{-iγ·H_C}
        for i in range(n):
            for j in range(i, n):
                if abs(Q[i, j]) > 1e-10:
                    angle = gammas[layer] * Q[i, j]
                    if i == j:
                        qc.rz(2 * angle, i)
                    else:
                        qc.rzz(2 * angle, i, j)

        # Mixer unitary: e^{-iβ·H_B}
        for i in range(n):
            qc.rx(2 * betas[layer], i)

    qc.measure(range(n), range(n))
    return qc


def solve_portfolio_qaoa(
    expected_returns: np.ndarray,
    cov_matrix: np.ndarray,
    risk_aversion: float = 0.5,
    budget: Optional[int] = None,
    n_layers: int = 2,
    n_shots: int = 1000,
    backend: Optional[QuantumBackend] = None,
) -> Dict[str, Any]:
    """
    QAOA portfolio optimizer.

    Parameters
    ----------
    expected_returns : shape (n,)
    cov_matrix       : shape (n, n)
    risk_aversion    : λ
    budget           : assets to select
    n_layers         : QAOA depth p
    n_shots          : shots per circuit evaluation
    backend          : QuantumBackend (default: local)

    Returns
    -------
    dict with selected_assets, objective_value, method, n_qaoa_calls
    """
    if backend is None:
        backend = QuantumBackend(mode="local")

    n = len(expected_returns)
    if budget is None:
        budget = n // 2

    Q = portfolio_qubo(expected_returns, cov_matrix, risk_aversion, budget)

    n_calls = [0]

    def _objective(params: np.ndarray) -> float:
        """QAOA expectation value estimated from counts."""
        gammas = params[:n_layers]
        betas = params[n_layers:]
        qc = _qaoa_circuit(n, gammas, betas, Q)
        counts = backend.run(qc, shots=n_shots)
        n_calls[0] += 1

        # Expectation value: weighted sum over samples
        total = sum(counts.values())
        exp_val = 0.0
        for bitstr, cnt in counts.items():
            x = np.array([int(b) for b in reversed(bitstr)], dtype=float)
            cost = x @ Q @ x
            exp_val += (cnt / total) * cost
        return exp_val

    # Optimize with COBYLA
    init = np.random.default_rng(42).uniform(0, np.pi, size=2 * n_layers)
    result = minimize(
        _objective, init, method="COBYLA", options={"maxiter": 200, "rhobeg": 0.5}
    )

    # Sample best bitstring
    gammas_opt = result.x[:n_layers]
    betas_opt = result.x[n_layers:]
    qc_final = _qaoa_circuit(n, gammas_opt, betas_opt, Q)
    counts = backend.run(qc_final, shots=n_shots * 5)

    # Filter to valid budget solutions
    best_bits = None
    best_cost = np.inf
    for bitstr, cnt in counts.items():
        x = [int(b) for b in reversed(bitstr)]
        if sum(x) != budget:
            continue
        cost = np.array(x, float) @ Q @ np.array(x, float)
        if cost < best_cost:
            best_cost = cost
            best_bits = x[:]

    if best_bits is None:
        best_bits = [0] * n
        best_bits[:budget] = [1] * budget

    selected = [i for i, b in enumerate(best_bits) if b]
    ret = float(sum(expected_returns[i] for i in selected))
    risk = float(np.array(best_bits) @ cov_matrix @ np.array(best_bits))

    return {
        "selected_assets": selected,
        "objective_value": float(best_cost),
        "expected_return": ret,
        "portfolio_risk": risk,
        "sharpe_ratio": ret / np.sqrt(risk) if risk > 0 else 0.0,
        "n_qaoa_layers": n_layers,
        "n_qaoa_calls": n_calls[0],
        "optimizer_success": result.success,
        "method": f"QAOA_p{n_layers}",
    }


# ============================================================================
# Portfolio Backtest (classical, always valid)
# ============================================================================


def backtest_portfolio(
    weights: np.ndarray,
    returns: np.ndarray,
) -> Dict[str, Any]:
    """
    Backtest equal-weight portfolio on historical returns.

    Parameters
    ----------
    weights  : shape (n,) — portfolio weights (sum=1)
    returns  : shape (T, n) — daily log-returns

    Returns
    -------
    dict with total_return, annual_vol, sharpe_ratio, max_drawdown
    """
    port_returns = returns @ weights
    total_return = float(np.sum(port_returns))
    annual_vol = float(np.std(port_returns) * np.sqrt(252))
    sharpe = total_return / annual_vol if annual_vol > 0 else 0.0
    cum = np.cumsum(port_returns)
    max_dd = float(np.min(cum - np.maximum.accumulate(cum)))

    return {
        "total_return": total_return,
        "annual_vol": annual_vol,
        "sharpe_ratio": sharpe,
        "max_drawdown": max_dd,
    }
