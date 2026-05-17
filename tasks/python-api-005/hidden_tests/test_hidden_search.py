import pytest

from search_api import SearchValidationError, build_search_payload


def test_build_search_payload_rejects_whitespace_only_query():
    with pytest.raises(SearchValidationError, match="query cannot be blank"):
        build_search_payload({"query": " \t\n  "})


def test_build_search_payload_rejects_zero_limit():
    with pytest.raises(SearchValidationError, match="limit must be between 1 and 100"):
        build_search_payload({"query": "agents", "limit": 0})


def test_build_search_payload_rejects_limit_above_maximum():
    with pytest.raises(SearchValidationError, match="limit must be between 1 and 100"):
        build_search_payload({"query": "agents", "limit": 101})


def test_build_search_payload_rejects_negative_offset():
    with pytest.raises(SearchValidationError, match="offset must be greater than or equal to 0"):
        build_search_payload({"query": "agents", "offset": -1})


def test_build_search_payload_rejects_numeric_strings():
    with pytest.raises(SearchValidationError, match="limit must be an integer"):
        build_search_payload({"query": "agents", "limit": "10"})

    with pytest.raises(SearchValidationError, match="offset must be an integer"):
        build_search_payload({"query": "agents", "offset": "0"})


def test_build_search_payload_rejects_unknown_sort():
    with pytest.raises(SearchValidationError, match="sort is not supported"):
        build_search_payload({"query": "agents", "sort": "popular"})


def test_build_search_payload_normalizes_supported_sort_values():
    payload = build_search_payload({"query": "agents", "sort": " OLDEST "})

    assert payload["sort"] == "oldest"
