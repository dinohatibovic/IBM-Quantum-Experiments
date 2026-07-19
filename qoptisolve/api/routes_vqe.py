"""VQE endpoint (scaffolding — NOT yet mounted in app.py).

Will expose POST /optimize/vqe once quantum/vqe_engine.py is implemented.
"""
from fastapi import APIRouter

router = APIRouter()
