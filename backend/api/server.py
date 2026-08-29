
from fastapi import FastAPI

from backend.api.routes import router as routes_router
from backend.api.webhook import router as webhook_router
from backend.database import init_db


app = FastAPI(
    title="FinGuard AI API"
)


# Initialize database
init_db()


# Normal API routes
app.include_router(
    routes_router,
    prefix="/api"
)


# Razorpay webhook routes
app.include_router(
    webhook_router,
    prefix="/api/webhooks"
)

