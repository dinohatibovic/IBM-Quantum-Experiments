"""
CHSH Bell Inequality Test — Function 9.
Qiskit 2.x API via QuantumBackend abstraction.

Correct CHSH angles for max violation (S = 2√2 ≈ 2.828):
  Alice: a=0, a'=π/4
  Bob:   b=π/8, b'=3π/8
Rotation: ry(2θ) then measure Z ≡ measuring along (sin2θ, 0, cos2θ).
"""

from __future__ import annotations
from typing import Any, Dict
import numpy as np

from qiskit import QuantumCircuit
from .backend import QuantumBackend


def bell_inequality_test(
    n_trials: int = 1000,
    backend: QuantumBackend | None = None,
) -> Dict[str, Any]:
    """
    CHSH Bell inequality test on |Φ+⟩ = (|00⟩ + |11⟩)/√2.

    Physics: E(α,β) = cos(2(α−β)) for |Φ+⟩.
    CHSH: S = |E(a,b) − E(a,b') + E(a',b) + E(a',b')|
    Classical ≤ 2, Quantum ≤ 2√2 ≈ 2.828 (Tsirelson bound).
    """
    if backend is None:
        backend = QuantumBackend(mode="local")

    # Optimal CHSH angles: a=0, a'=π/4, b=π/8, b'=3π/8
    a, ap = 0.0, np.pi / 4
    b, bp = np.pi / 8, 3 * np.pi / 8

    def _corr(alpha: float, beta: float) -> float:
        """E(α,β): ry(2θ) rotates Bloch sphere so Z-meas ≡ θ-axis."""
        qc = QuantumCircuit(2, 2)
        qc.h(0)
        qc.cx(0, 1)
        qc.ry(2 * alpha, 0)
        qc.ry(2 * beta, 1)
        qc.measure([0, 1], [0, 1])
        counts = backend.run(qc, shots=n_trials)
        n00 = counts.get("00", 0)
        n11 = counts.get("11", 0)
        n01 = counts.get("01", 0)
        n10 = counts.get("10", 0)
        return (n00 + n11 - n01 - n10) / n_trials

    E_ab = _corr(a, b)
    E_abp = _corr(a, bp)
    E_apb = _corr(ap, b)
    E_apbp = _corr(ap, bp)

    S = abs(E_ab - E_abp + E_apb + E_apbp)
    classical_limit = 2.0
    quantum_limit = 2.0 * np.sqrt(2)
    bell_violation = S > classical_limit

    interpretation = (
        f"CHSH Bell Test ({n_trials} trials, backend: {backend.name}). "
        f"Angles: a=0, a'=π/4, b=π/8, b'=3π/8 (optimal for |Φ+⟩). "
        f"E(a,b)={E_ab:.3f}, E(a,b')={E_abp:.3f}, "
        f"E(a',b)={E_apb:.3f}, E(a',b')={E_apbp:.3f}. "
        f"S={S:.4f}. Classical≤2.000, Quantum≤2.828. "
        f"Bell violation: {bell_violation}."
    )

    return {
        "n_trials": n_trials,
        "E_ab": float(E_ab),
        "E_ab_prime": float(E_abp),
        "E_a_prime_b": float(E_apb),
        "E_a_prime_b_prime": float(E_apbp),
        "S_value": float(S),
        "classical_limit": float(classical_limit),
        "quantum_limit": float(quantum_limit),
        "bell_violation": bool(bell_violation),
        "interpretation": interpretation,
    }
