#!/usr/bin/env python3
"""Ask Cloudflare Clef which team should get a Brickbox ticket."""
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
MODEL = "@cf/cloudflare/clef"


def request(ticket, account, token):
    payload = {
        "model": "clef",
        "state": ticket,
        "questions": {
            "team": {"type": "choice", "instructions": "Choose a team from the customer's question.", "criteria": LABELS}
        },
    }
    url = f"https://api.cloudflare.com/client/v4/accounts/{account}/ai/run/{MODEL}"
    req = Request(url, json.dumps(payload).encode(), {
        "Authorization": f"Bearer {token}", "Content-Type": "application/json",
    })
    with urlopen(req, timeout=20) as response:
        payload = json.load(response)
    if not payload["success"]:
        raise ValueError("Cloudflare did not complete the request")
    return payload["result"]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--live", action="store_true", required=True)
    parser.add_argument("ticket")
    args = parser.parse_args()
    started = perf_counter()
    account = os.environ.get("CLOUDFLARE_ACCOUNT_ID")
    token = os.environ.get("CLOUDFLARE_API_TOKEN")
    error = None
    result = {}
    label = "unclear"
    if not account or not token:
        error = "Set CLOUDFLARE_ACCOUNT_ID and CLOUDFLARE_API_TOKEN"
    else:
        try:
            result = request(args.ticket, account, token)
            label = result["answers"]["team"]["choice"]
            if label not in LABELS:
                raise ValueError("unknown label")
        except HTTPError as exc:
            error = f"Cloudflare returned HTTP {exc.code}"
        except (ValueError, TypeError, KeyError, URLError, OSError) as exc:
            error = f"Cloudflare request failed ({type(exc).__name__})"
    if error:
        label = "unclear"
    print(json.dumps({
        "source": "clef" if not error else "unavailable",
        "model": result.get("model") or MODEL,
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
