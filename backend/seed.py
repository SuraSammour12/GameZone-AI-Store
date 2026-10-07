"""
Populate orders.json, reviews.json, and activity.json from seed_data.py.

Run this once when you clone the project, or any time you want to reset the
store to the designed scenarios that the AI agent is meant to reason about.

Usage:
    python seed.py
"""

import json
import os
import sys

from data.seed_data import SEED_ORDERS, SEED_REVIEWS, SEED_ACTIVITY


DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
ORDERS_FILE = os.path.join(DATA_DIR, "orders.json")
REVIEWS_FILE = os.path.join(DATA_DIR, "reviews.json")
ACTIVITY_FILE = os.path.join(DATA_DIR, "activity.json")


def write_json(path, payload):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)


def summarize():
    unique_customers = {o["customer_name"] for o in SEED_ORDERS}
    unique_reviewers = {r["customer_name"] for r in SEED_REVIEWS}
    print("=" * 60)
    print("GameZone seed summary")
    print("=" * 60)
    print(f"Orders written    : {len(SEED_ORDERS)}")
    print(f"Reviews written   : {len(SEED_REVIEWS)}")
    print(f"Activity entries  : {len(SEED_ACTIVITY)}")
    print(f"Unique buyers     : {len(unique_customers)}")
    print(f"Unique reviewers  : {len(unique_reviewers)}")
    print("=" * 60)


def main():
    os.makedirs(DATA_DIR, exist_ok=True)
    write_json(ORDERS_FILE, SEED_ORDERS)
    write_json(REVIEWS_FILE, SEED_REVIEWS)
    write_json(ACTIVITY_FILE, SEED_ACTIVITY)
    summarize()
    print("Seed data written to data/ successfully.")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Seeding failed: {e}", file=sys.stderr)
        sys.exit(1)
