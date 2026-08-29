import random
import pandas as pd

def generate_transactions(n=1000, seed=42):
    random.seed(seed)
    rows = []
    for i in range(n):
        amount = round(random.uniform(200, 15000), 2)
        refund = round(amount * random.uniform(0.1, 0.8), 2) if random.random() < 0.10 else 0.0
        fee = round(amount * 0.02, 2)
        tax = round(fee * 0.18, 2)
        expected = round(amount - refund - fee - tax, 2)
        settlement = expected
        if random.random() < 0.05:
            settlement = round(expected * random.uniform(0.5, 0.95), 2)
        rows.append({
            "payment_id": f"pay_{i+1:05d}",
            "order_id": f"order_{i+1:05d}",
            "customer_id": f"cust_{random.randint(1,300)}",
            "amount": amount, "currency": "INR",
            "status": "failed" if random.random() < 0.08 else "success",
            "refund": refund, "fee": fee, "tax": tax,
            "expected": expected, "settlement": settlement,
            "payment_method": random.choice(["UPI","CARD","NETBANKING","WALLET"])
        })
    return pd.DataFrame(rows)
