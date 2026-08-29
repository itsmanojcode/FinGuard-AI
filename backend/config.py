import os
from dotenv import load_dotenv
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///finguard.db")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
RAZORPAY_KEY_ID = os.getenv("RAZORPAY_KEY_ID", "")
RAZORPAY_KEY_SECRET = os.getenv("RAZORPAY_KEY_SECRET", "")
RAZORPAY_WEBHOOK_SECRET = os.getenv("RAZORPAY_WEBHOOK_SECRET", "")
AUTO_ACTION_LIMIT = float(os.getenv("AUTO_ACTION_LIMIT", "1000"))
APPROVAL_LIMIT = float(os.getenv("APPROVAL_LIMIT", "5000"))
