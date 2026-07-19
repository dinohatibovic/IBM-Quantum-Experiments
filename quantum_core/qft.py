"""
Quantum Fourier Transform — Function 12.
Uses Statevector (no hardware needed); also provides IBM-runnable circuit.
Modern Qiskit API.
"""

from __future__ import annotations
from typing import Any, Dict
import numpy as np

from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector


def quantum_fourier_transform(n_qubits: int = 3) -> Dict[str, Any]:
    """
    Build QFT circuit and verify round-trip via inverse QFT.

    Physics: QFT|x⟩ = (1/√N) Σ_k e^(2πixk/N)|k⟩.
    Circuit: H + controlled-phase rotations, O(n²) depth.

    Parameters
    ----------
    n_qubits : register size

    Returns
    -------
    dict with output_probabilities, circuit_depth, gate_count,
    inverse_qft_recovers_input, interpretation
    """

    # ── Build QFT circuit ─────────────────────────────────────────────
    def _qft(n: int) -> QuantumCircuit:
        qc = QuantumCircuit(n, name="QFT")
        for j in range(n):
            qc.h(j)
            for k in range(j + 1, n):
                angle = 2 * np.pi / (2 ** (k - j + 1))
                qc.cp(angle, k, j)
        # Bit-reversal swap
        for i in range(n // 2):
            qc.swap(i, n - 1 - i)
        return qc

    qft_circ = _qft(n_qubits)

    # Input state: |0…01⟩  (last qubit = |1⟩)
    qc_input = QuantumCircuit(n_qubits)
    qc_input.x(n_qubits - 1)

    qc_full = qc_input.compose(qft_circ)

    # ── Statevector (exact, no sampling noise) ─────────────────────────
    sv = Statevector.from_instruction(qc_full)
    amplitudes = sv.data
    probabilities = (np.abs(amplitudes) ** 2).tolist()

    # ── Round-trip: QFT → IQFT should recover |0…01⟩ ─────────────────
    iqft_circ = qft_circ.inverse()
    qc_roundtrip = qc_full.compose(iqft_circ)
    sv_recovered = Statevector.from_instruction(qc_roundtrip)

    # Qiskit little-endian: x(n_qubits-1) sets MSB → state index 2^(n-1)
    target = np.zeros(2**n_qubits, dtype=complex)
    target[2 ** (n_qubits - 1)] = 1.0

    fidelity = float(np.abs(np.vdot(target, sv_recovered.data)) ** 2)
    round_trip_ok = fidelity > 0.999

    interpretation = (
        f"QFT ({n_qubits} qubits): maps |0…01⟩ to frequency basis. "
        f"Circuit depth: {qft_circ.depth()}, gate count: {qft_circ.size()}. "
        f"Inverse QFT round-trip fidelity: {fidelity:.6f} "
        f"({'✓' if round_trip_ok else '✗'} > 0.999). "
        f"Used in: Shor's algorithm, QPE, HHL."
    )

    return {
        "n_qubits": n_qubits,
        "input_state_label": "|0…01⟩",
        "output_probabilities": probabilities,
        "circuit_depth": qft_circ.depth(),
        "gate_count": qft_circ.size(),
        "round_trip_fidelity": fidelity,
        "inverse_qft_recovers_input": round_trip_ok,
        "interpretation": interpretation,
    }
