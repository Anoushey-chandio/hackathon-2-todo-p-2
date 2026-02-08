import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
print("Connecting to:", DATABASE_URL)

try:
    conn = psycopg2.connect(DATABASE_URL)
    print("SUCCESS: Connection established!")
    conn.close()
except Exception as e:
    print("FAILURE: Connection failed.")
    print(e)
