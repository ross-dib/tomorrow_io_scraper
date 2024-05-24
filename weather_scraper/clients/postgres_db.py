"""
Postgres client for creating, inserting, and updating postrgres db using pyscopg2
For more info on postrgresql see --> https://www.postgresql.org/docs/
For more info on pyscopg2 see --> https://www.psycopg.org/docs/usage.html
"""

import psycopg2
from psycopg2.extras import execute_values
import os

from weather_scraper.models.tomorrow_response import TomorrowIOWeatherData, unload_model_to_tuple

from weather_scraper.utils import logger

DB_NAME = os.environ['PGDATABASE']
DB_USER = os.environ['PGUSER']
DB_PASS = os.environ['PGPASSWORD']
DB_HOST = os.environ['PGHOST']
DB_PORT = os.environ['PGPORT']
TABLE_NAME = "tomorrow_io_timeline_data"


class PostrgresClient:
    def __init__(self, conn=None, columns=None, composite_key=None):
        self.conn = psycopg2.connect(
                host=DB_HOST,
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASS,
                port=DB_PORT
            ) if conn is None else conn
        self.logger = logger.get_logger()

    def load(self, data: list[TomorrowIOWeatherData]):
        insert_query = f"""
                    INSERT INTO {TABLE_NAME} (
                            start_time,
                            latitude,
                            longitude,
                            data_load_date,
                            dew_point,
                            humidity,
                            precipitation_intensity,
                            precipitation_probability,
                            precipitation_type,
                            temperature_c,
                            temperature_apparent_c,
                            uv_index,
                            wind_direction,
                            wind_gust,
                            wind_speed
                        )
                    VALUES %s
                    """

        unpacked_data = [unload_model_to_tuple(item) for item in data]
        execute_values(self.conn.cursor(), insert_query, unpacked_data)
        self.conn.commit()
        self.conn.cursor().close()

