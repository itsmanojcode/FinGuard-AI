from backend.razorpay.client import request
def get_payments(count=100):
    r=request("GET","/payments",params={"count":count}); r.raise_for_status(); return r.json()
def get_payment(payment_id):
    r=request("GET",f"/payments/{payment_id}"); r.raise_for_status(); return r.json()
