"""
inspect_h2.py
Scans the VQEzy H2 HDF5 dataset and prints the full key hierarchy.
Useful for understanding dataset structure before extraction.

Dataset: VQEzy/qchem/h2_4_qubit.h5
Source:  https://github.com/chizhang24/VQEzy
"""

import h5py
import os

DEFAULT_DATASET = os.path.join(
    os.path.dirname(__file__),
    "data", "h2_4_qubit.h5"
)


def inspect_dataset(dataset_path=None):
    """
    Print the full HDF5 key hierarchy of the H2 dataset.

    Parameters
    ----------
    dataset_path : str, optional
        Path to h2_4_qubit.h5
    """
    path = dataset_path or DEFAULT_DATASET

    if not os.path.exists(path):
        print(f"Error: Dataset not found at {path}")
        print("Download VQEzy dataset from: https://github.com/chizhang24/VQEzy")
        return

    try:
        with h5py.File(path, 'r') as h5_file:
            print(f"--- DATASET STRUCTURE: {os.path.basename(path)} ---")
            h5_file.visititems(lambda name, obj: print(f"  Key: {name}"))
            print("--- INSPECTION COMPLETE ---")

    except Exception as e:
        print(f"Error opening dataset: {e}")


if __name__ == "__main__":
    inspect_dataset()
