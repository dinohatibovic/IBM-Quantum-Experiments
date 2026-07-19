# Quickstart

Run all local demonstrations:

```bash
python examples/local_demo.py
```

Minimal example:

```python
from quantum_core import QuantumBackend, bell_inequality_test

backend = QuantumBackend(mode="local")
result = bell_inequality_test(1000, backend=backend)

print(result["S_value"])
print(result["interpretation"])
```
