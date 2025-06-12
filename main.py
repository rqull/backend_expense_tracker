# backend/app/main.py
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine
from app.models import Base
from app.routers import categories, expenses, budgets, accounts, tags, recurring, health

app = FastAPI(title="Expense Tracker API")

# CORS
origins = ["http://localhost:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables (dev lokal)
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(health.router)      
app.include_router(categories.router)
app.include_router(expenses.router)
app.include_router(budgets.router)
app.include_router(accounts.router)
app.include_router(tags.router)
app.include_router(recurring.router)
