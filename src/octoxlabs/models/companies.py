# Standard Library
from typing import Optional
from dataclasses import dataclass

# Octoxlabs
from octoxlabs.service import OctoxLabsService


@dataclass
class Company:
    id: int
    name: str
    domain: str
    is_active: bool

    service: Optional[OctoxLabsService] = None


@dataclass
class Domain:
    id: int
    domain: str
    tenant: int
    tenant_name: str

    service: Optional[OctoxLabsService] = None

    def __str__(self):
        return f"<{self.tenant_name}/{self.domain}>"


class CompanyAdmin:
    company = str
    original_user = str
    related_user_id = int

    service: Optional[OctoxLabsService] = None

    def __str__(self):
        return f"{self.company}/{self.original_user}"
