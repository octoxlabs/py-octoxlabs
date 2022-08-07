# Standard Library
import json

# Third Party
import responses

# Octoxlabs
from octoxlabs import OctoxLabs
from octoxlabs.utils import parse_string_datetime


def test_octoxlabs_search_assets(mock_response):
    octoxlabs = OctoxLabs(ip="octoxlabs.service", token="octoxlabs")
    mock_response.add(
        method=responses.POST,
        url="https://octoxlabs.service:8043/assets/assets",
        body=json.dumps(
            {
                "count": 300,
                "results": [
                    {
                        "IpAddresses": ["127.0.0.1"],
                        "Category": ["Server"],
                        "FirstFetchTime": ["2022-05-17T16:05:24.991Z"],
                        "Adapters": ["imperva-dam", "falcon-crowdstrike", "fireeye-hx"],
                        "Hostname": ["octoxlabs01"],
                        "OS.Type": ["Linux"],
                        "Domain": ["octoxlabs.com"],
                    }
                ],
            }
        ),
    )

    count, assets = octoxlabs.search_assets()
    asset = assets[0]

    assert count == 300
    assert asset["IpAddresses"] == ["127.0.0.1"]

    parsed_first_fetch_time = parse_string_datetime(string=asset["FirstFetchTime"][0])
    assert parsed_first_fetch_time.year == 2022


def test_octoxlabs_get_asset_detail(discovery_factory, mock_response):
    octoxlabs = OctoxLabs(ip="octoxlabs.service", token="octoxlabs")
    mock_response.add(
        method=responses.POST,
        url="https://octoxlabs.service:8043/assets/assets/octoxlabs01",
        body=json.dumps(
            {
                "IpAddresses": ["127.0.0.1"],
                "Category": ["Server"],
                "FirstFetchTime": ["2022-05-17T16:05:24.991Z"],
                "Adapters": ["imperva-dam", "falcon-crowdstrike", "fireeye-hx"],
                "Hostname": ["octoxlabs01"],
                "OS.Type": ["Linux"],
                "Domain": ["octoxlabs.com"],
            }
        ),
    )
    discovery = discovery_factory.create()

    asset = octoxlabs.get_asset_detail(hostname="octoxlabs01", discovery=discovery)
    assert asset["IpAddresses"] == ["127.0.0.1"]
