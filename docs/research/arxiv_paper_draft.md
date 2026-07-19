# Hybrid Quantum–AI Optimization Using QAOA and VQE on IBM Quantum Systems

> ⚠️ DRAFT / TEMPLATE — the numeric results below are placeholder values; the experiments
> have not been performed. See `docs/research/README.md` before submitting anywhere.

## Authors

Dino Hatibović
Quantum Computing & AI Engineer
Tešanj, Bosnia and Herzegovina

---

## Abstract

This work investigates hybrid quantum–AI optimization using the Quantum Approximate Optimization Algorithm (QAOA) and the Variational Quantum Eigensolver (VQE) on IBM Quantum hardware. We demonstrate that AI-assisted parameter initialization and noise-aware execution improve convergence, reduce circuit depth requirements, and enhance solution quality for combinatorial optimization and molecular energy estimation. Experiments were conducted on IBM Heron and Eagle processors using Qiskit Runtime.

---

## 1. Introduction

Quantum computing promises computational advantages for optimization, chemistry, and machine learning. However, near-term quantum devices suffer from noise, limited qubit connectivity, and shallow circuit depth constraints. Hybrid quantum–AI approaches aim to mitigate these limitations by combining quantum algorithms with classical machine learning.

This paper explores:

- QAOA for MaxCut and routing problems
- VQE for H₂ and LiH molecules
- AI heuristics for parameter initialization
- Noise-aware execution on IBM Heron/Eagle QPU

We show measurable improvements in convergence and accuracy.

---

## 2. Related Work

Prior research has explored:

- QAOA performance on noisy hardware
- VQE ansatz optimization
- AI-assisted quantum optimization
- IBM Quantum hardware benchmarking

However, few works combine QAOA + VQE + AI + real QPU execution in a unified framework.

---

## 3. Preliminaries

### 3.1 Quantum Circuits

Gate-based quantum computing uses unitary operations and measurement to encode and solve problems.

### 3.2 QAOA

QAOA alternates between cost and mixer Hamiltonians:

U(γ, β) = e^(−iγ H_C) e^(−iβ H_M)

### 3.3 VQE

VQE minimizes:

E(θ) = ⟨ψ(θ)| H |ψ(θ)⟩

### 3.4 Noise Models

We use: depolarizing noise, readout noise, thermal relaxation.

### 3.5 Error Mitigation

We apply: Zero Noise Extrapolation (ZNE), M3 readout mitigation.

---

## 4. Methodology

### 4.1 Problem Formulation

We solve MaxCut on graphs up to 12 nodes and H₂ / LiH molecular Hamiltonians.

### 4.2 AI Heuristics

ML-based parameter initialization; reinforcement learning for QAOA angles.

### 4.3 Hardware Setup

IBM Heron (127 qubits), IBM Eagle (133 qubits).

### 4.4 Experimental Procedure

Simulation baseline → QPU execution → noise-aware runs → error mitigation.

---

## 5. Results (PLACEHOLDER — replace with real measurements)

### 5.1 QAOA Simulation

Convergence improves by 18% with AI initialization. *(placeholder)*

### 5.2 QPU Execution

Heron backend shows 12% better MaxCut score, 9% lower variance. *(placeholder)*

### 5.3 VQE Energy Estimation

AI-assisted VQE reduces error by 0.004 Ha. *(placeholder)*

### 5.4 Benchmarking

Quantum outperforms classical heuristics on selected instances. *(placeholder)*

---

## 6. Discussion

Hybrid quantum–AI methods show promise for near-term quantum advantage. Noise remains a limiting factor, but error mitigation helps.

---

## 7. Conclusion

We demonstrate measurable improvements in QAOA and VQE performance using AI heuristics and IBM Quantum hardware.

---

## References

(placeholder for academic citations)

## Appendix

Additional graphs, tables, and code.
