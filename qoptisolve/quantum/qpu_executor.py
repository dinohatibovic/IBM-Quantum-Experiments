"""QPU executor for IBM Quantum backends via Qiskit Runtime.

NOTE: draft implementation from the startup-structure spec. Known issue:
``QuantumCircuit.from_dict`` does not exist in Qiskit — ``run`` expects a
serialized circuit and needs a real deserializer (e.g. QPY) before production
use. Kept unmounted from the API until then.
"""
from qiskit import QuantumCircuit
from qiskit_ibm_runtime import QiskitRuntimeService, Sampler


class QPUExecutor:
    def __init__(self):
        try:
            self.service = QiskitRuntimeService()
            self.backend = self.service.backend("ibm_brisbane")  # Heron/Eagle class
            self.sampler = Sampler(backend=self.backend)
        except Exception:
            self.service = None
            self.backend = None
            self.sampler = None

    def status(self):
        if self.backend:
            return {"backend": self.backend.name, "status": "connected"}
        return {"backend": None, "status": "offline"}

    def run(self, circuit_dict, backend_name="ibm_brisbane"):
        """Run a circuit on the QPU or a simulator."""
        qc = QuantumCircuit.from_dict(circuit_dict)  # FIXME: replace with QPY deserialization

        if self.service:
            backend = self.service.backend(backend_name)
            sampler = Sampler(backend=backend)
            result = sampler.run(qc).result()
            return {"qpu": backend_name, "counts": result.quasi_dists[0]}
        else:
            return {"error": "QPU not available"}
