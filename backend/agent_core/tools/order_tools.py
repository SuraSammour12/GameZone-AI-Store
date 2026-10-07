"""
Tools the order analysis agent can call.

Each function is decorated with @tool so the LLM sees its name, its docstring,
and its argument schema. The LLM decides which tool to invoke based on the
current situation. We never wire tool calls with if/else, that would defeat
the whole point of an agent.

All data reads go through the JSON files that seed.py populated. Reads are
lightweight and happen on the fly, so the agent always sees fresh state
between requests.
"""

import re
from difflib import SequenceMatcher

from langchain_core.tools import tool

from .. import repo


def _normalize_name(name: str) -> str:
    """Lowercase, strip punctuation, collapse whitespace for fuzzy matching."""
    return re.sub(r"[^a-z0-9\s]", "", name.lower()).strip()


def _normalize_address(address: str) -> str:
    """Same idea as normalize_name but tuned for street addresses."""
    return re.sub(r"[^a-z0-9\s]", "", address.lower()).strip()


def _name_similarity(a: str, b: str) -> float:
    """0.0 to 1.0 similarity between two names after normalization."""
    return SequenceMatcher(None, _normalize_name(a), _normalize_name(b)).ratio()


# =========================================================================
# TOOL 1: Customer order history
# =========================================================================

@tool
def get_customer_order_history(customer_name: str) -> dict:
    """
    Look up the past orders placed by a customer, matched by name.

    Use this when you need to understand how trustworthy a buyer is. A long
    clean history is a strong positive signal. A history of admin rejections
    is a strong negative signal. A missing history means the buyer is new,
    which is neutral on its own but relevant when combined with other flags.

    Returns a summary with total order count, approved count, rejected count,
    total spent, and the most recent five orders in short form.
    """
    orders = repo.load_orders()
    target = _normalize_name(customer_name)

    matches = [
        o for o in orders
        if _normalize_name(o.get("customer_name", "")) == target
    ]

    if not matches:
        return {
            "found": False,
            "customer_name": customer_name,
            "message": "No previous orders on file for this customer.",
        }

    approved = [o for o in matches if o.get("status") == "approved"]
    rejected = [o for o in matches if o.get("status") == "rejected"]
    flagged = [o for o in matches if o.get("status") == "flagged"]
    total_spent = sum(o.get("total", 0) for o in approved)

    recent = sorted(matches, key=lambda o: o.get("timestamp", ""), reverse=True)[:5]
    recent_summary = [
        {
            "id": o["id"],
            "total": o.get("total"),
            "status": o.get("status"),
            "timestamp": o.get("timestamp"),
            "item_count": o.get("item_count"),
            "admin_note": o.get("admin_note", ""),
        }
        for o in recent
    ]

    return {
        "found": True,
        "customer_name": customer_name,
        "total_orders": len(matches),
        "approved_count": len(approved),
        "rejected_count": len(rejected),
        "flagged_count": len(flagged),
        "total_spent_approved": total_spent,
        "recent_orders": recent_summary,
    }


# =========================================================================
# TOOL 2: Address frequency and alias detection
# =========================================================================

@tool
def check_address_frequency(address: str) -> dict:
    """
    Check how often a delivery address has been used and by which names.

    Use this when an order looks unusual and you want to rule in or out an
    address fraud ring. Multiple different names shipping to the same address
    is a strong fraud signal, especially when previous orders at that address
    were rejected.

    Returns the number of orders at the address, the distinct names used,
    similarity scores between those names, and the status breakdown.
    """
    orders = repo.load_orders()
    target = _normalize_address(address)

    matches = [
        o for o in orders
        if _normalize_address(o.get("customer_address", "")) == target
    ]

    if not matches:
        return {
            "found": False,
            "address": address,
            "message": "No previous orders at this address.",
        }

    names_used = list({o.get("customer_name", "") for o in matches})
    approved = sum(1 for o in matches if o.get("status") == "approved")
    rejected = sum(1 for o in matches if o.get("status") == "rejected")

    # Compute pairwise similarity to spot near duplicate aliases.
    alias_pairs = []
    for i, a in enumerate(names_used):
        for b in names_used[i + 1:]:
            score = _name_similarity(a, b)
            if score >= 0.4:
                alias_pairs.append({
                    "name_a": a,
                    "name_b": b,
                    "similarity": round(score, 2),
                })

    return {
        "found": True,
        "address": address,
        "total_orders_at_address": len(matches),
        "distinct_names": names_used,
        "distinct_name_count": len(names_used),
        "approved_at_address": approved,
        "rejected_at_address": rejected,
        "possible_aliases": alias_pairs,
    }


# =========================================================================
# TOOL 3: Reselling pattern detector
# =========================================================================

@tool
def check_reselling_pattern(customer_name: str) -> dict:
    """
    Detect whether a customer has been repeatedly buying high value hardware.

    Use this on orders that contain consoles or premium accessories, or when
    the order total is high. Two or more console purchases within the last 60
    days is a strong reseller signal, especially when previous ones were
    already rejected by an admin.

    Returns the count of console purchases, which specific consoles were
    bought, and whether any were rejected.
    """
    orders = repo.load_orders()
    products = repo.load_products()
    console_ids = {p["id"] for p in products if p.get("category") == "Consoles"}

    target = _normalize_name(customer_name)
    customer_orders = [
        o for o in orders
        if _normalize_name(o.get("customer_name", "")) == target
    ]

    console_orders = []
    for o in customer_orders:
        for item in o.get("items", []):
            if item.get("product_id") in console_ids:
                console_orders.append({
                    "order_id": o["id"],
                    "product_name": item.get("product_name"),
                    "quantity": item.get("quantity"),
                    "status": o.get("status"),
                    "timestamp": o.get("timestamp"),
                })

    rejected_consoles = sum(1 for c in console_orders if c["status"] == "rejected")

    return {
        "customer_name": customer_name,
        "console_purchases_total": len(console_orders),
        "rejected_console_purchases": rejected_consoles,
        "console_purchase_details": console_orders,
        "pattern_detected": len(console_orders) >= 2,
    }


# =========================================================================
# TOOL 4: Similar rejected orders lookup
# =========================================================================

@tool
def find_similar_rejected_orders(product_ids: list[str]) -> dict:
    """
    Search past rejected orders for ones that contained the same products.

    Use this when the current order's product mix looks suspicious and you
    want to know whether the store already rejected orders with a similar
    basket. Repeated rejections of the same product combination are a strong
    signal that the current order should also be flagged.

    Pass the product IDs from the current order. Returns matching rejected
    orders with their admin notes.
    """
    if not product_ids:
        return {"query_products": [], "matches": []}

    orders = repo.load_orders()
    target_set = set(product_ids)

    matches = []
    for o in orders:
        if o.get("status") != "rejected":
            continue
        order_products = {item.get("product_id") for item in o.get("items", [])}
        overlap = target_set & order_products
        if overlap:
            matches.append({
                "order_id": o["id"],
                "customer_name": o.get("customer_name"),
                "total": o.get("total"),
                "shared_products": list(overlap),
                "admin_note": o.get("admin_note", ""),
                "timestamp": o.get("timestamp"),
            })

    return {
        "query_products": product_ids,
        "match_count": len(matches),
        "matches": matches[:10],
    }


# =========================================================================
# TOOL 5: Store policy lookup
# =========================================================================

@tool
def get_store_policy() -> dict:
    """
    Fetch the store's current policy thresholds.

    Use this to ground your decision in explicit numbers rather than guessing.
    Returns the suspicious order threshold, maximum items per order, maximum
    same item quantity, free shipping cutoff, and return policy.
    """
    return repo.load_policy()


# =========================================================================
# Registry so the graph can bind them all in one shot.
# =========================================================================

ORDER_TOOLS = [
    get_customer_order_history,
    check_address_frequency,
    check_reselling_pattern,
    find_similar_rejected_orders,
    get_store_policy,
]
