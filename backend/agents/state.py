from typing import TypedDict, Any
class FinanceState(TypedDict, total=False):
    data: Any
    question: str
    reconciliation: Any
    anomalies: Any
    revenue: dict
    investigation: str
    decision: str
    safety_result: dict
    audit_events: list
