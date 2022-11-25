import psycopg2
from psycopg2 import sql
from urllib.parse import urlparse

# DATABASE_URL = postgres://postgres:kkk@localhost:5432/flaskcounter

def parse_db_url(db_url: str):
    print(db_url)
    db_url_parsed = urlparse(db_url)
    database = db_url_parsed.path[1:]
    credentals, address = db_url_parsed.netloc.split("@")
    uname, passwd = credentals.split(":")
    if ":" in address:
        host, port = address.split(":")
    else:
        host = address
        port = "5432"
    return {
        "dbname": database,
        "user": uname,
        "password": passwd,
        "host": host,
        "port": port,
    }


def db_exists(conn, db_name):
    exists = 0
    with conn.cursor() as cursor:
        cursor.execute(
            "SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s", (db_name,)
        )
        exists = cursor.fetchone()
        conn.commit()
    return exists == 1


def create_db_if_not_exist(conn, db_name):
    if not db_exists(conn, db_name):
        prev_autocommit_val, conn.autocommit = conn.autocommit, True
        with conn.cursor() as cursor:
            sql_cmd = sql.SQL("CREATE DATABASE {database_name}").format(
                database_name=sql.Identifier(db_name)
            )
            cursor.execute(sql_cmd)
            conn.commit()
        conn.autocommit = prev_autocommit_val


def apply_migrations(conn):
    with conn.cursor() as cursor:
        cursor.execute(open("migrations/001_create_db.sql", "r").read())
        conn.commit()
