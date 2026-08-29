from backend.analytics.revenue import calculate_revenue
from backend.ai.copilot import explain_finances

def finance_agent(state):
    revenue=calculate_revenue(state["data"])
    rec=state["reconciliation"]
    mismatch=float(rec.loc[rec["status"]=="MISMATCH","difference"].abs().sum())
    answer=explain_finances(
        state.get("question","Why is my revenue leaking?"),
        revenue, mismatch, int(state["anomalies"]["anomaly"].sum())
    )
    return {"revenue":revenue,"investigation":answer}
