#!/usr/bin/env python3
"""Return payment and shipping facts for one order."""
import argparse
import json
from pathlib import Path


def summarize(order_number, order):
    payments = order["payments"]
    return {
        "order": order_number,
        "currency": order["currency"],
        "shipping": order["shipping"],
        "captured_cents": sum(p["cents"] for p in payments if p["status"] == "captured"),
        "pending_cents": sum(p["cents"] for p in payments if p["status"] == "pending"),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("order")
    parser.add_argument("--file", type=Path, default=Path("data/orders.json"))
    args = parser.parse_args()
    orders = json.loads(args.file.read_text())
    if args.order not in orders:
        parser.exit(2, f"Order {args.order} was not found. Check the order number.\n")
    print(json.dumps(summarize(args.order, orders[args.order])))


if __name__ == "__main__":
    main()
