from backend.models import Payment
from backend.agents.revenue_agent import analyze_failed_payment
from backend.services.audit_service import create_audit_log


def process_payment_failed(db, event_id, payload):

    payment_entity = (
        payload.get("payload", {})
        .get("payment", {})
        .get("entity", {})
    )

    payment_id = payment_entity.get("id")

    amount = payment_entity.get("amount", 0) / 100

    order_id = payment_entity.get("order_id")

    method = payment_entity.get("method")

    error_description = (
        payment_entity.get("error_description")
        or payment_entity.get("error_reason")
        or "Unknown payment failure"
    )

    existing_payment = (
        db.query(Payment)
        .filter_by(payment_id=payment_id)
        .first()
    )

    if existing_payment:
        payment = existing_payment

        payment.status = "failed"
        payment.failure_reason = error_description

    else:
        payment = Payment(
            payment_id=payment_id,
            order_id=order_id,
            amount=amount,
            currency=payment_entity.get("currency", "INR"),
            status="failed",
            method=method,
            failure_reason=error_description
        )

        db.add(payment)

    db.flush()

    analysis = analyze_failed_payment(
        amount=amount,
        failure_reason=error_description
    )

    payment.risk_score = min(
        100,
        max(0, amount / 100)
    )

    payment.recovery_status = analysis["recovery_status"]

    create_audit_log(
        db=db,
        agent="RevenueRecoveryAgent",
        event="payment.failed",
        decision=analysis["decision"],
        reason=analysis["reason"],
        action=analysis["action"],
        result=analysis["recovery_status"]
    )

    db.commit()

    return analysis