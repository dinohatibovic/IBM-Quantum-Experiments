import numpy as np
from qiskit import QuantumCircuit
from qiskit_algorithms import QAOA
from qiskit_algorithms.optimizers import COBYLA
from qiskit.primitives import Estimator

class QAOAEngine:
    def __init__(self, p=2):
        self.p = p
        self.estimator = Estimator()

    def build_cost_hamiltonian(self, graph):
        """Build the Ising Hamiltonian for MaxCut."""
        n = len(graph)
        w = np.zeros((n, n))

        for u, v, weight in graph:
            w[u][v] = weight
            w[v][u] = weight

        return w

    def build_qaoa_circuit(self, graph):
        """Build the QAOA circuit."""
        n = len(graph)
        qc = QuantumCircuit(n)

        # initial superposition
        qc.h(range(n))

        # QAOA layers
        for _ in range(self.p):
            for u, v, w in graph:
                qc.cx(u, v)
                qc.rz(-w, v)
                qc.cx(u, v)

            qc.rx(np.pi / 2, range(n))

        qc.measure_all()
        return qc

    def optimize(self, graph):
        """Run the QAOA optimization."""
        cost_h = self.build_cost_hamiltonian(graph)
        qaoa = QAOA(optimizer=COBYLA(), reps=self.p, estimator=self.estimator)
        result = qaoa.compute_minimum_eigenvalue(cost_h)
        return result
