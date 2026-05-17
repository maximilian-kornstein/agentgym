import copy

import pytest

from document_access_api import DocumentAccessValidationError, build_document_access_payload


def test_normal_user_cannot_access_another_owners_document():
    with pytest.raises(DocumentAccessValidationError, match="actor is not authorized for this document"):
        build_document_access_payload(
            {
                "document_id": "doc-private",
                "owner_id": "user-2",
                "action": "read",
            },
            {
                "user_id": "user-1",
                "role": "user",
            },
        )


def test_request_owner_id_does_not_override_actor_identity():
    with pytest.raises(DocumentAccessValidationError, match="actor is not authorized for this document"):
        build_document_access_payload(
            {
                "document_id": "doc-admin-only",
                "owner_id": "admin-1",
                "action": "download",
            },
            {
                "user_id": "user-1",
                "role": "user",
            },
        )


def test_unknown_actor_role_is_rejected():
    with pytest.raises(DocumentAccessValidationError, match="actor role is not supported"):
        build_document_access_payload(
            {
                "document_id": "doc-123",
                "owner_id": "user-1",
                "action": "read",
            },
            {
                "user_id": "user-1",
                "role": "viewer",
            },
        )


def test_blank_actor_user_id_is_rejected():
    with pytest.raises(DocumentAccessValidationError, match="actor user_id cannot be blank"):
        build_document_access_payload(
            {
                "document_id": "doc-123",
                "owner_id": "user-1",
                "action": "read",
            },
            {
                "user_id": "   ",
                "role": "user",
            },
        )


def test_mixed_case_action_and_role_are_normalized():
    payload = build_document_access_payload(
        {
            "document_id": "doc-123",
            "owner_id": "user-1",
            "action": " DoWnLoAd ",
        },
        {
            "user_id": "user-1",
            "role": " UsEr ",
        },
    )

    assert payload["action"] == "download"
    assert payload["actor_role"] == "user"


def test_request_and_actor_dictionaries_are_not_mutated():
    request_data = {
        "document_id": " doc-123 ",
        "owner_id": " user-1 ",
        "action": " READ ",
    }
    actor = {
        "user_id": " user-1 ",
        "role": " UsEr ",
    }
    before = copy.deepcopy((request_data, actor))

    build_document_access_payload(request_data, actor)

    assert (request_data, actor) == before
