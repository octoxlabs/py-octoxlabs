# Standard Library
import json

# Third Party
import responses

# Octoxlabs
from octoxlabs import OctoxLabs


def test_octoxlabs_init():
    octoxlabs = OctoxLabs(ip="octoxlabs.test", token="octoxlabs")

    assert octoxlabs.service.ip == "octoxlabs.test"
    assert octoxlabs.service.token == "octoxlabs"


def test_octoxlabs_ping(mock_response):
    octoxlabs = OctoxLabs(ip="octoxlabs.service", token="octoxlabs")
    mock_response.add(
        method=responses.GET, url="https://octoxlabs.service:8043/api/ping", body=json.dumps({"pong": "ok"})
    )
    assert octoxlabs.ping()
