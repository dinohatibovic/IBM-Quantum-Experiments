from fastapi import APIRouter, HTTPException

from qoptisolve.core.exceptions import InvalidGraphError, SolverExecutionError
from qoptisolve.core.models import QAOARequest, QAOAResponse
from qoptisolve.quantum.qaoa_engine import QAOAEngine

router = APIRouter()


@router.post("/qaoa", response_model=QAOAResponse)
def optimize_qaoa(payload: QAOARequest) -> QAOAResponse:
    try:
        engine = QAOAEngine(
            reps=payload.reps,
            backend=payload.backend,
        )

        result = engine.optimize(payload.graph)

        return QAOAResponse(
            algorithm="QAOA",
            backend=result.backend,
            reps=payload.reps,
            optimal_value=result.optimal_value,
            bitstring=result.bitstring,
            status=result.status,
        )

    except InvalidGraphError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    except Exception as exc:
        raise SolverExecutionError(str(exc)) from exc
