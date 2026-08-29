import pandas as pd
from backend.analytics.anomaly import detect_anomalies
def test_anomaly_column():
    result=detect_anomalies(pd.DataFrame({"amount":[100,110,105,10000]}))
    assert "anomaly" in result.columns
    assert result["anomaly"].sum() >= 1
