import pytest


@pytest.mark.parametrize(
    ("path", "expected_status"),
    [("/", 200), ("/health.json", 200), ("/missing-page", 404)],
)
def test_http_status(http_get, path, expected_status):
    response = http_get(path)
    assert response.status_code == expected_status


def test_home_page_release(http_get, expected_release):
    response = http_get("/")
    assert expected_release in response.text


def test_health_json(http_get, expected_release):
    response = http_get("/health.json")
    data = response.json()
    assert data["status"] == "ok"
    assert data["release"] == expected_release
