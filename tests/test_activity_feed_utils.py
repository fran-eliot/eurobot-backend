# tests/test_activity_feed_utils.py

from app.modules.activity_feed.activity_feed_utils import (
    get_feed_color,
    get_feed_icon,
)


def test_get_feed_icon_known_events():
    assert get_feed_icon("TASK_CREATED") == "fa-plus-circle"
    assert get_feed_icon("TASK_UPDATED") == "fa-pen"
    assert get_feed_icon("TASK_DELETED") == "fa-trash"
    assert get_feed_icon("MEMBER_JOINED") == "fa-user-plus"


def test_get_feed_icon_unknown_event():
    assert get_feed_icon("UNKNOWN") == "fa-info-circle"


def test_get_feed_color_deleted():
    assert get_feed_color("TASK_DELETED") == "bg-danger"


def test_get_feed_color_removed():
    assert get_feed_color("MEMBER_REMOVED") == "bg-danger"


def test_get_feed_color_created():
    assert get_feed_color("TASK_CREATED") == "bg-success"


def test_get_feed_color_joined():
    assert get_feed_color("MEMBER_JOINED") == "bg-success"


def test_get_feed_color_status():
    assert get_feed_color("TASK_STATUS_CHANGED") == "bg-warning"


def test_get_feed_color_updated():
    assert get_feed_color("TASK_UPDATED") == "bg-primary"


def test_get_feed_color_empty():
    assert get_feed_color("") == "bg-secondary"


def test_get_feed_color_unknown():
    assert get_feed_color("RANDOM") == "bg-secondary"