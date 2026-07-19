from pydantic import BaseModel, Field


class GraphEdge(BaseModel):
    source: int = Field(..., ge=0, description="Source node index.")
    target: int = Field(..., ge=0, description="Target node index.")
    weight: float = Field(..., gt=0, description="Positive edge weight.")


class QAOARequest(BaseModel):
    graph: list[GraphEdge] = Field(..., min_length=1)
    reps: int = Field(default=2, ge=1, le=10)
    shots: int = Field(default=1024, ge=128, le=100000)
    backend: str = Field(default="simulator")


class QAOAResponse(BaseModel):
    algorithm: str
    backend: str
    reps: int
    optimal_value: float
    bitstring: str | None = None
    status: str
