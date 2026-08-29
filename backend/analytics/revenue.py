def calculate_revenue(df):
    gross = float(df["amount"].sum())
    refunds = float(df["refund"].sum())
    fees = float(df["fee"].sum())
    tax = float(df["tax"].sum())
    return {
        "gross_revenue": round(gross,2),
        "refunds": round(refunds,2),
        "fees": round(fees,2),
        "tax": round(tax,2),
        "net_revenue": round(gross-refunds-fees-tax,2)
    }
