# Standard Library
import json

# Third Party
import responses

# Octoxlabs
from octoxlabs import OctoxLabs


def test_octoxlabs_search_services(mock_response):
    mock_response.add(
        method=responses.POST,
        url="https://octoxlabs.service:8443/api/token/token",
        body=json.dumps({"access": "api-token"}),
    )
    octoxlabs = OctoxLabs(ip="octoxlabs.service", token="octoxlabs")
    mock_response.add(
        method=responses.POST,
        url="https://octoxlabs.service:8443/services/services",
        body=json.dumps(
            {
                "count": 1,
                "results": [{"ParentRegion": "east_us", "Name": "service01"}],
            }
        ),
    )

    count, services = octoxlabs.search_services()
    service = services[0]

    assert count == 1
    assert service["Name"] == "service01"


def test_octoxlabs_search_scroll_services(mock_response):
    mock_response.add(
        method=responses.POST,
        url="https://octoxlabs.service:8443/api/token/token",
        body=json.dumps({"access": "api-token"}),
    )
    octoxlabs = OctoxLabs(ip="octoxlabs.service", token="octoxlabs")
    mock_response.add(
        method=responses.POST,
        url="https://octoxlabs.service:8443/services/services",
        body=json.dumps(
            {
                "count": 1,
                "scroll_id": "octoxlabs-scroll-id",
                "results": [{"ParentRegion": "east_us", "Name": "service01"}],
            }
        ),
    )
    count, scroll_id, services = octoxlabs.search_scroll_services()
    service = services[0]
    assert count == 1
    assert service["Name"] == "service01"

    mock_response.add(
        method=responses.POST,
        url="https://octoxlabs.service:8443/services/services",
        body=json.dumps(
            {
                "count": 1,
                "scroll_id": "octoxlabs-scroll-id",
                "results": [],
            }
        ),
    )

    count, scroll_id, assets = octoxlabs.search_scroll_services(scroll_id="octoxlabs-scroll-id")
    assert count == 1
    assert assets == []


def test_octoxlabs_get_service_detail(discovery_factory, mock_response):
    mock_response.add(
        method=responses.POST,
        url="https://octoxlabs.service:8443/api/token/token",
        body=json.dumps({"access": "api-token"}),
    )

    octoxlabs = OctoxLabs(ip="octoxlabs.service", token="octoxlabs")
    mock_response.add(
        method=responses.POST,
        url="https://octoxlabs.service:8443/services/services/service-id",
        body=json.dumps({"ParentRegion": "east_us", "Name": "service01"}),
    )
    discovery = discovery_factory.create()

    service = octoxlabs.get_service_detail(service_id="service-id", discovery=discovery)
    assert service["Name"] == "service01"
