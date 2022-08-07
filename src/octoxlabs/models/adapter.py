# Standard Library
from dataclasses import dataclass
from typing import Dict, List, Tuple, Union, Optional

# Octoxlabs
from octoxlabs.service import OctoxLabsService
from octoxlabs.constants.paths import adapters_path, connections_path, connection_test_path

ADAPTER_STATUSES = {
    1: "Done",
    2: "Warning",
    3: "Error",
    4: "None",
}


@dataclass
class Adapter:
    id: int
    name: str
    slug: str
    description: str
    groups: List[str]
    beta: bool
    status: int

    service: Optional[OctoxLabsService] = None

    def get_connections(self) -> Tuple[int, List["Connection"]]:
        connections_data = self.service.request_builder(path=connections_path(), params={"adapter": self.id}).json()
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

    @property
    def hr_status(self) -> str:
        return ADAPTER_STATUSES.get(self.status)

    def __str__(self):
        return f"<Adapter: {self.id}/{self.name}>"


@dataclass
class Connection:
    id: int
    adapter_id: int
    adapter_name: str
    name: str
    status: bool
    description: str
    enabled: bool

    service: OctoxLabsService

    def get_adapter(self) -> Adapter:
        adapter = self.service.request_builder(path=adapters_path(adapter_id=self.adapter_id)).json()
        return Adapter(
            id=adapter.get("id"),
            name=adapter.get("name"),
            slug=adapter.get("slug"),
            description=adapter.get("description"),
            groups=adapter.get("groups"),
            beta=adapter.get("beta"),
            status=adapter.get("status"),
            service=self.service,
        )

    def connection_test(self) -> Dict[str, Union[int, Dict[str, str]]]:
        return self.service.request_builder(
            method="POST", path=connection_test_path(connection_id=self.id), json={}
        ).json()
