from subprocess import CompletedProcess, TimeoutExpired

import pytest

from scripts import check_service


@pytest.mark.parametrize(
    ("outcome", "code", "message"),
    [
        (CompletedProcess(["curl"], 0, "unit-release", ""), 0, "містить unit-release"),
        (CompletedProcess(["curl"], 0, "other", ""), 1, "реліз unit-release відсутній"),
        (CompletedProcess(["curl"], 7, "", "connection refused"), 1, "connection refused"),
        (TimeoutExpired(["curl"], 0.25), 2, "TIMEOUT"),
        (CompletedProcess(["curl"], 28, "", "timed out"), 2, "TIMEOUT"),
    ],
    ids=["success", "wrong-release", "curl-error", "python-timeout", "curl-timeout"],
)
def test_check_service(monkeypatch, capsys, outcome, code, message):
    monkeypatch.setenv("BASE_URL", "http://127.0.0.1:8123")
    monkeypatch.setenv("EXPECTED_RELEASE", "unit-release")
    monkeypatch.setenv("CHECK_TIMEOUT", "0.25")

    def fake_run(command, *, capture_output, text, timeout):
        assert command[0] == "curl"
        assert command[-1] == "http://127.0.0.1:8123/"
        assert capture_output and text
        assert timeout == 0.25
        if isinstance(outcome, TimeoutExpired):
            raise outcome
        return outcome

    monkeypatch.setattr(check_service.subprocess, "run", fake_run)
    assert check_service.main() == code
    assert message in capsys.readouterr().out
