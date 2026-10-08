"""Standard response wrapper used by every endpoint: {data, meta, error}."""
from typing import Any


def ok(data: Any = None, meta: dict | None = None) -> dict:
    return {"data": data, "meta": meta, "error": None}


def fail(code: str, message: str) -> dict:
    return {"data": None, "meta": None, "error": {"code": code, "message": message}}
