# IBM Quantum Research Proposal

## Hybrid Quantum–AI Optimization Using QAOA and VQE

### Principal Investigator

Dino Hatibović
Quantum Computing & AI Engineer
Tešanj, Bosnia and Herzegovina

---

## 1. Executive Summary

This proposal outlines a hybrid quantum–AI research project using QAOA and VQE on IBM Quantum systems. The goal is to evaluate whether AI-assisted parameter initialization and noise-aware execution can improve convergence and accuracy.

---

## 2. Background

Quantum algorithms such as QAOA and VQE offer potential computational advantages. However, near-term devices suffer from noise and limited depth. AI heuristics may help overcome these limitations.

---

## 3. Research Objectives

1. Implement QAOA for MaxCut and routing problems.
2. Implement VQE for H₂ and LiH molecules.
3. Execute algorithms on IBM Heron/Eagle QPU.
4. Evaluate AI-assisted parameter initialization.
5. Benchmark classical vs quantum performance.

---

## 4. Literature Review

Detailed review of:

- QAOA theory (Farhi et al.)
- VQE theory (Peruzzo et al.)
- IBM Quantum hardware
- AI-assisted quantum optimization

---

## 5. Methodology

### Algorithms

- QAOA with p = 1, 2, 3
- VQE with UCCSD ansatz

### Hardware

- IBM Heron (127 qubits)
- IBM Eagle (133 qubits)

### Software

- Qiskit Runtime
- Python 3.12
- Torch

### Experiments

- simulation baseline
- QPU execution
- noise-aware runs
- error mitigation (ZNE, M3)

---

## 6. AI Integration

- ML-based parameter initialization
- reinforcement learning for QAOA angles
- embeddings for optimization landscapes

---

## 7. Benchmarking Plan

- classical vs quantum
- different QPU backends
- different transpiler levels
- runtime performance

---

## 8. Expected Outcomes

- faster convergence
- improved accuracy
- demonstration of quantum advantage

---

## 9. Risk Analysis

- noise
- limited depth
- QPU queue times

---

## 10. Timeline

- Month 1: Theory + simulation
- Month 2: QPU experiments
- Month 3: Benchmarking + paper writing

---

## 11. Deliverables

- GitHub repository
- Jupyter notebooks
- Zenodo preprint
- arXiv paper

---

## 12. Budget

IBM Research Credits requested.

---

## 13. Conclusion

This project aligns with IBM Quantum's mission to explore hybrid quantum–AI methods.
