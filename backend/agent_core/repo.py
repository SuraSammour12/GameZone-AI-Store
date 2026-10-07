import uuid

from .db import (
    SessionLocal,
    Product,
    Policy,
    Order,
    Review,
    Activity,
    Invoice,
    now,
)


def _new_id(prefix):
    return f"{prefix}-{uuid.uuid4().hex[:6].upper()}"


def load_orders():
    with SessionLocal() as s:
        return [o.to_dict() for o in s.query(Order).all()]


def load_reviews():
    with SessionLocal() as s:
        return [r.to_dict() for r in s.query(Review).all()]


def load_products():
    with SessionLocal() as s:
        return [p.to_dict() for p in s.query(Product).all()]


def load_policy():
    with SessionLocal() as s:
        row = s.query(Policy).first()
        return row.to_dict() if row else {}


def load_activity():
    with SessionLocal() as s:
        return [a.to_dict() for a in s.query(Activity).all()]


def get_product(product_id):
    with SessionLocal() as s:
        p = s.get(Product, product_id)
        return p.to_dict() if p else None


def get_order(order_id):
    with SessionLocal() as s:
        o = s.get(Order, order_id)
        return o.to_dict() if o else None


def insert_order(order: dict):
    with SessionLocal() as s:
        s.add(Order(**order))
        s.commit()


def insert_review(review: dict):
    with SessionLocal() as s:
        s.add(Review(**review))
        s.commit()


def update_order_decision(order_id, status, admin_decision, admin_note):
    with SessionLocal() as s:
        o = s.get(Order, order_id)
        if not o:
            return None
        o.status = status
        o.admin_decision = admin_decision
        o.admin_note = admin_note
        s.commit()
        return o.to_dict()


def update_review_decision(review_id, status, admin_decision, admin_note):
    with SessionLocal() as s:
        r = s.get(Review, review_id)
        if not r:
            return None
        r.status = status
        r.admin_decision = admin_decision
        r.admin_note = admin_note
        s.commit()
        return r.to_dict()


def log_activity(action, details, actor="AI Agent", ref_id=""):
    with SessionLocal() as s:
        s.add(Activity(
            id=_new_id("LOG"),
            timestamp=now(),
            action=action,
            actor=actor,
            details=details,
            ref_id=ref_id,
        ))
        s.commit()


def published_reviews_for(product_id):
    with SessionLocal() as s:
        rows = (
            s.query(Review)
            .filter(Review.product_id == product_id, Review.status == "published")
            .all()
        )
        return [r.to_dict() for r in rows]


def stats():
    with SessionLocal() as s:
        orders = s.query(Order).all()
        reviews = s.query(Review).all()
        return {
            "orders": {
                "total": len(orders),
                "approved": sum(1 for o in orders if o.status == "approved"),
                "flagged": sum(1 for o in orders if o.status == "flagged"),
                "rejected": sum(1 for o in orders if o.status == "rejected"),
                "revenue": sum(o.total for o in orders if o.status == "approved"),
            },
            "reviews": {
                "total": len(reviews),
                "published": sum(1 for r in reviews if r.status == "published"),
                "flagged": sum(1 for r in reviews if r.status == "flagged"),
                "rejected": sum(1 for r in reviews if r.status == "rejected"),
            },
        }


# =========================================================================
# Invoices
# =========================================================================

def create_invoice_for_order(order_id):
    with SessionLocal() as s:
        o = s.get(Order, order_id)
        if not o:
            return None
        existing = s.query(Invoice).filter(Invoice.order_id == order_id).first()
        if existing:
            return existing.to_dict()
        inv = Invoice(
            id=_new_id("INV"),
            order_id=o.id,
            customer_name=o.customer_name,
            customer_address=o.customer_address,
            issued_at=now(),
            subtotal=o.subtotal,
            shipping=o.shipping,
            total=o.total,
            status="unpaid",
            paid_at="",
        )
        s.add(inv)
        s.commit()
        return inv.to_dict()


def load_invoices():
    with SessionLocal() as s:
        return [i.to_dict() for i in s.query(Invoice).all()]


def get_invoice(invoice_id):
    with SessionLocal() as s:
        i = s.get(Invoice, invoice_id)
        return i.to_dict() if i else None


def mark_invoice_paid(invoice_id):
    with SessionLocal() as s:
        i = s.get(Invoice, invoice_id)
        if not i:
            return None
        i.status = "paid"
        i.paid_at = now()
        s.commit()
        return i.to_dict()


def reset_all():
    with SessionLocal() as s:
        s.query(Invoice).delete()
        s.query(Order).delete()
        s.query(Review).delete()
        s.query(Activity).delete()
        s.commit()
