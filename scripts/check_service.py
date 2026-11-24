import os
import subprocess


def main():
    try:
        base_url = os.environ["BASE_URL"].strip().rstrip("/")
        release = os.environ["EXPECTED_RELEASE"].strip()
        timeout = float(os.environ["CHECK_TIMEOUT"])
    except (KeyError, ValueError) as error:
        print(f"FAIL — помилка налаштувань ({error})")
        return 1

    if not base_url or not release or not (0 < timeout < float("inf")):
        print("FAIL — потрібні адреса, реліз і додатний скінченний тайм-аут")
        return 1

    url = f"{base_url}/"
    try:
        result = subprocess.run(
            ["curl", "--fail", "--silent", "--show-error", "--", url],
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        print(f"TIMEOUT — {url} не відповів за {timeout:g} с")
        return 2
    except OSError as error:
        print(f"FAIL — помилка запуску curl ({error})")
        return 1

    if result.returncode == 28:
        print(f"TIMEOUT — curl повідомив про тайм-аут ({url})")
        return 2
    if result.returncode != 0:
        print(f"FAIL — curl повернув {result.returncode} ({result.stderr.strip()})")
        return 1
    if release not in result.stdout:
        print(f"FAIL — очікуваний реліз {release} відсутній")
        return 1

    print(f"OK — {url} містить {release}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
