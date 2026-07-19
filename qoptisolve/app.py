from fastapi import FastAPI

from qoptisolve.api.routes_health import router as health_router
from qoptisolve.api.routes_qaoa import router as qaoa_router

app = FastAPI(
    title="QOptiSolve",
    description="Quantum-AI Optimization Engine for QAOA, VQE, AI heuristics and QPU execution.",
    version="0.1.0",
)

app.include_router(health_router, tags=["Health"])
app.include_router(qaoa_router, prefix="/optimize", tags=["QAOA"])
