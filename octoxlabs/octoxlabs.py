# Standard Library
from typing import List

# Local Folder
from .service import OctoxLabsService
from .models.adapter import Adapter, Connection
from .constants.paths import adapters_path, connections_path


class OctoxLabs:
    service: OctoxLabsService

    def __init__(self, ip: str, token: str):
        self.service = OctoxLabsService(ip=ip, token=token)

    def get_adapters(self, search: str = "", size: int = 100) -> List[Adapter]:
        adapters_data = self.service.request_builder(
            path=adapters_path(), params={"search": search, "size": size}
        ).json()
        return [
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

    def get_connections(self, adapter: Adapter = None, adapter_id: int = None):
        filters = {"adapter": adapter.id if adapter else adapter_id}
        connections_data = self.service.request_builder(path=connections_path(), params=filters).json()
        return [
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
