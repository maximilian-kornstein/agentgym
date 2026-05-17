import pytest

from document_access_api import DocumentAccessValidationError, build_document_access_payload


def test_build_document_access_payload_allows_owner_user_to_read_document():
    payload = build_document_access_payload(
        {
            "document_id": " doc-123 ",
            "owner_id": " user-1 ",
            "action": " READ ",
        },
        {
            "user_id": "user-1",
            "role": "user",
        },
    )

    assert payload == {
        "document_id": "doc-123",
        "owner_id": "user-1",
        "actor_user_id": "user-1",
        "actor_role": "user",
        "action": "read",
        "authorized": True,
    }


def test_build_document_access_payload_allows_admin_to_delete_other_users_document():
    payload = build_document_access_payload(
        {
            "document_id": "doc-456",
            "owner_id": "user-2",
            "action": "delete",
        },
        {
            "user_id": "admin-1",
            "role": "admin",
        },
    )

    assert payload["document_id"] == "doc-456"
    assert payload["owner_id"] == "user-2"
    assert payload["actor_user_id"] == "admin-1"
    assert payload["actor_role"] == "admin"
    assert payload["action"] == "delete"
    assert payload["authorized"] is True


def test_build_document_access_payload_rejects_missing_document_id():
    with pytest.raises(DocumentAccessValidationError, match="document_id is required"):
        build_document_access_payload(
            {"owner_id": "user-1", "action": "read"},
            {"user_id": "user-1", "role": "user"},
        )


def test_build_document_access_payload_rejects_unsupported_action():
    with pytest.raises(DocumentAccessValidationError, match="action is not supported"):
        build_document_access_payload(
            {"document_id": "doc-123", "owner_id": "user-1", "action": "share"},
            {"user_id": "user-1", "role": "user"},
        )
