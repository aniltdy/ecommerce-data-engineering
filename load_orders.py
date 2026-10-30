import csv
import logging
import os
import psycopg

from decimal import Decimal, InvalidOperation


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("etl_pipeline.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)


def load_orders():

    loaded_count = 0
    duplicate_count = 0
    invalid_count = 0

    logging.info("ETL pipeline started")

    try:
        # Connect to PostgreSQL
        with psycopg.connect(
            host="localhost",
            port=5432,
            dbname="ecommerce_db",
            user="postgres",
            password=os.getenv("DB_PASSWORD")
        ) as connection:

            with connection.cursor() as cursor:

                # Read the source CSV
                with open(
                    "data/orders.csv",
                    "r",
                    newline="",
                    encoding="utf-8"
                ) as file:

                    reader = csv.DictReader(file)

                    required_columns = {
                        "order_id",
                        "customer_name",
                        "product",
                        "amount"
                    }

                    if not required_columns.issubset(reader.fieldnames or []):
                        raise ValueError(
                            "CSV is missing one or more required columns"
                        )

                    for row in reader:

                        try:
                            # Validate order ID
                            order_id = int(row["order_id"])

                            if order_id <= 0:
                                raise ValueError(
                                    "Order ID must be positive"
                                )

                            # Validate text fields
                            customer_name = row["customer_name"].strip()
                            product = row["product"].strip()

                            if not customer_name:
                                raise ValueError(
                                    "Customer name is missing"
                                )

                            if not product:
                                raise ValueError(
                                    "Product name is missing"
                                )

                            # Validate amount
                            amount = Decimal(row["amount"])

                            if not amount.is_finite():
                                raise ValueError(
                                    "Amount must be a finite number"
                                )

                            if amount < 0:
                                raise ValueError(
                                    "Amount cannot be negative"
                                )

                            # Insert the valid record
                            cursor.execute(
                                """
                                INSERT INTO orders
                                    (
                                        order_id,
                                        customer_name,
                                        product,
                                        amount
                                    )
                                VALUES (%s, %s, %s, %s)
                                ON CONFLICT (order_id) DO NOTHING
                                RETURNING order_id
                                """,
                                (
                                    order_id,
                                    customer_name,
                                    product,
                                    amount
                                )
                            )

                            if cursor.fetchone() is not None:
                                loaded_count += 1
                                logging.info(
                                    "Order %s loaded successfully",
                                    order_id
                                )
                            else:
                                duplicate_count += 1
                                logging.warning(
                                    "Duplicate order skipped: %s",
                                    order_id
                                )

                        except (
                            ValueError,
                            InvalidOperation,
                            TypeError,
                            KeyError
                        ) as error:

                            invalid_count += 1

                            logging.error(
                                "Invalid record %s: %s",
                                row,
                                error
                            )

        logging.info("===== ETL PIPELINE REPORT =====")
        logging.info("New orders loaded: %s", loaded_count)
        logging.info("Duplicate orders skipped: %s", duplicate_count)
        logging.info("Invalid records skipped: %s", invalid_count)
        logging.info("ETL pipeline completed successfully")

    except Exception:
        logging.exception("ETL pipeline failed")
        raise


if __name__ == "__main__":
    load_orders()