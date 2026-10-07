import json
import os
from collections import Counter
from typing import Any

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
ORDERS_FILE = os.path.join(DATA_DIR, "orders.json")
PRODUCTS_FILE = os.path.join(DATA_DIR, "products.json")
REVIEWS_FILE = os.path.join(DATA_DIR, "reviews.json")

CHILD_RATINGS = {"everyone", "everyone 10+"}
ADULT_RATINGS = {"16+", "17+", "18+"}

SPAM_URL_MARKERS = ("http", "www.", ".com", "dot example", "dot com")


def _load_json(path: str) -> Any:
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_policy() -> dict:
    data = _load_json(PRODUCTS_FILE)
    if isinstance(data, dict):
        return data.get("store_policy", {})
    return {}


def _console_ids() -> set:
    data = _load_json(PRODUCTS_FILE)
    products = data.get("products", []) if isinstance(data, dict) else []
    return {p["id"] for p in products if p.get("category") == "Consoles"}


def compute_order_flags(order: dict, policy: dict) -> list[str]:
    flags: list[str] = []
    items = order.get("items", [])

    threshold = policy.get("suspicious_order_threshold", 500)
    max_items = policy.get("max_items_per_order", 5)
    max_same = policy.get("max_same_item", 2)

    total = order.get("total", 0)
    item_count = order.get("item_count", sum(i.get("quantity", 0) for i in items))

    if total > threshold:
        flags.append(f"total_over_threshold ({total} > {threshold})")

    if item_count > max_items:
        flags.append(f"item_count_over_max ({item_count} > {max_items})")

    for item in items:
        qty = item.get("quantity", 0)
        if qty > max_same:
            flags.append(
                f"same_item_over_max ({item.get('product_name', item.get('product_id'))} x{qty} > {max_same})"
            )

    ratings = {str(i.get("age_rating", "")).lower() for i in items}
    if ratings & CHILD_RATINGS and ratings & ADULT_RATINGS:
        flags.append("mixed_age_ratings")

    console_ids = _console_ids()
    console_qty = sum(
        i.get("quantity", 0) for i in items if i.get("product_id") in console_ids
    )
    if console_qty >= 2:
        flags.append(f"multiple_consoles ({console_qty})")

    return flags


def load_recent_overrides(limit: int = 8) -> str:
    orders = _load_json(ORDERS_FILE)
    overrides = []
    for o in orders:
        analysis = o.get("ai_analysis") or {}
        ai_decision = analysis.get("decision")
        admin_decision = o.get("admin_decision")
        if not admin_decision:
            continue
        flipped = (
            (ai_decision == "flag_for_review" and admin_decision == "approve")
            or (ai_decision == "approve" and admin_decision == "reject")
        )
        if not flipped:
            continue
        note = o.get("admin_note", "") or "(no note)"
        overrides.append(
            f"- {o.get('customer_name', 'Unknown')}: AI said {ai_decision}, "
            f"admin chose {admin_decision}. Note: {note}"
        )

    overrides = overrides[-limit:]
    if not overrides:
        return "No recent admin overrides on file."
    return "Recent admin overrides (the human corrected the agent here):\n" + "\n".join(
        overrides
    )


def review_first_pass(review: dict) -> list[str]:
    flags: list[str] = []
    text = str(review.get("text", ""))
    normalized = text.lower()

    if any(marker in normalized for marker in SPAM_URL_MARKERS):
        flags.append("contains_link_or_promo")

    reviews = _load_json(REVIEWS_FILE)
    own_id = review.get("id")
    stripped = " ".join(normalized.split())
    exact_duplicates = sum(
        1
        for r in reviews
        if r.get("id") != own_id
        and " ".join(str(r.get("text", "")).lower().split()) == stripped and stripped
    )
    if exact_duplicates >= 1:
        flags.append(f"exact_duplicate_text ({exact_duplicates} prior)")

    return flags


def reviewer_status(customer_name: str) -> str:
    reviews = _load_json(REVIEWS_FILE)
    name = (customer_name or "").strip().lower()
    matches = [r for r in reviews if str(r.get("customer_name", "")).strip().lower() == name]
    if not matches:
        return "No prior reviews on file for this reviewer."
    statuses = Counter(r.get("status", "unknown") for r in matches)
    parts = ", ".join(f"{v} {k}" for k, v in statuses.items())
    return f"Reviewer has {len(matches)} prior reviews ({parts})."