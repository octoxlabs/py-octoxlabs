# Octoxlabs
from octoxlabs.models.users import User


class UserFactory:
    @staticmethod
    def create(
        id=1,
        name="Octoxlabs",
        email="user@octoxlabs.com",
        username="octoxlabs",
        first_name="octo",
        last_name="test",
        is_ldap=False,
        is_active=True,
        groups=None,
        service=None,
    ):
        return User(
            id=id,
            email=email,
            username=username,
            name=name,
            first_name=first_name,
            last_name=last_name,
            is_active=is_active,
            is_ldap=is_ldap,
            groups=groups,
            service=service,
        )
