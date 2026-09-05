# VLOO payment document template kit

This kit replaces the legacy receipt files with one shared visual system and seven logical documents:

1. `user-receipt` - emailed after payment and downloadable from Payment completed / Booking history.
2. `user-booking-confirmation` - the user's confirmed-booking record, downloadable while payment is pending or from Booking history.
3. `host-booking-confirmation` - the host's operational record of the confirmed booking, guest, access, and expected booking value.
4. `host-payout-statement` - emailed after payout and downloadable from Payouts / Booking history.
5. `commission-deduction-statement` - VLOO's accounting document for the 15% commission, 25% VAT on that commission, and the amount already deducted from payout.
6. `credit-note` - the refund accounting document, linked to the original receipt and showing the reversed booking charges, VAT, refund method, and Stripe refund reference.
7. `cancellation-record` - the non-accounting record of a Flex or Extended Stay cancellation, including what was cancelled, what remains active, and any related refund status.

The approved reference is `designs/VLOO-payment-document-template-preview.pdf`. It contains the user and host booking documents for both stay types, one refund credit note, two cancellation records, and—at the end—one consolidated monthly Host Payout Statement plus one consolidated VLOO Commission Deduction Statement. No booking-type-specific payout or commission statements are included. `build_preview.py` is the deterministic ReportLab source used to generate that PDF.

The PDF is the visual acceptance reference, not the production rendering engine. Developers should implement equivalent server-side HTML/CSS or reusable PDF components using the data and variant rules below.

## Regenerate the reference PDF

```bash
python3 -m pip install reportlab pypdf
python3 vloo-payment-documents/build_preview.py
```

The generated file is written to `output/pdf/VLOO-payment-document-template-preview.pdf`. Copy an approved export into `vloo-payment-documents/designs/` when updating the checked-in design reference.

## Design rules

- A4, one page for normal bookings; long host payout line-item lists may continue onto additional pages with repeated table headers.
- VLOO navy `#072739`, teal `#006988`, pale blue `#E0F0FB`, muted text `#667982`.
- Receipt and payout documents show money prominently. Booking copies show the workspace and dates prominently.
- Every document carries a unique document or booking reference, status, creation context, and page number.
- User and host booking copies must state that they are not receipts, payout statements, or commission deduction statements.
- Currency is shown as `NOK 2,500.00` consistently. Dates should be localized consistently in production.

## Variant logic

Use data conditions, not separate layouts:

- `booking.type = flex | extended_stay` changes the title and date section. Extended Stay confirmations show the full stay, booked weekdays, access time, desk quantity, and current paid billing period; they do not need a speculative future billing schedule.
- `host.vat_registered = true` shows subtotal excluding VAT, VAT rate/amount, and the host's MVA suffix.
- `host.vat_registered = false` hides rental VAT columns/rows and adds: "The host is not VAT registered. No VAT has been charged on this rental."
- VLOO commission VAT remains visible in host payout bookkeeping because VLOO AS is VAT registered; non-VAT-registered hosts should see that input VAT is not deductible.
- `payment.status = paid | pending | refunded | partially_refunded` controls the badge and amount label.
- `payout.status = paid | pending | failed` controls the host payout badge. Only `paid` should be labelled a payout receipt/statement.

## Required data

Common: document ID, generated timestamp, booking reference/type/status, workspace name/address, user, host legal name/org. no./VAT status, and VLOO legal details.

Receipt: Stripe payment ID, payment date/method, line items, subtotal, VAT rate/amount, total paid, currency, and refund data when relevant.

User booking confirmation: booking status, dates/times, workspace, guest count, access, amenities, cancellation terms, and price at booking.

Host booking confirmation: guest contact details, party size, booking status, access and preparation notes, gross value, expected VLOO fee, expected net payout, and payout timing.

For Extended Stay, generate and send the host booking confirmation immediately after the user's upfront payment succeeds and the booking changes to `confirmed`. Host approval or the upfront-payment request alone must not generate a host booking confirmation.

Host payout: Stripe payout ID/date, booking lines, gross collected, VLOO fee excluding and including VAT, net payout, and bookkeeping totals.

Commission deduction: related booking and payout IDs, commission base, 15% rate, commission excluding VAT, 25% VAT on commission, total deducted, and amount payable (zero when already deducted).

Production settlement rule: create one monthly Host Payout Statement and one matching VLOO Commission Deduction Statement per host. Both documents include Flex and Extended Stay consumption, share one settlement/payout reference, and are generated from the same canonical lines. Flex quantities use booked days; Extended Stay quantities use desks multiplied by chargeable days. Do not generate separate payout documents by booking type.

Cancellation record: cancellation request and confirmation timestamps, the original booking, cancelled and remaining access, capacity, payment impact, and refund or Credit Note status. Flex records list every booked date and its outcome; Extended Stay records show the effective end date and affected billing periods.

## Product placement

| Portal area | User download | Host download |
|---|---|---|
| Payment completed / Payouts | Receipt | Host payout statement |
| Payment pending | User booking confirmation / copy | Host booking confirmation / copy |
| Booking history | User booking confirmation plus receipt when paid | Host booking confirmation plus payout and commission statements when available |
| Cancelled Extended Stay | Cancellation record, original receipt, and Credit Note when a refund applies | Cancellation record or equivalent portal record |
| Cancelled Flex stay | Cancellation record, original receipt, and Credit Note when a refund applies | Cancellation record or equivalent portal record |

## Important content correction from legacy files

One non-VAT user receipt shows a total paid of NOK 2,000.00 in the summary but says NOK 2,500.00 in the note. Generate narrative text from the same canonical amount field as the totals to prevent this class of mismatch.
