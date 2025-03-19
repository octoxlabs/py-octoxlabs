# Standard Library
from dataclasses import dataclass
from typing import Any, Dict, List, Union, Optional

# Octoxlabs
from octoxlabs.models.users import Group
from octoxlabs.service import OctoxLabsService


@dataclass
class Dashboard:
    id: int
    name: str
    description: str
    is_public: bool
    hr_groups: List[Group]

    service: Optional[OctoxLabsService] = None


@dataclass
class Chart:
    id: int
    name: str
    description: str
    dashboard_name: str
    group_by_data: List[Dict[str, Any]]
    group_by_query: str
    group_by_query_name: str
    rows: List[Dict[str, Union[str, int]]]
