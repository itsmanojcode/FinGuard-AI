from backend.config import AUTO_ACTION_LIMIT, APPROVAL_LIMIT


def analyze_failed_payment(amount, failure_reason=None):
    """
    Analyze a failed payment and decide the safest recovery path.

    The agent does NOT directly move money.
    It only recommends a bounded recovery action.
    """

    amount = float(amount or 0)

    failure_reason = (
        failure_reason
        or "Unknown payment failure"
    )

    # -----------------------------
    # Risk / Failure Reason Analysis
    # -----------------------------

    reason_lower = failure_reason.lower()

    if "insufficient" in reason_lower:
        reason = "Payment failed due to insufficient funds."

    elif "declined" in reason_lower:
        reason = "Payment was declined by the bank or payment network."

    elif "timeout" in reason_lower:
        reason = "Payment attempt timed out and may be retried safely."

    elif "network" in reason_lower:
        reason = "Payment failed because of a possible network issue."

    else:
        reason = f"Payment failure detected: {failure_reason}"

    # -----------------------------
    # Safety Gate 1
    # -----------------------------

    if amount <= AUTO_ACTION_LIMIT:

        decision = "AUTO_ACTION_ALLOWED"
        action = "payment_retry"
        recovery_status = "eligible"

    # -----------------------------
    # Safety Gate 2
    # -----------------------------

    elif amount <= APPROVAL_LIMIT:

        decision = "APPROVAL_REQUIRED"
        action = "payment_retry_with_approval"
        recovery_status = "pending_approval"

    # -----------------------------
    # Safety Gate 3
    # -----------------------------

    else:

        decision = "MANUAL_REVIEW_REQUIRED"
        action = "manual_recovery"
        recovery_status = "manual_review"

    # -----------------------------
    # Risk Score
    # -----------------------------

    risk_score = min(
        100.0,
        max(0.0, amount / 100.0)
    )

    # -----------------------------
    # Final Agent Decision
    # -----------------------------

    return {
        "revenue_at_risk": amount,
        "risk_score": risk_score,
        "failure_reason": failure_reason,

        # IMPORTANT:
        # event_processor.py requires this key
        "reason": reason,

        "decision": decision,
        "action": action,
        "recovery_status": recovery_status
    }