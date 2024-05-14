# Standard Library
from typing import Any, Dict, List, Tuple, Union

# Local Folder
from .models.query import Query
from .service import OctoxLabsService
from .models.discovery import Discovery
from .models.companies import Domain, Company
from .models.adapter import Adapter, Connection
from .models.users import User, Group, Permission
from .exceptions import NotFound, CantCreate, CantDelete, CantUpdate, NoDiscoveryError
from .constants.paths import (
    users_path,
    groups_path,
    domains_path,
    queries_path,
    adapters_path,
    companies_path,
    ping_pong_path,
    connections_path,
    discoveries_path,
    permissions_path,
    user_detail_path,
    group_detail_path,
    query_detail_path,
    device_detail_path,
    device_search_path,
    domain_detail_path,
    company_detail_path,
    last_discovery_path,
    connection_detail_path,
)


class OctoxLabs:
    service: OctoxLabsService

    def __init__(self, ip: str, token: str):
        self.service = OctoxLabsService(ip=ip, token=token)

    def ping(self):
        response = self.service.request_builder(path=ping_pong_path()).json()
        if response.get("pong", None) == "ok":
            return True
        return False

    def get_adapters(self, search: str = "", size: int = 100, page: int = 1) -> Tuple[int, List[Adapter]]:
        adapters_data = self.service.request_builder(
            path=adapters_path(), params={"search": search, "size": size, "page": page}
        ).json()
        return adapters_data.get("count"), [
            Adapter(
                id=adapter.get("id"),
                name=adapter.get("name"),
                slug=adapter.get("slug"),
                description=adapter.get("description"),
                groups=adapter.get("groups"),
                beta=adapter.get("beta"),
                status=adapter.get("status"),
                service=self.service,
            )
            for adapter in adapters_data.get("results", [])
        ]

    def get_connections(
        self, adapter: Adapter = None, adapter_id: int = None, page: int = 1, search: str = "", size: int = 20
    ) -> Tuple[int, List[Connection]]:
        filters = {"adapter": adapter.id if adapter else adapter_id, "page": page, "search": search, "size": size}
        connections_data = self.service.request_builder(path=connections_path(), params=filters).json()
        return connections_data.get("count"), [
            Connection(
                id=connection.get("id"),
                adapter_id=connection.get("adapter"),
                adapter_name=connection.get("adapter_name"),
                name=connection.get("name"),
                status=connection.get("status"),
                description=connection.get("description"),
                enabled=connection.get("enabled"),
                service=self.service,
            )
            for connection in connections_data.get("results")
        ]

    def create_connection(
        self,
        adapter_id: int,
        connection_name: str,
        connection_description: str,
        connector_id: int,
        option_connections: List[Dict[str, Any]],
    ) -> Union[str, CantCreate]:
        payload = {
            "adapter": adapter_id,
            "name": connection_name,
            "description": connection_description,
            "connector": connector_id,
            "option_connections": option_connections,
        }

        try:
            connection = self.service.request_builder(method="POST", path=connections_path(), json=payload).json()
            return f"{connection.get('name')} connection created successfully"

        except Exception as e:
            return CantCreate(str(e))

    def delete_connection(self, connection_id: int) -> Union[str, CantDelete]:
        try:
            self.service.request_builder(method="DELETE", path=connection_detail_path(connection_id=connection_id))
            return "Connection deleted successfully."

        except Exception as e:
            return CantDelete(str(e))

    def get_discoveries(self, status: int = None, size: int = None, page: int = 1) -> Tuple[int, List[Discovery]]:
        filters = {"status": status, "size": size, "page": page}
        discoveries_data = self.service.request_builder(path=discoveries_path(), params=filters).json()
        return discoveries_data.get("count"), [
            Discovery(
                id=discovery.get("id"),
                start_time=discovery.get("start_time"),
                end_time=discovery.get("end_time"),
                status=discovery.get("status"),
                progress=discovery.get("progress"),
            )
            for discovery in discoveries_data.get("results")
        ]

    def get_last_discovery(self) -> Discovery:
        data = self.service.request_builder(path=last_discovery_path()).json()
        if data.get("id", None):
            return Discovery(
                id=data.get("id"),
                start_time=data.get("start_time"),
                end_time=data.get("end_time"),
                status=data.get("status"),
                progress=data.get("progress"),
            )
        raise NoDiscoveryError("No discovery.")

    def search_devices(
        self,
        query: str = "",
        fields: List[str] = None,
        page: int = 1,
        size: int = 50,
        discovery_id: int = None,
        discovery: Discovery = None,
        ordering: List[Dict[str, str]] = None,  # [{"field": "Hostname", "order": "desc"}]
    ) -> Tuple[int, List[Dict[str, List[Any]]]]:
        payload = {
            "query": query,
            "fields": fields,
            "page": page,
            "size": size,
            "index_id": discovery.id if discovery else discovery_id or None,
            "ordering": ordering or [],
        }
        data = self.service.request_builder(method="POST", path=device_search_path(), json=payload).json()
        return data.get("count"), data.get("results")

    def get_device_detail(
        self, hostname: str, discovery: Discovery = None, discovery_id: int = None
    ) -> Dict[str, List[Any]]:
        payload = {"index_id": discovery.id if discovery else discovery_id or self.get_last_discovery().id}
        return self.service.request_builder(
            method="POST", path=device_detail_path(hostname=hostname), json=payload
        ).json()

    def get_queries(self, page: int = 1, search: str = "", size: int = 20) -> Tuple[int, List[Query]]:
        payload = {"page": page, "search": search, "size": size}
        queries_data = self.service.request_builder(path=queries_path(), params=payload).json()
        return queries_data.get("count"), [
            Query(
                id=query.get("id"),
                name=query.get("name"),
                text=query.get("text"),
                tags=query.get("tags"),
                count=query.get("count"),
                is_public=query.get("is_public"),
                created_at=query.get("created_at"),
                updated_at=query.get("updated_at"),
                username=query.get("user_full_name"),
                is_temporary=query.get("temporary"),
                service=self.service,
            )
            for query in queries_data.get("results")
        ]

    def create_query(
        self, query_name: str, query_text: str, is_public: bool, tags: List[int] = None
    ) -> Union[str, CantCreate]:
        payload = {
            "name": query_name,
            "text": query_text,
            "is_public": is_public,
        }
        if tags:
            payload["tags"] = tags

        try:
            query = self.service.request_builder(method="POST", path=queries_path(), json=payload).json()
            return f"{query.get('name')} query created successfully"

        except Exception as e:
            return CantCreate(str(e))

    def update_query(
        self, query_id: str, query_name: str, query_text: str, is_public: bool = None, tags: List[int] = None
    ) -> Union[str, CantUpdate]:
        payload = {"name": query_name, "text": query_text}

        if is_public:
            payload["is_public"] = is_public
        if tags:
            payload["tags"] = tags

        try:
            query = self.service.request_builder(
                method="PUT", path=query_detail_path(query_id=query_id), json=payload
            ).json()
            return f"{query.get('name')} query successfully updated."

        except Exception as e:
            return CantUpdate(str(e))

    def delete_query(self, query_id: str) -> Union[str, CantDelete]:
        try:
            self.service.request_builder(method="DELETE", path=query_detail_path(query_id=query_id))
            return "Query deleted successfully."

        except Exception as e:
            return CantDelete(str(e))

    def get_query_by_id(self, query_id: str) -> Query:
        query = self.service.request_builder(path=query_detail_path(query_id=query_id)).json()
        return Query(
            id=query.get("id"),
            name=query.get("name"),
            text=query.get("text"),
            tags=query.get("tags"),
            count=query.get("count"),
            is_public=query.get("is_public"),
            created_at=query.get("created_at"),
            updated_at=query.get("updated_at"),
            username=query.get("user_full_name"),
            is_temporary=query.get("temporary"),
            service=self.service,
        )

    def get_query_by_name(self, query_name: str) -> Query:
        _, queries = self.get_queries(search=query_name, size=1000)
        for query in queries:
            if query_name == query.name:
                return query
        raise NotFound("Query not found.")

    def get_companies(self, page: int = 1, search: str = "", size: int = 20) -> Tuple[int, List[Company]]:
        payload = {"page": page, "search": search, "size": size}
        companies_data = self.service.request_builder(path=companies_path(), params=payload).json()

        return companies_data.get("count"), [
            Company(
                id=company.get("id"),
                name=company.get("name"),
                domain=company.get("domain"),
                is_active=company.get("is_active"),
                service=self.service,
            )
            for company in companies_data.get("results")
        ]

    def create_company(self, company_name: str) -> Union[str, CantCreate]:
        payload = {"name": company_name}
        try:
            company = self.service.request_builder(method="POST", path=companies_path(), json=payload).json()
            return f"{company.get('name')} company created successfully"

        except Exception as e:
            return CantCreate(str(e))

    def update_company(self, company_id: int, company_name: str) -> Union[str, CantUpdate]:
        payload = {"name": company_name}

        try:
            company = self.service.request_builder(
                method="PUT", path=company_detail_path(company_id=company_id), json=payload
            ).json()
            return f"{company.get('name')} company successfully renamed."

        except Exception as e:
            return CantUpdate(str(e))

    def delete_company(self, company_id: int) -> Union[str, CantDelete]:
        try:
            self.service.request_builder(method="DELETE", path=company_detail_path(company_id=company_id))
            return "Company deleted successfully."

        except Exception as e:
            return CantDelete(str(e))

    def get_company_by_id(self, company_id: int) -> Company:
        company = self.service.request_builder(path=company_detail_path(company_id=company_id)).json()
        return Company(
            id=company.get("id"),
            name=company.get("name"),
            domain=company.get("domain"),
            is_active=company.get("is_active"),
            service=self.service,
        )

    def get_company_by_name(self, company_name: str) -> Company:
        _, companies = self.get_companies(search=company_name, size=1000)
        for company in companies:
            if company_name == company.name:
                return company
        raise NotFound("Company not found.")

    def get_domains(self, page: int = 1, search: str = "", size: int = 20) -> Tuple[int, List[Domain]]:
        payload = {"page": page, "search": search, "size": size}
        domains_data = self.service.request_builder(path=domains_path(), params=payload).json()

        return domains_data.get("count"), [
            Domain(
                id=domain.get("id"),
                domain=domain.get("domain"),
                tenant=domain.get("tenant"),
                tenant_name=domain.get("tenant_name"),
                service=self.service,
            )
            for domain in domains_data.get("results")
        ]

    def create_domain(self, domain_name: str, company_id: int) -> Union[str, CantCreate]:
        payload = {"domain": domain_name, "tenant": company_id}
        try:
            domain = self.service.request_builder(method="POST", path=domains_path(), json=payload).json()
            return f"{domain.get('domain')} domain created successfully"

        except Exception as e:
            return CantCreate(str(e))

    def update_domain(
        self, domain_id: int, company_id: int, domain_name: str, is_primary: bool = None
    ) -> Union[str, CantUpdate]:
        payload = {"domain": domain_name, "tenant": company_id}

        if is_primary:
            payload["is_primary"] = is_primary
        try:
            domain = self.service.request_builder(
                method="PUT", path=domain_detail_path(domain_id=domain_id), json=payload
            ).json()
            return f"{domain.get('domain')} domain successfully updated."

        except Exception as e:
            return CantUpdate(str(e))

    def delete_domain(self, domain_id: int) -> Union[str, CantDelete]:
        try:
            self.service.request_builder(method="DELETE", path=domain_detail_path(domain_id=domain_id))
            return "Domain deleted successfully."

        except Exception as e:
            return CantDelete(str(e))

    def get_domain_by_id(self, domain_id: int) -> Domain:
        domain = self.service.request_builder(path=domain_detail_path(domain_id=domain_id)).json()
        return Domain(
            id=domain.get("id"),
            domain=domain.get("domain"),
            tenant=domain.get("tenant"),
            tenant_name=domain.get("tenant_name"),
            service=self.service,
        )

    def get_domains_by_domain_name(self, domain_name: str) -> Domain:
        _, domains = self.get_domains(search=domain_name, size=1000)

        for domain in domains:
            if domain_name == domain.domain:
                return domain

        raise NotFound("Domain not found.")

    def get_users(self, page: int = 1, search: str = "", size: int = 20) -> Tuple[int, List[User]]:
        payload = {"page": page, "search": search, "size": size}
        users_data = self.service.request_builder(path=users_path(), params=payload).json()
        return users_data.get("count"), [
            User(
                id=user.get("id"),
                name=user.get("name"),
                email=user.get("email"),
                username=user.get("username"),
                first_name=user.get("first_name"),
                last_name=user.get("last_name"),
                is_active=user.get("is_active"),
                is_ldap=user.get("is_ldap"),
                groups=user.get("groups"),
                service=self.service,
            )
            for user in users_data.get("results")
        ]

    def create_user(
        self, email: str, username: str, first_name: str, last_name: str, group_ids: List[int]
    ) -> Union[str, CantCreate]:
        payload = {
            "email": email,
            "username": username,
            "first_name": first_name,
            "last_name": last_name,
            "group_ids": group_ids,
        }
        try:
            user = self.service.request_builder(method="POST", path=users_path(), json=payload).json()
            return f"{user.get('username')} user created successfully"

        except Exception as e:
            return CantCreate(str(e))

    def update_user(
        self,
        user_id: int,
        username: str,
        email: str = None,
        first_name: str = None,
        last_name: str = None,
        group_ids: List[int] = None,
    ) -> Union[str, CantUpdate]:
        payload = {"username": username}

        if email:
            payload["email"] = email
        if first_name:
            payload["first_name"] = first_name
        if last_name:
            payload["last_name"] = last_name
        if group_ids:
            payload["group_ids"] = group_ids

        try:
            user = self.service.request_builder(
                method="PUT", path=user_detail_path(user_id=user_id), json=payload
            ).json()
            return f"{user.get('username')} user successfully renamed."

        except Exception as e:
            return CantUpdate(str(e))

    def delete_user(self, user_id: int) -> Union[str, CantDelete]:
        try:
            self.service.request_builder(method="DELETE", path=user_detail_path(user_id=user_id))
            return "User deleted successfully."

        except Exception as e:
            return CantDelete(str(e))

    def get_user_by_id(self, user_id: int) -> User:
        user = self.service.request_builder(path=user_detail_path(user_id=user_id)).json()
        return User(
            id=user.get("id"),
            name=user.get("name"),
            email=user.get("email"),
            username=user.get("username"),
            first_name=user.get("first_name"),
            last_name=user.get("last_name"),
            is_active=user.get("is_active"),
            is_ldap=user.get("is_ldap"),
            groups=user.get("groups"),
            service=self.service,
        )

    def get_user_by_username(self, username: str) -> User:
        _, users = self.get_users(search=username, size=1000)
        for user in users:
            if username == user.username:
                return user
        raise NotFound("User not found.")

    def get_groups(self, page: int = 1, search: str = "", size: int = 20) -> Tuple[int, List[Group]]:
        payload = {"page": page, "search": search, "size": size}
        groups_data = self.service.request_builder(path=groups_path(), params=payload).json()
        return groups_data.get("count"), [
            Group(
                id=group.get("id"),
                name=group.get("name"),
                users_count=group.get("user_count"),
                service=self.service,
            )
            for group in groups_data.get("results")
        ]

    def get_permissions(self, page: int = 1, search: str = "", size: int = 20) -> Tuple[int, List[Permission]]:
        payload = {"page": page, "search": search, "size": size}
        permissions_data = self.service.request_builder(path=permissions_path(), params=payload).json()
        return permissions_data.get("count"), [
            Permission(
                id=permission.get("id"),
                name=permission.get("name"),
                app=permission.get("app"),
                service=self.service,
            )
            for permission in permissions_data.get("results")
        ]

    def create_group(self, group_name: str, permissions: List[int]):
        payload = {"name": group_name, "permissions": permissions}
        try:
            group = self.service.request_builder(method="POST", path=groups_path(), json=payload).json()
            return f"{group.get('name')} group created successfully"

        except Exception as e:
            return CantCreate(str(e))

    def update_group(
        self,
        group_id: int,
        group_name: str,
        permissions: List[int] = None,
        user_ids: List[int] = None,
        adapter_ids: List[int] = None,
    ) -> Union[str, CantUpdate]:
        payload = {"name": group_name}

        if adapter_ids:
            payload["adapter_ids"] = adapter_ids
        if permissions:
            payload["permissions"] = permissions
        if user_ids:
            payload["user_ids"] = user_ids

        try:
            group = self.service.request_builder(
                method="PUT", path=group_detail_path(group_id=group_id), json=payload
            ).json()
            return f"{group.get('name')} group successfully updated."

        except Exception as e:
            return CantUpdate(str(e))

    def delete_group(self, group_id: int) -> Union[str, CantDelete]:
        try:
            self.service.request_builder(method="DELETE", path=group_detail_path(group_id=group_id))
            return "Group deleted successfully."

        except Exception as e:
            return CantDelete(str(e))
