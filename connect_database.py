import psycopg
import os

try:
    with psycopg.connect(
        host="localhost",
        port=5432,
        dbname="ecommerce_db",
        user="postgres",
        password=os.getenv("DB_PASSWORD")
    ) as connection:

        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM orders")

            rows = cursor.fetchall()

            for row in rows:
                print(row)

    print("Database connection successful!")

except Exception as error:
    print("Something went wrong:", error)