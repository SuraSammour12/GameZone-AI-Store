"""
Seed data for GameZone AI Store.

Each customer, order, and review is designed to trigger a specific scenario
that the AI agent should reason about. The goal is to give the agent enough
real historical context to make explainable, well founded decisions.

Scenarios covered:
    Trusted customers with clean history
    New customers with normal orders
    Address fraud (same address, different names)
    Reselling patterns (repeat console purchases)
    Repeat offenders (past rejected orders)
    Toxic reviewers with rejection history
    Spam bots (identical reviews across products)
    Fake reviewers (reviewing unpurchased products)
    Edge cases (good customer suspicious order, and vice versa)
"""

from datetime import datetime, timedelta


def days_ago(days, hour=10, minute=0):
    """Build a timestamp string for a moment in the recent past."""
    dt = datetime(2026, 7, 19, 5, 0, 0) - timedelta(days=days, hours=-hour, minutes=-minute)
    return dt.strftime("%Y-%m-%d %H:%M:%S")


# =========================================================================
# CUSTOMERS (20 total)
# Each customer has a profile that history will confirm through their orders
# and reviews. The agent never sees this profile directly. It discovers the
# pattern by calling tools against the seeded orders and reviews.
# =========================================================================

CUSTOMER_PROFILES = {
    # ---- Trusted, well behaved (6) ----
    "sarah_mitchell": {
        "name": "Sarah Mitchell",
        "phone": "+1 617-555-0142",
        "address": "45 Beacon Street, Boston, MA 02108",
        "archetype": "loyal_family_customer",
    },
    "emma_chen": {
        "name": "Emma Chen",
        "phone": "+1 415-555-0177",
        "address": "78 Sunset Blvd, San Francisco, CA 94122",
        "archetype": "family_gamer",
    },
    "david_kim": {
        "name": "David Kim",
        "phone": "+1 206-555-0198",
        "address": "312 Pine Avenue, Seattle, WA 98101",
        "archetype": "adult_gamer_returning",
    },
    "olivia_brown": {
        "name": "Olivia Brown",
        "phone": "+1 512-555-0165",
        "address": "890 Oak Lane, Austin, TX 78701",
        "archetype": "casual_buyer",
    },
    "james_wilson": {
        "name": "James Wilson",
        "phone": "+1 303-555-0134",
        "address": "22 Mountain View Rd, Denver, CO 80202",
        "archetype": "collector_positive_reviewer",
    },
    "sophia_martinez": {
        "name": "Sophia Martinez",
        "phone": "+1 305-555-0189",
        "address": "154 Palm Drive, Miami, FL 33139",
        "archetype": "family_gamer",
    },

    # ---- New but normal (3) ----
    "ahmed_hassan": {
        "name": "Ahmed Hassan",
        "phone": "+1 718-555-0121",
        "address": "67 Atlantic Ave, Brooklyn, NY 11217",
        "archetype": "first_time_buyer_normal",
    },
    "lucas_garcia": {
        "name": "Lucas Garcia",
        "phone": "+1 619-555-0156",
        "address": "425 Harbor Way, San Diego, CA 92101",
        "archetype": "first_time_buyer_normal",
    },
    "isabella_wright": {
        "name": "Isabella Wright",
        "phone": "+1 503-555-0143",
        "address": "88 River Street, Portland, OR 97201",
        "archetype": "first_time_buyer_normal",
    },

    # ---- Suspicious patterns (5) ----
    "john_smith_alias1": {
        "name": "John Smith",
        "phone": "+1 213-555-9911",
        "address": "1200 Industrial Park Dr, Los Angeles, CA 90021",
        "archetype": "address_fraud_ring",
    },
    "j_smyth_alias2": {
        "name": "J. Smyth",
        "phone": "+1 213-555-9912",
        "address": "1200 Industrial Park Dr, Los Angeles, CA 90021",
        "archetype": "address_fraud_ring",
    },
    "jonathan_s_alias3": {
        "name": "Jonathan S.",
        "phone": "+1 213-555-9913",
        "address": "1200 Industrial Park Dr, Los Angeles, CA 90021",
        "archetype": "address_fraud_ring",
    },
    "michael_chen_reseller": {
        "name": "Michael Chen",
        "phone": "+1 646-555-0288",
        "address": "500 Commerce Plaza, New York, NY 10013",
        "archetype": "reseller",
    },
    "alex_torres": {
        "name": "Alex Torres",
        "phone": "+1 702-555-0299",
        "address": "9800 Desert Rd, Las Vegas, NV 89109",
        "archetype": "high_value_rejected_history",
    },

    # ---- Repeat offenders on reviews (3) ----
    "absolute_trash_reviewer": {
        "name": "AbsoluteTrashReview",
        "phone": "",
        "address": "",
        "archetype": "toxic_reviewer",
    },
    "spam_bot_99": {
        "name": "SpamBot99",
        "phone": "",
        "address": "",
        "archetype": "spam_reviewer",
    },
    "fake_reviewer": {
        "name": "TotallyRealBuyer",
        "phone": "",
        "address": "",
        "archetype": "fake_reviewer",
    },

    # ---- Edge cases (3) ----
    "rachel_green": {
        "name": "Rachel Green",
        "phone": "+1 212-555-0177",
        "address": "90 Central Park West, New York, NY 10023",
        "archetype": "trusted_but_this_order_looks_odd",
    },
    "kevin_park": {
        "name": "Kevin Park",
        "phone": "+1 408-555-0166",
        "address": "1500 Tech Drive, San Jose, CA 95110",
        "archetype": "past_flagged_now_normal",
    },
    "natalie_foster": {
        "name": "Natalie Foster",
        "phone": "+1 617-555-0201",
        "address": "12 Harvard Square, Cambridge, MA 02138",
        "archetype": "respectful_negative_reviewer",
    },
}


# =========================================================================
# ORDERS (40 total)
# Every order is a snapshot of history the agent can query. The status,
# admin decision, and timestamp are all meaningful.
# =========================================================================

SEED_ORDERS = [
    # ------------------------------------------------------------------
    # Sarah Mitchell: 5 clean approved orders over 3 months, family games
    # Signal: loyal customer, low risk baseline
    # ------------------------------------------------------------------
    {
        "id": "ORD-SEED001",
        "customer_name": "Sarah Mitchell",
        "customer_phone": "+1 617-555-0142",
        "customer_address": "45 Beacon Street, Boston, MA 02108",
        "items": [
            {"product_id": "GAME-006", "product_name": "Mario Kart 8 Deluxe (Switch)",
             "price": 59, "quantity": 1, "subtotal": 59, "age_rating": "Everyone"},
        ],
        "item_count": 1, "subtotal": 59, "shipping": 5, "total": 64,
        "payment": "Cash on delivery", "timestamp": days_ago(95),
        "status": "approved",
        "ai_analysis": {
            "decision": "approve", "risk_level": "low", "flags": [],
            "reason": "Single family friendly item at low total.",
            "recommendation": "No action needed.",
        },
        "admin_decision": "", "admin_note": "",
    },
    {
        "id": "ORD-SEED002",
        "customer_name": "Sarah Mitchell",
        "customer_phone": "+1 617-555-0142",
        "customer_address": "45 Beacon Street, Boston, MA 02108",
        "items": [
            {"product_id": "GAME-004", "product_name": "Minecraft (Switch)",
             "price": 29, "quantity": 1, "subtotal": 29, "age_rating": "Everyone 10+"},
            {"product_id": "ACC-001", "product_name": "PS5 DualSense Controller",
             "price": 69, "quantity": 1, "subtotal": 69, "age_rating": "Everyone"},
        ],
        "item_count": 2, "subtotal": 98, "shipping": 5, "total": 103,
        "payment": "Cash on delivery", "timestamp": days_ago(72),
        "status": "approved",
        "ai_analysis": {
            "decision": "approve", "risk_level": "low", "flags": [],
            "reason": "Two consistent family items, returning customer.",
            "recommendation": "No action needed.",
        },
        "admin_decision": "", "admin_note": "",
    },
    {
        "id": "ORD-SEED003",
        "customer_name": "Sarah Mitchell",
        "customer_phone": "+1 617-555-0142",
        "customer_address": "45 Beacon Street, Boston, MA 02108",
        "items": [
            {"product_id": "GAME-003", "product_name": "EA Sports FC 25 (PS5)",
             "price": 69, "quantity": 1, "subtotal": 69, "age_rating": "Everyone"},
        ],
        "item_count": 1, "subtotal": 69, "shipping": 5, "total": 74,
        "payment": "Cash on delivery", "timestamp": days_ago(48),
        "status": "approved",
        "ai_analysis": {
            "decision": "approve", "risk_level": "low", "flags": [],
            "reason": "Standard sports title, trusted customer.",
            "recommendation": "No action needed.",
        },
        "admin_decision": "", "admin_note": "",
    },
    {
        "id": "ORD-SEED004",
        "customer_name": "Sarah Mitchell",
        "customer_phone": "+1 617-555-0142",
        "customer_address": "45 Beacon Street, Boston, MA 02108",
        "items": [
            {"product_id": "GAME-006", "product_name": "Mario Kart 8 Deluxe (Switch)",
             "price": 59, "quantity": 1, "subtotal": 59, "age_rating": "Everyone"},
            {"product_id": "GAME-004", "product_name": "Minecraft (Switch)",
             "price": 29, "quantity": 1, "subtotal": 29, "age_rating": "Everyone 10+"},
        ],
        "item_count": 2, "subtotal": 88, "shipping": 5, "total": 93,
        "payment": "Cash on delivery", "timestamp": days_ago(30),
        "status": "approved",
        "ai_analysis": {
            "decision": "approve", "risk_level": "low", "flags": [],
            "reason": "Family Switch titles, consistent history.",
            "recommendation": "No action needed.",
        },
        "admin_decision": "", "admin_note": "",
    },
    {
        "id": "ORD-SEED005",
        "customer_name": "Sarah Mitchell",
        "customer_phone": "+1 617-555-0142",
        "customer_address": "45 Beacon Street, Boston, MA 02108",
        "items": [
            {"product_id": "ACC-003", "product_name": "HyperX Cloud III Gaming Headset",
             "price": 79, "quantity": 1, "subtotal": 79, "age_rating": "Everyone"},
        ],
        "item_count": 1, "subtotal": 79, "shipping": 5, "total": 84,
        "payment": "Cash on delivery", "timestamp": days_ago(12),
        "status": "approved",
        "ai_analysis": {
            "decision": "approve", "risk_level": "low", "flags": [],
            "reason": "Single accessory, trusted long term customer.",
            "recommendation": "No action needed.",
        },
        "admin_decision": "", "admin_note": "",
    },

    # ------------------------------------------------------------------
    # Emma Chen: 4 family orders, all approved
    # ------------------------------------------------------------------
    {
        "id": "ORD-SEED006",
        "customer_name": "Emma Chen",
        "customer_phone": "+1 415-555-0177",
        "customer_address": "78 Sunset Blvd, San Francisco, CA 94122",
        "items": [
            {"product_id": "CON-003", "product_name": "Nintendo Switch OLED",
             "price": 349, "quantity": 1, "subtotal": 349, "age_rating": "Everyone"},
        ],
        "item_count": 1, "subtotal": 349, "shipping": 0, "total": 349,
        "payment": "Cash on delivery", "timestamp": days_ago(85),
        "status": "approved",
        "ai_analysis": {
            "decision": "approve", "risk_level": "low", "flags": [],
            "reason": "Single console purchase, reasonable total, family friendly.",
            "recommendation": "No action needed.",
        },
        "admin_decision": "", "admin_note": "",
    },
    {
        "id": "ORD-SEED007",
        "customer_name": "Emma Chen",
        "customer_phone": "+1 415-555-0177",
        "customer_address": "78 Sunset Blvd, San Francisco, CA 94122",
        "items": [
            {"product_id": "GAME-004", "product_name": "Minecraft (Switch)",
             "price": 29, "quantity": 1, "subtotal": 29, "age_rating": "Everyone 10+"},
            {"product_id": "GAME-006", "product_name": "Mario Kart 8 Deluxe (Switch)",
             "price": 59, "quantity": 1, "subtotal": 59, "age_rating": "Everyone"},
        ],
        "item_count": 2, "subtotal": 88, "shipping": 5, "total": 93,
        "payment": "Cash on delivery", "timestamp": days_ago(80),
        "status": "approved",
        "ai_analysis": {
            "decision": "approve", "risk_level": "low", "flags": [],
            "reason": "Family Switch bundle after console purchase.",
            "recommendation": "No action needed.",
        },
        "admin_decision": "", "admin_note": "",
    },
    {
        "id": "ORD-SEED008",
        "customer_name": "Emma Chen",
        "customer_phone": "+1 415-555-0177",
        "customer_address": "78 Sunset Blvd, San Francisco, CA 94122",
        "items": [
            {"product_id": "GAME-006", "product_name": "Mario Kart 8 Deluxe (Switch)",
             "price": 59, "quantity": 1, "subtotal": 59, "age_rating": "Everyone"},
        ],
        "item_count": 1, "subtotal": 59, "shipping": 5, "total": 64,
        "payment": "Cash on delivery", "timestamp": days_ago(50),
        "status": "approved",
        "ai_analysis": {
            "decision": "approve", "risk_level": "low", "flags": [],
            "reason": "Repeat family gaming purchase.",
            "recommendation": "No action needed.",
        },
        "admin_decision": "", "admin_note": "",
    },
    {
        "id": "ORD-SEED009",
        "customer_name": "Emma Chen",
        "customer_phone": "+1 415-555-0177",
        "customer_address": "78 Sunset Blvd, San Francisco, CA 94122",
        "items": [
            {"product_id": "GAME-004", "product_name": "Minecraft (Switch)",
             "price": 29, "quantity": 2, "subtotal": 58, "age_rating": "Everyone 10+"},
        ],
        "item_count": 2, "subtotal": 58, "shipping": 5, "total": 63,
        "payment": "Cash on delivery", "timestamp": days_ago(20),
        "status": "approved",
        "ai_analysis": {
            "decision": "approve", "risk_level": "low", "flags": [],
            "reason": "Two copies of family game, likely for siblings.",
            "recommendation": "No action needed.",
        },
        "admin_decision": "", "admin_note": "",
    },

    # ------------------------------------------------------------------
    # David Kim: 3 approved adult game orders
    # ------------------------------------------------------------------
    {
        "id": "ORD-SEED010",
        "customer_name": "David Kim",
        "customer_phone": "+1 206-555-0198",
        "customer_address": "312 Pine Avenue, Seattle, WA 98101",
        "items": [
            {"product_id": "GAME-001", "product_name": "God of War Ragnarok (PS5)",
             "price": 59, "quantity": 1, "subtotal": 59, "age_rating": "17+"},
        ],
        "item_count": 1, "subtotal": 59, "shipping": 5, "total": 64,
        "payment": "Cash on delivery", "timestamp": days_ago(60),
        "status": "approved",
        "ai_analysis": {
            "decision": "approve", "risk_level": "low", "flags": [],
            "reason": "Single adult title, consistent buyer profile.",
            "recommendation": "No action needed.",
        },
        "admin_decision": "", "admin_note": "",
    },
    {
        "id": "ORD-SEED011",
        "customer_name": "David Kim",
        "customer_phone": "+1 206-555-0198",
        "customer_address": "312 Pine Avenue, Seattle, WA 98101",
        "items": [
            {"product_id": "GAME-005", "product_name": "Call of Duty MW3 (Xbox)",
             "price": 69, "quantity": 1, "subtotal": 69, "age_rating": "18+"},
        ],
        "item_count": 1, "subtotal": 69, "shipping": 5, "total": 74,
        "payment": "Cash on delivery", "timestamp": days_ago(35),
        "status": "approved",
        "ai_analysis": {
            "decision": "approve", "risk_level": "low", "flags": [],
            "reason": "Single 18+ title, aligned with buyer history.",
            "recommendation": "No action needed.",
        },
        "admin_decision": "", "admin_note": "",
    },
    {
        "id": "ORD-SEED012",
        "customer_name": "David Kim",
        "customer_phone": "+1 206-555-0198",
        "customer_address": "312 Pine Avenue, Seattle, WA 98101",
        "items": [
            {"product_id": "SUB-001", "product_name": "Xbox Game Pass Ultimate 12 Month",
             "price": 119, "quantity": 1, "subtotal": 119, "age_rating": "Everyone"},
        ],
        "item_count": 1, "subtotal": 119, "shipping": 0, "total": 119,
        "payment": "Cash on delivery", "timestamp": days_ago(10),
        "status": "approved",
        "ai_analysis": {
            "decision": "approve", "risk_level": "low", "flags": [],
            "reason": "Subscription purchase from repeat customer.",
            "recommendation": "No action needed.",
        },
        "admin_decision": "", "admin_note": "",
    },

    # ------------------------------------------------------------------
    # Olivia Brown, James Wilson, Sophia Martinez: normal history
    # ------------------------------------------------------------------
    {
        "id": "ORD-SEED013",
        "customer_name": "Olivia Brown",
        "customer_phone": "+1 512-555-0165",
        "customer_address": "890 Oak Lane, Austin, TX 78701",
        "items": [
            {"product_id": "GAME-007", "product_name": "Horizon Forbidden West (PS5)",
             "price": 49, "quantity": 1, "subtotal": 49, "age_rating": "16+"},
        ],
        "item_count": 1, "subtotal": 49, "shipping": 5, "total": 54,
        "payment": "Cash on delivery", "timestamp": days_ago(55),
        "status": "approved",
        "ai_analysis": {
            "decision": "approve", "risk_level": "low", "flags": [],
            "reason": "Single mainstream title.",
            "recommendation": "No action needed.",
        },
        "admin_decision": "", "admin_note": "",
    },
    {
        "id": "ORD-SEED014",
        "customer_name": "Olivia Brown",
        "customer_phone": "+1 512-555-0165",
        "customer_address": "890 Oak Lane, Austin, TX 78701",
        "items": [
            {"product_id": "ACC-004", "product_name": "PlayStation HD Camera",
             "price": 59, "quantity": 1, "subtotal": 59, "age_rating": "Everyone"},
        ],
        "item_count": 1, "subtotal": 59, "shipping": 5, "total": 64,
        "payment": "Cash on delivery", "timestamp": days_ago(25),
        "status": "approved",
        "ai_analysis": {
            "decision": "approve", "risk_level": "low", "flags": [],
            "reason": "Single accessory.",
            "recommendation": "No action needed.",
        },
        "admin_decision": "", "admin_note": "",
    },
    {
        "id": "ORD-SEED015",
        "customer_name": "James Wilson",
        "customer_phone": "+1 303-555-0134",
        "customer_address": "22 Mountain View Rd, Denver, CO 80202",
        "items": [
            {"product_id": "CON-001", "product_name": "PlayStation 5 Slim",
             "price": 449, "quantity": 1, "subtotal": 449, "age_rating": "Everyone"},
        ],
        "item_count": 1, "subtotal": 449, "shipping": 0, "total": 449,
        "payment": "Cash on delivery", "timestamp": days_ago(90),
        "status": "approved",
        "ai_analysis": {
            "decision": "approve", "risk_level": "low", "flags": [],
            "reason": "Single console purchase, below suspicious threshold.",
            "recommendation": "No action needed.",
        },
        "admin_decision": "", "admin_note": "",
    },
    {
        "id": "ORD-SEED016",
        "customer_name": "James Wilson",
        "customer_phone": "+1 303-555-0134",
        "customer_address": "22 Mountain View Rd, Denver, CO 80202",
        "items": [
            {"product_id": "GAME-001", "product_name": "God of War Ragnarok (PS5)",
             "price": 59, "quantity": 1, "subtotal": 59, "age_rating": "17+"},
            {"product_id": "GAME-007", "product_name": "Horizon Forbidden West (PS5)",
             "price": 49, "quantity": 1, "subtotal": 49, "age_rating": "16+"},
        ],
        "item_count": 2, "subtotal": 108, "shipping": 0, "total": 108,
        "payment": "Cash on delivery", "timestamp": days_ago(75),
        "status": "approved",
        "ai_analysis": {
            "decision": "approve", "risk_level": "low", "flags": [],
            "reason": "Two consistent PS5 titles following console purchase.",
            "recommendation": "No action needed.",
        },
        "admin_decision": "", "admin_note": "",
    },
    {
        "id": "ORD-SEED017",
        "customer_name": "Sophia Martinez",
        "customer_phone": "+1 305-555-0189",
        "customer_address": "154 Palm Drive, Miami, FL 33139",
        "items": [
            {"product_id": "GAME-006", "product_name": "Mario Kart 8 Deluxe (Switch)",
             "price": 59, "quantity": 1, "subtotal": 59, "age_rating": "Everyone"},
        ],
        "item_count": 1, "subtotal": 59, "shipping": 5, "total": 64,
        "payment": "Cash on delivery", "timestamp": days_ago(40),
        "status": "approved",
        "ai_analysis": {
            "decision": "approve", "risk_level": "low", "flags": [],
            "reason": "Single family title.",
            "recommendation": "No action needed.",
        },
        "admin_decision": "", "admin_note": "",
    },
    {
        "id": "ORD-SEED018",
        "customer_name": "Sophia Martinez",
        "customer_phone": "+1 305-555-0189",
        "customer_address": "154 Palm Drive, Miami, FL 33139",
        "items": [
            {"product_id": "GAME-004", "product_name": "Minecraft (Switch)",
             "price": 29, "quantity": 1, "subtotal": 29, "age_rating": "Everyone 10+"},
        ],
        "item_count": 1, "subtotal": 29, "shipping": 5, "total": 34,
        "payment": "Cash on delivery", "timestamp": days_ago(15),
        "status": "approved",
        "ai_analysis": {
            "decision": "approve", "risk_level": "low", "flags": [],
            "reason": "Single family title.",
            "recommendation": "No action needed.",
        },
        "admin_decision": "", "admin_note": "",
    },

    # ------------------------------------------------------------------
    # First time buyers (Ahmed, Lucas, Isabella): normal small orders
    # ------------------------------------------------------------------
    {
        "id": "ORD-SEED019",
        "customer_name": "Ahmed Hassan",
        "customer_phone": "+1 718-555-0121",
        "customer_address": "67 Atlantic Ave, Brooklyn, NY 11217",
        "items": [
            {"product_id": "GAME-003", "product_name": "EA Sports FC 25 (PS5)",
             "price": 69, "quantity": 1, "subtotal": 69, "age_rating": "Everyone"},
        ],
        "item_count": 1, "subtotal": 69, "shipping": 5, "total": 74,
        "payment": "Cash on delivery", "timestamp": days_ago(3),
        "status": "approved",
        "ai_analysis": {
            "decision": "approve", "risk_level": "low", "flags": [],
            "reason": "First order, small total, mainstream item.",
            "recommendation": "No action needed.",
        },
        "admin_decision": "", "admin_note": "",
    },
    {
        "id": "ORD-SEED020",
        "customer_name": "Lucas Garcia",
        "customer_phone": "+1 619-555-0156",
        "customer_address": "425 Harbor Way, San Diego, CA 92101",
        "items": [
            {"product_id": "ACC-001", "product_name": "PS5 DualSense Controller",
             "price": 69, "quantity": 1, "subtotal": 69, "age_rating": "Everyone"},
        ],
        "item_count": 1, "subtotal": 69, "shipping": 5, "total": 74,
        "payment": "Cash on delivery", "timestamp": days_ago(2),
        "status": "approved",
        "ai_analysis": {
            "decision": "approve", "risk_level": "low", "flags": [],
            "reason": "Single accessory, low value first order.",
            "recommendation": "No action needed.",
        },
        "admin_decision": "", "admin_note": "",
    },
    {
        "id": "ORD-SEED021",
        "customer_name": "Isabella Wright",
        "customer_phone": "+1 503-555-0143",
        "customer_address": "88 River Street, Portland, OR 97201",
        "items": [
            {"product_id": "GAME-006", "product_name": "Mario Kart 8 Deluxe (Switch)",
             "price": 59, "quantity": 1, "subtotal": 59, "age_rating": "Everyone"},
        ],
        "item_count": 1, "subtotal": 59, "shipping": 5, "total": 64,
        "payment": "Cash on delivery", "timestamp": days_ago(5),
        "status": "approved",
        "ai_analysis": {
            "decision": "approve", "risk_level": "low", "flags": [],
            "reason": "First order, single family game.",
            "recommendation": "No action needed.",
        },
        "admin_decision": "", "admin_note": "",
    },

    # ------------------------------------------------------------------
    # ADDRESS FRAUD RING at 1200 Industrial Park Dr, LA
    # Same address, three near identical names, all previously flagged
    # ------------------------------------------------------------------
    {
        "id": "ORD-SEED022",
        "customer_name": "John Smith",
        "customer_phone": "+1 213-555-9911",
        "customer_address": "1200 Industrial Park Dr, Los Angeles, CA 90021",
        "items": [
            {"product_id": "CON-001", "product_name": "PlayStation 5 Slim",
             "price": 449, "quantity": 1, "subtotal": 449, "age_rating": "Everyone"},
            {"product_id": "ACC-001", "product_name": "PS5 DualSense Controller",
             "price": 69, "quantity": 2, "subtotal": 138, "age_rating": "Everyone"},
        ],
        "item_count": 3, "subtotal": 587, "shipping": 0, "total": 587,
        "payment": "Cash on delivery", "timestamp": days_ago(45),
        "status": "rejected",
        "ai_analysis": {
            "decision": "flag_for_review", "risk_level": "high",
            "flags": ["Total exceeds suspicious threshold", "Console plus multiple controllers"],
            "reason": "New customer, high total, console with two controllers is a common resale bundle.",
            "recommendation": "Verify identity before shipping.",
        },
        "admin_decision": "reject", "admin_note": "Suspected reseller, rejected",
    },
    {
        "id": "ORD-SEED023",
        "customer_name": "J. Smyth",
        "customer_phone": "+1 213-555-9912",
        "customer_address": "1200 Industrial Park Dr, Los Angeles, CA 90021",
        "items": [
            {"product_id": "CON-002", "product_name": "Xbox Series X",
             "price": 499, "quantity": 1, "subtotal": 499, "age_rating": "Everyone"},
        ],
        "item_count": 1, "subtotal": 499, "shipping": 0, "total": 499,
        "payment": "Cash on delivery", "timestamp": days_ago(28),
        "status": "rejected",
        "ai_analysis": {
            "decision": "flag_for_review", "risk_level": "high",
            "flags": ["Same address as previously flagged order", "High value console"],
            "reason": "Address 1200 Industrial Park Dr already tied to a rejected order under name John Smith.",
            "recommendation": "Reject and blacklist address.",
        },
        "admin_decision": "reject", "admin_note": "Same address as ORD-SEED022, likely alias",
    },
    {
        "id": "ORD-SEED024",
        "customer_name": "Jonathan S.",
        "customer_phone": "+1 213-555-9913",
        "customer_address": "1200 Industrial Park Dr, Los Angeles, CA 90021",
        "items": [
            {"product_id": "CON-001", "product_name": "PlayStation 5 Slim",
             "price": 449, "quantity": 1, "subtotal": 449, "age_rating": "Everyone"},
        ],
        "item_count": 1, "subtotal": 449, "shipping": 0, "total": 449,
        "payment": "Cash on delivery", "timestamp": days_ago(14),
        "status": "rejected",
        "ai_analysis": {
            "decision": "flag_for_review", "risk_level": "high",
            "flags": ["Address fraud pattern", "Console purchase"],
            "reason": "Third order to the same address with a near variant of the name John Smith.",
            "recommendation": "Reject.",
        },
        "admin_decision": "reject", "admin_note": "Third alias at same address",
    },

    # ------------------------------------------------------------------
    # Michael Chen: reselling pattern, 4 console orders in short time
    # ------------------------------------------------------------------
    {
        "id": "ORD-SEED025",
        "customer_name": "Michael Chen",
        "customer_phone": "+1 646-555-0288",
        "customer_address": "500 Commerce Plaza, New York, NY 10013",
        "items": [
            {"product_id": "CON-001", "product_name": "PlayStation 5 Slim",
             "price": 449, "quantity": 1, "subtotal": 449, "age_rating": "Everyone"},
        ],
        "item_count": 1, "subtotal": 449, "shipping": 0, "total": 449,
        "payment": "Cash on delivery", "timestamp": days_ago(38),
        "status": "approved",
        "ai_analysis": {
            "decision": "approve", "risk_level": "low", "flags": [],
            "reason": "Single console below threshold.",
            "recommendation": "No action needed.",
        },
        "admin_decision": "", "admin_note": "",
    },
    {
        "id": "ORD-SEED026",
        "customer_name": "Michael Chen",
        "customer_phone": "+1 646-555-0288",
        "customer_address": "500 Commerce Plaza, New York, NY 10013",
        "items": [
            {"product_id": "CON-001", "product_name": "PlayStation 5 Slim",
             "price": 449, "quantity": 1, "subtotal": 449, "age_rating": "Everyone"},
        ],
        "item_count": 1, "subtotal": 449, "shipping": 0, "total": 449,
        "payment": "Cash on delivery", "timestamp": days_ago(27),
        "status": "rejected",
        "ai_analysis": {
            "decision": "flag_for_review", "risk_level": "medium",
            "flags": ["Second identical console within a month"],
            "reason": "Same customer purchased a second PS5 eleven days after the first, possible reseller.",
            "recommendation": "Contact customer before shipping.",
        },
        "admin_decision": "reject", "admin_note": "Reseller pattern",
    },
    {
        "id": "ORD-SEED027",
        "customer_name": "Michael Chen",
        "customer_phone": "+1 646-555-0288",
        "customer_address": "500 Commerce Plaza, New York, NY 10013",
        "items": [
            {"product_id": "CON-002", "product_name": "Xbox Series X",
             "price": 499, "quantity": 1, "subtotal": 499, "age_rating": "Everyone"},
        ],
        "item_count": 1, "subtotal": 499, "shipping": 0, "total": 499,
        "payment": "Cash on delivery", "timestamp": days_ago(18),
        "status": "rejected",
        "ai_analysis": {
            "decision": "flag_for_review", "risk_level": "high",
            "flags": ["Third console order this month", "Reseller pattern confirmed"],
            "reason": "Third console purchase in under 30 days, now switching to Xbox.",
            "recommendation": "Reject.",
        },
        "admin_decision": "reject", "admin_note": "Confirmed reseller",
    },

    # ------------------------------------------------------------------
    # Alex Torres: high value, previously rejected
    # ------------------------------------------------------------------
    {
        "id": "ORD-SEED028",
        "customer_name": "Alex Torres",
        "customer_phone": "+1 702-555-0299",
        "customer_address": "9800 Desert Rd, Las Vegas, NV 89109",
        "items": [
            {"product_id": "CON-002", "product_name": "Xbox Series X",
             "price": 499, "quantity": 2, "subtotal": 998, "age_rating": "Everyone"},
        ],
        "item_count": 2, "subtotal": 998, "shipping": 0, "total": 998,
        "payment": "Cash on delivery", "timestamp": days_ago(50),
        "status": "rejected",
        "ai_analysis": {
            "decision": "flag_for_review", "risk_level": "high",
            "flags": ["Two identical consoles", "Total near 1000"],
            "reason": "Two Xbox Series X consoles at once is a clear reselling signal.",
            "recommendation": "Reject.",
        },
        "admin_decision": "reject", "admin_note": "Bulk console rejected",
    },
    {
        "id": "ORD-SEED029",
        "customer_name": "Alex Torres",
        "customer_phone": "+1 702-555-0299",
        "customer_address": "9800 Desert Rd, Las Vegas, NV 89109",
        "items": [
            {"product_id": "CON-001", "product_name": "PlayStation 5 Slim",
             "price": 449, "quantity": 1, "subtotal": 449, "age_rating": "Everyone"},
            {"product_id": "ACC-002", "product_name": "Xbox Elite Controller Series 2",
             "price": 179, "quantity": 1, "subtotal": 179, "age_rating": "Everyone"},
        ],
        "item_count": 2, "subtotal": 628, "shipping": 0, "total": 628,
        "payment": "Cash on delivery", "timestamp": days_ago(22),
        "status": "rejected",
        "ai_analysis": {
            "decision": "flag_for_review", "risk_level": "high",
            "flags": ["High total", "Previously rejected customer"],
            "reason": "Customer has prior rejected order, new order still over 500 threshold.",
            "recommendation": "Reject.",
        },
        "admin_decision": "reject", "admin_note": "Second rejection for this customer",
    },

    # ------------------------------------------------------------------
    # Rachel Green: trusted history, one odd order
    # ------------------------------------------------------------------
    {
        "id": "ORD-SEED030",
        "customer_name": "Rachel Green",
        "customer_phone": "+1 212-555-0177",
        "customer_address": "90 Central Park West, New York, NY 10023",
        "items": [
            {"product_id": "GAME-003", "product_name": "EA Sports FC 25 (PS5)",
             "price": 69, "quantity": 1, "subtotal": 69, "age_rating": "Everyone"},
        ],
        "item_count": 1, "subtotal": 69, "shipping": 5, "total": 74,
        "payment": "Cash on delivery", "timestamp": days_ago(70),
        "status": "approved",
        "ai_analysis": {
            "decision": "approve", "risk_level": "low", "flags": [],
            "reason": "Single mainstream title.",
            "recommendation": "No action needed.",
        },
        "admin_decision": "", "admin_note": "",
    },
    {
        "id": "ORD-SEED031",
        "customer_name": "Rachel Green",
        "customer_phone": "+1 212-555-0177",
        "customer_address": "90 Central Park West, New York, NY 10023",
        "items": [
            {"product_id": "GAME-006", "product_name": "Mario Kart 8 Deluxe (Switch)",
             "price": 59, "quantity": 1, "subtotal": 59, "age_rating": "Everyone"},
        ],
        "item_count": 1, "subtotal": 59, "shipping": 5, "total": 64,
        "payment": "Cash on delivery", "timestamp": days_ago(42),
        "status": "approved",
        "ai_analysis": {
            "decision": "approve", "risk_level": "low", "flags": [],
            "reason": "Single family title.",
            "recommendation": "No action needed.",
        },
        "admin_decision": "", "admin_note": "",
    },
    {
        "id": "ORD-SEED032",
        "customer_name": "Rachel Green",
        "customer_phone": "+1 212-555-0177",
        "customer_address": "90 Central Park West, New York, NY 10023",
        "items": [
            {"product_id": "ACC-003", "product_name": "HyperX Cloud III Gaming Headset",
             "price": 79, "quantity": 1, "subtotal": 79, "age_rating": "Everyone"},
        ],
        "item_count": 1, "subtotal": 79, "shipping": 5, "total": 84,
        "payment": "Cash on delivery", "timestamp": days_ago(20),
        "status": "approved",
        "ai_analysis": {
            "decision": "approve", "risk_level": "low", "flags": [],
            "reason": "Single accessory.",
            "recommendation": "No action needed.",
        },
        "admin_decision": "", "admin_note": "",
    },

    # ------------------------------------------------------------------
    # Kevin Park: past flagged order, now clean recent activity
    # ------------------------------------------------------------------
    {
        "id": "ORD-SEED033",
        "customer_name": "Kevin Park",
        "customer_phone": "+1 408-555-0166",
        "customer_address": "1500 Tech Drive, San Jose, CA 95110",
        "items": [
            {"product_id": "CON-001", "product_name": "PlayStation 5 Slim",
             "price": 449, "quantity": 1, "subtotal": 449, "age_rating": "Everyone"},
            {"product_id": "GAME-002", "product_name": "GTA V Premium Edition (PS5)",
             "price": 29, "quantity": 1, "subtotal": 29, "age_rating": "18+"},
            {"product_id": "GAME-004", "product_name": "Minecraft (Switch)",
             "price": 29, "quantity": 1, "subtotal": 29, "age_rating": "Everyone 10+"},
        ],
        "item_count": 3, "subtotal": 507, "shipping": 0, "total": 507,
        "payment": "Cash on delivery", "timestamp": days_ago(88),
        "status": "approved",
        "ai_analysis": {
            "decision": "flag_for_review", "risk_level": "medium",
            "flags": ["Total just above threshold", "Mixed age ratings"],
            "reason": "Console with mixed age rated games, total slightly above 500.",
            "recommendation": "Confirm buyer.",
        },
        "admin_decision": "approve", "admin_note": "Legit family purchase after confirmation",
    },
    {
        "id": "ORD-SEED034",
        "customer_name": "Kevin Park",
        "customer_phone": "+1 408-555-0166",
        "customer_address": "1500 Tech Drive, San Jose, CA 95110",
        "items": [
            {"product_id": "GAME-006", "product_name": "Mario Kart 8 Deluxe (Switch)",
             "price": 59, "quantity": 1, "subtotal": 59, "age_rating": "Everyone"},
        ],
        "item_count": 1, "subtotal": 59, "shipping": 5, "total": 64,
        "payment": "Cash on delivery", "timestamp": days_ago(45),
        "status": "approved",
        "ai_analysis": {
            "decision": "approve", "risk_level": "low", "flags": [],
            "reason": "Single family title.",
            "recommendation": "No action needed.",
        },
        "admin_decision": "", "admin_note": "",
    },
    {
        "id": "ORD-SEED035",
        "customer_name": "Kevin Park",
        "customer_phone": "+1 408-555-0166",
        "customer_address": "1500 Tech Drive, San Jose, CA 95110",
        "items": [
            {"product_id": "GAME-003", "product_name": "EA Sports FC 25 (PS5)",
             "price": 69, "quantity": 1, "subtotal": 69, "age_rating": "Everyone"},
        ],
        "item_count": 1, "subtotal": 69, "shipping": 5, "total": 74,
        "payment": "Cash on delivery", "timestamp": days_ago(18),
        "status": "approved",
        "ai_analysis": {
            "decision": "approve", "risk_level": "low", "flags": [],
            "reason": "Single mainstream title.",
            "recommendation": "No action needed.",
        },
        "admin_decision": "", "admin_note": "",
    },

    # ------------------------------------------------------------------
    # Natalie Foster: 2 approved orders, will pair with respectful negative review
    # ------------------------------------------------------------------
    {
        "id": "ORD-SEED036",
        "customer_name": "Natalie Foster",
        "customer_phone": "+1 617-555-0201",
        "customer_address": "12 Harvard Square, Cambridge, MA 02138",
        "items": [
            {"product_id": "GAME-001", "product_name": "God of War Ragnarok (PS5)",
             "price": 59, "quantity": 1, "subtotal": 59, "age_rating": "17+"},
        ],
        "item_count": 1, "subtotal": 59, "shipping": 5, "total": 64,
        "payment": "Cash on delivery", "timestamp": days_ago(58),
        "status": "approved",
        "ai_analysis": {
            "decision": "approve", "risk_level": "low", "flags": [],
            "reason": "Single adult title.",
            "recommendation": "No action needed.",
        },
        "admin_decision": "", "admin_note": "",
    },
    {
        "id": "ORD-SEED037",
        "customer_name": "Natalie Foster",
        "customer_phone": "+1 617-555-0201",
        "customer_address": "12 Harvard Square, Cambridge, MA 02138",
        "items": [
            {"product_id": "GAME-005", "product_name": "Call of Duty MW3 (Xbox)",
             "price": 69, "quantity": 1, "subtotal": 69, "age_rating": "18+"},
        ],
        "item_count": 1, "subtotal": 69, "shipping": 5, "total": 74,
        "payment": "Cash on delivery", "timestamp": days_ago(33),
        "status": "approved",
        "ai_analysis": {
            "decision": "approve", "risk_level": "low", "flags": [],
            "reason": "Single 18+ title, aligned with buyer history.",
            "recommendation": "No action needed.",
        },
        "admin_decision": "", "admin_note": "",
    },

    # ------------------------------------------------------------------
    # James Wilson extra positive purchase to back positive reviews
    # ------------------------------------------------------------------
    {
        "id": "ORD-SEED038",
        "customer_name": "James Wilson",
        "customer_phone": "+1 303-555-0134",
        "customer_address": "22 Mountain View Rd, Denver, CO 80202",
        "items": [
            {"product_id": "GAME-006", "product_name": "Mario Kart 8 Deluxe (Switch)",
             "price": 59, "quantity": 1, "subtotal": 59, "age_rating": "Everyone"},
        ],
        "item_count": 1, "subtotal": 59, "shipping": 5, "total": 64,
        "payment": "Cash on delivery", "timestamp": days_ago(40),
        "status": "approved",
        "ai_analysis": {
            "decision": "approve", "risk_level": "low", "flags": [],
            "reason": "Single family title from repeat customer.",
            "recommendation": "No action needed.",
        },
        "admin_decision": "", "admin_note": "",
    },
    {
        "id": "ORD-SEED039",
        "customer_name": "James Wilson",
        "customer_phone": "+1 303-555-0134",
        "customer_address": "22 Mountain View Rd, Denver, CO 80202",
        "items": [
            {"product_id": "GAME-005", "product_name": "Call of Duty MW3 (Xbox)",
             "price": 69, "quantity": 1, "subtotal": 69, "age_rating": "18+"},
        ],
        "item_count": 1, "subtotal": 69, "shipping": 5, "total": 74,
        "payment": "Cash on delivery", "timestamp": days_ago(20),
        "status": "approved",
        "ai_analysis": {
            "decision": "approve", "risk_level": "low", "flags": [],
            "reason": "Single 18+ title from repeat customer.",
            "recommendation": "No action needed.",
        },
        "admin_decision": "", "admin_note": "",
    },
    {
        "id": "ORD-SEED040",
        "customer_name": "David Kim",
        "customer_phone": "+1 206-555-0198",
        "customer_address": "312 Pine Avenue, Seattle, WA 98101",
        "items": [
            {"product_id": "GAME-001", "product_name": "God of War Ragnarok (PS5)",
             "price": 59, "quantity": 1, "subtotal": 59, "age_rating": "17+"},
        ],
        "item_count": 1, "subtotal": 59, "shipping": 5, "total": 64,
        "payment": "Cash on delivery", "timestamp": days_ago(4),
        "status": "approved",
        "ai_analysis": {
            "decision": "approve", "risk_level": "low", "flags": [],
            "reason": "Single 17+ title from repeat customer.",
            "recommendation": "No action needed.",
        },
        "admin_decision": "", "admin_note": "",
    },
]


# =========================================================================
# REVIEWS (30 total)
# Reviews tied to real seed orders so verify_customer_purchased works.
# Toxic and spam reviewers have clear rejection histories.
# =========================================================================

SEED_REVIEWS = [
    # ---- Sarah Mitchell: 3 positive reviews on games she bought ----
    {
        "id": "REV-SEED001",
        "product_id": "GAME-006",
        "customer_name": "Sarah Mitchell",
        "rating": 5,
        "text": "Mario Kart never gets old. My kids love the new tracks and the DLC content is excellent value.",
        "timestamp": days_ago(90),
        "status": "published",
        "ai_analysis": {
            "decision": "auto_publish",
            "reason": "Positive review from verified buyer.",
            "toxicity_level": "none",
            "category": "positive",
        },
        "admin_decision": "", "admin_note": "",
    },
    {
        "id": "REV-SEED002",
        "product_id": "GAME-004",
        "customer_name": "Sarah Mitchell",
        "rating": 5,
        "text": "Minecraft is a great creative outlet for my children. Runs smoothly on Switch.",
        "timestamp": days_ago(68),
        "status": "published",
        "ai_analysis": {
            "decision": "auto_publish",
            "reason": "Positive product focused review.",
            "toxicity_level": "none",
            "category": "positive",
        },
        "admin_decision": "", "admin_note": "",
    },
    {
        "id": "REV-SEED003",
        "product_id": "GAME-003",
        "customer_name": "Sarah Mitchell",
        "rating": 4,
        "text": "Good football game overall. Menu navigation could be smoother but gameplay is solid.",
        "timestamp": days_ago(44),
        "status": "published",
        "ai_analysis": {
            "decision": "auto_publish",
            "reason": "Balanced positive review with constructive note.",
            "toxicity_level": "none",
            "category": "positive",
        },
        "admin_decision": "", "admin_note": "",
    },

    # ---- Emma Chen: 3 positive family reviews ----
    {
        "id": "REV-SEED004",
        "product_id": "CON-003",
        "customer_name": "Emma Chen",
        "rating": 5,
        "text": "The OLED screen is beautiful and the whole family enjoys handheld mode. Perfect purchase.",
        "timestamp": days_ago(83),
        "status": "published",
        "ai_analysis": {
            "decision": "auto_publish",
            "reason": "Verified positive review.",
            "toxicity_level": "none",
            "category": "positive",
        },
        "admin_decision": "", "admin_note": "",
    },
    {
        "id": "REV-SEED005",
        "product_id": "GAME-004",
        "customer_name": "Emma Chen",
        "rating": 5,
        "text": "Endless fun. My daughter has built entire villages and loves the survival mode.",
        "timestamp": days_ago(76),
        "status": "published",
        "ai_analysis": {
            "decision": "auto_publish",
            "reason": "Personal positive review.",
            "toxicity_level": "none",
            "category": "positive",
        },
        "admin_decision": "", "admin_note": "",
    },
    {
        "id": "REV-SEED006",
        "product_id": "GAME-006",
        "customer_name": "Emma Chen",
        "rating": 5,
        "text": "Party game gold. Local multiplayer with the family is a weekend tradition now.",
        "timestamp": days_ago(48),
        "status": "published",
        "ai_analysis": {
            "decision": "auto_publish",
            "reason": "Positive review from verified buyer.",
            "toxicity_level": "none",
            "category": "positive",
        },
        "admin_decision": "", "admin_note": "",
    },

    # ---- David Kim: 3 positive reviews on titles he owns ----
    {
        "id": "REV-SEED007",
        "product_id": "GAME-001",
        "customer_name": "David Kim",
        "rating": 5,
        "text": "One of the best action adventures I have ever played. Story, combat, and visuals all exceptional.",
        "timestamp": days_ago(58),
        "status": "published",
        "ai_analysis": {
            "decision": "auto_publish",
            "reason": "Verified positive review.",
            "toxicity_level": "none",
            "category": "positive",
        },
        "admin_decision": "", "admin_note": "",
    },
    {
        "id": "REV-SEED008",
        "product_id": "GAME-005",
        "customer_name": "David Kim",
        "rating": 4,
        "text": "Great multiplayer, campaign is decent. Install size is huge though.",
        "timestamp": days_ago(32),
        "status": "published",
        "ai_analysis": {
            "decision": "auto_publish",
            "reason": "Balanced positive review with a specific concern.",
            "toxicity_level": "none",
            "category": "positive",
        },
        "admin_decision": "", "admin_note": "",
    },
    {
        "id": "REV-SEED009",
        "product_id": "SUB-001",
        "customer_name": "David Kim",
        "rating": 5,
        "text": "Best value in gaming. Cloud saves and day one releases keep me subscribed.",
        "timestamp": days_ago(8),
        "status": "published",
        "ai_analysis": {
            "decision": "auto_publish",
            "reason": "Verified positive review.",
            "toxicity_level": "none",
            "category": "positive",
        },
        "admin_decision": "", "admin_note": "",
    },

    # ---- James Wilson: 2 positive collector style reviews ----
    {
        "id": "REV-SEED010",
        "product_id": "CON-001",
        "customer_name": "James Wilson",
        "rating": 5,
        "text": "Setup was easy, SSD load times are incredible. Very happy with the slim form factor.",
        "timestamp": days_ago(88),
        "status": "published",
        "ai_analysis": {
            "decision": "auto_publish",
            "reason": "Positive review from verified buyer.",
            "toxicity_level": "none",
            "category": "positive",
        },
        "admin_decision": "", "admin_note": "",
    },
    {
        "id": "REV-SEED011",
        "product_id": "GAME-001",
        "customer_name": "James Wilson",
        "rating": 5,
        "text": "A masterpiece. Every hour felt earned. Highly recommended for any PS5 owner.",
        "timestamp": days_ago(73),
        "status": "published",
        "ai_analysis": {
            "decision": "auto_publish",
            "reason": "Positive review.",
            "toxicity_level": "none",
            "category": "positive",
        },
        "admin_decision": "", "admin_note": "",
    },

    # ---- Natalie Foster: respectful negative review ----
    {
        "id": "REV-SEED012",
        "product_id": "GAME-005",
        "customer_name": "Natalie Foster",
        "rating": 2,
        "text": "Multiplayer is fun but the campaign felt short and repetitive. Not worth full price in my opinion.",
        "timestamp": days_ago(30),
        "status": "published",
        "ai_analysis": {
            "decision": "auto_publish",
            "reason": "Negative but respectful review from verified buyer.",
            "toxicity_level": "none",
            "category": "negative_respectful",
        },
        "admin_decision": "", "admin_note": "",
    },
    {
        "id": "REV-SEED013",
        "product_id": "GAME-001",
        "customer_name": "Natalie Foster",
        "rating": 4,
        "text": "Strong story and characters. Some backtracking sections dragged for me but overall a great experience.",
        "timestamp": days_ago(55),
        "status": "published",
        "ai_analysis": {
            "decision": "auto_publish",
            "reason": "Balanced positive review with constructive criticism.",
            "toxicity_level": "none",
            "category": "positive",
        },
        "admin_decision": "", "admin_note": "",
    },

    # ---- Sophia Martinez: 2 positive family reviews ----
    {
        "id": "REV-SEED014",
        "product_id": "GAME-006",
        "customer_name": "Sophia Martinez",
        "rating": 5,
        "text": "Great for family game night. Everyone can jump in and have fun.",
        "timestamp": days_ago(38),
        "status": "published",
        "ai_analysis": {
            "decision": "auto_publish",
            "reason": "Positive family review.",
            "toxicity_level": "none",
            "category": "positive",
        },
        "admin_decision": "", "admin_note": "",
    },
    {
        "id": "REV-SEED015",
        "product_id": "GAME-004",
        "customer_name": "Sophia Martinez",
        "rating": 5,
        "text": "My kids play this every day. Endless creativity.",
        "timestamp": days_ago(13),
        "status": "published",
        "ai_analysis": {
            "decision": "auto_publish",
            "reason": "Positive family review.",
            "toxicity_level": "none",
            "category": "positive",
        },
        "admin_decision": "", "admin_note": "",
    },

    # ---- Olivia Brown: 1 positive review ----
    {
        "id": "REV-SEED016",
        "product_id": "GAME-007",
        "customer_name": "Olivia Brown",
        "rating": 5,
        "text": "Stunning open world, great combat variety. Sequel that improves on the original in every way.",
        "timestamp": days_ago(52),
        "status": "published",
        "ai_analysis": {
            "decision": "auto_publish",
            "reason": "Verified positive review.",
            "toxicity_level": "none",
            "category": "positive",
        },
        "admin_decision": "", "admin_note": "",
    },

    # ---- Kevin Park: 1 positive review on his purchase ----
    {
        "id": "REV-SEED017",
        "product_id": "CON-001",
        "customer_name": "Kevin Park",
        "rating": 5,
        "text": "Solid console. Setup was straightforward and the interface is snappy.",
        "timestamp": days_ago(85),
        "status": "published",
        "ai_analysis": {
            "decision": "auto_publish",
            "reason": "Positive product review.",
            "toxicity_level": "none",
            "category": "positive",
        },
        "admin_decision": "", "admin_note": "",
    },

    # ---- Rachel Green: 1 positive review ----
    {
        "id": "REV-SEED018",
        "product_id": "GAME-003",
        "customer_name": "Rachel Green",
        "rating": 4,
        "text": "Enjoying the new career mode. Some UI choices are odd but the football itself feels great.",
        "timestamp": days_ago(65),
        "status": "published",
        "ai_analysis": {
            "decision": "auto_publish",
            "reason": "Positive review with constructive criticism.",
            "toxicity_level": "none",
            "category": "positive",
        },
        "admin_decision": "", "admin_note": "",
    },

    # ---- AbsoluteTrashReview: 5 rejected toxic reviews across products ----
    {
        "id": "REV-SEED019",
        "product_id": "GAME-006",
        "customer_name": "AbsoluteTrashReview",
        "rating": 1,
        "text": "This game is garbage, you scammers stole my money, refund me right now you thieves.",
        "timestamp": days_ago(60),
        "status": "rejected",
        "ai_analysis": {
            "decision": "flag_for_review",
            "reason": "Offensive language and accusations directed at the store.",
            "toxicity_level": "high",
            "category": "negative_offensive",
        },
        "admin_decision": "reject", "admin_note": "Toxic",
    },
    {
        "id": "REV-SEED020",
        "product_id": "GAME-001",
        "customer_name": "AbsoluteTrashReview",
        "rating": 1,
        "text": "Trash. Everyone who likes this is an idiot. Do not waste your money on this fake company.",
        "timestamp": days_ago(45),
        "status": "rejected",
        "ai_analysis": {
            "decision": "flag_for_review",
            "reason": "Insults toward other customers and the store.",
            "toxicity_level": "high",
            "category": "negative_offensive",
        },
        "admin_decision": "reject", "admin_note": "Toxic",
    },
    {
        "id": "REV-SEED021",
        "product_id": "CON-001",
        "customer_name": "AbsoluteTrashReview",
        "rating": 1,
        "text": "Absolute joke of a console. Whoever bought this is an idiot. Sony ripped us all off.",
        "timestamp": days_ago(30),
        "status": "rejected",
        "ai_analysis": {
            "decision": "flag_for_review",
            "reason": "Personal insults and hostile tone.",
            "toxicity_level": "high",
            "category": "negative_offensive",
        },
        "admin_decision": "reject", "admin_note": "Toxic",
    },
    {
        "id": "REV-SEED022",
        "product_id": "GAME-005",
        "customer_name": "AbsoluteTrashReview",
        "rating": 1,
        "text": "The devs are lazy morons and the store is a scam. Never buying from you criminals again.",
        "timestamp": days_ago(15),
        "status": "rejected",
        "ai_analysis": {
            "decision": "flag_for_review",
            "reason": "Insults toward developers and the store.",
            "toxicity_level": "high",
            "category": "negative_offensive",
        },
        "admin_decision": "reject", "admin_note": "Toxic",
    },
    {
        "id": "REV-SEED023",
        "product_id": "GAME-002",
        "customer_name": "AbsoluteTrashReview",
        "rating": 1,
        "text": "Complete garbage, whoever made this deserves to lose their job. You are all thieves.",
        "timestamp": days_ago(6),
        "status": "rejected",
        "ai_analysis": {
            "decision": "flag_for_review",
            "reason": "Aggressive hostile content.",
            "toxicity_level": "high",
            "category": "negative_offensive",
        },
        "admin_decision": "reject", "admin_note": "Toxic",
    },

    # ---- SpamBot99: identical text posted across 4 products ----
    {
        "id": "REV-SEED024",
        "product_id": "GAME-001",
        "customer_name": "SpamBot99",
        "rating": 5,
        "text": "Best deals here visit our website cheapgames dot example for 90 percent off all titles today only!",
        "timestamp": days_ago(25),
        "status": "rejected",
        "ai_analysis": {
            "decision": "flag_for_review",
            "reason": "Promotional spam with external link.",
            "toxicity_level": "low",
            "category": "spam",
        },
        "admin_decision": "reject", "admin_note": "Spam",
    },
    {
        "id": "REV-SEED025",
        "product_id": "GAME-006",
        "customer_name": "SpamBot99",
        "rating": 5,
        "text": "Best deals here visit our website cheapgames dot example for 90 percent off all titles today only!",
        "timestamp": days_ago(25),
        "status": "rejected",
        "ai_analysis": {
            "decision": "flag_for_review",
            "reason": "Duplicate promotional content posted across multiple products.",
            "toxicity_level": "low",
            "category": "spam",
        },
        "admin_decision": "reject", "admin_note": "Spam duplicate",
    },
    {
        "id": "REV-SEED026",
        "product_id": "CON-001",
        "customer_name": "SpamBot99",
        "rating": 5,
        "text": "Best deals here visit our website cheapgames dot example for 90 percent off all titles today only!",
        "timestamp": days_ago(24),
        "status": "rejected",
        "ai_analysis": {
            "decision": "flag_for_review",
            "reason": "Duplicate promotional content.",
            "toxicity_level": "low",
            "category": "spam",
        },
        "admin_decision": "reject", "admin_note": "Spam duplicate",
    },
    {
        "id": "REV-SEED027",
        "product_id": "ACC-001",
        "customer_name": "SpamBot99",
        "rating": 5,
        "text": "Best deals here visit our website cheapgames dot example for 90 percent off all titles today only!",
        "timestamp": days_ago(24),
        "status": "rejected",
        "ai_analysis": {
            "decision": "flag_for_review",
            "reason": "Duplicate promotional content.",
            "toxicity_level": "low",
            "category": "spam",
        },
        "admin_decision": "reject", "admin_note": "Spam duplicate",
    },

    # ---- TotallyRealBuyer: fake reviews on products never purchased ----
    {
        "id": "REV-SEED028",
        "product_id": "CON-002",
        "customer_name": "TotallyRealBuyer",
        "rating": 5,
        "text": "Amazing product must buy five stars ten out of ten no complaints just perfect.",
        "timestamp": days_ago(20),
        "status": "rejected",
        "ai_analysis": {
            "decision": "flag_for_review",
            "reason": "Generic language with no product specific detail from a customer with no purchase history.",
            "toxicity_level": "none",
            "category": "spam",
        },
        "admin_decision": "reject", "admin_note": "No purchase found, generic content",
    },
    {
        "id": "REV-SEED029",
        "product_id": "ACC-002",
        "customer_name": "TotallyRealBuyer",
        "rating": 5,
        "text": "Amazing product must buy five stars ten out of ten no complaints just perfect.",
        "timestamp": days_ago(19),
        "status": "rejected",
        "ai_analysis": {
            "decision": "flag_for_review",
            "reason": "Same generic template used across products, no purchase on file.",
            "toxicity_level": "none",
            "category": "spam",
        },
        "admin_decision": "reject", "admin_note": "Fake reviewer",
    },
    {
        "id": "REV-SEED030",
        "product_id": "GAME-007",
        "customer_name": "TotallyRealBuyer",
        "rating": 5,
        "text": "Amazing product must buy five stars ten out of ten no complaints just perfect.",
        "timestamp": days_ago(18),
        "status": "rejected",
        "ai_analysis": {
            "decision": "flag_for_review",
            "reason": "Generic template, no verified purchase.",
            "toxicity_level": "none",
            "category": "spam",
        },
        "admin_decision": "reject", "admin_note": "Fake reviewer",
    },
]


# =========================================================================
# ACTIVITY LOGS derived from the orders and reviews above
# Kept short. The main log file will populate as the app runs.
# =========================================================================

SEED_ACTIVITY = [
    {
        "id": "LOG-SEED001",
        "timestamp": days_ago(45),
        "action": "order_rejected",
        "actor": "Admin",
        "details": "Admin rejected order ORD-SEED022 from John Smith at 1200 Industrial Park Dr, suspected reseller.",
    },
    {
        "id": "LOG-SEED002",
        "timestamp": days_ago(28),
        "action": "order_rejected",
        "actor": "Admin",
        "details": "Admin rejected order ORD-SEED023 from J. Smyth, same address as ORD-SEED022.",
    },
    {
        "id": "LOG-SEED003",
        "timestamp": days_ago(27),
        "action": "order_rejected",
        "actor": "Admin",
        "details": "Admin rejected order ORD-SEED026 from Michael Chen, second PS5 purchase in eleven days.",
    },
    {
        "id": "LOG-SEED004",
        "timestamp": days_ago(22),
        "action": "order_rejected",
        "actor": "Admin",
        "details": "Admin rejected order ORD-SEED029 from Alex Torres, second rejection for this customer.",
    },
    {
        "id": "LOG-SEED005",
        "timestamp": days_ago(15),
        "action": "review_rejected",
        "actor": "Admin",
        "details": "Admin rejected review REV-SEED022 from AbsoluteTrashReview.",
    },
    {
        "id": "LOG-SEED006",
        "timestamp": days_ago(6),
        "action": "review_rejected",
        "actor": "Admin",
        "details": "Admin rejected review REV-SEED023 from AbsoluteTrashReview.",
    },
]
