"""
extract_data.py
Extracts bond length, final energy, and optimal parameters
for a specific sample from the VQEzy H2 dataset.

Dataset: VQEzy/qchem/h2_4_qubit.h5
Samples: 0-149 (150 bond lengths from ~0.5 to 2.5 Angstrom)
"""

import h5py
import os

DEFAULT_DATASET = os.path.join(
    os.path.dirname(__file__),
    "data", "h2_4_qubit.h5"
)


def extract_h2_data(sample_index=0, dataset_path=None):
    """
    Extract data for a specific H2 sample.

    Parameters
    ----------
    sample_index : int
        Sample index 0-149 corresponding to a bond length
    dataset_path : str, optional
        Path to h2_4_qubit.h5
    """
    path = dataset_path or DEFAULT_DATASET

    if not os.path.exists(path):
        print(f"Error: Dataset not found at {path}")
        print("Download VQEzy dataset from: https://github.com/chizhang24/VQEzy")
        return

    try:
        with h5py.File(path, 'r') as f:
            bond_key   = f'bond_length/sample_{sample_index}'
            loss_key   = f'loss_history/sample_{sample_index}'
            params_key = f'opt_params/sample_{sample_index}'

            bond_val     = f[bond_key][()]
            loss_history = f[loss_key][()]
            params_val   = f[params_key][()]

            print(f"--- DATA EXTRACTION REPORT (Sample {sample_index}) ---")
            print(f"Bond Length:    {bond_val:.6f} Angstrom")
            print(f"Final Energy:   {loss_history[-1]:.8f} Hartree")
            print(f"Params Count:   {len(params_val)}")
            print(f"First 3 Params: {params_val[:3]}")
            print("------------------------------------------------------")

    except KeyError:
        print(f"Error: Sample {sample_index} not found. Valid range: 0-149.")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    extract_h2_data(sample_index=0)
