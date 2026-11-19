---
name: triage-order
description: Prepare a support handoff from an incoming Brickbox order ticket, including billing and shipping tickets.
---

# Prepare an order handoff

Process steps in order. Do not skip ahead.

## Step 1 — Look up the order

Use the order number from the ticket. If it is missing, ask for it and
finish here. From the project folder, run
`python3 skills/triage-order/scripts/lookup_order.py ORDER_NUMBER`,
replacing `ORDER_NUMBER` with the ticket's number. If the script reports
an unknown order, ask the customer to check the number and finish here.
Proceed immediately to Step 2.

## Step 2 — Route the ticket

Run `python3 skills/triage-order/scripts/route.py --live "TICKET_TEXT"`
with the ticket text as a single argument. Use the returned Billing or
Shipping label. For an unclear ticket, ask one question that would let
you choose a team. If the service is unavailable, use the same three
choices yourself and say the live call was unavailable. Proceed
immediately to Step 3.

## Step 3 — Write the note

State what the customer says, the order facts, the team or follow-up
question, and the next action. Keep completed payments and pending holds
separate. Return the note in chat unless the attendee asks to save it.
Finish here.
