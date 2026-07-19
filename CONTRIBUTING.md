# Contributing to QOptiSolve

Thank you for wanting to contribute to the QOptiSolve project!
This document describes the rules, coding style, pull request process, and code quality guidelines.

---

## 🧭 Getting started

1. Fork the repository
2. Create a new branch:

    ```bash
    git checkout -b feature/my-feature
    ```

3. Make your changes following the style rules
4. Run the tests:

    ```bash
    pytest
    ```

5. Open a Pull Request (PR)

---

## 🧱 Coding style

- Python 3.12+
- PEP8 standard
- Type hints required (`typing`)
- Docstring for every function
- Clear module structure:
  - `api/`
  - `core/`
  - `quantum/`
  - `ai/`
  - `tests/`

---

## 🧪 Tests

Every new feature must have tests in `tests/` or `qoptisolve/tests/`.

Example:

```python
def test_qaoa_runs():
    engine = QAOAEngine()
    result = engine.optimize([(0, 1, 1)])
    assert result is not None
```

---

## 🔍 Pull Request rules

- At least 1 reviewer
- A PR must contain:
  - a description of the change
  - a link to the issue (if one exists)
  - a screenshot or output (if relevant)
- CI must pass without errors

---

## 🛠 Branch conventions

- `main` → stable version
- `dev` → active development
- `feature/*` → new features
- `fix/*` → bugfixes

---

## ❤️ Ways to contribute

- fix a bug
- add a new feature
- improve documentation
- optimize QAOA/VQE
- add AI heuristics
- improve QPU integration

Thank you for contributing!
