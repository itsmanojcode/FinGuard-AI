from fastapi import APIRouter
from backend.database import get_db
from backend.models import Payment, AuditLog

router = APIRouter()


@router.get("/health")
def health():
    return {
        "status": "ok",
        "service": "FinGuard AI"
    }


@router.get("/payments")
def get_payments():
    db = get_db()

    try:
        payments = db.query(Payment).order_by(
            Payment.id.desc()
        ).all()

        return [
            {
                "id": p.id,
                "payment_id": p.payment_id,
                "order_id": p.order_id,
                "amount": p.amount,
                "currency": p.currency,
                "status": p.status,
                "method": p.method,
                "failure_reason": getattr(
                    p, "failure_reason", None
                ),
                "risk_score": getattr(
                    p, "risk_score", None
                ),
                "recovery_status": getattr(
                    p, "recovery_status", None
                )
            }
            for p in payments
        ]

    finally:
        db.close()


@router.get("/payments/failed")
def get_failed_payments():
    db = get_db()

    try:
        payments = db.query(Payment).filter(
            Payment.status == "failed"
        ).order_by(
            Payment.id.desc()
        ).all()

        return [
            {
                "payment_id": p.payment_id,
                "amount": p.amount,
                "currency": p.currency,
                "method": p.method,
                "failure_reason": getattr(
                    p, "failure_reason", None
                ),
                "risk_score": getattr(
                    p, "risk_score", None
                ),
                "recovery_status": getattr(
                    p, "recovery_status", None
                )
            }
            for p in payments
        ]

    finally:
        db.close()


@router.get("/revenue-risk")
def revenue_risk():
    db = get_db()

    try:
        failed = db.query(Payment).filter(
            Payment.status == "failed"
        ).all()

        total_revenue_at_risk = sum(
            p.amount or 0 for p in failed
        )

        auto_recovery = sum(
            p.amount or 0
            for p in failed
            if getattr(p, "recovery_status", None)
            == "eligible"
        )

        approval_required = sum(
            p.amount or 0
            for p in failed
            if getattr(p, "recovery_status", None)
            == "pending_approval"
        )

        manual_review = sum(
            p.amount or 0
            for p in failed
            if getattr(p, "recovery_status", None)
            == "manual_review"
        )

        return {
            "failed_payments": len(failed),
            "total_revenue_at_risk": total_revenue_at_risk,
            "auto_recovery_amount": auto_recovery,
            "approval_required_amount": approval_required,
            "manual_review_amount": manual_review
        }

    finally:
        db.close()