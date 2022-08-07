# Standard Library
from typing import Any, Dict, List, Tuple

# Local Folder
from .service import OctoxLabsService
from .models.discovery import Discovery
from .exceptions import NoDiscoveryError
from .models.adapter import Adapter, Connection
from .constants.paths import (
    adapters_path,
    connections_path,
    discoveries_path,
    asset_detail_path,
    asset_search_path,
    last_discovery_path,
)


class OctoxLabs:
    service: OctoxLabsService

    def __init__(self, ip: str, token: str):
        self.service = OctoxLabsService(ip=ip, token=token)

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

    def search_assets(
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
        data = self.service.request_builder(method="POST", path=asset_search_path(), json=payload).json()
        return data.get("count"), data.get("results")

    def get_asset_detail(
        self, hostname: str, discovery: Discovery = None, discovery_id: int = None
    ) -> Dict[str, List[Any]]:
        payload = {"index_id": discovery.id if discovery else discovery_id or self.get_last_discovery().id}
        return self.service.request_builder(
            method="POST", path=asset_detail_path(hostname=hostname), json=payload
        ).json()
