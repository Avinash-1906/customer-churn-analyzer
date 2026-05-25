# Read customers.csv and insert all rows into MySQL
# database: churn_db, table: customers
# host: localhost, user: root, password: yourpassword
# skip row if customer_id already exists

import csv
from datetime import datetime

import mysql.connector

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "root123",
    "database": "churn_db",
}


def get_connection():
    conn = mysql.connector.connect(
        host=DB_CONFIG["host"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
    )
    return conn


def create_database_and_table():
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("CREATE DATABASE IF NOT EXISTS churn_db")
            cursor.execute("USE churn_db")
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS customers (
                    customer_id VARCHAR(50) PRIMARY KEY,
                    subscription_start DATE NOT NULL,
                    last_active_date DATE NOT NULL,
                    plan_type VARCHAR(50) NOT NULL,
                    status VARCHAR(20) NOT NULL
                )
                """
            )
        conn.commit()
    finally:
        conn.close()


def load_customers(csv_path="customers.csv"):
    create_database_and_table()

    conn = mysql.connector.connect(**DB_CONFIG)
    inserted = 0
    skipped = 0

    try:
        with conn.cursor() as cursor, open(csv_path, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                try:
                    subscription_start = datetime.strptime(row["subscription_start"], "%Y-%m-%d").date()
                    last_active_date = datetime.strptime(row["last_active_date"], "%Y-%m-%d").date()
                except ValueError as exc:
                    raise ValueError(f"Invalid date in row: {row}") from exc

                cursor.execute(
                    """
                    INSERT IGNORE INTO customers
                    (customer_id, subscription_start, last_active_date, plan_type, status)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (
                        row["customer_id"],
                        subscription_start,
                        last_active_date,
                        row["plan_type"],
                        row["status"],
                    ),
                )
                if cursor.rowcount == 1:
                    inserted += 1
                else:
                    skipped += 1

        conn.commit()
    finally:
        conn.close()

    print(f"Inserted {inserted} rows, skipped {skipped} existing rows")


if __name__ == "__main__":
    load_customers()
