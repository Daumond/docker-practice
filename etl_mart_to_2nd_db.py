import logging
import os
import sys
import time
from datetime import datetime, timezone

import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

LOG_FORMAT = "%(asctime)s | %(levelname)s | %(message)s"
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT, datefmt="%Y-%m-%d %H:%M:%S")

SOURCE_URL = os.environ.get(
    "SOURCE_DB_URL",
    "postgresql://postgres:pass@localhost:5432/demo",
)
TARGET_URL = os.environ.get(
    "TARGET_DB_URL",
    "postgresql://postgres:pass@localhost:5433/mart",
)
MART_QUERY = "SELECT * FROM public.airplanes_marts"
TARGET_TABLE = "airplanes_stats"


def move_data() -> int:
    t0 = time.perf_counter()
    source = create_engine(SOURCE_URL, pool_pre_ping=True)
    destination = create_engine(TARGET_URL, pool_pre_ping=True)
    started_at = datetime.now(timezone.utc).isoformat()
    logging.info("Старт ETL, source=%s target=%s", SOURCE_URL, TARGET_URL)
    logging.info("Время старта (UTC): %s", started_at)

    try:
        t_read = time.perf_counter()
        df = pd.read_sql(MART_QUERY, source)
        read_s = time.perf_counter() - t_read
        logging.info("Прочитано в DataFrame: %s строк за %.2f c", len(df), read_s)

        t_write = time.perf_counter()
        df.to_sql(
            TARGET_TABLE,
            destination,
            if_exists="replace",
            index=False,
        )
        write_s = time.perf_counter() - t_write
        logging.info("Записано в %s: %s строк за %.2f c", TARGET_TABLE, len(df), write_s)
    except (SQLAlchemyError, OSError) as e:
        logging.exception("Ошибка ETL: %s", e)
        return 1
    except Exception as e:
        logging.exception("Непредвиденная ошибка: %s", e)
        return 1

    total = time.perf_counter() - t0
    logging.info("Успех. Всего %.2f c (включая чтение и запись).", total)
    return 0


if __name__ == "__main__":
    sys.exit(move_data())
