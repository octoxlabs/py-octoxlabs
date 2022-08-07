# Standard Library
import json

# Third Party
import pytest
import responses

# Octoxlabs
from octoxlabs import OctoxLabs
from octoxlabs.exceptions import NoDiscoveryError


def test_octoxlabs_get_discoveries(mock_response):
    octoxlabs = OctoxLabs(ip="octoxlabs.service", token="octoxlabs")
    mock_response.add(
        method=responses.GET,
        url="https://octoxlabs.service:8043/discoveries/discoveries",
        body=json.dumps(
            {
                "results": [
                    {
                        "id": 1,
                        "start_time": "2022-07-22T00:23:28.752662Z",
                        "end_time": "2022-07-22T00:25:28.752662Z",
                        "status": 2,
                        "progress": 100.0,
                    }
                ]
            }
        ),
    )

    discovery = octoxlabs.get_discoveries()[0]
    assert discovery.status == 2


def test_octoxlabs_get_last_discovery(mock_response):
    octoxlabs = OctoxLabs(ip="octoxlabs.service", token="octoxlabs")
    mock_response.add(
        method=responses.GET,
        url="https://octoxlabs.service:8043/discoveries/last",
        body=json.dumps(
            {
                "id": 1,
                "start_time": "2022-07-22T00:23:28.752662Z",
                "end_time": "2022-07-22T00:25:28.752662Z",
                "status": 2,
                "progress": 100.0,
            }
        ),
    )

    discovery = octoxlabs.get_last_discovery()
    assert discovery.status == 2

    mock_response.add(
        method=responses.GET,
        url="https://octoxlabs.service:8043/discoveries/last",
        body=json.dumps(
            {
                "status": 2,
                "progress": 0.0,
            }
        ),
    )

    with pytest.raises(NoDiscoveryError):
        octoxlabs.get_last_discovery()
