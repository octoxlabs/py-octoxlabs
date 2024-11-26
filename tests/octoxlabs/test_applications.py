# Standard Library
import json

# Third Party
import responses

# Octoxlabs
from octoxlabs import OctoxLabs


def test_octoxlabs_search_applications(mock_response):
    mock_response.add(
        method=responses.POST,
        url="https://octoxlabs.service:8443/api/token/token",
        body=json.dumps({"access": "api-token"}),
    )
    octoxlabs = OctoxLabs(ip="octoxlabs.service", token="octoxlabs")
    mock_response.add(
        method=responses.POST,
        url="https://octoxlabs.service:8443/appinventory/applications",
        body=json.dumps(
            {
                "count": 1,
                "results": [
                    {
                        "VulnerabilityMaxSeverity": ["Critical"],
                        "Description": ["Microsoft Edge Description"],
                        "Architecture": ["x86"],
                        "Version": [""],
                        "VulnerabilityCount": [10],
                        "Groups": ["group01"],
                        "Count": [233],
                        "Publisher": ["Microsoft Corporation"],
                        "VulnerabilityMaxScore": [9.6],
                        "Name": ["Microsoft Edge - 120.0.2210.77"],
                        "Id": "application-id",
                    }
                ],
            }
        ),
    )

    count, applications = octoxlabs.search_applications()
    application = applications[0]

    assert count == 1
    assert application["Description"] == ["Microsoft Edge Description"]


def test_octoxlabs_search_scroll_applications(mock_response):
    mock_response.add(
        method=responses.POST,
        url="https://octoxlabs.service:8443/api/token/token",
        body=json.dumps({"access": "api-token"}),
    )
    octoxlabs = OctoxLabs(ip="octoxlabs.service", token="octoxlabs")
    mock_response.add(
        method=responses.POST,
        url="https://octoxlabs.service:8443/appinventory/applications",
        body=json.dumps(
            {
                "count": 1,
                "scroll_id": "octoxlabs-scroll-id",
                "results": [
                    {
                        "VulnerabilityMaxSeverity": ["Critical"],
                        "Description": ["Microsoft Edge Description"],
                        "Architecture": ["x86"],
                        "Version": [""],
                        "VulnerabilityCount": [10],
                        "Groups": ["group01"],
                        "Count": [233],
                        "Publisher": ["Microsoft Corporation"],
                        "VulnerabilityMaxScore": [9.6],
                        "Name": ["Microsoft Edge - 120.0.2210.77"],
                        "Id": "application-id",
                    }
                ],
            }
        ),
    )
    count, scroll_id, applications = octoxlabs.search_scroll_applications()
    application = applications[0]
    assert count == 1
    assert application["Id"] == "application-id"

    mock_response.add(
        method=responses.POST,
        url="https://octoxlabs.service:8443/appinventory/applications",
        body=json.dumps(
            {
                "count": 1,
                "scroll_id": "octoxlabs-scroll-id",
                "results": [],
            }
        ),
    )

    count, scroll_id, assets = octoxlabs.search_scroll_applications(scroll_id="octoxlabs-scroll-id")
    assert count == 1
    assert assets == []


def test_octoxlabs_get_application_detail(discovery_factory, mock_response):
    mock_response.add(
        method=responses.POST,
        url="https://octoxlabs.service:8443/api/token/token",
        body=json.dumps({"access": "api-token"}),
    )

    octoxlabs = OctoxLabs(ip="octoxlabs.service", token="octoxlabs")
    mock_response.add(
        method=responses.POST,
        url="https://octoxlabs.service:8443/appinventory/applications/application-id",
        body=json.dumps(
            {
                "VulnerabilityMaxSeverity": "Critical",
                "Description": "Microsoft Edge Description",
                "Architecture": "x86",
                "Version": "",
                "VulnerabilityCount": 10,
                "Groups": ["group01"],
                "Count": 233,
                "Publisher": "Microsoft Corporation",
                "VulnerabilityMaxScore": 9.6,
                "Name": "Microsoft Edge - 120.0.2210.77",
                "Id": "application-id",
            }
        ),
    )
    discovery = discovery_factory.create()

    application = octoxlabs.get_application_detail(application_id="application-id", discovery=discovery)
    assert application["Id"] == "application-id"
