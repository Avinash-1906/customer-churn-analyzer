# Connect to MySQL churn_db
# Function 1: churn rate by plan type (total, churned count, churn percentage)
# Function 2: average customer lifetime in days by plan type
# Function 3: monthly churn trend (how many churned each month)
# Function 4: top 10 high risk active customers inactive for more than 180 days

from mysql.connector import Error

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "root123",
    "database": "churn_db",
}


def get_connection():
    return __import__("mysql.connector").connector.connect(**DB_CONFIG)


def churn_rate_by_plan_type():
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    plan_type,
                    COUNT(*) AS total_customers,
                    SUM(status = 'churned') AS churned_customers,
                    ROUND((SUM(status = 'churned') / COUNT(*)) * 100, 2) AS churn_percentage
                FROM customers
                GROUP BY plan_type
                ORDER BY plan_type
                """
            )
            return cursor.fetchall()
    finally:
        conn.close()


def average_customer_lifetime_by_plan_type():
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    plan_type,
                    ROUND(AVG(DATEDIFF(last_active_date, subscription_start)), 2) AS avg_lifetime_days
                FROM customers
                GROUP BY plan_type
                ORDER BY plan_type
                """
            )
            return cursor.fetchall()
    finally:
        conn.close()


def monthly_churn_trend():
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    DATE_FORMAT(last_active_date, '%Y-%m') AS churn_month,
                    COUNT(*) AS churned_customers
                FROM customers
                WHERE status = 'churned'
                GROUP BY churn_month
                ORDER BY churn_month
                """
            )
            return cursor.fetchall()
    finally:
        conn.close()


def top_risk_active_customers(limit=10):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    customer_id,
                    plan_type,
                    subscription_start,
                    last_active_date,
                    DATEDIFF(CURDATE(), last_active_date) AS inactive_days
                FROM customers
                WHERE status = 'active'
                  AND DATEDIFF(CURDATE(), last_active_date) > 180
                ORDER BY inactive_days DESC
                LIMIT %s
                """,
                (limit,),
            )
            return cursor.fetchall()
    finally:
        conn.close()


if __name__ == "__main__":
    try:
        print("Churn rate by plan type:")
        for row in churn_rate_by_plan_type():
            print(row)

        print("\nAverage customer lifetime by plan type:")
        for row in average_customer_lifetime_by_plan_type():
            print(row)

        print("\nMonthly churn trend:")
        for row in monthly_churn_trend():
            print(row)

        print("\nTop risk active customers:")
        for row in top_risk_active_customers():
            print(row)
    except Error as exc:
        print(f"Database error: {exc}")
