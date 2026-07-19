"""
find_target.py
Finds the VQEzy dataset sample closest to the IBM Heron r2 hardware result.

IBM Hardware result (ibm_fez, Heron r2, 156 qubits):
  Energy: -1.196080 Hartree
  DOI: 10.5281/zenodo.20749395

VQEzy dataset: 150 H2 samples, 4-qubit STO-3G basis
  Source: https://github.com/chizhang24/VQEzy
"""

import h5py
import numpy as np
import os

# IBM Heron r2 hardware result (Zenodo DOI: 10.5281/zenodo.20749395)
IBM_HERON_ENERGY = -1.196080   # Hartree
IBM_HERON_BOND   = 0.735       # Angstrom

DEFAULT_DATASET = os.path.join(
    os.path.dirname(__file__),
    "data", "h2_4_qubit.h5"
)


def find_closest_bond(dataset_path=None):
    """
    Finds the VQEzy sample closest to IBM hardware bond length.
    Compares energies and prints a benchmark report.

    Parameters
    ----------
    dataset_path : str, optional
        Path to h2_4_qubit.h5. Defaults to ./data/h2_4_qubit.h5
    """
    path = dataset_path or DEFAULT_DATASET

    if not os.path.exists(path):
        print(f"Error: Dataset not found at {path}")
        print("Download VQEzy dataset from: https://github.com/chizhang24/VQEzy")
        return

    try:
        with h5py.File(path, 'r') as f:
            closest_sample = -1
            min_diff = float('inf')

            # Search through all 150 bond length samples
            for i in range(150):
                bond_key = f'bond_length/sample_{i}'
                if bond_key in f:
                    bond_val = f[bond_key][()]
                    diff = abs(bond_val - IBM_HERON_BOND)
                    if diff < min_diff:
                        min_diff = diff
                        closest_sample = i

            best_bond = f[f'bond_length/sample_{closest_sample}'][()]
            best_loss = f[f'loss_history/sample_{closest_sample}'][()][-1]

            diff_ha = IBM_HERON_ENERGY - best_loss
            diff_ev = diff_ha * 27.2114

            print("=" * 54)
            print("  BENCHMARK: IBM Heron r2 vs VQEzy Dataset")
            print("=" * 54)
            print(f"Closest VQEzy sample:     sample_{closest_sample}")
            print(f"Bond length (dataset):    {best_bond:.6f} Angstrom")
            print(f"Bond length (IBM target): {IBM_HERON_BOND:.6f} Angstrom")
            print()
            print(f"VQEzy energy (4q STO-3G): {best_loss:.6f} Hartree")
            print(f"IBM Heron energy (VQC):   {IBM_HERON_ENERGY:.6f} Hartree")
            print(f"Difference:               {diff_ha:.6f} Ha = {diff_ev:.4f} eV")
            print()
            print("Note: Energy difference is expected.")
            print("VQEzy uses minimal STO-3G basis (4 qubits).")
            print("IBM result uses full VQC on Heron r2 hardware.")
            print("=" * 54)

    except Exception as e:
        print(f"Error reading dataset: {e}")


if __name__ == "__main__":
    find_closest_bond()
