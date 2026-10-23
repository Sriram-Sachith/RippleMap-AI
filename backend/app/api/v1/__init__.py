"""API v1 router initialization."""

from fastapi import APIRouter

api_router = APIRouter(prefix="/api/v1")

__all__ = ["api_router"]
