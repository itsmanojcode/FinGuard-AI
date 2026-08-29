from backend.safety.policy import evaluate_action

def decision_agent(state):
    rec=state["reconciliation"]
    amount=float(rec.loc[rec["status"]=="MISMATCH","difference"].abs().sum())
    decision=("No exception requires intervention." if amount==0 else
              f"Create an exception case for ₹{amount:,.2f}. Do not autonomously move merchant funds.")
    safety=evaluate_action(amount,"exception_resolution")
    return {
        "decision":decision,
        "safety_result":safety,
        "audit_events":[{
            "agent":"Decision Agent","event":"Bounded financial decision",
            "decision":decision,"safety_status":safety["status"]
        }]
    }
