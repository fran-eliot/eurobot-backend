# tests/test_dashboard_web_extra.py


from unittest.mock import patch

from tests.test_utils import login_admin


def test_dashboard_metrics_called(client):
    login_admin(client)

    with patch(
        "app.modules.dashboard.dashboard_web.get_dashboard_metrics",
        return_value={
            "total_users": 1,
            "active_users": 1,
            "inactive_users": 0,
            "total_roles": 1,
            "total_identities": 1,
            "local_identities": 1,
            "external_identities": 0,
            "total_projects": 1,
            "active_projects": 1,
            "finished_projects": 0,
            "total_tasks": 1,
            "pending_tasks": 1,
            "progress_tasks": 0,
            "completed_tasks": 0,
            "completion_rate": 0,
            "total_activities": 0,
            "total_hours": 0,
            "recent_activities": [],
            "recent_logs": [],
            "recent_feed": [],
        },
    ) as mock_metrics:
        response = client.get("/dashboard")

    assert response.status_code == 200
    assert mock_metrics.called


def test_dashboard_template_error(client):
    login_admin(client)

    with patch(
        "app.modules.dashboard.dashboard_web.templates.TemplateResponse",
        side_effect=[
            Exception("template error"),
            "fallback-response",
        ],
    ):
        response = client.get("/dashboard")

    assert response.status_code == 200