# Pet-проект: Docker, две PostgreSQL, витрина, ETL в Python

## Что внутри

- **postgres-demo** (порт `5432`) — демо-БД [Postgres Pro «Авиалинии»](https://postgrespro.ru/education/demodb), данные в named volume, переживают перезапуск контейнера.
- **postgres-mart** (порт `5433`) — вторая БД; в неё скрипт заливает витрину из первой.
- **Витрина** `public.airplanes_marts` в БД `demo` — `SELECT` с `JOIN` и фильтром `status <> 'Cancelled'` (см. `init/02-create-mart-in-demo.sql`).
- **ETL** `etl_mart_to_2nd_db.py` — читает витрину в pandas, пишет в `mart.public.airplanes_stats`, логирует время и число строк.

## Подготовка (один раз)

1. Скачать дамп (файл большой, в репозиторий не коммитится):

   ```bash
   chmod +x scripts/download-demo-dump.sh
   ./scripts/download-demo-dump.sh
   ```

   В каталоге `init/` должен появиться `01-demo-20250901-3m.sql.gz`.

2. Поднять контейнеры (инициализация БД при **первом** создании volume может занять несколько минут):

   ```bash
   docker compose up -d
   ```

   Дождаться готовности: `docker compose ps` — оба сервиса `healthy`.

3. Окружение Python и запуск ETL:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate   # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   python etl_mart_to_2nd_db.py
   ```

4. Проверка во второй БД:

   ```bash
   docker exec -it postgres17-mart psql -U postgres -d mart -c "SELECT COUNT(*) FROM airplanes_stats;"
   ```

## Переменные окружения (опционально)

По умолчанию скрипт подключается к `localhost:5432` и `localhost:5433`. Можно переопределить:

- `SOURCE_DB_URL` — например `postgresql://postgres:pass@host:5432/demo`
- `TARGET_DB_URL` — например `postgresql://postgres:pass@host:5433/mart`

## Если нужно пересоздать данные с нуля

```bash
docker compose down -v
./scripts/download-demo-dump.sh
docker compose up -d
```

**Внимание:** `-v` удалит volumes со всеми данными.

## Порядок файлов в `init/`

1. `00-init.sql.gz` — создаёт пустую БД `demo`, чтобы выдержать первый `DROP DATABASE` в дампе.
2. `01-demo-20250901-3m.sql.gz` — скачивается скриптом, не хранится в git.
3. `02-create-mart-in-demo.sql` — витрина в БД `demo`.
