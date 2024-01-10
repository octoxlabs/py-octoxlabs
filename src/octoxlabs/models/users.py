# Standard Library
from dataclasses import dataclass
from typing import Dict, List, Union, Optional

# Octoxlabs
from octoxlabs.service import OctoxLabsService


@dataclass
class User:
    id: int
    email: str
    username: str
    name: str
    first_name: str
    last_name: str
    is_active: bool
    is_ldap: bool
    groups: List[Dict[str, Union[int, str]]]

    service: Optional[OctoxLabsService] = None

    def __str__(self):
        return f"<{self.username}>"


@dataclass
class Group:
    id: int
    name: str
    users_count: int

    service: Optional[OctoxLabsService] = None


@dataclass
class Permission:
    id: int
    name: str
    app: str

    service: Optional[OctoxLabsService] = None
