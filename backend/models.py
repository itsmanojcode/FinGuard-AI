from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime
from backend.database import Base

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True)
    payment_id = Column(String, unique=True, index=True)
    order_id = Column(String, index=True)
    customer_id = Column(String)
    amount = Column(Float)
    currency = Column(String, default="INR")
    status = Column(String)
    method = Column(String)

    failure_reason = Column(String, nullable=True)
    risk_score = Column(Float, nullable=True)
    recovery_status = Column(String, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

class Refund(Base):
    __tablename__ = "refunds"
    id = Column(Integer, primary_key=True)
    refund_id = Column(String, unique=True, index=True)
    payment_id = Column(String, index=True)
    amount = Column(Float)
    status = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

class Settlement(Base):
    __tablename__ = "settlements"
    id = Column(Integer, primary_key=True)
    settlement_id = Column(String, unique=True, index=True)
    payment_id = Column(String, index=True)
    amount = Column(Float)
    status = Column(String)
    settlement_date = Column(DateTime, default=datetime.utcnow)

class Fee(Base):
    __tablename__ = "fees"
    id = Column(Integer, primary_key=True)
    payment_id = Column(String, index=True)
    fee = Column(Float)
    tax = Column(Float)
    total_deduction = Column(Float)

class Reconciliation(Base):
    __tablename__ = "reconciliation"
    id = Column(Integer, primary_key=True)
    payment_id = Column(String, index=True)
    expected_amount = Column(Float)
    settled_amount = Column(Float)
    difference = Column(Float)
    status = Column(String)
    reason = Column(String)

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(Integer, primary_key=True)
    event_id = Column(String, unique=True, index=True)
    agent = Column(String)
    event = Column(String)
    decision = Column(String)
    reason = Column(String)
    action = Column(String)
    result = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)

class WebhookEvent(Base):
    __tablename__ = "webhook_events"
    id = Column(Integer, primary_key=True)
    event_id = Column(String, unique=True, index=True)
    event_type = Column(String)
    received_at = Column(DateTime, default=datetime.utcnow)
