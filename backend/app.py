import os
import uuid

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from dotenv import load_dotenv

from agent_core.graph import analyze_order, analyze_review
from agent_core.config import health_check, GROQ_MODEL
from agent_core.db import init_db, now
from agent_core import repo
from agent_core.invoice import render_invoice_pdf, invoice_path

load_dotenv()

app = Flask(__name__)
CORS(app)


def new_id(prefix):
    return f"{prefix}-{uuid.uuid4().hex[:6].upper()}"


@app.route("/api/products", methods=["GET"])
def get_products():
    category = request.args.get("category", "")
    products = repo.load_products()
    if category:
        products = [p for p in products if p["category"].lower() == category.lower()]
    return jsonify({"products": products})


@app.route("/api/products/<product_id>", methods=["GET"])
def get_product(product_id):
    product = repo.get_product(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404
    return jsonify({"product": product, "reviews": repo.published_reviews_for(product_id)})


@app.route("/api/orders", methods=["POST"])
def place_order():
    data = request.get_json()
    customer_name = data.get("customer_name", "")
    customer_phone = data.get("customer_phone", "")
    customer_address = data.get("customer_address", "")
    items = data.get("items", [])

    if not customer_name or not items or not customer_address:
        return jsonify({"error": "Missing required fields"}), 400

    policy = repo.load_policy()
    total = 0
    order_items = []
    for item in items:
        product = repo.get_product(item["product_id"])
        if not product:
            return jsonify({"error": f"Product {item['product_id']} not found"}), 400
        subtotal = product["price"] * item["quantity"]
        total += subtotal
        order_items.append({
            "product_id": product["id"],
            "product_name": product["name"],
            "price": product["price"],
            "quantity": item["quantity"],
            "subtotal": subtotal,
            "age_rating": product["age_rating"],
        })

    shipping = 0 if total >= policy["free_shipping_over"] else policy["shipping_cost"]
    total += shipping

    order = {
        "id": new_id("ORD"),
        "customer_name": customer_name,
        "customer_phone": customer_phone,
        "customer_address": customer_address,
        "items": order_items,
        "item_count": sum(i["quantity"] for i in order_items),
        "subtotal": total - shipping,
        "shipping": shipping,
        "total": total,
        "payment": "Cash on delivery",
        "timestamp": now(),
        "status": "pending_ai",
        "ai_analysis": None,
        "admin_decision": "",
        "admin_note": "",
    }

    try:
        analysis = analyze_order(order)
    except Exception as e:
        repo.log_activity("order_analysis_failed", f"AI analysis failed for order {order['id']}: {str(e)}")
        return jsonify({
            "error": "AI analysis failed",
            "stage": "order_analysis",
            "detail": str(e),
            "order_id": order["id"],
        }), 502

    order["ai_analysis"] = analysis
    if analysis["decision"] == "approve":
        order["status"] = "approved"
        repo.insert_order(order)
        repo.log_activity("order_approved", f"Order {order['id']} auto-approved. Total: ${total}", ref_id=order["id"])
        inv = repo.create_invoice_for_order(order["id"])
        if inv:
            repo.log_activity("invoice_created", f"Invoice {inv['id']} created for order {order['id']}", ref_id=inv["id"])
    else:
        order["status"] = "flagged"
        repo.insert_order(order)
        repo.log_activity("order_flagged", f"Order {order['id']} flagged: {analysis['reason']}", ref_id=order["id"])

    return jsonify({
        "order": order,
        "message": "Order placed successfully!" if order["status"] == "approved"
                   else "Your order is being reviewed. We will confirm shortly.",
    })


@app.route("/api/orders", methods=["GET"])
def get_orders():
    orders = repo.load_orders()
    status = request.args.get("status", "")
    if status:
        orders = [o for o in orders if o["status"] == status]
    orders = sorted(orders, key=lambda o: o["timestamp"] or "", reverse=True)
    return jsonify({"orders": orders})


@app.route("/api/orders/<order_id>/decide", methods=["POST"])
def decide_order(order_id):
    data = request.get_json()
    action = data.get("action", "")
    note = data.get("note", "")

    if action not in ["approve", "reject"]:
        return jsonify({"error": "Action must be approve or reject"}), 400

    status = "approved" if action == "approve" else "rejected"
    updated = repo.update_order_decision(order_id, status, action, note)
    if not updated:
        return jsonify({"error": "Order not found"}), 404

    repo.log_activity(f"order_{action}", f"Admin {action} order {order_id}: {note}", actor="Admin", ref_id=order_id)

    if action == "approve":
        inv = repo.create_invoice_for_order(order_id)
        if inv:
            repo.log_activity("invoice_created", f"Invoice {inv['id']} created for order {order_id}", ref_id=inv["id"])

    return jsonify({"message": f"Order {order_id} {action}ed"})


@app.route("/api/reviews", methods=["POST"])
def submit_review():
    data = request.get_json()
    product_id = data.get("product_id", "")
    customer_name = data.get("customer_name", "")
    rating = data.get("rating", 5)
    text = data.get("text", "")

    if not product_id or not text:
        return jsonify({"error": "Missing required fields"}), 400

    review = {
        "id": new_id("REV"),
        "product_id": product_id,
        "customer_name": customer_name or "Anonymous",
        "rating": rating,
        "text": text,
        "timestamp": now(),
        "status": "pending_ai",
        "ai_analysis": None,
        "admin_decision": "",
        "admin_note": "",
    }

    try:
        analysis = analyze_review(review)
    except Exception as e:
        repo.log_activity("review_analysis_failed", f"AI analysis failed for review {review['id']}: {str(e)}")
        return jsonify({
            "error": "AI analysis failed",
            "stage": "review_analysis",
            "detail": str(e),
            "review_id": review["id"],
        }), 502

    review["ai_analysis"] = analysis
    if analysis["decision"] == "auto_publish":
        review["status"] = "published"
        repo.insert_review(review)
        repo.log_activity("review_published", f"Review {review['id']} auto-published: {analysis['category']}", ref_id=review["id"])
    else:
        review["status"] = "flagged"
        repo.insert_review(review)
        repo.log_activity("review_flagged", f"Review {review['id']} flagged: {analysis['reason']}", ref_id=review["id"])

    return jsonify({
        "review": review,
        "message": "Thank you for your review!" if review["status"] == "published"
                   else "Your review is being reviewed and will be published soon.",
    })


@app.route("/api/reviews", methods=["GET"])
def get_reviews():
    reviews = repo.load_reviews()
    status = request.args.get("status", "")
    product_id = request.args.get("product_id", "")
    if status:
        reviews = [r for r in reviews if r["status"] == status]
    if product_id:
        reviews = [r for r in reviews if r["product_id"] == product_id]
    reviews = sorted(reviews, key=lambda r: r["timestamp"] or "", reverse=True)
    return jsonify({"reviews": reviews})


@app.route("/api/reviews/<review_id>/decide", methods=["POST"])
def decide_review(review_id):
    data = request.get_json()
    action = data.get("action", "")
    note = data.get("note", "")

    if action not in ["publish", "reject"]:
        return jsonify({"error": "Action must be publish or reject"}), 400

    status = "published" if action == "publish" else "rejected"
    updated = repo.update_review_decision(review_id, status, action, note)
    if not updated:
        return jsonify({"error": "Review not found"}), 404

    repo.log_activity(f"review_{action}", f"Admin {action} review {review_id}: {note}", actor="Admin", ref_id=review_id)
    return jsonify({"message": f"Review {review_id} {action}ed"})


# =============================================
# INVOICES
# =============================================

@app.route("/api/invoices", methods=["GET"])
def get_invoices():
    invoices = repo.load_invoices()
    invoices = sorted(invoices, key=lambda i: i["issued_at"] or "", reverse=True)
    return jsonify({"invoices": invoices})


@app.route("/api/invoices/<invoice_id>", methods=["GET"])
def get_invoice(invoice_id):
    inv = repo.get_invoice(invoice_id)
    if not inv:
        return jsonify({"error": "Invoice not found"}), 404
    return jsonify({"invoice": inv})


@app.route("/api/invoices/<invoice_id>/pdf", methods=["GET"])
def invoice_pdf(invoice_id):
    inv = repo.get_invoice(invoice_id)
    if not inv:
        return jsonify({"error": "Invoice not found"}), 404
    path = invoice_path(invoice_id)
    if not os.path.exists(path):
        render_invoice_pdf(inv)
    return send_file(path, mimetype="application/pdf",
                     as_attachment=False, download_name=f"{invoice_id}.pdf")


@app.route("/api/invoices/<invoice_id>/pay", methods=["POST"])
def pay_invoice(invoice_id):
    inv = repo.mark_invoice_paid(invoice_id)
    if not inv:
        return jsonify({"error": "Invoice not found"}), 404
    render_invoice_pdf(inv)
    repo.log_activity("invoice_paid", f"Invoice {invoice_id} marked paid", actor="Admin", ref_id=invoice_id)
    return jsonify({"message": f"Invoice {invoice_id} marked paid", "invoice": inv})


# =============================================
# ADMIN
# =============================================

@app.route("/api/admin/stats", methods=["GET"])
def admin_stats():
    return jsonify(repo.stats())


@app.route("/api/admin/activity", methods=["GET"])
def get_activity():
    logs = repo.load_activity()
    logs = sorted(logs, key=lambda l: l["timestamp"] or "", reverse=True)
    return jsonify({"logs": logs})


@app.route("/api/admin/health", methods=["GET"])
def admin_health():
    return jsonify(health_check())


@app.route("/api/admin/reset", methods=["POST"])
def reset_data():
    repo.reset_all()
    return jsonify({"message": "All data cleared"})


@app.route("/api/policy", methods=["GET"])
def get_policy():
    return jsonify(repo.load_policy())


if __name__ == "__main__":
    init_db()
    products = repo.load_products()
    status = health_check()
    print("=" * 50)
    print("GameZone AI Store - Backend")
    print(f"Products: {len(products)} items loaded")
    print(f"Model: {GROQ_MODEL}")
    if status["healthy"]:
        print("Model health check: OK")
    else:
        print(f"Model health check: FAILED - {status['detail']}")
    print("API running at: http://localhost:5000")
    print("=" * 50)
    app.run(debug=True, port=5000)
