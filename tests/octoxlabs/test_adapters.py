# Standard Library
import json

import pytest

# Third Party
import responses

# Octoxlabs
from octoxlabs import OctoxLabs


def test_octoxlabs_get_adapters(mock_response):
    mock_response.add(
        method=responses.POST,
        url="https://octoxlabs.service:8443/api/token/token",
        body=json.dumps({"access": "api-token"}),
    )
    octoxlabs = OctoxLabs(ip="octoxlabs.service", token="octoxlabs")
    mock_response.add(
        method=responses.GET,
        url="https://octoxlabs.service:8443/adapters/adapters?search=octox&size=1&page=1",
        body=json.dumps(
            {
                "count": 1,
                "results": [
                    {
                        "id": 1,
                        "name": "Octox Labs",
                        "slug": "octoxlabs",
                        "description": "Octox Labs Description",
                        "groups": ["CS"],
                        "beta": True,
                        "status": 1,
                    }
                ],
            }
        ),
    )

    count, adapters = octoxlabs.get_adapters(search="octox", size=1)
    assert count == 1
    assert adapters[0].id == 1
    assert adapters[0].name == "Octox Labs"


def test_octoxlabs_get_connections(adapter_factory, mock_response):
    mock_response.add(
        method=responses.POST,
        url="https://octoxlabs.service:8443/api/token/token",
        body=json.dumps({"access": "api-token"}),
    )

    octoxlabs = OctoxLabs(ip="octoxlabs.service", token="octoxlabs")
    mock_response.add(
        method=responses.GET,
        url="https://octoxlabs.service:8443/adapters/connections?adapter=1&page=1&search=&size=20",
        body=json.dumps(
            {
                "count": 1,
                "results": [
                    {
                        "id": 1,
                        "adapter": 1,
                        "adapter_name": "Octox Labs",
                        "name": "octoxlabs01",
                        "status": True,
                        "description": "",
                        "enabled": False,
                    }
                ],
            }
        ),
    )
    adapter = adapter_factory.create()

    count, connections = octoxlabs.get_connections(adapter=adapter)
    assert count == 1
    assert connections[0].name == "octoxlabs01"

    count2, connections2 = octoxlabs.get_connections(adapter_id=1)
    assert count2 == 1
    assert connections2[0].name == "octoxlabs01"


def test_octoxlabs_create_connection(mock_response, octoxlabs_client):
    octoxlabs = octoxlabs_client

    mock_response.add(
        method=responses.POST,
        url="https://octoxlabs.service:8443/adapters/connections",
        body=json.dumps(
            {
                "adapter": 1,
                "name": "test-connection",
                "description": "connection",
                "option_connections": [{"name": "test-option", "typed_value": False, "is_sensitive": False}],
                "connector": 1,
            }
        ),
    )

    connection_message = octoxlabs.create_connection(
        adapter_id=1,
        connection_name="test-connection",
        connection_description="connection",
        connector_id=1,
        option_connections=[{"name": "test-option", "typed_value": False, "is_sensitive": False}],
    )

    assert connection_message == "test-connection connection created successfully"


def test_octoxlabs_delete_connection(mock_response, octoxlabs_client):
    octoxlabs = octoxlabs_client

    mock_response.add(
        method=responses.DELETE,
        url="https://octoxlabs.service:8443/adapters/connections/1",
    )
    delete_message = octoxlabs.delete_connection(connection_id=1)
    assert delete_message == "Connection deleted successfully."
