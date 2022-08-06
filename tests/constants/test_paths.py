# Octoxlabs
from octoxlabs.constants.paths import adapters_path, connections_path, connection_test_path


def test_adapters_path():
    assert adapters_path() == "/adapters/adapters"
    assert adapters_path(adapter_id=1) == "/adapters/adapters/1"


def test_connections_path():
    assert connections_path() == "/adapters/connections"


def test_connection_test_path():
    assert connection_test_path(connection_id=1) == "/adapters/test/1"
