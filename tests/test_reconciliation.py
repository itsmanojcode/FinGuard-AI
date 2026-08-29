import pandas as pd
from backend.analytics.reconciliation import reconcile_dataframe
def test_reconciled_transaction():
    df=pd.DataFrame([{"payment_id":"p1","amount":1000,"refund":100,"fee":20,"tax":3.6,"settlement":876.4}])
    assert reconcile_dataframe(df).iloc[0]["status"]=="RECONCILED"
def test_mismatch_transaction():
    df=pd.DataFrame([{"payment_id":"p1","amount":1000,"refund":100,"fee":20,"tax":3.6,"settlement":500}])
    assert reconcile_dataframe(df).iloc[0]["status"]=="MISMATCH"
