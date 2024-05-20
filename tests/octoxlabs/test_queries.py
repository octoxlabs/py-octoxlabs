# Standard Library
import json

# Third Party
import pytest
import responses

# Octoxlabs
from octoxlabs.exceptions import NotFound


def test_octoxlabs_get_queries(mock_response, octoxlabs_client):
    octoxlabs = octoxlabs_client

    mock_response.add(
        method=responses.GET,
        url="https://octoxlabs.service:8443/queries/queries",
        body=json.dumps(
            {
                "count": 1,
                "results": [
                    {
                        "id": "1",
                        "name": "Test",
                        "text": "",
                        "tags": [],
                        "tag_names": "",
                        "tag": [],
                        "count": 0,
                        "is_public": False,
                        "tagging_enabled": True,
                        "created_at": "2024-04-10T17:34:00.456396",
                        "updated_at": "2024-05-16T12:46:13.407771",
                        "user_full_name": "Test Octoxlabs",
                        "temporary": False,
                        "type": 1,
                        "grouped_query": False,
                    }
                ],
            }
        ),
    )

    count, queries = octoxlabs.get_queries()

    assert count == 1
    assert queries[0].id == "1"


def test_octoxlabs_create_query(mock_response, octoxlabs_client):
    octoxlabs = octoxlabs_client

    mock_response.add(
        method=responses.POST,
        url="https://octoxlabs.service:8443/queries/queries",
        body=json.dumps({"name": "Octoxlabs", "text": "Hostname = Octoxlabs", "is_public": True}),
    )

    create_message = octoxlabs.create_query(
        query_name="Octoxlabs", query_text="Hostname = Octoxlabs", is_public=True, tags="octo-tag"
    )

    assert create_message == "Octoxlabs query created successfully"


def test_octoxlabs_update_query(mock_response, octoxlabs_client):
    octoxlabs = octoxlabs_client

    mock_response.add(
        method=responses.PUT,
        url="https://octoxlabs.service:8443/queries/queries/00000000-0000",
        body=json.dumps(
            {
                "id": "1",
                "name": "updated-name",
                "text": "text",
                "tags": [],
                "tag_names": "",
                "tag": ["octo-tag"],
                "count": 0,
                "is_public": False,
                "tagging_enabled": True,
                "created_at": "2024-04-10T17:34:00.456396",
                "updated_at": "2024-05-16T12:46:13.407771",
                "user_full_name": "Test Octoxlabs",
                "temporary": False,
                "type": 1,
                "grouped_query": False,
            }
        ),
    )
    update_message = octoxlabs.update_query(
        query_id="00000000-0000", query_name="updated-name", query_text="text", is_public=False, tags="octo-tag"
    )

    assert update_message == "updated-name query successfully updated."


def test_octoxlabs_delete_query(mock_response, octoxlabs_client):
    octoxlabs = octoxlabs_client

    mock_response.add(
        method=responses.DELETE,
        url="https://octoxlabs.service:8443/queries/queries/00000000-0000",
    )

    delete_message = octoxlabs.delete_query(query_id="00000000-0000")

    assert delete_message == "Query deleted successfully."


def test_octoxlabs_get_queries_by_id(mock_response, octoxlabs_client):
    octoxlabs = octoxlabs_client

    mock_response.add(
        method=responses.GET,
        url="https://octoxlabs.service:8443/queries/queries/00000000-0000",
        body=json.dumps(
            {
                "id": "1",
                "name": "Test",
                "text": "",
                "tags": [],
                "tag_names": "",
                "tag": [],
                "count": 0,
                "is_public": False,
                "tagging_enabled": True,
                "created_at": "2024-04-10T17:34:00.456396",
                "updated_at": "2024-05-16T12:46:13.407771",
                "user_full_name": "Test Octoxlabs",
                "temporary": False,
                "type": 1,
                "grouped_query": False,
            }
        ),
    )

    query = octoxlabs.get_query_by_id(query_id="00000000-0000")

    assert query.name == "Test"


def test_octoxlabs_get_queries_by_name(mock_response, octoxlabs_client):
    octoxlabs = octoxlabs_client

    mock_response.add(
        method=responses.GET,
        url="https://octoxlabs.service:8443/queries/queries",
        body=json.dumps(
            {
                "count": 1,
                "results": [
                    {
                        "id": "1",
                        "name": "Test",
                        "text": "",
                        "tags": [],
                        "tag_names": "",
                        "tag": [],
                        "count": 0,
                        "is_public": False,
                        "tagging_enabled": True,
                        "created_at": "2024-04-10T17:34:00.456396",
                        "updated_at": "2024-05-16T12:46:13.407771",
                        "user_full_name": "Test Octoxlabs",
                        "temporary": False,
                        "type": 1,
                        "grouped_query": False,
                    }
                ],
            }
        ),
    )

    queries = octoxlabs.get_query_by_name(query_name="Test")
    assert queries.name == "Test"

    mock_response.add(
        method=responses.GET,
        url="https://octoxlabs.service:8443/queries/queries",
        body=json.dumps(
            {
                "count": 0,
                "results": [],
            }
        ),
    )

    with pytest.raises(NotFound):
        octoxlabs.get_query_by_name(query_name="octoxlabs")
