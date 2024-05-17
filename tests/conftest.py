# Standard Library
import json

# Third Party
import pytest
import responses

# Octoxlabs
from octoxlabs.service import OctoxLabsService

# Tests
from tests.factories.discovery_factory import DiscoveryFactory
from tests.factories.adapter_factory import AdapterFactory, ConnectionFactory


@pytest.fixture()
def mock_response():
    with responses.RequestsMock() as rsps:
        yield rsps


@pytest.fixture()
def octoxlabs_service(mock_response):
    mock_response.add(
        method=responses.POST,
        url="https://octoxlabs.test:8443/api/token/token",
        body=json.dumps({"access": "api-token"}),
    )
    return OctoxLabsService(ip="octoxlabs.test", token="octoxlabs")


@pytest.fixture()
def adapter_factory():
    return AdapterFactory


@pytest.fixture()
def connection_factory():
    return ConnectionFactory


@pytest.fixture()
def discovery_factory():
    return DiscoveryFactory
