import pytest

from qoptisolve.core.exceptions import InvalidGraphError
from qoptisolve.core.models import GraphEdge
from qoptisolve.quantum.qaoa_engine import QAOAEngine


def test_qaoa_engine_returns_result():
    graph = [
        GraphEdge(source=0, target=1, weight=1.0),
        GraphEdge(source=1, target=2, weight=1.0),
    ]

    engine = QAOAEngine(reps=2)
    result = engine.optimize(graph)

    assert result.status == "completed"
    assert result.optimal_value >= 0
    assert result.bitstring is not None


def test_qaoa_rejects_empty_graph():
    engine = QAOAEngine()

    with pytest.raises(InvalidGraphError):
        engine.optimize([])


def test_qaoa_rejects_self_loop():
    graph = [
        GraphEdge(source=0, target=0, weight=1.0),
    ]

    engine = QAOAEngine()

    with pytest.raises(InvalidGraphError):
        engine.optimize(graph)
