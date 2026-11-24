# Практична робота №7. Перевірка сервісу nginx

## Локальний запуск

Потрібні Bash у Linux або WSL, Git, Docker, Python 3.14 і `curl`.

```bash
git clone https://github.com/gal4xyit/devops7-checks.git
cd devops7-checks
python3.14 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt

export BASE_URL=http://127.0.0.1:8080
export EXPECTED_RELEASE=devops7-gal4xyit
export CHECK_TIMEOUT=5

docker build -t devops7-app .
docker run -d --name devops7-app -p 127.0.0.1:8080:80 devops7-app
```

## Перевірка

```bash
curl -fsS --retry 3 --retry-all-errors --max-time 5 "$BASE_URL/health.json"
python -m pytest -q --hosts=docker://devops7-app tests
python scripts/check_service.py
echo "Код скрипту = $?"
```

Очікуваний результат — `14 passed` і код скрипту `0`.

## Відтворення збоїв

Після кожного відновлення повтори команди з розділу «Перевірка».

**1. Неправильна версія сторінки**

```bash
docker exec devops7-app sh -c 'echo "<h1>wrong-release</h1>" > /usr/share/nginx/html/index.html'
python -m pytest -q --tb=no --hosts=docker://devops7-app tests
python scripts/check_service.py
echo "Код скрипту = $?"
docker cp ./index.html devops7-app:/usr/share/nginx/html/index.html
```

**2. Помилковий порт** — `BASE_URL` залишається на `8080`.

```bash
docker rm -f devops7-app
docker run -d --name devops7-app -p 127.0.0.1:8081:80 devops7-app
python -m pytest -q --tb=no --hosts=docker://devops7-app tests
python scripts/check_service.py
echo "Код скрипту = $?"

# Відновлення порту 8080
docker rm -f devops7-app
docker run -d --name devops7-app -p 127.0.0.1:8080:80 devops7-app
```

**3. Призупинення контейнера**

```bash
docker pause devops7-app
time python scripts/check_service.py
echo "Код скрипту = $?"
python -m pytest -q --tb=no tests/http/test_endpoints.py::test_health_json tests/unit
docker unpause devops7-app
```

Завершення роботи — `docker rm -f devops7-app` і `deactivate`.

[Журнали експериментів](experiments/) · [Невдалий запуск CI](https://github.com/gal4xyit/devops7-checks/actions/runs/45465281988) · [Успішний запуск CI](https://github.com/gal4xyit/devops7-checks/actions/runs/45468768839)
