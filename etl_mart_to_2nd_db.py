import pandas as pd
from sqlalchemy import create_engine
import logging

logging.basicConfig(level=logging.INFO)


def move_data():
    source = create_engine('postgresql://postgres:pass@localhost:5432/demo')
    destination = create_engine('postgresql://postgres:pass@localhost:5433/mart')

    try:
        logging.info("Extracting data...")
        df = pd.read_sql("SELECT * FROM airplanes_marts", source)

        logging.info(f"Transforming/Loading {len(df)} rows...")
        df.to_sql('airplanes_stats', destination, if_exists='replace', index=False)

        logging.info("Success!")
    except Exception as e:
        logging.error(f"Error: {e}")


if __name__ == "__main__":
    move_data()