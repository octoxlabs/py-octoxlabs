# Standard Library
import json

# Third Party
import responses

# Octoxlabs
from octoxlabs import OctoxLabs
from octoxlabs.utils import parse_string_datetime


def test_octoxlabs_search_users(mock_response):
    mock_response.add(
        method=responses.POST,
        url="https://octoxlabs.service:8443/api/token/token",
        body=json.dumps({"access": "api-token"}),
    )
    octoxlabs = OctoxLabs(ip="octoxlabs.service", token="octoxlabs")
    mock_response.add(
        method=responses.POST,
        url="https://octoxlabs.service:8443/userinventory/users",
        body=json.dumps(
            {
                "count": 1,
                "results": [
                    {
                        "Username": ["octouser-1"],
                        "Adapters": ["active-directory"],
                        "LastLogOnTime": ["2024-10-21T00:00:00.000Z"],
                    }
                ],
            }
        ),
    )

    count, users = octoxlabs.search_users()
    user = users[0]

    assert count == 1
    assert user["Username"] == ["octouser-1"]

    parsed_first_fetch_time = parse_string_datetime(string=user["LastLogOnTime"][0])
    assert parsed_first_fetch_time.year == 2024


def test_octoxlabs_search_scroll_users(mock_response):
    mock_response.add(
        method=responses.POST,
        url="https://octoxlabs.service:8443/api/token/token",
        body=json.dumps({"access": "api-token"}),
    )
    octoxlabs = OctoxLabs(ip="octoxlabs.service", token="octoxlabs")
    mock_response.add(
        method=responses.POST,
        url="https://octoxlabs.service:8443/userinventory/users",
        body=json.dumps(
            {
                "count": 1,
                "scroll_id": "octoxlabs-scroll-id",
                "results": [
                    {
                        "Username": ["octouser-1"],
                        "Adapters": ["active-directory"],
                        "LastLogOnTime": ["2024-10-21T00:00:00.000Z"],
                    }
                ],
            }
        ),
    )
    count, scroll_id, users = octoxlabs.search_scroll_users()
    user = users[0]
    assert count == 1
    assert user["Username"] == ["octouser-1"]

    mock_response.add(
        method=responses.POST,
        url="https://octoxlabs.service:8443/userinventory/users",
        body=json.dumps(
            {
                "count": 1,
                "scroll_id": "octoxlabs-scroll-id",
                "results": [],
            }
        ),
    )

    count, scroll_id, assets = octoxlabs.search_scroll_users(scroll_id="octoxlabs-scroll-id")
    assert count == 1
    assert assets == []


def test_octoxlabs_get_user_inventory_detail(discovery_factory, mock_response):
    mock_response.add(
        method=responses.POST,
        url="https://octoxlabs.service:8443/api/token/token",
        body=json.dumps({"access": "api-token"}),
    )

    octoxlabs = OctoxLabs(ip="octoxlabs.service", token="octoxlabs")
    mock_response.add(
        method=responses.POST,
        url="https://octoxlabs.service:8443/userinventory/users/octouser-1",
        body=json.dumps(
            {
                "Username": "octouser-1",
                "Adapters": ["active-directory"],
                "LastLogOnTime": "2024-10-21T00:00:00.000Z",
            }
        ),
    )
    discovery = discovery_factory.create()

    user = octoxlabs.get_user_inventory_detail(username="octouser-1", discovery=discovery)
    assert user["Username"] == "octouser-1"
