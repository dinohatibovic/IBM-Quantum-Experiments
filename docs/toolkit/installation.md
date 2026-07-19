# Installation

Recommended Python version: 3.12.

## Standard setup

```bash
git clone https://github.com/dinohatibovic/qiskit-nisq-toolkit.git
cd qiskit-nisq-toolkit

python -m venv .venv
source .venv/bin/activate

python -m pip install --upgrade pip setuptools wheel
python -m pip install -e ".[dev]"
```

## Run tests

```bash
python -m pytest tests -v
```

## Run local demo

```bash
python examples/local_demo.py
```

## Notes for Linux on mobile/proot

If `qiskit-aer` tries to build from source, prefer a Linux `aarch64` Python environment instead of Android/Termux Python.

This project was locally verified with:

```text
Python 3.12.8
linux-aarch64
Qiskit 2.5.0
Qiskit Aer 0.17.2
```
