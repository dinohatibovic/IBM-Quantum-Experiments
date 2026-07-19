"""
First-time IBM Quantum account setup.
Run once: python scripts/setup_ibm.py

Saves credentials to ~/.qiskit/qiskit-ibm.json
"""

import os
from qiskit_ibm_runtime import QiskitRuntimeService

TOKEN = os.getenv("IBM_QUANTUM_TOKEN")
if not TOKEN:
    TOKEN = input("Enter your IBM Quantum API token: ").strip()

QiskitRuntimeService.save_account(
    channel="ibm_quantum",
    token=TOKEN,
    overwrite=True,
)

print("\nCredentials saved to ~/.qiskit/qiskit-ibm.json")

# List available backends
service = QiskitRuntimeService(channel="ibm_quantum")
backends = service.backends(operational=True, simulator=False)
print("\nYour accessible real quantum backends:")
for b in backends:
    print(f"  {b.name}  —  {b.num_qubits} qubits")

print("\nRecommended backends from your IBM portfolio:")
print("  ibm_fez    (Eagle r3, 127 qubits)")
print("  ibm_torino (Heron r1, 133 qubits)")
