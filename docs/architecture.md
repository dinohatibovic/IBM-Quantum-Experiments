# QOptiSolve Architecture

QOptiSolve is a hybrid Quantum–AI optimization platform combining QAOA, VQE, AI heuristics,
RAG documentation, and IBM QPU execution behind a FastAPI service layer.

## Layers

```text
qoptisolve/
├── api/              # FastAPI endpoints (health, qaoa, vqe*, optimize*)
├── core/             # Config, Pydantic models, validators, exceptions
├── quantum/          # QAOA engine, VQE engine*, QPU executor, transpiler tools*, noise models*
├── ai/               # Heuristics*, ML models*, embeddings*, RAG engine*
└── tests/            # Unit tests

(*) scaffolding — planned in ROADMAP.md Phase 1–3
```

## Supporting modules (migrated from the four source repositories)

| Directory | Role |
| --- | --- |
| `quantum_core/` | Qiskit algorithm library (BB84, Grover, QPE, Bell, QFT, portfolio QAOA) |
| `parse_ibm_json.py`, `docs/`, `data/` | Verified IBM QPU results parser, methodology docs, and dataset (this repo's original content) |
| `materials/` | Classical materials/catalyst screening and PV simulation |
| `benchmarks/` | IBM Heron VQE vs classical VQEzy H2 comparison |

## Request flow (MVP)

1. Client POSTs a weighted graph to `/optimize/qaoa`.
2. `core/validators.py` checks the graph (no self-loops, positive weights).
3. `quantum/qaoa_engine.py` solves MaxCut (MVP: exact enumeration; roadmap: SparsePauliOp + QAOA).
4. `QAOAResponse` returns optimal value, bitstring, and status.

## Deployment

- `deployment/Dockerfile` + `docker-compose.yml` for containers
- `deployment/k8s/` for Kubernetes (Deployment, Service, Ingress)
- `.github/workflows/` for CI (pytest + flake8) and PyPI release
