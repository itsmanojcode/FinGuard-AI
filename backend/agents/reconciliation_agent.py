from backend.analytics.reconciliation import reconcile_dataframe
def reconciliation_agent(state):
    return {"reconciliation": reconcile_dataframe(state["data"])}
