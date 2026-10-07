import os

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer,
)

INVOICE_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "invoices")

ACCENT = colors.HexColor("#4f46e5")
MUTED = colors.HexColor("#6b7280")
LIGHT = colors.HexColor("#f3f4f6")


def invoice_path(invoice_id):
    return os.path.join(INVOICE_DIR, f"{invoice_id}.pdf")


def render_invoice_pdf(invoice: dict) -> str:
    os.makedirs(INVOICE_DIR, exist_ok=True)
    path = invoice_path(invoice["id"])

    styles = getSampleStyleSheet()
    title = styles["Title"]
    title.textColor = ACCENT
    normal = styles["Normal"]
    small = styles["Normal"].clone("small")
    small.fontSize = 8
    small.textColor = MUTED

    doc = SimpleDocTemplate(
        path, pagesize=A4,
        leftMargin=20 * mm, rightMargin=20 * mm,
        topMargin=20 * mm, bottomMargin=20 * mm,
    )
    story = []

    story.append(Paragraph("GameZone", title))
    story.append(Paragraph("Invoice", styles["Heading2"]))
    story.append(Spacer(1, 6 * mm))

    status = invoice.get("status", "unpaid").upper()
    meta = [
        [Paragraph(f"<b>Invoice #</b> {invoice['id']}", normal),
         Paragraph(f"<b>Status</b> {status}", normal)],
        [Paragraph(f"<b>Order #</b> {invoice.get('order_id', '')}", normal),
         Paragraph(f"<b>Issued</b> {invoice.get('issued_at', '')}", normal)],
        [Paragraph(f"<b>Bill to</b> {invoice.get('customer_name', '')}", normal),
         Paragraph(f"<b>Paid</b> {invoice.get('paid_at') or '-'}", normal)],
        [Paragraph(f"<b>Address</b> {invoice.get('customer_address', '')}", normal), ""],
    ]
    meta_tbl = Table(meta, colWidths=[90 * mm, 80 * mm])
    meta_tbl.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(meta_tbl)
    story.append(Spacer(1, 8 * mm))

    rows = [["Item", "Qty", "Price", "Subtotal"]]
    for item in invoice.get("items", []):
        rows.append([
            item.get("product_name", item.get("product_id", "")),
            str(item.get("quantity", 0)),
            f"${item.get('price', 0)}",
            f"${item.get('subtotal', 0)}",
        ])

    items_tbl = Table(rows, colWidths=[95 * mm, 20 * mm, 27 * mm, 28 * mm])
    items_tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), ACCENT),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("ALIGN", (1, 0), (-1, -1), "RIGHT"),
        ("ALIGN", (0, 0), (0, -1), "LEFT"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHT]),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    story.append(items_tbl)
    story.append(Spacer(1, 6 * mm))

    totals = [
        ["Subtotal", f"${invoice.get('subtotal', 0)}"],
        ["Shipping", "Free" if invoice.get("shipping", 0) == 0 else f"${invoice.get('shipping', 0)}"],
        ["Total", f"${invoice.get('total', 0)}"],
    ]
    totals_tbl = Table(totals, colWidths=[142 * mm, 28 * mm])
    totals_tbl.setStyle(TableStyle([
        ("ALIGN", (0, 0), (-1, -1), "RIGHT"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("LINEABOVE", (0, -1), (-1, -1), 0.5, MUTED),
        ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
        ("TOPPADDING", (0, -1), (-1, -1), 5),
    ]))
    story.append(totals_tbl)
    story.append(Spacer(1, 12 * mm))

    story.append(Paragraph("Payment: Cash on delivery. Thank you for shopping with GameZone.", small))

    doc.build(story)
    return path
