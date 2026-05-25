# Generate fake customer churn CSV data
# 100 customers, columns: customer_id, subscription_start, last_active_date, plan_type, status
# plan_type: Basic, Standard, Premium
# status: active or churned (60% active, 40% churned)
# dates between 2022 and 2024
# save as customers.csv

import csv
import random
from datetime import datetime, timedelta

OUTPUT_PATH = "customers.csv"
PLAN_TYPES = ["Basic", "Standard", "Premium"]
ACTIVE_COUNT = 60
CHURNED_COUNT = 40
TODAY = datetime(2026, 5, 26)

PLAN_LIFETIME_DAYS = {
    "Basic": (30, 150),
    "Standard": (90, 270),
    "Premium": (180, 500),
}

def random_date_between(start, end):
    delta = (end - start).days
    return start + timedelta(days=random.randint(0, delta))

def build_customer(customer_id, status):
    plan_type = random.choice(PLAN_TYPES)
    min_days, max_days = PLAN_LIFETIME_DAYS[plan_type]
    sub_start = random_date_between(datetime(2024, 1, 1), datetime(2025, 6, 30))
    lifetime_days = random.randint(min_days, max_days)

    if status == "churned":
        # churned customers went inactive sometime in the past
        last_active = sub_start + timedelta(days=lifetime_days)
        if last_active > TODAY:
            last_active = TODAY - timedelta(days=random.randint(200, 500))
    else:
        if random.random() < 0.20:
            last_active = TODAY - timedelta(days=random.randint(181, 400))
        else:
            last_active = TODAY - timedelta(days=random.randint(1, 180))
        if last_active < sub_start:
            last_active = sub_start + timedelta(days=random.randint(10, 30))

    return {
        "customer_id": customer_id,
        "subscription_start": sub_start.strftime("%Y-%m-%d"),
        "last_active_date": last_active.strftime("%Y-%m-%d"),
        "plan_type": plan_type,
        "status": status,
    }

def main():
    statuses = ["active"] * ACTIVE_COUNT + ["churned"] * CHURNED_COUNT
    random.shuffle(statuses)

    customers = []
    for idx, status in enumerate(statuses, start=1):
        customers.append(build_customer(f"CUST{idx:04d}", status))

    with open(OUTPUT_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["customer_id", "subscription_start", "last_active_date", "plan_type", "status"])
        writer.writeheader()
        writer.writerows(customers)

    print(f"Generated {len(customers)} customers in {OUTPUT_PATH}")

if __name__ == "__main__":
    main()