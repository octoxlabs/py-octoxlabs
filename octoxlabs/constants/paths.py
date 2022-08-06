def adapters_path(adapter_id: int = None) -> str:
    if adapter_id:
        return f"/adapters/adapters/{adapter_id}"
    return "/adapters/adapters"


def connections_path():
    return "/adapters/connections"


def connection_test_path(connection_id: int) -> str:
    return f"/adapters/test/{connection_id}"
