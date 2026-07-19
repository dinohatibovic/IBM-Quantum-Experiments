# Drafts — unverified variants

Files in this folder are **variants from the pasted specification** that would
overwrite the working, tested MVP code — which is why they live here instead of
their "real" locations. **They are untested and have known bugs.** The working
versions are in `qoptisolve/`.

| File | Working version | Known issues in the variant |
| --- | --- | --- |
| `app_startup_variant.py` | `qoptisolve/app.py` | accepts a raw `dict` payload without Pydantic validation; imports QPUExecutor at app level (crashes without IBM credentials) |
| `qaoa_engine_qiskit_variant.py` | `qoptisolve/quantum/qaoa_engine.py` | `QAOA.compute_minimum_eigenvalue` does not accept a numpy matrix — it needs a `SparsePauliOp`; the `Estimator` import is deprecated in Qiskit 2.x |
| `qpu_pyproject_variant.toml` | `pyproject.toml` | different dependencies (torch, scikit-learn in core); placeholder email |
| `requirements_variant.txt` | `requirements.txt` | narrower set, no dev tools |
