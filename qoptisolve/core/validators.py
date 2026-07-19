from qoptisolve.core.exceptions import InvalidGraphError
from qoptisolve.core.models import GraphEdge


def validate_graph(graph: list[GraphEdge]) -> None:
    if not graph:
        raise InvalidGraphError("Graph must contain at least one edge.")

    for edge in graph:
        if edge.source == edge.target:
            raise InvalidGraphError("Self-loops are not supported.")

        if edge.weight <= 0:
            raise InvalidGraphError("Edge weights must be positive.")


def get_number_of_nodes(graph: list[GraphEdge]) -> int:
    validate_graph(graph)

    max_node = max(max(edge.source, edge.target) for edge in graph)
    return max_node + 1
