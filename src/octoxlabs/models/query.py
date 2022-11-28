# Standard Library
from datetime import datetime
from dataclasses import dataclass
from typing import List, Optional

# Octoxlabs
from octoxlabs.service import OctoxLabsService
from octoxlabs.utils import parse_string_datetime
from octoxlabs.constants.paths import query_detail_path


@dataclass
class Query:
    id: int
    name: str
    text: str
    tags: List[str]
    count: int
    is_public: bool
    created_at: str
    updated_at: str
    username: str
    is_temporary: bool

    service: Optional[OctoxLabsService] = None

    def add_tag(self, tag: str) -> List[str]:
        if tag not in self.tags:
            self.tags.append(tag)
            self.service.request_builder(
                method="PATCH", path=query_detail_path(query_id=self.id), json={"tags": self.tags}
            ).json()
        return self.tags

    def save(self):
        self.service.request_builder(
            method="PUT",
            path=query_detail_path(query_id=self.id),
            json={"name": self.name, "text": self.text, "tags": self.tags},
        ).json()

    @property
    def parsed_created_at(self) -> datetime:
        return parse_string_datetime(string=self.created_at)

    @property
    def parsed_updated_at(self) -> datetime:
        return parse_string_datetime(string=self.updated_at)
