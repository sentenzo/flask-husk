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
        if db_name == None or connection_settings["dbname"] == db_name:
            return

        dbhelper.create_db_if_not_exist(self._conn, db_name)

        connection_settings["dbname"] = db_name
        self._conn = psycopg2.connect(**connection_settings)


db = DB()
