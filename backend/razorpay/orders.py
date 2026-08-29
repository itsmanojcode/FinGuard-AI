from backend.razorpay.client import request
def create_order(amount_paise, receipt, currency="INR"):
    r=request("POST","/orders",json={"amount":int(amount_paise),"currency":currency,"receipt":receipt})
    r.raise_for_status(); return r.json()
def get_order(order_id):
    r=request("GET",f"/orders/{order_id}"); r.raise_for_status(); return r.json()
