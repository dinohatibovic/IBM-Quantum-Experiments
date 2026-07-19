"""
Qiskit circuit optimization utilities — Function 6.
Uses generate_preset_pass_manager (replaces deprecated PassManager + manual passes).
"""

from __future__ import annotations
from typing import Any, Dict

import numpy as np
from qiskit import QuantumCircuit
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_aer import AerSimulator


def qiskit_circuit_optimization(n_qubits: int = 5) -> Dict[str, Any]:
    """
    Build a sample circuit, optimize at level 3, compare gate counts.

    Modern Qiskit workflows use generate_preset_pass_manager(optimization_level=...)
    instead of the deprecated PassManager + Optimize1qGates pattern.

    Parameters
    ----------
    n_qubits : circuit width

    Returns
    -------
    dict with gate counts, depths, error estimates, interpretation
    """
    # ── Build original circuit ─────────────────────────────────────────
    qc = QuantumCircuit(n_qubits, name="sample")
    qc.h(range(n_qubits))
    for i in range(n_qubits - 1):
        qc.cx(i, i + 1)
    for i in range(n_qubits):
        qc.rz(np.pi / 4, i)
    for i in range(n_qubits - 1):
        qc.cx(i, i + 1)
    qc.h(range(n_qubits))

    count_before = qc.size()
    depth_before = qc.depth()

    # ── Optimize via preset pass manager (modern Qiskit way) ─────────────
    sim = AerSimulator()
    pm = generate_preset_pass_manager(optimization_level=3, backend=sim)
    qc_opt = pm.run(qc)

    count_after = qc_opt.size()
    depth_after = qc_opt.depth()

    # ── Error model: p_1q=0.1%, p_2q=1.5% ────────────────────────────
    def _count_gate_types(circ: QuantumCircuit):
        one_q = sum(1 for inst in circ.data if inst.operation.num_qubits == 1)
        two_q = sum(1 for inst in circ.data if inst.operation.num_qubits == 2)
        return one_q, two_q

    p1, p2 = 0.001, 0.015

    def _error(c):
        q1, q2 = _count_gate_types(c)
        return 1 - (1 - p1) ** q1 * (1 - p2) ** q2

    err_before = _error(qc)
    err_after = _error(qc_opt)

    interpretation = (
        f"Circuit Optimization ({n_qubits} qubits, modern Qiskit preset level-3). "
        f"Gates: {count_before} → {count_after} "
        f"({100*(1-count_after/count_before):.1f}% reduction). "
        f"Depth: {depth_before} → {depth_after} "
        f"({100*(1-depth_after/depth_before):.1f}% reduction). "
        f"Estimated error: {err_before:.4f} → {err_after:.4f}."
    )

    return {
        "n_qubits": n_qubits,
        "gate_count_before": count_before,
        "gate_count_after": count_after,
        "circuit_depth_before": depth_before,
        "circuit_depth_after": depth_after,
        "estimated_error_before": float(err_before),
        "estimated_error_after": float(err_after),
        "interpretation": interpretation,
    }
