# Standard Library
import json

# Third Party
import responses


def test_adapter_get_connections(adapter_factory, octoxlabs_service, mock_response):
    adapter = adapter_factory.create(service=octoxlabs_service)
    mock_response.add(
        method=responses.GET,
        url="https://octoxlabs.test:8043/adapters/connections?adapter=1",
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

    count, connections = adapter.get_connections()
    assert connections[0].name == "octoxlabs01"
    assert connections[0].id == 1
    assert connections[0].adapter_id == 1


def test_connection_get_adapter(connection_factory, octoxlabs_service, mock_response):
    connection = connection_factory.create(service=octoxlabs_service)
    mock_response.add(
        responses.GET,
        url="https://octoxlabs.test:8043/adapters/adapters/1",
        body=json.dumps(
            {
                "id": 1,
                "name": "Octox Labs",
                "slug": "octoxlabs",
                "description": "Octox Labs Description",
                "groups": ["CS"],
                "beta": True,
                "status": 1,
            }
        ),
    )

    adapter = connection.get_adapter()
    assert adapter.name == "Octox Labs"
    assert adapter.id == 1


def test_connection_connection_test(connection_factory, octoxlabs_service, mock_response):
    connection = connection_factory.create(service=octoxlabs_service)
    mock_response.add(
        method=responses.POST,
        url="https://octoxlabs.test:8043/adapters/test/1",
        body=json.dumps({"data": {"detail": "Bad request."}, "status": 400}),
    )

    result = connection.connection_test()
    assert result.get("status") == 400
    assert result.get("data").get("detail") == "Bad request."
