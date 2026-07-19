from dataclasses import dataclass
from itertools import product

from qoptisolve.core.models import GraphEdge
from qoptisolve.core.validators import get_number_of_nodes, validate_graph


@dataclass
class QAOAResult:
    optimal_value: float
    bitstring: str
    backend: str
    status: str = "completed"


class QAOAEngine:
    def __init__(self, reps: int = 2, backend: str = "simulator"):
        self.reps = reps
        self.backend = backend

    def _cut_value(self, bitstring: str, graph: list[GraphEdge]) -> float:
        value = 0.0

        for edge in graph:
            if bitstring[edge.source] != bitstring[edge.target]:
                value += edge.weight

        return value

    def optimize(self, graph: list[GraphEdge]) -> QAOAResult:
        validate_graph(graph)

        num_nodes = get_number_of_nodes(graph)

        best_bitstring = ""
        best_value = float("-inf")

        for bits in product("01", repeat=num_nodes):
            bitstring = "".join(bits)
            value = self._cut_value(bitstring, graph)

            if value > best_value:
                best_value = value
                best_bitstring = bitstring

        return QAOAResult(
            optimal_value=best_value,
            bitstring=best_bitstring,
            backend=self.backend,
        )
