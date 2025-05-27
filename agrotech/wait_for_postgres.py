import os
import time
import psycopg2
from psycopg2 import OperationalError

while True:
    try:
        conn = psycopg2.connect(
            dbname=os.getenv("SQL_DATABASE", "agrotech"),
            user=os.getenv("SQL_USER", "username"),
            password=os.getenv("SQL_PASSWORD", "passwd!"),
            host=os.getenv("SQL_HOST", "pg"),
            port=os.getenv("SQL_PORT", "5432"),
        )
        conn.close()
        break
    except OperationalError:
        print("Waiting for postgres...")
        time.sleep(1)
