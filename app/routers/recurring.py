from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date

from .. import crud, schemas
from ..database import get_db

router = APIRouter(
    prefix="/recurring",
    tags=["recurring"]
)

@router.post("/", response_model=schemas.RecurringExpense, status_code=status.HTTP_201_CREATED)
def create_recurring_expense(recurring: schemas.RecurringExpenseCreate, db: Session = Depends(get_db)):
    return crud.create_recurring_expense(db=db, recurring=recurring)

@router.get("/", response_model=List[schemas.RecurringExpense])
def read_recurring_expenses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    recurring_expenses = crud.get_recurring_expenses(db, skip=skip, limit=limit)
    return recurring_expenses

@router.get("/{recurring_id}", response_model=schemas.RecurringExpense)
def read_recurring_expense(recurring_id: int, db: Session = Depends(get_db)):
    db_recurring = crud.get_recurring_expense(db, recurring_id=recurring_id)
    if db_recurring is None:
        raise HTTPException(status_code=404, detail="Recurring expense not found")
    return db_recurring

@router.put("/{recurring_id}", response_model=schemas.RecurringExpense)
def update_recurring_expense(recurring_id: int, recurring: schemas.RecurringExpenseUpdate, db: Session = Depends(get_db)):
    return crud.update_recurring_expense(db=db, recurring_id=recurring_id, recurring=recurring)

@router.delete("/{recurring_id}", status_code=status.HTTP_200_OK)
def delete_recurring_expense(recurring_id: int, db: Session = Depends(get_db)):
    return crud.delete_recurring_expense(db=db, recurring_id=recurring_id)

@router.post("/generate/", response_model=List[schemas.Expense])
def generate_recurring_expenses(date_today: Optional[date] = None, db: Session = Depends(get_db)):
    """Generate expenses from recurring expenses that are due"""
    if date_today is None:
        date_today = date.today()

    generated = crud.generate_recurring_expenses(db=db, date_today=date_today)
    return generated