# IBM Quantum Hardware

Set your IBM Quantum token:

```bash
export IBM_QUANTUM_TOKEN="your_token"
```

Save credentials:

```bash
python scripts/setup_ibm.py
```

Run IBM demo:

```bash
python examples/ibm_demo.py --backend ibm_fez --shots 1000
```

Real hardware results may vary due to backend noise, queue conditions, and calibration state.
