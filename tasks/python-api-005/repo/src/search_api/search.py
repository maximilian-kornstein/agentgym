from __future__ import annotations

from typing import Any, Mapping


DEFAULT_LIMIT = 20
DEFAULT_OFFSET = 0
DEFAULT_SORT = "relevance"
SUPPORTED_SORTS = {"relevance", "newest", "oldest"}


class SearchValidationError(ValueError):
    """Raised when a search request cannot be normalized."""


def build_search_payload(request_data: Mapping[str, Any]) -> dict[str, Any]:
    """Build a normalized search payload from request input."""
    if "query" not in request_data:
        raise SearchValidationError("query is required")

    query = request_data["query"]
    if not isinstance(query, str):
        raise SearchValidationError("query must be a string")

    query = query.strip()

    limit = _parse_number(request_data.get("limit", DEFAULT_LIMIT), "limit")
    offset = _parse_number(request_data.get("offset", DEFAULT_OFFSET), "offset")
    sort = _parse_sort(request_data.get("sort", DEFAULT_SORT))

    return {
        "query": query,
        "limit": limit,
        "offset": offset,
        "sort": sort,
    }


def _parse_number(value: Any, field_name: str) -> int:
    if isinstance(value, str) and value.strip().isdigit():
        return int(value)

    if not isinstance(value, int) or isinstance(value, bool):
        raise SearchValidationError(f"{field_name} must be an integer")

    return value


def _parse_sort(value: Any) -> str:
    if not isinstance(value, str):
        raise SearchValidationError("sort must be a string")

    value = value.strip().lower()
    if value == "":
        raise SearchValidationError("sort is not supported")

    return value
