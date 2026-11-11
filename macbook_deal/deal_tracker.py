"""Track MacBook Air M5 13" 512GB offers and rank them by effective price.

Usage:
    python3 deal_tracker.py add --store Amazon --price 899.99 [--tax 8.25]
        [--gift-card 0] [--gift-card-value 0.85] [--cashback 2] [--card 2] [--note "..."]
    python3 deal_tracker.py list            # all offers, cheapest effective price first
    python3 deal_tracker.py best            # cheapest offer + verdict vs. targets
    python3 deal_tracker.py history Amazon  # price history for one store

Data is stored in offers.csv next to this script. Standard library only.
"""

import argparse
import csv
import datetime
import os
import sys

DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "offers.csv")
FIELDS = ["date", "store", "price", "tax_pct", "gift_card", "gift_card_value",
          "cashback_pct", "card_pct", "note"]

BUY_NOW = 900.00      # at or below the all-time low ($899.99, May 2026)
GOOD_DEAL = 949.00
WALK_AWAY = 999.00


def effective_price(row):
    """Return the effective cost of an offer after tax and every saving."""
    price = float(row["price"])
    taxed = price * (1 + float(row["tax_pct"]) / 100)
    # Gift cards/store credit are worth less than cash: discount by their value factor.
    gift = float(row["gift_card"]) * float(row["gift_card_value"])
    # Portal cash back is usually paid on the pre-tax price; card rewards on the total.
    portal = price * float(row["cashback_pct"]) / 100
    card = taxed * float(row["card_pct"]) / 100
    return round(taxed - gift - portal - card, 2)


def load():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, newline="") as f:
        return list(csv.DictReader(f))


def verdict(amount):
    if amount <= BUY_NOW:
        return "BUY NOW: at or below the all-time low"
    if amount <= GOOD_DEAL:
        return "GOOD DEAL: buy if you can't wait for Cyber Monday"
    if amount <= WALK_AWAY:
        return "OK: keep watching"
    return "WAIT: above target"


def print_rows(rows):
    if not rows:
        print("No offers recorded yet. Add one with: python3 deal_tracker.py add --store X --price Y")
        return
    print(f"{'date':<11}{'store':<14}{'sticker':>10}{'effective':>11}  note")
    for r in rows:
        print(f"{r['date']:<11}{r['store']:<14}{float(r['price']):>10.2f}"
              f"{effective_price(r):>11.2f}  {r['note']}")


def cmd_add(args):
    row = {
        "date": args.date or datetime.date.today().isoformat(),
        "store": args.store,
        "price": f"{args.price:.2f}",
        "tax_pct": args.tax,
        "gift_card": args.gift_card,
        "gift_card_value": args.gift_card_value,
        "cashback_pct": args.cashback,
        "card_pct": args.card,
        "note": args.note,
    }
    new_file = not os.path.exists(DATA_FILE)
    with open(DATA_FILE, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        if new_file:
            writer.writeheader()
        writer.writerow(row)
    eff = effective_price(row)
    print(f"Saved {args.store}: sticker ${args.price:.2f}, effective ${eff:.2f} -> {verdict(eff)}")


def latest_per_store(rows):
    latest = {}
    for r in rows:  # file is append-only, so later rows are newer
        latest[r["store"].lower()] = r
    return list(latest.values())


def cmd_list(args):
    rows = load() if args.all else latest_per_store(load())
    print_rows(sorted(rows, key=effective_price))


def cmd_best(args):
    rows = latest_per_store(load())
    if not rows:
        print_rows(rows)
        return
    best = min(rows, key=effective_price)
    eff = effective_price(best)
    print(f"Best current offer: {best['store']} at ${eff:.2f} effective "
          f"(sticker ${float(best['price']):.2f}, recorded {best['date']})")
    print(verdict(eff))
    all_time = min(load(), key=effective_price)
    print(f"Lowest you've ever recorded: {all_time['store']} ${effective_price(all_time):.2f} on {all_time['date']}")


def cmd_history(args):
    print_rows([r for r in load() if r["store"].lower() == args.store.lower()])


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="command", required=True)

    a = sub.add_parser("add", help="record an offer")
    a.add_argument("--store", required=True)
    a.add_argument("--price", type=float, required=True, help="sticker price before tax")
    a.add_argument("--tax", type=float, default=0.0,
                   help="sales tax %%; targets are pre-tax, so set this only for comparing tax-free stores")
    a.add_argument("--gift-card", type=float, default=0.0, help="gift card / store credit included")
    a.add_argument("--gift-card-value", type=float, default=0.85,
                   help="what $1 of that credit is worth to you (default 0.85)")
    a.add_argument("--cashback", type=float, default=0.0, help="cash-back portal %% (Rakuten etc.)")
    a.add_argument("--card", type=float, default=0.0, help="credit card rewards %%")
    a.add_argument("--date", help="YYYY-MM-DD (default today)")
    a.add_argument("--note", default="")
    a.set_defaults(func=cmd_add)

    l = sub.add_parser("list", help="latest offer per store, cheapest first")
    l.add_argument("--all", action="store_true", help="show every recorded offer")
    l.set_defaults(func=cmd_list)

    sub.add_parser("best", help="cheapest current offer and verdict").set_defaults(func=cmd_best)

    h = sub.add_parser("history", help="price history for one store")
    h.add_argument("store")
    h.set_defaults(func=cmd_history)

    args = p.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    sys.exit(main())
