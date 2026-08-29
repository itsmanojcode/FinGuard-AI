from datetime import datetime
def audit_agent(state):
    events=state.get("audit_events",[])
    events.append({"agent":"Audit Agent","event":"Workflow completed",
                   "decision":"Recorded","timestamp":datetime.utcnow().isoformat()})
    return {"audit_events":events}
