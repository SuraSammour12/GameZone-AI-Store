"""
Tools the review moderation agent can call.

Same pattern as order_tools. The LLM picks which one to run based on the
review text and the reviewer name. We provide the raw facts, the LLM decides
what they mean in context.
"""

import re
from difflib import SequenceMatcher

from langchain_core.tools import tool

from .. import repo


def _normalize_name(name: str) -> str:
    return re.sub(r"[^a-z0-9\s]", "", name.lower()).strip()


def _normalize_text(text: str) -> str:
    """Aggressive normalization for spam similarity checks."""
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9\s]", "", text.lower())).strip()


def _text_similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, _normalize_text(a), _normalize_text(b)).ratio()


# =========================================================================
# TOOL 1: Reviewer history
# =========================================================================

@tool
def get_reviewer_history(customer_name: str) -> dict:
    """
    Look up a reviewer's past review activity, matched by name.

    Use this before making a moderation call. A history of published,
    thoughtful reviews raises trust. A history of admin rejections is a
    strong negative signal, especially when the current review looks
    similar in tone to the rejected ones.

    Returns total review count, published and rejected breakdowns,
    average rating, and short summaries of the most recent reviews.
    """
    reviews = repo.load_reviews()
    target = _normalize_name(customer_name)

    matches = [
        r for r in reviews
        if _normalize_name(r.get("customer_name", "")) == target
    ]

    if not matches:
        return {
            "found": False,
            "customer_name": customer_name,
            "message": "No previous reviews from this reviewer.",
        }

    published = [r for r in matches if r.get("status") == "published"]
    rejected = [r for r in matches if r.get("status") == "rejected"]
    avg_rating = round(sum(r.get("rating", 0) for r in matches) / len(matches), 2)

    recent = sorted(matches, key=lambda r: r.get("timestamp", ""), reverse=True)[:5]
    recent_summary = [
        {
            "id": r["id"],
            "product_id": r.get("product_id"),
            "rating": r.get("rating"),
            "status": r.get("status"),
            "text_preview": (r.get("text", "")[:120] + "...") if len(r.get("text", "")) > 120 else r.get("text", ""),
            "admin_note": r.get("admin_note", ""),
        }
        for r in recent
    ]

    return {
        "found": True,
        "customer_name": customer_name,
        "total_reviews": len(matches),
        "published_count": len(published),
        "rejected_count": len(rejected),
        "average_rating": avg_rating,
        "recent_reviews": recent_summary,
    }


# =========================================================================
# TOOL 2: Duplicate content detector
# =========================================================================

@tool
def check_review_similarity(review_text: str) -> dict:
    """
    Compare a review's text against every past review to catch duplicate spam.

    Use this when a review looks generic, promotional, or suspiciously short.
    Bots often post the same body across many products. A similarity score
    above 0.85 against a previous review is a very strong spam signal.

    Returns the top matches with their similarity scores, the reviewer that
    posted them, and the product they were attached to.
    """
    if not review_text or not review_text.strip():
        return {"similarity_matches": [], "message": "Empty review text."}

    reviews = repo.load_reviews()

    scored = []
    for r in reviews:
        past = r.get("text", "")
        if not past.strip():
            continue
        score = _text_similarity(review_text, past)
        if score >= 0.75:
            scored.append({
                "review_id": r["id"],
                "customer_name": r.get("customer_name"),
                "product_id": r.get("product_id"),
                "status": r.get("status"),
                "similarity": round(score, 2),
                "text_preview": (past[:120] + "...") if len(past) > 120 else past,
            })

    scored.sort(key=lambda x: x["similarity"], reverse=True)

    return {
        "review_text_preview": (review_text[:120] + "...") if len(review_text) > 120 else review_text,
        "match_count": len(scored),
        "top_matches": scored[:5],
    }


# =========================================================================
# TOOL 3: Verify the reviewer actually bought the product
# =========================================================================

@tool
def verify_customer_purchased(customer_name: str, product_id: str) -> dict:
    """
    Check whether a reviewer has actually bought the product they are reviewing.

    Use this whenever a review looks generic or when the reviewer name has no
    history of activity. Reviews from customers with no purchase on file are
    typically fake or promotional and should be flagged.

    Returns a verification flag and, if any, the order IDs where the product
    was purchased by this customer.
    """
    orders = repo.load_orders()
    target = _normalize_name(customer_name)

    purchase_orders = []
    for o in orders:
        if _normalize_name(o.get("customer_name", "")) != target:
            continue
        if o.get("status") != "approved":
            continue
        for item in o.get("items", []):
            if item.get("product_id") == product_id:
                purchase_orders.append({
                    "order_id": o["id"],
                    "timestamp": o.get("timestamp"),
                    "quantity": item.get("quantity"),
                })
                break

    return {
        "customer_name": customer_name,
        "product_id": product_id,
        "verified_buyer": len(purchase_orders) > 0,
        "purchase_orders": purchase_orders,
    }


# =========================================================================
# TOOL 4: Product context
# =========================================================================

@tool
def get_product_context(product_id: str) -> dict:
    """
    Fetch product name, category, and age rating so you can judge if the
    review is actually about this product.

    Use this when a review's content sounds unrelated to what the product is.
    A review that talks about a football game on a page for a survival game
    is off topic and should be flagged.

    Returns the product's name, brand, category, description, and age rating.
    """
    products = repo.load_products()

    product = next((p for p in products if p.get("id") == product_id), None)
    if not product:
        return {
            "found": False,
            "product_id": product_id,
            "message": "Product not found in catalog.",
        }

    return {
        "found": True,
        "product_id": product["id"],
        "name": product.get("name"),
        "brand": product.get("brand"),
        "category": product.get("category"),
        "age_rating": product.get("age_rating"),
        "description": product.get("description"),
    }


# =========================================================================
# Registry
# =========================================================================

REVIEW_TOOLS = [
    get_reviewer_history,
    check_review_similarity,
    verify_customer_purchased,
    get_product_context,
]
