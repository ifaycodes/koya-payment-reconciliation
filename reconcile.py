#!/usr/bin/env python3
"""Payment reconciliation.

Reads payments.jsonl and works out how much money we actually collected.
Run:  python3 reconcile.py
"""
import json

total = 0.0
count = 0

id_transactions = {}

with open("payments.jsonl") as f:
    for line in f:
        line = line.strip()

        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue

        txn_id = event.get("txn_id")
        if not txn_id:
            continue

        most_recent_txn = id_transactions.get(txn_id)
        if most_recent_txn is None or event["ts"] >= most_recent_txn["ts"]:
            id_transactions[txn_id] = event

for event in id_transactions.values():
    if event["status"] == "success":
        amount = event["amount"]
        if type(amount) == str:
            amount = amount.replace(",", "")
        total += float(amount)
        count += 1

with open("expected.txt") as f:
    expected = int(f.read().strip())

if count != expected:
    print(f"Check failed: counted {count} successful payments, expected {expected}.")
    print("Something in the data isn't being handled the way the README describes.")
else:
    print(f"Check passed: {count} successful payments.")
    print(f"Your code: KOYA-{round(total)}")
