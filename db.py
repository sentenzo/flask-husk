import psycopg2
from psycopg2 import sql
from urllib.parse import urlparse
import os
import dbhelper

ENV_DATABASE_URL = "DATABASE_URL"


class DB:
    def __init__(self, db_name=None):
        connection_settings = dbhelper.parse_db_url(
            os.environ[ENV_DATABASE_URL])
        self._conn = psycopg2.connect(**connection_settings)

        if db_name and connection_settings["dbname"] != db_name:
            dbhelper.create_db_if_not_exist(self._conn, db_name)
            connection_settings["dbname"] = db_name
            self._conn = psycopg2.connect(**connection_settings)

        dbhelper.apply_migrations(self._conn)

    def inc_counter(self, delta):
        sql_command = """
UPDATE Counters
SET count = count + %s
WHERE id = %s
        """
        with self._conn.cursor() as cursor:
            cursor.execute(sql_command, (delta, 1))
            self._conn.commit()

    def get_counter(self):
        sql_command = """
SELECT count
FROM Counters
WHERE id = %s
LIMIT 1
        """
        with self._conn.cursor() as cursor:
            cursor.execute(sql_command, (1,))
            return cursor.fetchone()


db = DB()
