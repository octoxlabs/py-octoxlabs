# Standard Library
import json

# Third Party
import responses


def test_octoxlabs_get_dashboards(mock_response, octoxlabs_client):
    octoxlabs = octoxlabs_client

    mock_response.add(
        method=responses.GET,
        url="https://octoxlabs.service:8443/dashboards/dashboards",
        body=json.dumps(
            {
                "count": 1,
                "results": [
                    {
                        "id": 1,
                        "name": "Dashboard",
                        "is_public": True,
                        "hr_groups": [],
                    }
                ],
            }
        ),
    )

    count, dashboards = octoxlabs.get_dashboards()
    assert count == 1
    assert dashboards[0].name == "Dashboard"


def test_octoxlabs_create_dashboard(mock_response, octoxlabs_client):
    octoxlabs = octoxlabs_client

    mock_response.add(
        method=responses.POST,
        url="https://octoxlabs.service:8443/dashboards/dashboards",
        body=json.dumps({"name": "TestBoard"}),
    )

    dashboard_message = octoxlabs.create_dashboard(dashboard_name="TestBoard")

    assert dashboard_message == "TestBoard dashboard created successfully."


def test_octoxlabs_update_dashboard(mock_response, octoxlabs_client):
    octoxlabs = octoxlabs_client

    mock_response.add(
        method=responses.PUT,
        url="https://octoxlabs.service:8443/dashboards/dashboards/1",
        body=json.dumps({"id": 1, "name": "TestBoard"}),
    )
    update_message = octoxlabs.update_dashboard(dashboard_id=1, dashboard_name="Octoxlabs")

    assert update_message == "TestBoard dashboard successfully updated."


def test_octoxlabs_delete_dashboard(mock_response, octoxlabs_client):
    octoxlabs = octoxlabs_client

    mock_response.add(
        method=responses.DELETE,
        url="https://octoxlabs.service:8443/dashboards/dashboards/1",
    )
    delete_message = octoxlabs.delete_dashboard(dashboard_id=1)
    assert delete_message == "Dashboard deleted successfully."


def test_octoxlabs_dashboard_by_id(mock_response, octoxlabs_client):
    octoxlabs = octoxlabs_client

    mock_response.add(
        method=responses.GET,
        url="https://octoxlabs.service:8443/dashboards/dashboards/1",
        body=json.dumps(
            {
                "id": 1,
                "name": "Dashboard",
                "is_public": True,
                "hr_groups": [],
            }
        ),
    )

    dashboard = octoxlabs.get_dashboard_by_id(dashboard_id=1)

    assert dashboard.id == 1


def test_octoxlabs_get_charts(mock_response, octoxlabs_client):
    octoxlabs = octoxlabs_client

    mock_response.add(
        method=responses.GET,
        url="https://octoxlabs.service:8443/dashboards/charts",
        body=json.dumps(
            {
                "count": 2,
                "results": [
                    {
                        "id": 1,
                        "name": "Chart",
                        "description": "",
                        "dashboard_name": "Dashboard",
                        "group_by_data": [],
                        "group_by_query": "Query-id",
                        "group_by_query_name": "Test Query",
                        "rows": [],
                    },
                    {
                        "id": 2,
                        "name": "Chart2",
                        "description": "",
                        "dashboard_name": "Test",
                        "group_by_data": [],
                        "group_by_query": "Query-id",
                        "group_by_query_name": "Test Query",
                        "rows": [],
                    },
                ],
            }
        ),
    )

    count, charts = octoxlabs.get_charts()
    assert count == 2
    assert charts[0].name == "Chart"

    mock_response.add(
        method=responses.GET,
        url="https://octoxlabs.service:8443/dashboards/charts",
        body=json.dumps(
            {
                "count": 1,
                "results": [
                    {
                        "id": 1,
                        "name": "Chart",
                        "description": "",
                        "dashboard_name": "Dashboard",
                        "group_by_data": [],
                        "group_by_query": "Query-id",
                        "group_by_query_name": "Test Query",
                        "rows": [],
                    }
                ],
            }
        ),
    )

    count, charts = octoxlabs.get_charts(dashboard_id=1)
    assert count == 1
    assert charts[0].name == "Chart"


def test_octoxlabs_chart_by_id(mock_response, octoxlabs_client):
    octoxlabs = octoxlabs_client

    mock_response.add(
        method=responses.GET,
        url="https://octoxlabs.service:8443/dashboards/charts/1",
        body=json.dumps(
            {
                "id": 1,
                "name": "Chart",
                "description": "",
                "dashboard_name": "Dashboard",
                "group_by_data": [],
                "group_by_query": "Query-id",
                "group_by_query_name": "Test Query",
                "rows": [],
            }
        ),
    )

    chart = octoxlabs.get_chart_by_id(chart_id=1)

    assert chart.id == 1
