"""
Grover's Quantum Search Algorithm — Function 2.
Modern Qiskit API: no execute(), uses backend.run() via QuantumBackend.
"""

from __future__ import annotations
from typing import Any, Dict
import numpy as np

from qiskit import QuantumCircuit
from .backend import QuantumBackend


def grover_search(
    n_qubits: int,
    marked_state: int,
    backend: QuantumBackend | None = None,
    shots: int = 1000,
) -> Dict[str, Any]:
    """
    Grover search: quadratic speedup for unstructured search.

    Physics: oracle phase-flips marked state; diffusion operator inverts
    about average. Optimal iterations ≈ π/4 · √N. Success prob → 1.

    Parameters
    ----------
    n_qubits     : search space 2^n_qubits
    marked_state : target state (0 … 2^n_qubits - 1)
    backend      : QuantumBackend (default: local AerSimulator)
    shots        : measurement shots

    Returns
    -------
    dict with optimal_iterations, success_probability, speedup_vs_classical,
    circuit_depth, interpretation
    """
    if backend is None:
        backend = QuantumBackend(mode="local")

    N = 2**n_qubits
    optimal_iterations = max(1, int(np.pi / 4 * np.sqrt(N)))
    marked_binary = format(marked_state, f"0{n_qubits}b")

    # ── Build circuit ──────────────────────────────────────────────────
    qc = QuantumCircuit(n_qubits, n_qubits, name="Grover")

    # 1. Superposition
    qc.h(range(n_qubits))

    for _ in range(optimal_iterations):
        # 2. Oracle: phase-flip |marked_state⟩
        for i, bit in enumerate(marked_binary):
            if bit == "0":
                qc.x(i)
        _multi_cz(qc, n_qubits)
        for i, bit in enumerate(marked_binary):
            if bit == "0":
                qc.x(i)

        # 3. Diffusion operator: 2|0⟩⟨0| − I
        qc.h(range(n_qubits))
        qc.x(range(n_qubits))
        _multi_cz(qc, n_qubits)
        qc.x(range(n_qubits))
        qc.h(range(n_qubits))

    qc.measure(range(n_qubits), range(n_qubits))

    # ── Run ────────────────────────────────────────────────────────────
    counts = backend.run(qc, shots=shots)

    marked_key = format(marked_state, f"0{n_qubits}b")
    success_count = counts.get(marked_key, 0)
    success_prob = success_count / shots
    speedup = N / optimal_iterations

    interpretation = (
        f"Grover Search: N = {N} states (2^{n_qubits}), target = {marked_state}. "
        f"Optimal iterations: {optimal_iterations}. "
        f"Success probability: {success_prob:.3f}. "
        f"Quantum speedup: {speedup:.1f}× (theoretical √N = {np.sqrt(N):.1f}×). "
        f"Circuit depth: {qc.depth()}. "
        f"Backend: {backend.name}."
    )

    return {
        "search_space_size": N,
        "marked_state": marked_state,
        "optimal_iterations": optimal_iterations,
        "success_probability": float(success_prob),
        "speedup_vs_classical": float(speedup),
        "circuit_depth": qc.depth(),
        "interpretation": interpretation,
    }


# ── Helper ────────────────────────────────────────────────────────────────────


def _multi_cz(qc: QuantumCircuit, n: int) -> None:
    """Multi-controlled Z on n qubits (H-MCX-H pattern)."""
    if n == 1:
        qc.z(0)
    else:
        qc.h(n - 1)
        qc.mcx(list(range(n - 1)), n - 1)
        qc.h(n - 1)
