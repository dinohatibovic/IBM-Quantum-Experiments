class QOptiSolveError(Exception):
    """Base exception for QOptiSolve."""


class InvalidGraphError(QOptiSolveError):
    """Raised when graph input is invalid."""


class SolverExecutionError(QOptiSolveError):
    """Raised when a solver fails during execution."""


class QPUUnavailableError(QOptiSolveError):
    """Raised when QPU execution is requested but unavailable."""
