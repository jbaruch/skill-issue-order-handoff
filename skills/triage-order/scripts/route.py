#!/usr/bin/env python3
"""Ask Jev which team should get a Brickbox ticket."""
import argparse
import json
import os
from time import perf_counter
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

LABELS = {
    "billing": "The customer asks about charges, payment, an invoice, or a refund.",
    "shipping": "The customer asks about where an order is or when it will arrive.",
    "unclear": "Neither team is clear, or the text gives equally relevant reasons for both.",
}
URL = "https://api.typesafe.ai/v1/systemone"


def request(ticket, key):
    payload = {
        "model": "jev-latest",
        "state": ticket,
        "questions": {
            "team": {"type": "choice", "instructions": "Choose a team from the customer's question.", "criteria": LABELS}
        },
    }
    req = Request(URL, json.dumps(payload).encode(), {
        "Authorization": f"Bearer {key}", "Content-Type": "application/json",
    })
    with urlopen(req, timeout=20) as response:
        return json.load(response)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--live", action="store_true", required=True)
    parser.add_argument("ticket")
    args = parser.parse_args()
    started = perf_counter()
    key = os.environ.get("TYPESAFE_API_KEY")
    error = None
    result = {}
    label = "unclear"
    if not key:
        error = "TYPESAFE_API_KEY is missing"
    else:
        try:
            result = request(args.ticket, key)
            label = result["answers"]["team"]["choice"]
            if label not in LABELS:
                raise ValueError("unknown label")
        except HTTPError as exc:
            error = f"TypeSafe returned HTTP {exc.code}"
        except (ValueError, TypeError, KeyError, URLError, OSError) as exc:
            error = f"TypeSafe request failed ({type(exc).__name__})"
    if error:
        label = "unclear"
    print(json.dumps({
        "source": "jev" if not error else "unavailable",
        "model": result.get("model"),
        "ticket": args.ticket,
        "label": label,
        "next": "reasoning" if label == "unclear" else "handoff",
        "elapsed_ms": round(1000 * (perf_counter() - started)),
        "usage": result.get("usage"),
        "error": error,
    }))
    return int(error is not None)


if __name__ == "__main__":
    raise SystemExit(main())
