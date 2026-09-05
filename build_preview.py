from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    BaseDocTemplate, Frame, PageTemplate, Paragraph, Spacer, Table, TableStyle,
    KeepTogether, PageBreak
)

OUT = "output/pdf/VLOO-payment-document-template-preview.pdf"
Path(OUT).parent.mkdir(parents=True, exist_ok=True)
NAVY = colors.HexColor("#072739")
BODY = colors.HexColor("#263f4a")
MUTED = colors.HexColor("#667982")
TEAL = colors.HexColor("#006988")
SKY = colors.HexColor("#e0f0fb")
LINE = colors.HexColor("#d7e3e8")
SOFT = colors.HexColor("#f5f8f9")
GREEN = colors.HexColor("#13795b")
WHITE = colors.white

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="Logo", fontName="Helvetica-Bold", fontSize=20, leading=20, textColor=NAVY, spaceAfter=0))
styles.add(ParagraphStyle(name="Eyebrow", fontName="Helvetica-Bold", fontSize=7, leading=9, textColor=TEAL, spaceAfter=2, uppercase=True))
styles.add(ParagraphStyle(name="Meta", fontName="Helvetica-Bold", fontSize=8.5, leading=11, textColor=NAVY, alignment=TA_RIGHT))
styles.add(ParagraphStyle(name="TitleX", fontName="Helvetica-Bold", fontSize=22, leading=24, textColor=NAVY, spaceBefore=17, spaceAfter=5))
styles.add(ParagraphStyle(name="LeadX", fontName="Helvetica", fontSize=8.5, leading=12, textColor=MUTED, spaceAfter=12))
styles.add(ParagraphStyle(name="SectionX", fontName="Helvetica-Bold", fontSize=8, leading=10, textColor=NAVY, spaceBefore=12, spaceAfter=7, uppercase=True))
styles.add(ParagraphStyle(name="LabelX", fontName="Helvetica-Bold", fontSize=6.5, leading=8, textColor=MUTED, spaceAfter=2, uppercase=True))
styles.add(ParagraphStyle(name="ValueX", fontName="Helvetica-Bold", fontSize=8, leading=10.5, textColor=NAVY))
styles.add(ParagraphStyle(name="SmallX", fontName="Helvetica", fontSize=7.2, leading=10, textColor=BODY))
styles.add(ParagraphStyle(name="SmallBold", fontName="Helvetica-Bold", fontSize=7.2, leading=10, textColor=NAVY))
styles.add(ParagraphStyle(name="HeroLabel", fontName="Helvetica-Bold", fontSize=7, leading=9, textColor=TEAL))
styles.add(ParagraphStyle(name="HeroValue", fontName="Helvetica-Bold", fontSize=19, leading=21, textColor=NAVY))
styles.add(ParagraphStyle(name="WhiteEye", fontName="Helvetica-Bold", fontSize=7, leading=9, textColor=colors.HexColor("#91d8e7")))
styles.add(ParagraphStyle(name="WhiteTitle", fontName="Helvetica-Bold", fontSize=16, leading=18, textColor=WHITE))
styles.add(ParagraphStyle(name="WhiteSmall", fontName="Helvetica", fontSize=7.5, leading=10, textColor=colors.HexColor("#d8e5e9")))


def P(text, style="SmallX"):
    return Paragraph(text, styles[style])


def header(kind, ident, status, status_color=GREEN):
    badge = Table([[P(status.upper(), "SmallBold")]], style=[
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#e9f6f1") if status_color == GREEN else SKY),
        ("TEXTCOLOR", (0, 0), (-1, -1), status_color),
        ("LEFTPADDING", (0, 0), (-1, -1), 7), ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ])
    right = Table([[P(kind.upper(), "Eyebrow")], [P(ident, "Meta")], [badge]], colWidths=[55*mm], style=[
        ("ALIGN", (0, 0), (-1, -1), "RIGHT"), ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0), ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
    ])
    return Table([[P("VLOO", "Logo"), right]], colWidths=[99*mm, 55*mm], style=[
        ("VALIGN", (0, 0), (-1, -1), "TOP"), ("ALIGN", (1, 0), (1, 0), "RIGHT"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0), ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ])


def hero(label, amount, side1, side2):
    t = Table([[[P(label.upper(), "HeroLabel"), P(amount, "HeroValue")],
                [P(side1, "SmallBold"), P(side2, "SmallX")]]], colWidths=[92*mm, 62*mm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), SKY), ("BOX", (0, 0), (-1, -1), 0, SKY),
        ("LEFTPADDING", (0, 0), (-1, -1), 12), ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("TOPPADDING", (0, 0), (-1, -1), 10), ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ("ALIGN", (1, 0), (1, 0), "RIGHT"), ("VALIGN", (0, 0), (-1, -1), "BOTTOM"),
    ]))
    return t


def fields(items):
    rows = []
    for i in range(0, len(items), 2):
        row = []
        for label, value in items[i:i+2]:
            row.append([P(label.upper(), "LabelX"), P(value, "ValueX")])
        if len(row) == 1: row.append("")
        rows.append(row)
    t = Table(rows, colWidths=[74*mm, 74*mm], hAlign="LEFT")
    t.setStyle(TableStyle([
        ("LINEBELOW", (0, 0), (-1, -1), .6, LINE), ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 9),
        ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))
    return t


def data_table(headers, rows, widths):
    content = [[P(h.upper(), "LabelX") for h in headers]] + [[P(str(v), "SmallX") for v in r] for r in rows]
    t = Table(content, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([
        ("LINEBELOW", (0, 0), (-1, 0), 1, NAVY), ("LINEBELOW", (0, 1), (-1, -1), .5, LINE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4), ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("ALIGN", (1, 0), (-1, -1), "RIGHT"),
    ]))
    return t


def totals(rows):
    content = [[P(a, "SmallX"), P(b, "SmallX")] for a, b in rows[:-1]] + [[P(rows[-1][0], "ValueX"), P(rows[-1][1], "ValueX")]]
    t = Table(content, colWidths=[37*mm, 37*mm], hAlign="RIGHT")
    t.setStyle(TableStyle([
        ("ALIGN", (1, 0), (-1, -1), "RIGHT"), ("LINEABOVE", (0, -1), (-1, -1), 1, NAVY),
        ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    return t


def callout(text):
    t = Table([[P(text, "SmallX")]], colWidths=[154*mm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), SOFT), ("LINEBEFORE", (0, 0), (0, 0), 2, TEAL),
        ("LEFTPADDING", (0, 0), (-1, -1), 9), ("RIGHTPADDING", (0, 0), (-1, -1), 9),
        ("TOPPADDING", (0, 0), (-1, -1), 7), ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))
    return t


def booking_banner(kind, name, location, code):
    left = [P(kind.upper(), "WhiteEye"), P(name, "WhiteTitle"), P(location, "WhiteSmall")]
    right = [P("BOOKING REFERENCE", "WhiteEye"), P(code, "WhiteTitle")]
    t = Table([[left, right]], colWidths=[105*mm, 49*mm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), NAVY), ("LINEBEFORE", (1, 0), (1, 0), .5, colors.HexColor("#718690")),
        ("LEFTPADDING", (0, 0), (-1, -1), 12), ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("TOPPADDING", (0, 0), (-1, -1), 11), ("BOTTOMPADDING", (0, 0), (-1, -1), 11),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    return t


def dates(left_label, left, right_label, right):
    card = lambda lab, val: [P(lab.upper(), "LabelX"), P(val, "ValueX")]
    t = Table([[card(left_label, left), P("→", "ValueX"), card(right_label, right)]], colWidths=[68*mm, 18*mm, 68*mm])
    t.setStyle(TableStyle([
        ("BOX", (0, 0), (0, 0), .7, LINE), ("BOX", (2, 0), (2, 0), .7, LINE),
        ("ALIGN", (1, 0), (1, 0), "CENTER"), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 9), ("RIGHTPADDING", (0, 0), (-1, -1), 9),
        ("TOPPADDING", (0, 0), (-1, -1), 8), ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    return t


def page_footer(canvas, doc):
    canvas.saveState(); canvas.setStrokeColor(LINE); canvas.setLineWidth(.5)
    canvas.line(28*mm, 13*mm, 182*mm, 13*mm)
    canvas.setFont("Helvetica", 6.5); canvas.setFillColor(MUTED)
    canvas.drawString(28*mm, 9*mm, "Generated by VLOO · vloo.no")
    canvas.drawRightString(182*mm, 9*mm, "VLOO payment document template preview")
    canvas.restoreState()


doc = BaseDocTemplate(OUT, pagesize=A4, leftMargin=28*mm, rightMargin=28*mm, topMargin=17*mm, bottomMargin=18*mm)
frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
doc.addPageTemplates(PageTemplate(id="A4", frames=[frame], onPage=page_footer))
story = []

# User receipt
story += [header("Payment document", "Receipt R-2026-00842", "Paid"), P("Payment receipt", "TitleX"), P("Issued by VLOO AS on behalf of the host. Keep this document for your records.", "LeadX"), hero("Total paid", "NOK 7,500.00", "Paid 1 December 2026", "Stripe · Visa ending 4242"), P("Booking", "SectionX"), fields([("Workspace", "Star Design Agency · Studio 3"), ("Booking reference", "VLOO-FX-8K4Q2"), ("Booking type", "Flex booking · 3 days"), ("Access time", "09:00-17:00 each booked day")]), P("Price details", "SectionX"), data_table(["Booked date", "Qty", "Price excl. VAT", "VAT", "Total"], [["Tue 1 Dec 2026", "1 day", "2,000.00", "25%", "2,500.00"], ["Wed 2 Dec 2026", "1 day", "2,000.00", "25%", "2,500.00"], ["Fri 4 Dec 2026", "1 day", "2,000.00", "25%", "2,500.00"]], [65*mm, 18*mm, 27*mm, 18*mm, 26*mm]), Spacer(1, 5), totals([("Subtotal", "NOK 6,000.00"), ("VAT (25%)", "NOK 1,500.00"), ("Total paid", "NOK 7,500.00")]), P("Supplier", "SectionX"), fields([("Host", "Nordic Workspaces AS<br/>Org. no. 123 456 789 MVA"), ("Payment facilitator", "VLOO AS · Org. no. 929 102 452 MVA<br/>Krokvolden 14, 1369 Stabekk")]), Spacer(1, 8), callout("This receipt covers three non-consecutive Flex booking days. VLOO AS processed the payment through Stripe on behalf of the host."), PageBreak()]

# Host payout
story += [header("Host payment document", "Payout P-2026-00119", "Paid out"), P("Host payout statement", "TitleX"), P("A clear record of booking revenue, VLOO fees, and the amount transferred through Stripe.", "LeadX"), hero("Net payout", "NOK 6,375.00", "Transferred 2 December 2026", "Stripe payout po_1Qx84…"), P("Payout details", "SectionX"), fields([("Host", "Nordic Workspaces AS<br/>Org. no. 123 456 789 MVA"), ("Statement period", "1-4 December 2026"), ("Booking reference", "VLOO-FX-8K4Q2 · 3 days"), ("Workspace", "Star Design Agency · Studio 3")]), P("Payout calculation", "SectionX"), data_table(["Booked days", "Gross incl. VAT", "VLOO fee incl. VAT", "Net to host"], [["1, 2 and 4 Dec 2026<br/>VLOO-FX-8K4Q2", "7,500.00", "1,125.00", "6,375.00"]], [70*mm, 28*mm, 29*mm, 27*mm]), Spacer(1, 5), totals([("Gross collected", "NOK 7,500.00"), ("VLOO fee deducted", "NOK 1,125.00"), ("Net payout", "NOK 6,375.00")]), P("Bookkeeping summary", "SectionX"), fields([("Rental revenue incl. VAT", "NOK 7,500.00"), ("Output VAT", "NOK 1,500.00"), ("Commission expense excl. VAT", "NOK 900.00"), ("Input VAT on commission", "NOK 225.00")]), Spacer(1, 7), callout("This statement combines all three booked Flex days. The VLOO commission was deducted before payout; no further payment is required."), PageBreak()]

# User booking confirmation / copy
story += [header("User booking confirmation / copy", "VLOO-FX-8K4Q2", "Confirmed", TEAL), P("Your booking confirmation", "TitleX"), P("This copy confirms all booked Flex days for the user. It is not a payment receipt.", "LeadX"), booking_banner("Flex booking · 3 days", "Studio 3 at Nordic Workspaces", "Krokvolden 14, 1369 Stabekk · Floor 2", "8K4Q2"), P("Booked days", "SectionX"), data_table(["Date", "Access time", "Status"], [["Tue 1 Dec 2026", "09:00-17:00", "Confirmed"], ["Wed 2 Dec 2026", "09:00-17:00", "Confirmed"], ["Fri 4 Dec 2026", "09:00-17:00", "Confirmed"]], [62*mm, 48*mm, 44*mm]), P("Booking details", "SectionX"), fields([("Booked by", "Alex Morgan · alex@example.com"), ("Guests", "4 people"), ("Workspace", "Private studio · 4 desks"), ("Booking status", "Confirmed · 3 days")]), P("What is included", "SectionX"), fields([("Amenities", "Wi-Fi · monitor · coffee · phone booth"), ("Access", "Unsure? Use the host chat to plan the details.")]), P("Price at booking", "SectionX"), data_table(["Description", "Qty", "Subtotal", "VAT", "Total"], [["Studio 3 · full-day workspace", "3 days", "6,000.00", "1,500.00", "NOK 7,500.00"]], [62*mm, 20*mm, 24*mm, 22*mm, 26*mm]), Spacer(1, 8), callout("<b>Need help?</b> Contact VLOO at +47 95 11 22 84 or VLOO support at andreas@vloo.co. Cancellation terms are the terms accepted when this booking was made."), PageBreak()]

# Host booking confirmation / copy
story += [header("Host booking confirmation / copy", "VLOO-FX-8K4Q2", "Confirmed", TEAL), P("Confirmed host booking", "TitleX"), P("The host's operational record of all confirmed Flex days and the guest details needed to deliver the booking.", "LeadX"), booking_banner("Flex booking · 3 days", "Studio 3 at Nordic Workspaces", "Krokvolden 14, 1369 Stabekk · Floor 2", "8K4Q2"), P("Booked days", "SectionX"), data_table(["Date", "Guest access", "Status"], [["Tue 1 Dec 2026", "09:00-17:00", "Confirmed"], ["Wed 2 Dec 2026", "09:00-17:00", "Confirmed"], ["Fri 4 Dec 2026", "09:00-17:00", "Confirmed"]], [62*mm, 48*mm, 44*mm]), P("Guest and booking", "SectionX"), fields([("Primary guest", "Alex Morgan · alex@example.com<br/>+47 900 11 222"), ("Party size", "4 people"), ("Workspace", "Private studio · 4 desks"), ("Booking status", "Confirmed · 3 days")]), P("Host preparation", "SectionX"), fields([("Access instruction", "Use the user chat to plan the details."), ("Included amenities", "Wi-Fi · monitor · coffee · phone booth"), ("Need help?", "Contact VLOO at +47 95 11 22 84 or VLOO support at andreas@vloo.co")]), P("Booking value", "SectionX"), data_table(["Gross incl. VAT", "VLOO fee incl. VAT", "Expected net payout", "Payout timing"], [["NOK 7,500.00", "NOK 1,125.00", "NOK 6,375.00", "Start of each month"]], [38*mm, 38*mm, 40*mm, 38*mm]), Spacer(1, 8), callout("<b>Host record:</b> the three dates above are the booked days. Dates between them are not included unless listed."), PageBreak()]

# VLOO commission deduction statement
story += [header("Accounting document", "Commission C-2026-00119", "Deducted"), P("VLOO commission deduction statement", "TitleX"), P("Accounting document for VLOO's 15% commission and VAT on the commission, deducted before the host payout.", "LeadX"), hero("Commission deducted", "NOK 1,125.00", "Booking VLOO-FX-8K4Q2 · 3 days", "Related payout P-2026-00119"), P("Statement details", "SectionX"), fields([("Issued by", "VLOO AS<br/>Org. no. 929 102 452 MVA"), ("Charged to", "Nordic Workspaces AS<br/>Org. no. 123 456 789 MVA"), ("Commission date", "2 December 2026"), ("Booked dates", "1, 2 and 4 December 2026")]), P("Commission calculation", "SectionX"), data_table(["Description", "Commission base", "Rate", "Amount excl. VAT", "VAT"], [["Flex commission · 3 booked days", "NOK 7,500.00", "15%", "NOK 900.00", "25%"]], [54*mm, 31*mm, 17*mm, 32*mm, 20*mm]), Spacer(1, 6), totals([("Commission excl. VAT", "NOK 900.00"), ("VAT on commission (25%)", "NOK 225.00"), ("Total commission deducted", "NOK 1,125.00")]), P("Bookkeeping summary", "SectionX"), fields([("Commission expense excl. VAT", "NOK 900.00"), ("Input VAT", "NOK 225.00"), ("Settlement method", "Deducted from host payout"), ("Amount payable", "NOK 0.00")]), Spacer(1, 9), callout("This statement combines the three listed Flex booking days. The total commission was already deducted from the related host payout; no further payment is required."), PageBreak()]

# Extended Stay user receipt - one receipt per completed monthly billing period
story += [header("Extended Stay payment document", "Receipt R-2027-00031", "Paid"), P("Extended Stay payment receipt", "TitleX"), P("Issued by VLOO AS on behalf of the host for one completed monthly billing period.", "LeadX"), hero("Total paid", "NOK 7,500.00", "Paid 1 January 2027", "Stripe · Visa ending 4242"), P("Booking", "SectionX"), fields([("Workspace", "Dedicated desk 14 · Nordic Workspaces<br/>1 desk"), ("Booking reference", "VLOO-ES-2N7P6"), ("Booked days", "Monday-Friday · 09:00-17:00"), ("Billing period", "1-31 January 2027")]), P("Price details", "SectionX"), data_table(["Description", "Qty", "Price excl. VAT", "VAT", "Total"], [["Dedicated desk · January 2027", "1 desk", "6,000.00", "25%", "7,500.00"]], [65*mm, 18*mm, 27*mm, 18*mm, 26*mm]), Spacer(1, 5), totals([("Subtotal", "NOK 6,000.00"), ("VAT (25%)", "NOK 1,500.00"), ("Total paid", "NOK 7,500.00")]), P("Supplier", "SectionX"), fields([("Host", "Nordic Workspaces AS<br/>Org. no. 123 456 789 MVA"), ("Payment facilitator", "VLOO AS · Org. no. 929 102 452 MVA<br/>Krokvolden 14, 1369 Stabekk")]), Spacer(1, 8), callout("This receipt covers only the stated monthly billing period. The Extended Stay booking confirmation records the full stay, booked days, desk quantity, and recurring billing arrangement."), PageBreak()]

# Extended Stay host payout - one statement per monthly payout period
story += [header("Extended Stay host payment document", "Payout P-2027-00018", "Paid out"), P("Extended Stay host payout statement", "TitleX"), P("Monthly record of Extended Stay revenue, VLOO fees, and the amount transferred through Stripe.", "LeadX"), hero("Net payout", "NOK 6,375.00", "Transferred 2 January 2027", "Stripe payout po_2Es18…"), P("Payout details", "SectionX"), fields([("Host", "Nordic Workspaces AS<br/>Org. no. 123 456 789 MVA"), ("Statement period", "1-31 January 2027"), ("Booking reference", "VLOO-ES-2N7P6"), ("Workspace", "Dedicated desk 14 · Nordic Workspaces")]), P("Payout calculation", "SectionX"), data_table(["Billing period", "Gross incl. VAT", "VLOO fee incl. VAT", "Net to host"], [["1-31 Jan 2027 · VLOO-ES-2N7P6", "7,500.00", "1,125.00", "6,375.00"]], [70*mm, 28*mm, 29*mm, 27*mm]), Spacer(1, 5), totals([("Gross collected", "NOK 7,500.00"), ("VLOO fee deducted", "NOK 1,125.00"), ("Net payout", "NOK 6,375.00")]), P("Bookkeeping summary", "SectionX"), fields([("Rental revenue incl. VAT", "NOK 7,500.00"), ("Output VAT", "NOK 1,500.00"), ("Commission expense excl. VAT", "NOK 900.00"), ("Input VAT on commission", "NOK 225.00")]), Spacer(1, 7), callout("This payout covers the stated monthly period. The next Extended Stay payout is scheduled for the start of the following month, subject to successful payment processing."), PageBreak()]

# Extended Stay user booking confirmation / copy
story += [header("Extended Stay user confirmation / copy", "VLOO-ES-2N7P6", "Active", TEAL), P("Your Extended Stay confirmation", "TitleX"), P("This copy confirms the full stay, booked access, and current monthly payment period. It is not a payment receipt.", "LeadX"), booking_banner("Extended Stay · 1 desk", "Dedicated desk at Nordic Workspaces", "Krokvolden 14, 1369 Stabekk · Floor 2", "2N7P6"), P("Stay period", "SectionX"), dates("Move in", "1 Dec 2026", "Current end date", "28 Feb 2027"), P("Booked days and desks", "SectionX"), data_table(["Booked weekdays", "Access time", "Number of desks", "Status"], [["Monday-Friday", "09:00-17:00", "1 desk", "Active"]], [48*mm, 38*mm, 34*mm, 34*mm]), P("Booking details", "SectionX"), fields([("Booked by", "Alex Morgan · alex@example.com"), ("Workspace", "Dedicated desk 14"), ("Billing frequency", "Monthly · charged on the 1st"), ("Status", "Active")]), P("Access", "SectionX"), fields([("Access details", "Unsure? Use the host chat to plan the details."), ("Included amenities", "Wi-Fi · monitor · coffee · phone booth")]), P("Current payment period", "SectionX"), data_table(["Billing period", "Status", "Amount incl. VAT", "Receipt"], [["1-31 Jan 2027", "Paid", "NOK 7,500.00", "R-2027-00031"]], [36*mm, 24*mm, 38*mm, 56*mm]), Spacer(1, 8), callout("<b>Recurring payment:</b> charged monthly on the 1st. Future receipts are issued only after each payment succeeds.<br/><b>Need help?</b> Contact VLOO at +47 95 11 22 84 or VLOO support at andreas@vloo.co. Cancellation terms are the terms accepted when this booking was made."), PageBreak()]

# Extended Stay host booking confirmation / copy
story += [header("Extended Stay host confirmation / copy", "VLOO-ES-2N7P6", "Active", TEAL), P("Confirmed Extended Stay booking", "TitleX"), P("The host's operational record of the active stay, booked access, guest, and expected monthly payout.", "LeadX"), booking_banner("Extended Stay · 1 desk · 1 person", "Dedicated desk at Nordic Workspaces", "Krokvolden 14, 1369 Stabekk · Floor 2", "2N7P6"), P("Stay period", "SectionX"), dates("Guest moves in", "1 Dec 2026", "Current end date", "28 Feb 2027"), P("Booked days and capacity", "SectionX"), data_table(["Booked weekdays", "Access time", "Desks", "People"], [["Monday-Friday", "09:00-17:00", "1", "1"]], [52*mm, 42*mm, 30*mm, 30*mm]), P("Guest and booking", "SectionX"), fields([("Primary guest", "Alex Morgan · alex@example.com<br/>+47 900 11 222"), ("Workspace", "Dedicated desk 14"), ("Billing frequency", "Monthly · charged on the 1st"), ("Booking status", "Active")]), P("Host preparation", "SectionX"), fields([("Access instruction", "Use the user chat to plan the details."), ("Included amenities", "Wi-Fi · monitor · coffee · phone booth"), ("Need help?", "Contact VLOO at +47 95 11 22 84 or VLOO support at andreas@vloo.co")]), P("Monthly booking value", "SectionX"), data_table(["Gross incl. VAT", "VLOO fee incl. VAT", "Expected net payout", "Payout timing"], [["NOK 7,500.00", "NOK 1,125.00", "NOK 6,375.00", "Start of each month"]], [38*mm, 38*mm, 40*mm, 38*mm]), Spacer(1, 8), callout("<b>Host record:</b> the weekdays and capacity above are confirmed for the full stay period. Monthly payout and commission statements are generated after each successful payment."), PageBreak()]

# Extended Stay VLOO commission deduction statement
story += [header("Extended Stay accounting document", "Commission C-2027-00018", "Deducted"), P("VLOO commission deduction statement", "TitleX"), P("Monthly accounting document for VLOO's 15% Extended Stay commission and VAT on the commission.", "LeadX"), hero("Commission deducted", "NOK 1,125.00", "Booking VLOO-ES-2N7P6", "Billing period 1-31 Jan 2027"), P("Statement details", "SectionX"), fields([("Issued by", "VLOO AS<br/>Org. no. 929 102 452 MVA"), ("Charged to", "Nordic Workspaces AS<br/>Org. no. 123 456 789 MVA"), ("Commission date", "2 January 2027"), ("Related payout", "P-2027-00018")]), P("Commission calculation", "SectionX"), data_table(["Description", "Commission base", "Rate", "Amount excl. VAT", "VAT"], [["Extended Stay commission · Jan 2027", "NOK 7,500.00", "15%", "NOK 900.00", "25%"]], [54*mm, 31*mm, 17*mm, 32*mm, 20*mm]), Spacer(1, 6), totals([("Commission excl. VAT", "NOK 900.00"), ("VAT on commission (25%)", "NOK 225.00"), ("Total commission deducted", "NOK 1,125.00")]), P("Bookkeeping summary", "SectionX"), fields([("Commission expense excl. VAT", "NOK 900.00"), ("Input VAT", "NOK 225.00"), ("Settlement method", "Deducted from monthly host payout"), ("Amount payable", "NOK 0.00")]), Spacer(1, 9), callout("This statement covers one Extended Stay billing period. The 15% commission is calculated from the gross monthly booking amount, with 25% VAT applied to VLOO's commission."), PageBreak()]

# Extended Stay cancellation record - non-accounting record for the user portal
story += [header("Extended Stay booking record", "Cancellation X-2027-00042", "Cancelled", TEAL), P("Extended Stay cancellation record", "TitleX"), P("This record confirms when the Extended Stay ends and what happens to paid and future billing periods. It is not a receipt or credit note.", "LeadX"), booking_banner("Cancelled · 1 desk · 1 person", "Dedicated desk at Nordic Workspaces", "Krokvolden 14, 1369 Stabekk · Floor 2", "2N7P6"), P("Cancellation", "SectionX"), fields([("Cancellation requested", "18 January 2027 by Alex Morgan"), ("Cancellation confirmed", "18 January 2027"), ("Effective end date", "31 January 2027"), ("Access ends", "31 January 2027 at 17:00")]), P("Cancelled booking", "SectionX"), fields([("Original stay", "1 December 2026-28 February 2027"), ("Workspace", "Dedicated desk 14"), ("Booked days", "Monday-Friday · 09:00-17:00"), ("Capacity", "1 desk · 1 person")]), P("Payment impact", "SectionX"), data_table(["Billing period", "Status", "Amount incl. VAT", "Document"], [["1-31 Jan 2027", "Paid · access remains", "NOK 7,500.00", "Receipt R-2027-00031"], ["1-28 Feb 2027", "Cancelled · not charged", "NOK 0.00", "No receipt"]], [36*mm, 44*mm, 36*mm, 38*mm]), P("Refund", "SectionX"), fields([("Refund status", "No refund due"), ("Reason", "The paid January period remains active until its effective end date")]), Spacer(1, 8), callout("No future recurring payments will be collected after the effective end date. If a paid amount is refunded, VLOO issues a separate Credit Note linked to the original receipt.<br/><b>Need help?</b> Contact VLOO at +47 95 11 22 84 or VLOO support at andreas@vloo.co."), PageBreak()]

# Credit note - shared template for full or partial Flex / Extended Stay refunds
story += [header("Refund accounting document", "Credit note CN-2026-00124", "Refunded"), P("Credit note", "TitleX"), P("Issued in the same VLOO document system to reverse all or part of a previously issued receipt.", "LeadX"), hero("Total refunded", "NOK 7,500.00", "Refund submitted 28 November 2026", "Visa ending 4242 · 3-5 business days"), P("Original payment", "SectionX"), fields([("Original receipt", "R-2026-00842"), ("Booking reference", "VLOO-FX-8K4Q2"), ("Credit note date", "28 November 2026"), ("Stripe refund reference", "re_3Qx84…")]), P("Refunded booking days", "SectionX"), data_table(["Reversed date", "Qty", "Subtotal", "VAT", "Total"], [["Tue 1 Dec 2026", "1 day", "-2,000.00", "-500.00", "-2,500.00"], ["Wed 2 Dec 2026", "1 day", "-2,000.00", "-500.00", "-2,500.00"], ["Fri 4 Dec 2026", "1 day", "-2,000.00", "-500.00", "-2,500.00"]], [60*mm, 18*mm, 27*mm, 22*mm, 27*mm]), Spacer(1, 6), totals([("Reversed subtotal", "NOK -6,000.00"), ("Reversed VAT (25%)", "NOK -1,500.00"), ("Credit note total", "NOK -7,500.00")]), P("Issued by", "SectionX"), fields([("Supplier", "Nordic Workspaces AS<br/>Org. no. 123 456 789 MVA"), ("Payment facilitator", "VLOO AS · Org. no. 929 102 452 MVA<br/>Krokvolden 14, 1369 Stabekk")]), Spacer(1, 9), callout("This credit note fully reverses receipt R-2026-00842. The refund was submitted to the original payment method through Stripe. Keep both the original receipt and this credit note for your records."), PageBreak()]

# Flex cancellation record - supports full or partial cancellation of booked dates
story += [header("Flex booking record", "Cancellation X-2026-00125", "Partially cancelled", TEAL), P("Flex cancellation record", "TitleX"), P("This record shows which Flex dates were cancelled and which dates remain booked. It is not a receipt or credit note.", "LeadX"), booking_banner("Flex · 2 cancelled · 1 remains", "Studio 3 at Nordic Workspaces", "Krokvolden 14, 1369 Stabekk · Floor 2", "8K4Q2"), P("Cancellation", "SectionX"), fields([("Cancellation requested", "28 November 2026 by Alex Morgan"), ("Cancellation confirmed", "28 November 2026"), ("Original booking", "3 non-consecutive days"), ("Capacity", "4 desks · 4 people")]), P("Booked dates and outcome", "SectionX"), data_table(["Booked date", "Access time", "Outcome", "Amount incl. VAT"], [["Tue 1 Dec 2026", "09:00-17:00", "Cancelled · refunded", "NOK 2,500.00"], ["Wed 2 Dec 2026", "09:00-17:00", "Cancelled · refunded", "NOK 2,500.00"], ["Fri 4 Dec 2026", "09:00-17:00", "Confirmed · access remains", "NOK 2,500.00"]], [48*mm, 38*mm, 42*mm, 26*mm]), P("Refund", "SectionX"), fields([("Refund status", "Partial refund submitted"), ("Refund amount", "NOK 5,000.00"), ("Original receipt", "R-2026-00842"), ("Credit Note", "CN-2026-00125")]), P("Remaining booking", "SectionX"), fields([("Workspace", "Studio 3 · Nordic Workspaces"), ("Remaining date", "Friday 4 December 2026 · 09:00-17:00"), ("Access", "Use the host chat to plan the details."), ("Booking status", "Partially cancelled")]), Spacer(1, 8), callout("The original receipt remains part of the payment history. The separate Credit Note records the refunded amount. Only the date marked Confirmed remains available for access.<br/><b>Need help?</b> Contact VLOO at +47 95 11 22 84 or VLOO support at andreas@vloo.co."), PageBreak()]

# Consolidated monthly host payout - production recommendation for all booking types
story += [header("Monthly host settlement", "Payout P-2027-00022", "Paid out"), P("Combined host payout statement", "TitleX"), P("One monthly payout covering all completed Flex and Extended Stay consumption for this host.", "LeadX"), hero("Net payout", "NOK 30,175.00", "Transferred 2 February 2027", "Stripe payout po_3Hs22…"), P("Settlement details", "SectionX"), fields([("Host", "Nordic Workspaces AS<br/>Org. no. 123 456 789 MVA"), ("Consumption period", "1-31 January 2027"), ("Payout batch", "SET-2027-01-NW"), ("Payout timing", "Start of each month")]), P("Flex Stay consumption", "SectionX"), data_table(["Booking / service", "Quantity", "Gross incl. VAT", "VLOO fee incl. VAT", "Net"], [["VLOO-FX-9M2D7<br/>5 booked dates in Jan", "5 booked days", "12,500.00", "1,875.00", "10,625.00"]], [58*mm, 29*mm, 25*mm, 24*mm, 18*mm]), P("Extended Stay consumption", "SectionX"), data_table(["Booking / billing period", "Quantity", "Gross incl. VAT", "VLOO fee incl. VAT", "Net"], [["VLOO-ES-2N7P6<br/>1-31 Jan 2027", "2 desks × 23 days<br/>46 desk-days", "23,000.00", "3,450.00", "19,550.00"]], [58*mm, 29*mm, 25*mm, 24*mm, 18*mm]), Spacer(1, 5), totals([("Gross collected", "NOK 35,500.00"), ("VLOO fee deducted", "NOK 5,325.00"), ("Net payout", "NOK 30,175.00")]), P("Bookkeeping summary", "SectionX"), fields([("Rental revenue excl. VAT", "NOK 28,400.00"), ("Output VAT", "NOK 7,100.00"), ("Commission expense excl. VAT", "NOK 4,260.00"), ("Input VAT on commission", "NOK 1,065.00")]), Spacer(1, 7), callout("Flex and Extended Stay lines use different quantity units but reconcile to the same monthly payout batch. Each line must reference the underlying booking, payment, and receipt records."), PageBreak()]

# Consolidated monthly commission deduction - same settlement lines and payout batch
story += [Spacer(1, 13*mm), header("Monthly accounting document", "Commission C-2027-00022", "Deducted"), P("Monthly commission deduction statement", "TitleX"), P("One accounting statement for VLOO's commission on all Flex and Extended Stay consumption included in the monthly payout.", "LeadX"), hero("Commission deducted", "NOK 5,325.00", "Settlement SET-2027-01-NW", "Related payout P-2027-00022"), P("Statement details", "SectionX"), fields([("Issued by", "VLOO AS<br/>Org. no. 929 102 452 MVA"), ("Charged to", "Nordic Workspaces AS<br/>Org. no. 123 456 789 MVA"), ("Consumption period", "1-31 January 2027"), ("Commission date", "2 February 2027")]), P("Commission calculation", "SectionX"), data_table(["Consumption type", "Commission base", "Rate", "Amount excl. VAT", "VAT", "Total"], [["Flex Stay · 5 booked days", "NOK 12,500.00", "15%", "NOK 1,500.00", "NOK 375.00", "NOK 1,875.00"], ["Extended Stay · 46 desk-days", "NOK 23,000.00", "15%", "NOK 2,760.00", "NOK 690.00", "NOK 3,450.00"]], [48*mm, 29*mm, 16*mm, 26*mm, 19*mm, 22*mm]), Spacer(1, 6), totals([("Commission excl. VAT", "NOK 4,260.00"), ("VAT on commission (25%)", "NOK 1,065.00"), ("Total commission deducted", "NOK 5,325.00")]), P("Reconciliation", "SectionX"), fields([("Flex gross", "NOK 12,500.00"), ("Extended Stay gross", "NOK 23,000.00"), ("Total commission base", "NOK 35,500.00"), ("Amount payable", "NOK 0.00 · deducted from payout")]), Spacer(1, 8), callout("This statement and payout P-2027-00022 are generated from the same canonical settlement lines. The total commission deducted here must equal the fee deduction on the payout statement.")]

doc.build(story)
from pypdf import PdfReader, PdfWriter
reader = PdfReader(OUT)
writer = PdfWriter()
for page_index in [0, 2, 3, 1, 4, 5, 7, 8, 6, 9, 11, 10, 12, 13, 14]:
    writer.add_page(reader.pages[page_index])
with open(OUT, "wb") as stream:
    writer.write(stream)
print(OUT)
