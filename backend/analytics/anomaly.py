def detect_anomalies(df, z_threshold=2.5):
    r = df.copy()
    mean, std = r["amount"].mean(), r["amount"].std()
    r["z_score"] = 0.0 if std == 0 else (r["amount"] - mean) / std
    r["anomaly"] = r["z_score"].abs() > z_threshold
    return r

def detect_refund_spike(df, threshold=0.15):
    rate = float((df["refund"] > 0).mean())
    return {"refund_rate": round(rate*100,2), "is_spike": rate > threshold}
