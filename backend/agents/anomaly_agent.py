from backend.analytics.anomaly import detect_anomalies, detect_refund_spike
def anomaly_agent(state):
    df=detect_anomalies(state["data"].copy())
    info=detect_refund_spike(df)
    return {"anomalies":df, "investigation":f"Refund rate is {info['refund_rate']}%."}
