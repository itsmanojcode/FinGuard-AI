from backend.ai.gemini import generate_with_gemini
from backend.ai.prompts import FINANCE_PROMPT

def explain_finances(question, revenue, mismatch_amount, anomaly_count):
    facts = (
        f"Question: {question}\n"
        f"Gross: ₹{revenue['gross_revenue']:,.2f}\n"
        f"Refunds: ₹{revenue['refunds']:,.2f}\n"
        f"Fees: ₹{revenue['fees']:,.2f}\n"
        f"Tax: ₹{revenue['tax']:,.2f}\n"
        f"Net: ₹{revenue['net_revenue']:,.2f}\n"
        f"Unreconciled: ₹{mismatch_amount:,.2f}\n"
        f"Anomalies: {anomaly_count}\n"
    )
    answer=generate_with_gemini(FINANCE_PROMPT+"\n"+facts)
    return answer or (
        f"Net revenue is ₹{revenue['net_revenue']:,.2f}. "
        f"Refunds are ₹{revenue['refunds']:,.2f}; fees and tax are "
        f"₹{revenue['fees']+revenue['tax']:,.2f}; unreconciled amount is "
        f"₹{mismatch_amount:,.2f}. {anomaly_count} anomalies were detected. "
        "Gemini is not configured, so this is the deterministic fallback."
    )
