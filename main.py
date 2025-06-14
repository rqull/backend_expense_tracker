# backend/app/main.py
import os
import time
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine
from app.models import Base
from app.routers import categories, expenses, budgets, accounts, tags, recurring, health, auth
from app.utils.error_handlers import (
    AppException, app_exception_handler,
    integrity_error_handler, operational_error_handler,
    validation_error_handler
)
from sqlalchemy.exc import IntegrityError, OperationalError

app = FastAPI(
    title="Expense Tracker API",
    description="API for tracking personal expenses and managing budgets",
    version="1.0.0"
)

# CORS middleware
origins = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request timing middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

# Exception handlers
app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(IntegrityError, integrity_error_handler)
app.add_exception_handler(OperationalError, operational_error_handler)
app.add_exception_handler(ValueError, validation_error_handler)

# Create tables (dev only)
if os.getenv("DEBUG", "False").lower() == "true":
    Base.metadata.create_all(bind=engine)

# Include routers with tags and prefixes
app.include_router(auth.router)
app.include_router(health.router)
app.include_router(categories.router)
app.include_router(expenses.router)
app.include_router(budgets.router)
app.include_router(accounts.router)
app.include_router(tags.router)
app.include_router(recurring.router)

@app.get("/")
async def root():
    return {
        "message": "Welcome to Expense Tracker API",
        "docs_url": "/docs",
        "redoc_url": "/redoc",
        "version": "1.0.0"
    }
