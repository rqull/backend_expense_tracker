from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List

from .. import crud, schemas
from ..database import get_db

router = APIRouter(
    prefix="/budgets",
    tags=["budgets"]
)

@router.post("/", response_model=schemas.Budget, status_code=status.HTTP_201_CREATED)
def create_budget(budget: schemas.BudgetCreate, db: Session = Depends(get_db)):
    return crud.create_budget(db=db, budget=budget)

@router.get("/", response_model=List[schemas.Budget])
def read_budgets(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    budgets = crud.get_budgets(db, skip=skip, limit=limit)
    return budgets

@router.get("/{budget_id}", response_model=schemas.Budget)
def read_budget(budget_id: int, db: Session = Depends(get_db)):
    db_budget = crud.get_budget(db, budget_id=budget_id)
    if db_budget is None:
        raise HTTPException(status_code=404, detail="Budget not found")
    return db_budget

@router.put("/{budget_id}", response_model=schemas.Budget)
def update_budget(budget_id: int, budget: schemas.BudgetUpdate, db: Session = Depends(get_db)):
    return crud.update_budget(db=db, budget_id=budget_id, budget=budget)

@router.delete("/{budget_id}", status_code=status.HTTP_200_OK)
def delete_budget(budget_id: int, db: Session = Depends(get_db)):
    return crud.delete_budget(db=db, budget_id=budget_id)

@router.get("/status/", response_model=List[schemas.BudgetStatus])
def read_budget_status(
    year: int = Query(..., description="Year for budget status"),
    month: int = Query(..., description="Month for budget status (1-12)"),
    db: Session = Depends(get_db)
):
    # Validate month
    if month < 1 or month > 12:
        raise HTTPException(status_code=400, detail="Month must be between 1 and 12")

    return crud.get_budget_status(db=db, year=year, month=month)