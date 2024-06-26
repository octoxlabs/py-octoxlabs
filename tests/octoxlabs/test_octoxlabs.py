# Standard Library
import json

# Third Party
import responses

# Octoxlabs
from octoxlabs import OctoxLabs


def test_octoxlabs_init(mock_response):
    mock_response.add(
        method=responses.POST,
        url="https://octoxlabs.test:8443/api/token/token",
        body=json.dumps({"access": "api-token"}),
    )
    octoxlabs = OctoxLabs(ip="octoxlabs.test", token="octoxlabs")

    assert octoxlabs.service.ip == "octoxlabs.test"
    assert octoxlabs.service.token == "octoxlabs"


def test_octoxlabs_ping(mock_response):
    mock_response.add(
        method=responses.POST,
        url="https://octoxlabs.service:8443/api/token/token",
        body=json.dumps({"access": "api-token"}),
    )
    octoxlabs = OctoxLabs(ip="octoxlabs.service", token="octoxlabs")
    mock_response.add(
        method=responses.GET, url="https://octoxlabs.service:8443/api/ping", body=json.dumps({"pong": "ok"})
    )
    assert octoxlabs.ping()
