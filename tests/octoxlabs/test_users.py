# Standard Library
import json

# Third Party
import responses
import pytest

# Octoxlabs
from octoxlabs.exceptions import NotFound


def test_octoxlabs_get_users(mock_response, octoxlabs_client):
    octoxlabs = octoxlabs_client

    mock_response.add(
        method=responses.GET,
        url="https://octoxlabs.service:8443/users/users",
        body=json.dumps(
            {
                "count": 1,
                "results": [
                    {
                        "id": 1,
                        "email": "",
                        "username": "octoxlabs",
                        "name": "Test OctoxLabs",
                        "first_name": "Octo",
                        "last_name": "Test",
                        "is_active": True,
                        "is_ldap": False,
                        "groups": [],
                    }
                ],
            }
        ),
    )

    count, users = octoxlabs.get_users()

    assert count == 1
    assert users[0].username == "octoxlabs"


def test_octoxlabs_get_user_by_id(mock_response, octoxlabs_client):
    octoxlabs = octoxlabs_client

    mock_response.add(
        method=responses.GET,
        url="https://octoxlabs.service:8443/users/users/1",
        body=json.dumps(
            {
                "id": 1,
                "email": "",
                "username": "octoxlabs",
                "name": "Test OctoxLabs",
                "first_name": "Octo",
                "last_name": "Test",
                "is_active": True,
                "is_ldap": False,
                "groups": [],
            }
        ),
    )

    user = octoxlabs.get_user_by_id(user_id=1)

    assert user.id == 1


def test_octoxlabs_get_user_by_username(mock_response, octoxlabs_client):
    octoxlabs = octoxlabs_client

    mock_response.add(
        method=responses.GET,
        url="https://octoxlabs.service:8443/users/users",
        body=json.dumps(
            {
                "count": 1,
                "results": [
                    {
                        "id": 1,
                        "email": "",
                        "username": "octoxlabs",
                        "name": "Test OctoxLabs",
                        "first_name": "Octo",
                        "last_name": "Test",
                        "is_active": True,
                        "is_ldap": False,
                        "groups": [],
                    }
                ],
            }
        ),
    )

    user = octoxlabs.get_user_by_username(username="octoxlabs")

    assert user.username == "octoxlabs"

    mock_response.add(
        method=responses.GET,
        url="https://octoxlabs.service:8443/users/users",
        body=json.dumps(
            {
                "count": 0,
                "results": [],
            }
        ),
    )

    with pytest.raises(NotFound):
        octoxlabs.get_user_by_username(username="test")


def test_octoxlabs_get_groups(mock_response, octoxlabs_client):
    octoxlabs = octoxlabs_client

    mock_response.add(
        method=responses.GET,
        url="https://octoxlabs.service:8443/users/groups",
        body=json.dumps({"count": 1, "results": [{"id": 1, "name": "Administrators", "user_count": 1}]}),
    )

    count, groups = octoxlabs.get_groups()

    assert count == 1
    assert groups[0].name == "Administrators"


def test_octoxlabs_get_permissions(mock_response, octoxlabs_client):
    octoxlabs = octoxlabs_client

    mock_response.add(
        method=responses.GET,
        url="https://octoxlabs.service:8443/users/permissions",
        body=json.dumps(
            {
                "count": 1,
                "results": [{"id": 1, "name": "Permission Name", "codename": "permission_name", "app": "permission"}],
            }
        ),
    )

    count, permissions = octoxlabs.get_permissions()

    assert count == 1
    assert permissions[0].app == "permission"