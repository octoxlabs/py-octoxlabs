# Octoxlabs
from octoxlabs.models.companies import Domain, Company


class CompanyFactory:
    @staticmethod
    def create(
        id=1,
        name="Octoxlabs",
        domain="localhost",
        is_active=True,
        service=None,
    ):
        return Company(
            id=id,
            name=name,
            domain=domain,
            is_active=is_active,
            service=service,
        )


class DomainFactory:
    @staticmethod
    def create(
        id=1,
        tenant=1,
        domain="localhost",
        tenant_name="Octoxlabs",
        service=None,
    ):
        return Domain(
            id=id,
            domain=domain,
            tenant=tenant,
            tenant_name=tenant_name,
            service=service,
        )
