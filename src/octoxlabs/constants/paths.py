def adapters_path(adapter_id: int = None) -> str:
    if adapter_id:
        return f"/adapters/adapters/{adapter_id}"
    return "/adapters/adapters"


def connections_path() -> str:
    return "/adapters/connections"


def connection_detail_path(connection_id: int) -> str:
    return f"/adapters/connections/{connection_id}"


def connection_test_path(connection_id: int) -> str:
    return f"/adapters/test/{connection_id}"


def discoveries_path() -> str:
    return "/discoveries/discoveries"


def last_discovery_path() -> str:
    return "/discoveries/last"


def device_search_path() -> str:
    return "/devices/devices"


def device_detail_path(hostname: str) -> str:
    return f"/devices/devices/{hostname}"


def queries_path() -> str:
    return "/queries/queries"


def query_detail_path(query_id: str) -> str:
    return f"/queries/queries/{query_id}"


def ping_pong_path() -> str:
    return "/api/ping"


def companies_path() -> str:
    return "/companies/companies"


def company_detail_path(company_id: int) -> str:
    return f"/companies/companies/{company_id}"


def domains_path() -> str:
    return "/companies/domains"


def domain_detail_path(domain_id: int) -> str:
    return f"/companies/domains/{domain_id}"


def users_path() -> str:
    return "/users/users"


def user_detail_path(user_id: int) -> str:
    return f"/users/users/{user_id}"


def groups_path() -> str:
    return "/users/groups"


def group_detail_path(group_id: int) -> str:
    return f"/users/groups/{group_id}"


def permissions_path() -> str:
    return "/users/permissions"


def access_token_path() -> str:
    return "/api/token/token"
