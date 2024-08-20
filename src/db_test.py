import psycopg2
import os
from dotenv import load_dotenv
from os import getenv

# Enables the `.env` file to be loaded
load_dotenv()

try:
    conn = psycopg2.connect(
        dbname=getenv('DB_NAME'),
        user=getenv('DB_USER'),
        password=getenv('DB_PASSWORD'),
        host=getenv('DB_HOST'),
        port=getenv('DB_PORT', '6543')
    )
    print("Connection successful")
except Exception as e:
    print(f"Error: {e}")
    dbname=getenv('DB_NAME')
    print(dbname)
finally:
    if conn:
        conn.close()
        print("connected closed")