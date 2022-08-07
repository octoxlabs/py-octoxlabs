def adapters_path(adapter_id: int = None) -> str:
    if adapter_id:
        return f"/adapters/adapters/{adapter_id}"
    return "/adapters/adapters"


def connections_path() -> str:
    return "/adapters/connections"


def connection_test_path(connection_id: int) -> str:
    return f"/adapters/test/{connection_id}"


def discoveries_path() -> str:
    return "/discoveries/discoveries"


def last_discovery_path() -> str:
    return "/discoveries/last"


def asset_search_path() -> str:
    return "/assets/assets"


def asset_detail_path(hostname: str) -> str:
    return f"/assets/assets/{hostname}"
