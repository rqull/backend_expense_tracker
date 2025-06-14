from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from typing import List

from .. import crud, schemas
from ..database import get_db

router = APIRouter(
    prefix="/budgets",
    tags=["Budgets"]
)

@router.post("/")
def create_budget(budget: schemas.BudgetCreate, db: Session = Depends(get_db)):
    new_budget = crud.create_budget(db=db, budget=budget)
    return JSONResponse(
        status_code=201,
        content={
            "status": "success",
            "data": schemas.Budget.from_orm(new_budget).dict(),
            "message": "Budget created successfully"
        }
    )

@router.get("/")
def read_budgets(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    budgets = crud.get_budgets(db, skip=skip, limit=limit)
    return JSONResponse(
        status_code=200,
        content={
            "status": "success",
            "data": {
                "items": [schemas.Budget.from_orm(b).dict() for b in budgets],
                "total": len(budgets),
                "page": 1,
                "size": len(budgets),
                "pages": 1
            },
            "message": None
        }
    )

@router.get("/{budget_id}")
def read_budget(budget_id: int, db: Session = Depends(get_db)):
    db_budget = crud.get_budget(db, budget_id=budget_id)
    if db_budget is None:
        raise HTTPException(status_code=404, detail="Budget not found")
    return JSONResponse(
        status_code=200,
        content={
            "status": "success",
            "data": schemas.Budget.from_orm(db_budget).dict(),
            "message": None
        }
    )

@router.put("/{budget_id}")
def update_budget(budget_id: int, budget: schemas.BudgetUpdate, db: Session = Depends(get_db)):
    updated = crud.update_budget(db=db, budget_id=budget_id, budget=budget)
    return JSONResponse(
        status_code=200,
        content={
            "status": "success",
            "data": schemas.Budget.from_orm(updated).dict(),
            "message": "Budget updated successfully"
        }
    )

@router.delete("/{budget_id}")
def delete_budget(budget_id: int, db: Session = Depends(get_db)):
    crud.delete_budget(db=db, budget_id=budget_id)
    return JSONResponse(
        status_code=200,
        content={
            "status": "success",
            "data": None,
            "message": "Budget deleted successfully"
        }
    )

@router.get("/status/")
def read_budget_status(
    year: int = Query(..., description="Year for budget status"),
    month: int = Query(..., description="Month for budget status (1-12)"),
    db: Session = Depends(get_db)
):
    if month < 1 or month > 12:
        raise HTTPException(status_code=400, detail="Month must be between 1 and 12")
    status_data = crud.get_budget_status(db=db, year=year, month=month)
    return JSONResponse(
        status_code=200,
        content={
            "status": "success",
            "data": [s for s in status_data],
            "message": None
        }
    )