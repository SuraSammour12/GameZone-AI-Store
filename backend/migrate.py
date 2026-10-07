import json
import os
import sys

from agent_core.db import (
    init_db,
    SessionLocal,
    Product,
    Policy,
    Order,
    Review,
    Activity,
)
from data.seed_data import SEED_ORDERS, SEED_REVIEWS, SEED_ACTIVITY

PRODUCTS_FILE = os.path.join(os.path.dirname(__file__), "data", "products.json")


def load_catalog():
    with open(PRODUCTS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    init_db()
    catalog = load_catalog()

    with SessionLocal() as s:
        s.query(Activity).delete()
        s.query(Review).delete()
        s.query(Order).delete()
        s.query(Product).delete()
        s.query(Policy).delete()
        s.commit()

        for p in catalog["products"]:
            s.add(Product(
                id=p["id"],
                name=p["name"],
                brand=p.get("brand"),
                category=p.get("category"),
                price=p["price"],
                age_rating=p.get("age_rating"),
                image=p.get("image"),
                description=p.get("description"),
                specs=p.get("specs", {}),
                in_stock=1 if p.get("in_stock", True) else 0,
                rating=p.get("rating", 0),
                review_count=p.get("review_count", 0),
            ))

        pol = catalog["store_policy"]
        s.add(Policy(
            id=1,
            payment=pol.get("payment"),
            shipping_cost=pol.get("shipping_cost"),
            free_shipping_over=pol.get("free_shipping_over"),
            delivery_time=pol.get("delivery_time"),
            return_policy=pol.get("return_policy"),
            suspicious_order_threshold=pol.get("suspicious_order_threshold"),
            max_items_per_order=pol.get("max_items_per_order"),
            max_same_item=pol.get("max_same_item"),
        ))

        for o in SEED_ORDERS:
            s.add(Order(
                id=o["id"],
                customer_name=o["customer_name"],
                customer_phone=o.get("customer_phone", ""),
                customer_address=o.get("customer_address", ""),
                items=o.get("items", []),
                item_count=o.get("item_count", 0),
                subtotal=o.get("subtotal", 0),
                shipping=o.get("shipping", 0),
                total=o.get("total", 0),
                payment=o.get("payment", "Cash on delivery"),
                timestamp=o.get("timestamp"),
                status=o.get("status"),
                ai_analysis=o.get("ai_analysis"),
                admin_decision=o.get("admin_decision", ""),
                admin_note=o.get("admin_note", ""),
            ))

        for r in SEED_REVIEWS:
            s.add(Review(
                id=r["id"],
                product_id=r.get("product_id"),
                customer_name=r.get("customer_name"),
                rating=r.get("rating", 5),
                text=r.get("text", ""),
                timestamp=r.get("timestamp"),
                status=r.get("status"),
                ai_analysis=r.get("ai_analysis"),
                admin_decision=r.get("admin_decision", ""),
                admin_note=r.get("admin_note", ""),
            ))

        for a in SEED_ACTIVITY:
            s.add(Activity(
                id=a["id"],
                timestamp=a.get("timestamp"),
                action=a.get("action"),
                actor=a.get("actor"),
                details=a.get("details"),
                ref_id=a.get("ref_id", ""),
            ))

        s.commit()

        print("=" * 60)
        print("GameZone database migration")
        print("=" * 60)
        print(f"Products : {s.query(Product).count()}")
        print(f"Orders   : {s.query(Order).count()}")
        print(f"Reviews  : {s.query(Review).count()}")
        print(f"Activity : {s.query(Activity).count()}")
        print(f"Policy   : {s.query(Policy).count()} row")
        print("=" * 60)
        print("Database ready at data/gamezone.db")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Migration failed: {e}", file=sys.stderr)
        sys.exit(1)
