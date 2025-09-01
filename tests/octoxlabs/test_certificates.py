# Standard Library
import json

# Third Party
import responses

# Octoxlabs
from octoxlabs import OctoxLabs


def test_octoxlabs_search_certificates(mock_response):
    mock_response.add(
        method=responses.POST,
        url="https://octoxlabs.service:8443/api/token/token",
        body=json.dumps({"access": "api-token"}),
    )
    octoxlabs = OctoxLabs(ip="octoxlabs.service", token="octoxlabs")
    mock_response.add(
        method=responses.POST,
        url="https://octoxlabs.service:8443/certificates/certificates",
        body=json.dumps(
            {
                "count": 1,
                "results": [{"CertificateType": "client_certificate", "Name": "cf-1234aabb"}],
            }
        ),
    )

    count, certificates = octoxlabs.search_certificates()
    certificate = certificates[0]

    assert count == 1
    assert certificate["Name"] == "cf-1234aabb"


def test_octoxlabs_search_scroll_certificates(mock_response):
    mock_response.add(
        method=responses.POST,
        url="https://octoxlabs.service:8443/api/token/token",
        body=json.dumps({"access": "api-token"}),
    )
    octoxlabs = OctoxLabs(ip="octoxlabs.service", token="octoxlabs")
    mock_response.add(
        method=responses.POST,
        url="https://octoxlabs.service:8443/certificates/certificates",
        body=json.dumps(
            {
                "count": 1,
                "scroll_id": "octoxlabs-scroll-id",
                "results": [{"CertificateType": "client_certificate", "Name": "cf-1234aabb"}],
            }
        ),
    )
    count, scroll_id, certificates = octoxlabs.search_scroll_certificates()
    certificate = certificates[0]
    assert count == 1
    assert certificate["Name"] == "cf-1234aabb"

    mock_response.add(
        method=responses.POST,
        url="https://octoxlabs.service:8443/certificates/certificates",
        body=json.dumps(
            {
                "count": 1,
                "scroll_id": "octoxlabs-scroll-id",
                "results": [],
            }
        ),
    )

    count, scroll_id, assets = octoxlabs.search_scroll_certificates(scroll_id="octoxlabs-scroll-id")
    assert count == 1
    assert assets == []


def test_octoxlabs_get_certificate_detail(discovery_factory, mock_response):
    mock_response.add(
        method=responses.POST,
        url="https://octoxlabs.service:8443/api/token/token",
        body=json.dumps({"access": "api-token"}),
    )

    octoxlabs = OctoxLabs(ip="octoxlabs.service", token="octoxlabs")
    mock_response.add(
        method=responses.POST,
        url="https://octoxlabs.service:8443/certificates/certificates/certificate-id",
        body=json.dumps({"CertificateType": "client_certificate", "Name": "cf-1234aabb"}),
    )
    discovery = discovery_factory.create()

    certificate = octoxlabs.get_certificate_detail(certificate_id="certificate-id", discovery=discovery)
    assert certificate["Name"] == "cf-1234aabb"
