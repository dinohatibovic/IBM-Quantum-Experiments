"""
Backend abstraction layer.
  - "local"  → AerSimulator (no credentials needed)
  - "ibm"    → IBM Quantum real hardware via QiskitRuntimeService

Usage
-----
backend = QuantumBackend(mode="local")
counts = backend.run(qc, shots=1000)

# Real hardware:
backend = QuantumBackend(mode="ibm", ibm_backend="ibm_fez")
counts = backend.run(qc, shots=1000)
"""

from __future__ import annotations
import os
from typing import Dict

from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator


class QuantumBackend:
    """
    Unified interface for local simulation and IBM Quantum.

    Parameters
    ----------
    mode : "local" | "ibm"
    ibm_backend : name of IBM backend (e.g. "ibm_fez", "ibm_torino")
    token : IBM Quantum API token; falls back to IBM_QUANTUM_TOKEN env var
    """

    def __init__(
        self,
        mode: str = "local",
        ibm_backend: str = "ibm_fez",
        token: str | None = None,
    ):
        self.mode = mode
        self._pm = None  # preset pass manager (IBM only)

        if mode == "local":
            self._backend = AerSimulator()
            self.is_real = False

        elif mode == "ibm":
            from qiskit_ibm_runtime import QiskitRuntimeService
            from qiskit.transpiler.preset_passmanagers import (
                generate_preset_pass_manager,
            )

            _token = token or os.getenv("IBM_QUANTUM_TOKEN")
            if not _token:
                raise ValueError(
                    "IBM_QUANTUM_TOKEN env var not set. "
                    "Run: export IBM_QUANTUM_TOKEN='your_token'"
                )

            service = QiskitRuntimeService(channel="ibm_quantum", token=_token)
            self._backend = service.backend(ibm_backend)
            self._pm = generate_preset_pass_manager(
                optimization_level=1, backend=self._backend
            )
            self.is_real = True

        else:
            raise ValueError(f"mode must be 'local' or 'ibm', got '{mode}'")

    # ------------------------------------------------------------------
    def run(self, qc: QuantumCircuit, shots: int = 1000) -> Dict[str, int]:
        """
        Transpile and run circuit; return counts dict.
        Works identically for local and IBM backends.
        """
        if self.is_real:
            return self._run_ibm(qc, shots)
        return self._run_local(qc, shots)

    # ------------------------------------------------------------------
    def _run_local(self, qc: QuantumCircuit, shots: int) -> Dict[str, int]:
        t_qc = transpile(qc, self._backend, optimization_level=1)
        job = self._backend.run(t_qc, shots=shots)
        return job.result().get_counts()

    # ------------------------------------------------------------------
    def _run_ibm(self, qc: QuantumCircuit, shots: int) -> Dict[str, int]:
        from qiskit_ibm_runtime import SamplerV2

        isa_qc = self._pm.run(qc)
        sampler = SamplerV2(mode=self._backend)
        job = sampler.run([isa_qc], shots=shots)
        result = job.result()

        # Extract counts from first PubResult; handle any classical register name
        pub_result = result[0]
        for _name, register_data in pub_result.data.items():
            return register_data.get_counts()

        return {}

    # ------------------------------------------------------------------
    @property
    def name(self) -> str:
        return getattr(self._backend, "name", str(self._backend))
