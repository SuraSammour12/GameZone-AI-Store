import argparse
import json
import os
import sys

from agent_core.graph import analyze_order, analyze_review
from data.seed_data import SEED_ORDERS, SEED_REVIEWS

REPORT_FILE = os.path.join(os.path.dirname(__file__), "eval_report.json")


def expected_order(o):
    return "approve" if o.get("status") == "approved" else "flag_for_review"


def expected_review(r):
    return "auto_publish" if r.get("status") == "published" else "flag_for_review"


def run_orders(orders):
    results = []
    for o in orders:
        want = expected_order(o)
        try:
            analysis = analyze_order(o)
            got = analysis["decision"]
            reason = analysis.get("reason", "")
            error = None
        except Exception as e:
            got = "ERROR"
            reason = ""
            error = str(e)
        results.append({
            "id": o["id"],
            "customer": o["customer_name"],
            "expected": want,
            "got": got,
            "match": got == want,
            "reason": reason,
            "error": error,
        })
    return results


def run_reviews(reviews):
    results = []
    for r in reviews:
        want = expected_review(r)
        try:
            analysis = analyze_review(r)
            got = analysis["decision"]
            reason = analysis.get("reason", "")
            error = None
        except Exception as e:
            got = "ERROR"
            reason = ""
            error = str(e)
        results.append({
            "id": r["id"],
            "reviewer": r["customer_name"],
            "expected": want,
            "got": got,
            "match": got == want,
            "reason": reason,
            "error": error,
        })
    return results


def summarize(name, results, positive, negative):
    total = len(results)
    matches = sum(1 for r in results if r["match"])
    errors = [r for r in results if r["got"] == "ERROR"]
    false_negatives = [
        r for r in results
        if r["expected"] == negative and r["got"] == positive
    ]
    false_positives = [
        r for r in results
        if r["expected"] == positive and r["got"] == negative
    ]
    disagreements = [r for r in results if not r["match"] and r["got"] != "ERROR"]

    scored = total - len(errors)
    rate = round(100 * matches / scored) if scored else 0

    print(f"\n{'=' * 60}")
    print(f"{name}: {matches}/{scored} match ({rate}%)   [{len(errors)} errors excluded]")
    print(f"{'=' * 60}")
    print(f"  Dangerous ({negative} expected, agent said {positive}): {len(false_negatives)}")
    print(f"  Annoying  ({positive} expected, agent said {negative}): {len(false_positives)}")
    print(f"  Errors: {len(errors)}")
    if disagreements:
        print("\n  Disagreements:")
        for d in disagreements:
            who = d.get("customer") or d.get("reviewer")
            print(f"   - {d['id']} ({who}): expected {d['expected']}, got {d['got']}")
            print(f"       {d['reason'][:140]}")
    if errors:
        print("\n  Errors:")
        for e in errors:
            who = e.get("customer") or e.get("reviewer")
            print(f"   - {e['id']} ({who}): {e['error']}")

    return {
        "total": total,
        "scored": scored,
        "matches": matches,
        "agreement_rate": round(matches / scored, 3) if scored else None,
        "dangerous_misses": len(false_negatives),
        "annoying_misses": len(false_positives),
        "errors": len(errors),
        "results": results,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=0, help="Max records per set (0 = all)")
    args = parser.parse_args()

    orders = SEED_ORDERS[:args.limit] if args.limit else SEED_ORDERS
    reviews = SEED_REVIEWS[:args.limit] if args.limit else SEED_REVIEWS

    print("Running order agent over", len(orders), "seed orders...")
    order_results = run_orders(orders)
    order_summary = summarize("ORDERS", order_results, "approve", "flag_for_review")

    print("\nRunning review agent over", len(reviews), "seed reviews...")
    review_results = run_reviews(reviews)
    review_summary = summarize("REVIEWS", review_results, "auto_publish", "flag_for_review")

    report = {"orders": order_summary, "reviews": review_summary}
    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f"\nFull report written to {REPORT_FILE}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Eval failed: {e}", file=sys.stderr)
        sys.exit(1)