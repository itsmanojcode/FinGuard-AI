import uuid
from backend.models import AuditLog
def create_audit_log(db,agent,event,decision,reason,action,result):
    row=AuditLog(event_id=str(uuid.uuid4()),agent=agent,event=event,
                 decision=decision,reason=reason,action=action,result=result)
    db.add(row); db.commit(); return row
