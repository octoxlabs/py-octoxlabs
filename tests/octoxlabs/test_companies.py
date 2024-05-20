# Standard Library
import json

# Third Party
import pytest
import responses

# Octoxlabs
from octoxlabs.exceptions import NotFound


def test_octoxlabs_get_companies(mock_response, octoxlabs_client):
    octoxlabs = octoxlabs_client

    mock_response.add(
        method=responses.GET,
        url="https://octoxlabs.service:8443/companies/companies",
        body=json.dumps(
            {
                "count": 1,
                "results": [
                    {"id": 1, "name": "Octoxlabs", "is_constant": True, "domain": "localhost", "is_active": True}
                ],
            }
        ),
    )

    count, companies = octoxlabs.get_companies()
    assert count == 1
    assert companies[0].name == "Octoxlabs"


def test_octoxlabs_create_company(mock_response, octoxlabs_client):
    octoxlabs = octoxlabs_client

    mock_response.add(
        method=responses.POST,
        url="https://octoxlabs.service:8443/companies/companies",
        body=json.dumps({"name": "Octoxlabs"}),
    )

    company_message = octoxlabs.create_company(company_name="Octoxlabs")

    assert company_message == "Octoxlabs company created successfully"


def test_octoxlabs_update_company(mock_response, octoxlabs_client):
    octoxlabs = octoxlabs_client

    mock_response.add(
        method=responses.PUT,
        url="https://octoxlabs.service:8443/companies/companies/1",
        body=json.dumps({"id": 1, "name": "Octoxlabs", "is_constant": True, "domain": "localhost", "is_active": True}),
    )
    update_message = octoxlabs.update_company(company_id=1, company_name="Octoxlabs")

    assert update_message == "Octoxlabs company successfully renamed."


def test_octoxlabs_delete_company(mock_response, octoxlabs_client):
    octoxlabs = octoxlabs_client

    mock_response.add(
        method=responses.DELETE,
        url="https://octoxlabs.service:8443/companies/companies/1",
    )
    delete_message = octoxlabs.delete_company(company_id=1)
    assert delete_message == "Company deleted successfully."


def test_octoxlabs_company_by_id(mock_response, octoxlabs_client):
    octoxlabs = octoxlabs_client

    mock_response.add(
        method=responses.GET,
        url="https://octoxlabs.service:8443/companies/companies/1",
        body=json.dumps({"id": 1, "name": "Octoxlabs", "is_constant": True, "domain": "localhost", "is_active": True}),
    )

    company = octoxlabs.get_company_by_id(company_id=1)

    assert company.id == 1


def test_octoxlabs_get_company_by_name(mock_response, company_factory, octoxlabs_client):
    octoxlabs = octoxlabs_client

    mock_response.add(
        method=responses.GET,
        url="https://octoxlabs.service:8443/companies/companies",
        body=json.dumps(
            {
                "count": 1,
                "results": [
                    {"id": 1, "name": "Octoxlabs", "is_constant": True, "domain": "localhost", "is_active": True}
                ],
            }
        ),
    )

    company = octoxlabs.get_company_by_name(company_name="Octoxlabs")

    assert company.id == 1

    mock_response.add(
        method=responses.GET,
        url="https://octoxlabs.service:8443/companies/companies",
        body=json.dumps(
            {
                "count": 0,
                "results": [],
            }
        ),
    )

    with pytest.raises(NotFound):
        octoxlabs.get_company_by_name(company_name="test")


def test_octoxlabs_get_domains(mock_response, octoxlabs_client):
    octoxlabs = octoxlabs_client

    mock_response.add(
        method=responses.GET,
        url="https://octoxlabs.service:8443/companies/domains",
        body=json.dumps(
            {
                "count": 1,
                "results": [
                    {"id": 1, "domain": "localhost", "tenant": 1, "is_primary": True, "tenant_name": "Octoxlabs"}
                ],
            }
        ),
    )

    count, domains = octoxlabs.get_domains()

    assert count == 1
    assert domains[0].tenant_name == "Octoxlabs"


def test_octoxlabs_create_domain(mock_response, octoxlabs_client):
    octoxlabs = octoxlabs_client

    mock_response.add(
        method=responses.POST,
        url="https://octoxlabs.service:8443/companies/domains",
        body=json.dumps(
            {
                "domain": "localhost",
                "tenant": 1,
                "is_primary": True,
            }
        ),
    )
    create_message = octoxlabs.create_domain(domain_name="localhost", company_id=1)

    assert create_message == "localhost domain created successfully"


def test_octoxlabs_update_domain(mock_response, octoxlabs_client):
    octoxlabs = octoxlabs_client

    mock_response.add(
        method=responses.PUT,
        url="https://octoxlabs.service:8443/companies/domains/1",
        body=json.dumps(
            {
                "domain": "localhost",
                "tenant": 1,
                "is_primary": True,
            }
        ),
    )

    update_message = octoxlabs.update_domain(domain_name="localhost", company_id=1, domain_id=1, is_primary=False)

    assert update_message == "localhost domain successfully updated."


def test_octoxlabs_delete_domain(mock_response, octoxlabs_client):
    octoxlabs = octoxlabs_client

    mock_response.add(method=responses.DELETE, url="https://octoxlabs.service:8443/companies/domains/1")

    delete_message = octoxlabs.delete_domain(domain_id=1)

    assert delete_message == "Domain deleted successfully."


def test_octoxlabs_domains_by_id(mock_response, octoxlabs_client):
    octoxlabs = octoxlabs_client

    mock_response.add(
        method=responses.GET,
        url="https://octoxlabs.service:8443/companies/domains/1",
        body=json.dumps({"id": 1, "domain": "localhost", "tenant": 1, "is_primary": True, "tenant_name": "Octoxlabs"}),
    )

    domain = octoxlabs.get_domain_by_id(domain_id=1)

    assert domain.id == 1


def test_octoxlabs_domains_by_domain_name(mock_response, octoxlabs_client):
    octoxlabs = octoxlabs_client

    mock_response.add(
        method=responses.GET,
        url="https://octoxlabs.service:8443/companies/domains",
        body=json.dumps(
            {
                "count": 1,
                "results": [
                    {"id": 1, "domain": "localhost", "tenant": 1, "is_primary": True, "tenant_name": "Octoxlabs"}
                ],
            }
        ),
    )

    domain = octoxlabs.get_domains_by_domain_name(domain_name="localhost")

    assert domain.id == 1

    mock_response.add(
        method=responses.GET,
        url="https://octoxlabs.service:8443/companies/domains",
        body=json.dumps(
            {
                "count": 0,
                "results": [],
            }
        ),
    )

    with pytest.raises(NotFound):
        octoxlabs.get_domains_by_domain_name(domain_name="test")
