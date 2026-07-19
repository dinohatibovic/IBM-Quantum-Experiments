"""Generic client-facing optimization endpoint (scaffolding — NOT yet mounted).

Will route arbitrary optimization problems to QAOA/VQE/AI solvers.
"""
from fastapi import APIRouter

router = APIRouter()
