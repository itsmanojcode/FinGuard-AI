import requests
from backend.config import RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET
BASE_URL="https://api.razorpay.com/v1"

def request(method,path,**kwargs):
    if not RAZORPAY_KEY_ID or not RAZORPAY_KEY_SECRET:
        raise RuntimeError("Razorpay test credentials are not configured in .env")
    return requests.request(method,BASE_URL+path,
                            auth=(RAZORPAY_KEY_ID,RAZORPAY_KEY_SECRET),
                            timeout=20,**kwargs)
