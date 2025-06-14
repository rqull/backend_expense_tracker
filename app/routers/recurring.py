from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from typing import Optional
from datetime import date

from .. import crud, schemas
from ..database import get_db

router = APIRouter(
    prefix="/recurring",
    tags=["Recurring"]
)

@router.post("/")
def create_recurring_expense(recurring: schemas.RecurringExpenseCreate, db: Session = Depends(get_db)):
    new_rec = crud.create_recurring_expense(db=db, recurring=recurring)
    return JSONResponse(
        status_code=201,
        content={
            "status": "success",
            "data": schemas.RecurringExpense.from_orm(new_rec).dict(),
            "message": "Recurring expense created successfully"
        }
    )

@router.get("/")
def read_recurring_expenses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    recs = crud.get_recurring_expenses(db, skip=skip, limit=limit)
    return JSONResponse(
        status_code=200,
        content={
            "status": "success",
            "data": {
                "items": [schemas.RecurringExpense.from_orm(r).dict() for r in recs],
                "total": len(recs),
                "page": 1,
                "size": len(recs),
                "pages": 1
            },
            "message": None
        }
    )

@router.get("/{recurring_id}")
def read_recurring_expense(recurring_id: int, db: Session = Depends(get_db)):
    db_rec = crud.get_recurring_expense(db, recurring_id=recurring_id)
    if db_rec is None:
        raise HTTPException(status_code=404, detail="Recurring expense not found")
    return JSONResponse(
        status_code=200,
        content={
            "status": "success",
            "data": schemas.RecurringExpense.from_orm(db_rec).dict(),
            "message": None
        }
    )

@router.put("/{recurring_id}")
def update_recurring_expense(recurring_id: int, recurring: schemas.RecurringExpenseUpdate, db: Session = Depends(get_db)):
    updated = crud.update_recurring_expense(db=db, recurring_id=recurring_id, recurring=recurring)
    return JSONResponse(
        status_code=200,
        content={
            "status": "success",
            "data": schemas.RecurringExpense.from_orm(updated).dict(),
            "message": "Recurring expense updated successfully"
        }
    )

@router.delete("/{recurring_id}")
def delete_recurring_expense(recurring_id: int, db: Session = Depends(get_db)):
    crud.delete_recurring_expense(db=db, recurring_id=recurring_id)
    return JSONResponse(
        status_code=200,
        content={
            "status": "success",
            "data": None,
            "message": "Recurring expense deleted successfully"
        }
    )

@router.post("/generate/")
def generate_recurring_expenses(date_today: Optional[date] = None, db: Session = Depends(get_db)):
    if date_today is None:
        date_today = date.today()
    generated = crud.generate_recurring_expenses(db=db, date_today=date_today)
    return JSONResponse(
        status_code=200,
        content={
            "status": "success",
            "data": [schemas.Expense.from_orm(e).dict() for e in generated],
            "message": "Successfully generated recurring expenses"
        }
    )