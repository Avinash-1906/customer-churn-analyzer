# Import all functions from analyze.py
# Print a formatted report to terminal with all 4 analyses
# Use headers and separators to make it readable

from analyze import (
    average_customer_lifetime_by_plan_type,
    churn_rate_by_plan_type,
    monthly_churn_trend,
    top_risk_active_customers,
)


def print_separator(title):
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)


def print_churn_rate_by_plan_type():
    print_separator("1. Churn Rate by Plan Type")
    rows = churn_rate_by_plan_type()
    if not rows:
        print("No data available.")
        return

    print(f"{'Plan Type':<12} {'Total':>5} {'Churned':>8} {'Churn %':>9}")
    print("-" * 40)
    for plan_type, total, churned, churn_pct in rows:
        print(f"{plan_type:<12} {total:>5} {churned:>8} {churn_pct:>8.2f}%")


def print_average_customer_lifetime_by_plan_type():
    print_separator("2. Average Customer Lifetime by Plan Type")
    rows = average_customer_lifetime_by_plan_type()
    if not rows:
        print("No data available.")
        return

    print(f"{'Plan Type':<12} {'Average Lifetime (days)':>24}")
    print("-" * 40)
    for plan_type, avg_lifetime in rows:
        print(f"{plan_type:<12} {avg_lifetime:>24.2f}")


def print_monthly_churn_trend():
    print_separator("3. Monthly Churn Trend")
    rows = monthly_churn_trend()
    if not rows:
        print("No data available.")
        return

    print(f"{'Month':<8} {'Churned Customers':>18}")
    print("-" * 30)
    for month, churned_customers in rows:
        print(f"{month:<8} {churned_customers:>18}")


def print_top_risk_active_customers():
    print_separator("4. Top 10 High-Risk Active Customers")
    rows = top_risk_active_customers()
    if not rows:
        print("No data available.")
        return

    print(f"{'Customer ID':<12} {'Plan':<10} {'Subscription Start':<18} {'Last Active':<12} {'Inactive Days':>14}")
    print("-" * 80)
    for customer_id, plan_type, subscription_start, last_active_date, inactive_days in rows:
        print(
            f"{customer_id:<12} {plan_type:<10} {str(subscription_start):<18} {str(last_active_date):<12} {inactive_days:>14}"
        )


def main():
    print_churn_rate_by_plan_type()
    print_average_customer_lifetime_by_plan_type()
    print_monthly_churn_trend()
    print_top_risk_active_customers()


if __name__ == "__main__":
    main()
