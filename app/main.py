from fastapi import FastAPI
from app.api import auth, users

app = FastAPI(title="Eurobot Backend API")

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(users.router, prefix="/users", tags=["Users"])

