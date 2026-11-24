import pytest


def test_nginx_configuration(host):
    result = host.run("nginx -t")
    assert result.rc == 0, result.stderr


@pytest.mark.parametrize("filename", ["index.html", "health.json"])
def test_required_file_exists(host, filename):
    assert host.file(f"/usr/share/nginx/html/{filename}").is_file


def test_release_content(host, expected_release):
    page = host.file("/usr/share/nginx/html/index.html")
    assert expected_release in page.content_string
