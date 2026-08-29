import pandas as pd

def reconcile_dataframe(df):
    r = df.copy()
    r["expected_amount"] = (r["amount"] - r["refund"] - r["fee"] - r["tax"]).round(2)
    r["difference"] = (r["expected_amount"] - r["settlement"]).round(2)
    r["status"] = r["difference"].abs().le(1).map({True:"RECONCILED", False:"MISMATCH"})
    r["reason"] = r["status"].map({
        "RECONCILED":"Settlement matches expected amount",
        "MISMATCH":"Settlement differs from expected amount"
    })
    return r[["payment_id","expected_amount","settlement","difference","status","reason"]].rename(
        columns={"settlement":"settled_amount"}
    )
