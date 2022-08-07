# Standard Library
import json

# Third Party
import responses

# Octoxlabs
from octoxlabs import OctoxLabs


def test_octoxlabs_get_adapters(mock_response):
    octoxlabs = OctoxLabs(ip="octoxlabs.service", token="octoxlabs")
    mock_response.add(
        method=responses.GET,
        url="https://octoxlabs.service:8043/adapters/adapters?search=octox&size=1",
        body=json.dumps(
            {
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
                ]
            }
        ),
    )

    adapter = octoxlabs.get_adapters(search="octox", size=1)[0]
    assert adapter.id == 1
    assert adapter.name == "Octox Labs"


def test_octoxlabs_get_connections(adapter_factory, mock_response):
    octoxlabs = OctoxLabs(ip="octoxlabs.service", token="octoxlabs")
    mock_response.add(
        method=responses.GET,
        url="https://octoxlabs.service:8043/adapters/connections?adapter=1",
        body=json.dumps(
            {
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
                ]
            }
        ),
    )
    adapter = adapter_factory.create()

    connection = octoxlabs.get_connections(adapter=adapter)[0]
    assert connection.name == "octoxlabs01"

    connection2 = octoxlabs.get_connections(adapter_id=1)[0]
    assert connection2.name == "octoxlabs01"
