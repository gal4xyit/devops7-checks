import os

import pytest
import requests


@pytest.fixture(scope="session")
def expected_release():
    return os.environ["EXPECTED_RELEASE"]


@pytest.fixture(scope="session")
def http_get():
    base_url = os.environ["BASE_URL"].rstrip("/")
    timeout = float(os.environ.get("CHECK_TIMEOUT", "5"))

    def get(path):
        return requests.get(
            f"{base_url}{path}", timeout=timeout, allow_redirects=False
        )

    return get
