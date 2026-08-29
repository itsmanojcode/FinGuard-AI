def create_approval_request(action, amount, reason):
    return {"status":"PENDING","action":action,"amount":float(amount),"reason":reason}
def approve_request(request):
    r=dict(request); r["status"]="APPROVED"; return r
def reject_request(request, reason="Rejected by reviewer"):
    r=dict(request); r["status"]="REJECTED"; r["review_reason"]=reason; return r
