# Standard Library
import json

# Third Party
import responses

# Octoxlabs
from octoxlabs import OctoxLabs


def test_octoxlabs_search_avm(mock_response):
    mock_response.add(
        method=responses.POST,
        url="https://octoxlabs.service:8443/api/token/token",
        body=json.dumps({"access": "api-token"}),
    )
    octoxlabs = OctoxLabs(ip="octoxlabs.service", token="octoxlabs")
    mock_response.add(
        method=responses.POST,
        url="https://octoxlabs.service:8443/avm/vulnerabilities",
        body=json.dumps(
            {
                "count": 1,
                "results": [
                    {
                        "Description": ["Microsoft Edge (Chromium-based) Elevation of Privilege Vulnerability"],
                        "AssetCount": [233],
                        "Id": ["CVE-ID"],
                        "ApplicationCount": [1],
                        "Cvss3Score": [8.3],
                        "Cvss3Severity": ["High"],
                    }
                ],
            }
        ),
    )

    count, vulnerabilities = octoxlabs.search_avm()
    vuln = vulnerabilities[0]

    assert count == 1
    assert vuln["Id"] == ["CVE-ID"]


def test_octoxlabs_search_scroll_avm(mock_response):
    mock_response.add(
        method=responses.POST,
        url="https://octoxlabs.service:8443/api/token/token",
        body=json.dumps({"access": "api-token"}),
    )
    octoxlabs = OctoxLabs(ip="octoxlabs.service", token="octoxlabs")
    mock_response.add(
        method=responses.POST,
        url="https://octoxlabs.service:8443/avm/vulnerabilities",
        body=json.dumps(
            {
                "count": 1,
                "results": [
                    {
                        "Description": ["Microsoft Edge (Chromium-based) Elevation of Privilege Vulnerability"],
                        "AssetCount": [233],
                        "Id": ["CVE-ID"],
                        "ApplicationCount": [1],
                        "Cvss3Score": [8.3],
                        "Cvss3Severity": ["High"],
                    }
                ],
            }
        ),
    )
    count, scroll_id, vulnerabilities = octoxlabs.search_scroll_avm()
    vuln = vulnerabilities[0]
    assert count == 1
    assert vuln["Id"] == ["CVE-ID"]

    mock_response.add(
        method=responses.POST,
        url="https://octoxlabs.service:8443/avm/vulnerabilities",
        body=json.dumps(
            {
                "count": 1,
                "scroll_id": "octoxlabs-scroll-id",
                "results": [],
            }
        ),
    )

    count, scroll_id, assets = octoxlabs.search_scroll_avm(scroll_id="octoxlabs-scroll-id")
    assert count == 1
    assert assets == []
