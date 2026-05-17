import pytest

from search_api import SearchValidationError, build_search_payload


def test_build_search_payload_uses_defaults_for_minimal_request():
    payload = build_search_payload({"query": "  vector database  "})

    assert payload == {
        "query": "vector database",
        "limit": 20,
        "offset": 0,
        "sort": "relevance",
    }


def test_build_search_payload_accepts_explicit_options():
    payload = build_search_payload(
        {
            "query": "agents",
            "limit": 25,
            "offset": 50,
            "sort": " newest ",
        }
    )

    assert payload == {
        "query": "agents",
        "limit": 25,
        "offset": 50,
        "sort": "newest",
    }


def test_build_search_payload_rejects_missing_query():
    with pytest.raises(SearchValidationError, match="query is required"):
        build_search_payload({"limit": 10})


def test_build_search_payload_rejects_float_limit():
    with pytest.raises(SearchValidationError, match="limit must be an integer"):
        build_search_payload({"query": "agents", "limit": 10.5})
