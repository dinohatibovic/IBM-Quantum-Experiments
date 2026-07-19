"""AI heuristics for QAOA/VQE parameter initialization.

Planned (ROADMAP Phase 3): ML-based initial angle prediction and
reinforcement-learning tuning of QAOA parameters.
"""


def suggest_initial_parameters(num_parameters: int) -> list[float]:
    """Return neutral initial parameters until ML models are integrated."""
    return [0.0] * num_parameters
