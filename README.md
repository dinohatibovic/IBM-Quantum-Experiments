# QOptiSolve

**Quantum-AI Optimization Engine** — QAOA, VQE, AI heuristics and QPU execution, served over a FastAPI REST API.

QOptiSolve is a monorepo that combines four previously separate projects by Dino Hatibović into a single codebase, built around a functional FastAPI + QAOA MVP.

## Repository map

| Directory | Contents | Origin |
| --- | --- | --- |
| `qoptisolve/` | **MVP core** — FastAPI app, `/health` and `/optimize/qaoa` endpoints, Pydantic models, graph validators, QAOA engine, pytest suite | New (QOptiSolve MVP) |
| `quantum_core/` | Qiskit 2.x algorithm library: BB84 QKD, Grover, phase estimation, Bell/CHSH tests, QFT, physics demos, market encoder, portfolio optimizer | [qiskit-nisq-toolkit](https://github.com/dinohatibovic/qiskit-nisq-toolkit) |
| `parse_ibm_json.py`, `docs/`, `data/`, `figures/` | IBM SamplerV2 result parser (counts, QBER, fidelity, concurrence, entropy, chi-squared), methodology docs, and the verified dataset from runs on ibm_fez / ibm_torino (Zenodo DOI 10.5281/zenodo.20749395) | this repository (original content — see [docs/RESEARCH_OVERVIEW.md](docs/RESEARCH_OVERVIEW.md)) |
| `materials/` | Classical materials & catalyst screening (Monte-Carlo scoring, DE/GA/PSO optimization, PyTorch MLP predictor) and photovoltaic cell simulation (Hartree-Fock, photon spectra) | [quantum-materials-screener](https://github.com/dinohatibovic/quantum-materials-screener) |
| `benchmarks/` | IBM Heron VQE vs. classical VQEzy H2 dataset comparison scripts (HDF5) | [nisq-hardware-benchmark](https://github.com/dinohatibovic/nisq-hardware-benchmark) |
| `examples/` | IBM Runtime and local simulator demos | qiskit-nisq-toolkit |
| `scripts/` | IBM Quantum account setup helper | qiskit-nisq-toolkit |
| `tests/` | Verification test suite for `quantum_core` | qiskit-nisq-toolkit |

This repository keeps its own research artifacts (figures, verified CSV, release manifests); binary artifacts of the other three source repositories stay where they are — only their code and docs were migrated here.

## Quick start

```bash
pip install -r requirements.txt
uvicorn qoptisolve.app:app --reload
```

Health check:

```bash
curl http://127.0.0.1:8000/health
```

QAOA (MaxCut) optimization:

```bash
curl -X POST http://127.0.0.1:8000/optimize/qaoa \
  -H "Content-Type: application/json" \
  -d '{
    "graph": [
      {"source": 0, "target": 1, "weight": 1.0},
      {"source": 1, "target": 2, "weight": 2.0}
    ],
    "reps": 2,
    "shots": 1024,
    "backend": "simulator"
  }'
```

Expected response:

```json
{
  "algorithm": "QAOA",
  "backend": "simulator",
  "reps": 2,
  "optimal_value": 3.0,
  "bitstring": "010",
  "status": "completed"
}
```

## Legacy module dependencies

`requirements.txt` covers the QOptiSolve MVP core only. The migrated modules need extras from their original repositories:

```bash
# quantum_core/, examples/, tests/  (from qiskit-nisq-toolkit)
pip install "qiskit-aer>=0.15.0" "scipy>=1.13.0" "matplotlib>=3.9.0" "python-dotenv>=1.0.0"

# materials/  (from quantum-materials-screener)
pip install pandas scikit-learn torch

# benchmarks/  (from nisq-hardware-benchmark; HDF5 dataset is user-supplied)
pip install "h5py>=3.9"
```

## Tests and lint

```bash
pytest                # MVP suite (qoptisolve/tests, configured in pyproject.toml)
pytest tests/         # legacy quantum_core verification suite (run explicitly)
flake8 qoptisolve/
```

## Status and roadmap

The current QAOA engine is an MVP: it solves MaxCut by exact brute-force enumeration, which keeps results stable and testable. Planned next steps:

1. Real Qiskit `SparsePauliOp` + QAOA solver replacing the brute-force engine.
2. QPU executor via `qiskit-ibm-runtime` — `quantum_core/backend.py` (backend selection) and `parse_ibm_json.py` (SamplerV2 result parsing) are the natural building blocks.
3. VQE endpoint, reusing the H2 benchmark methodology from `benchmarks/`.
4. AI heuristics / RAG modules, building on the optimizers in `materials/` and `quantum_core/optimizer.py`.

## Repository extensions

Beyond the core modules above, the repository also contains:

| Directory | Contents |
| --- | --- |
| `docs/` | Architecture, pitch deck, sponsors page, landing page copy, toolkit docs, research drafts (`docs/research/` — templates with placeholder results, see its README) |
| `notebooks/` | Bell, BB84, VQC, QRNG, QPU benchmarking, and extended noise-model notebooks |
| `analysis/` | Extended QPU noise model (gate-dependent depolarizing, crosstalk, bootstrap, AIC/BIC) |
| `benchmarking/` | Synthetic demo datasets for the benchmarking pipeline |
| `latex/` | LaTeX papers (QOptiSolve draft, IBM experiments paper, statistical appendix) |
| `deployment/` | Dockerfile, docker-compose, Kubernetes manifests |
| `drafts/` | Unverified code variants from the specification (see `drafts/README.md`) |

## License

Apache-2.0. Migrated modules retain their original attribution; see source repositories.
