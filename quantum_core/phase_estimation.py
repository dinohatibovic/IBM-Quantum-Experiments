"""
Quantum Phase Estimation (QPE) — Function 8.
Qiskit 2.x: uses QFTGate.inverse() (replaces deprecated QFT class).

Phase kickback convention (Qiskit LSB):
  qubit j gets CU^(2^j), producing phase 2π·φ·2^j on qubit j.
  After IQFT: measurement gives round(φ·2^n) as integer.
"""

from __future__ import annotations
from typing import Any, Dict
import numpy as np

from qiskit import QuantumCircuit
from qiskit.circuit.library import QFTGate
from .backend import QuantumBackend


def quantum_phase_estimation(
    unitary_phase: float,
    n_counting_qubits: int = 4,
    backend: QuantumBackend | None = None,
    shots: int = 2000,
) -> Dict[str, Any]:
    """
    QPE: estimate φ in U|1⟩ = e^(2πiφ)|1⟩.

    Physics: phase kickback + QFT⁻¹ encodes φ·2^n as integer.
    Precision: 1/2^n_counting_qubits.

    Parameters
    ----------
    unitary_phase      : true phase φ ∈ [0, 1)
    n_counting_qubits  : precision (error ≤ 1/2^n)
    backend            : QuantumBackend (default: local)
    shots              : measurement shots

    Returns
    -------
    dict with true_phase, estimated_phase, estimation_error, circuit_depth
    """
    if backend is None:
        backend = QuantumBackend(mode="local")

    n = n_counting_qubits
    state_qubit = n  # index of eigenstate qubit
    total = n + 1

    qc = QuantumCircuit(total, n, name="QPE")

    # State register: eigenstate |1⟩ of phase gate P(2πφ)
    qc.x(state_qubit)

    # Counting register: equal superposition
    qc.h(range(n))

    # Phase kickback: qubit j controls U^(2^j)
    # LSB convention — qubit 0 gets smallest phase, qubit n-1 gets largest
    for j in range(n):
        angle = 2 * np.pi * unitary_phase * (2**j)
        qc.cp(angle, j, state_qubit)

    # Inverse QFT (Qiskit 2.x: QFTGate)
    iqft_gate = QFTGate(n).inverse()
    qc.append(iqft_gate, range(n))

    # Measure counting register
    qc.measure(range(n), range(n))

    # Run
    counts = backend.run(qc, shots=shots)
    best = max(counts, key=counts.get)
    estimated = int(best, 2) / (2**n)
    error = abs(unitary_phase - estimated)

    interpretation = (
        f"QPE: true φ={unitary_phase:.6f}, estimated φ={estimated:.6f}. "
        f"Error={error:.6f} (precision 1/2^{n}={1/(2**n):.6f}). "
        f"Backend: {backend.name}. "
        f"Used in: VQE energy, Shor period-finding, HHL solver."
    )

    return {
        "true_phase": float(unitary_phase),
        "estimated_phase": float(estimated),
        "estimation_error": float(error),
        "n_counting_qubits": n,
        "circuit_depth": qc.decompose().depth(),
        "interpretation": interpretation,
    }
