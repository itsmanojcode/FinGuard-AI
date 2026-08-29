from langgraph.graph import StateGraph, END
from backend.agents.state import FinanceState
from backend.agents.reconciliation_agent import reconciliation_agent
from backend.agents.anomaly_agent import anomaly_agent
from backend.agents.finance_agent import finance_agent
from backend.agents.decision_agent import decision_agent
from backend.agents.audit_agent import audit_agent

def build_graph():
    g=StateGraph(FinanceState)
    g.add_node("reconcile",reconciliation_agent)
    g.add_node("anomaly",anomaly_agent)
    g.add_node("finance",finance_agent)
    g.add_node("decision",decision_agent)
    g.add_node("audit",audit_agent)
    g.set_entry_point("reconcile")
    g.add_edge("reconcile","anomaly")
    g.add_edge("anomaly","finance")
    g.add_edge("finance","decision")
    g.add_edge("decision","audit")
    g.add_edge("audit",END)
    return g.compile()
