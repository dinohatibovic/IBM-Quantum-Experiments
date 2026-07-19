from fastapi import FastAPI
from qoptisolve.quantum.qaoa_engine import QAOAEngine
from qoptisolve.quantum.qpu_executor import QPUExecutor

app = FastAPI(title="QOptiSolve Quantum-AI Engine")

qaoa_engine = QAOAEngine()
qpu = QPUExecutor()

@app.get("/health")
def health():
    return {"status": "ok", "qpu": qpu.status()}

@app.post("/optimize/qaoa")
def optimize_qaoa(payload: dict):
    graph = payload["graph"]
    result = qaoa_engine.optimize(graph)
    return {"optimal_value": result.eigenvalue.real}

@app.post("/qpu/run")
def run_qpu(payload: dict):
    circuit = payload["circuit"]
    backend = payload.get("backend", "ibm_qpu")
    return qpu.run(circuit, backend)
