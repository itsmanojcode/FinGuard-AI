from backend.razorpay.client import request
def get_settlements(count=100):
    r=request("GET","/settlements",params={"count":count}); r.raise_for_status(); return r.json()
