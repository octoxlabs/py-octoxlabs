# Standard Library
import json

# Third Party
import pytest
import responses

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


def test_octoxlabs_create_user(mock_response, octoxlabs_client):
    octoxlabs = octoxlabs_client
    body = {
        "email": "test@octoxlabs.com",
        "username": "test",
        "first_name": "Octo",
        "last_name": "Test",
        "group_ids": [1, 2, 3],
    }
    mock_response.add(
        method=responses.POST,
        url="https://octoxlabs.service:8443/users/users",
        body=json.dumps(body),
    )

    create_message = octoxlabs.create_user(**body)

    assert create_message == "test user created successfully."


def test_octoxlabs_update_user(mock_response, octoxlabs_client):
    octoxlabs = octoxlabs_client
    body = {
        "email": "test@octoxlabs.com",
        "username": "test",
        "first_name": "Octo",
        "last_name": "Test",
        "group_ids": [1, 2, 3],
    }
    mock_response.add(
        method=responses.PUT,
        url="https://octoxlabs.service:8443/users/users/1",
        body=json.dumps(body),
    )

    update_message = octoxlabs.update_user(**body, user_id=1)

    assert update_message == "test user successfully renamed."


def test_octoxlabs_delete_user(mock_response, octoxlabs_client):
    octoxlabs = octoxlabs_client

    mock_response.add(method=responses.DELETE, url="https://octoxlabs.service:8443/users/users/1")
    delete_message = octoxlabs.delete_user(user_id=1)

    assert delete_message == "User deleted successfully."


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


def test_octoxlabs_create_group(mock_response, octoxlabs_client):
    octoxlabs = octoxlabs_client

    mock_response.add(
        method=responses.POST,
        url="https://octoxlabs.service:8443/users/groups",
        body=json.dumps({"id": 1, "name": "created-group"}),
    )
    create_message = octoxlabs.create_group(group_name="created-group", permissions=[1, 2, 3, 4])
    assert create_message == "created-group group created successfully."


def test_octoxlabs_update_group(mock_response, octoxlabs_client):
    octoxlabs = octoxlabs_client

    mock_response.add(
        method=responses.PUT,
        url="https://octoxlabs.service:8443/users/groups/1",
        body=json.dumps(
            {
                "id": 1,
                "name": "updated-group",
                "adapter_ids": [1, 2, 3],
                "permissions": [1, 2, 3],
                "user_ids": [1, 2, 3],
            }
        ),
    )
    update_message = octoxlabs.update_group(
        group_id=1, group_name="updated-group", permissions=[1, 2, 3], user_ids=[1, 2, 3], adapter_ids=[1, 2, 3]
    )
    assert update_message == "updated-group group successfully updated."


def test_octoxlabs_delete_group(mock_response, octoxlabs_client):
    octoxlabs = octoxlabs_client

    mock_response.add(method=responses.DELETE, url="https://octoxlabs.service:8443/users/groups/1")

    delete_message = octoxlabs.delete_group(group_id=1)
    assert delete_message == "Group deleted successfully."


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
