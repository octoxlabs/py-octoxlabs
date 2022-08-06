# Octoxlabs
from octoxlabs.models.adapter import Adapter, Connection


class AdapterFactory:
    @staticmethod
    def create(
        id=1,
        name="Octox Labs",
        slug="octoxlabs",
        description="octoxlabs",
        groups=["CS"],
        beta=True,
        status=1,
        service=None,
    ):
        return Adapter(
            id=id,
            name=name,
            slug=slug,
            description=description,
            groups=groups,
            beta=beta,
            status=status,
            service=service,
        )


class ConnectionFactory:
    @staticmethod
    def create(
        id=1,
        adapter_id=1,
        adapter_name="octoxlabs",
        name="octoxlabs",
        status=True,
        description="octoxlabs connection",
        enabled=True,
        service=None,
    ):
        return Connection(
            id=id,
            adapter_id=adapter_id,
            adapter_name=adapter_name,
            name=name,
            status=status,
            description=description,
            enabled=enabled,
            service=service,
        )
