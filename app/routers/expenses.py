from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from typing import Optional
from datetime import date

from .. import crud, schemas
from ..database import get_db

router = APIRouter(
    prefix="/expenses",
    tags=["Expenses"]
)

@router.post("/")
def create_expense(expense: schemas.ExpenseCreate, db: Session = Depends(get_db)):
    new_exp = crud.create_expense(db=db, expense=expense)
    return JSONResponse(
        status_code=201,
        content={
            "status": "success",
            "data": schemas.Expense.from_orm(new_exp).dict(),
            "message": "Expense created successfully"
        }
    )

@router.get("/")
def read_expenses(
    skip: int = 0,
    limit: int = 100,
    category_id: Optional[int] = None,
    account_id: Optional[int] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: Session = Depends(get_db)
):
    expenses = crud.get_expenses(
        db,
        skip=skip,
        limit=limit,
        category_id=category_id,
        account_id=account_id,
        start_date=start_date,
        end_date=end_date
    )
    return JSONResponse(
        status_code=200,
        content={
            "status": "success",
            "data": {
                "items": [schemas.Expense.from_orm(e).dict() for e in expenses],
                "total": len(expenses),
                "page": 1,
                "size": len(expenses),
                "pages": 1
            },
            "message": None
        }
    )

@router.get("/stats")
def get_expense_summary(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    category_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    summary = crud.get_expense_summary(
        db,
        start_date=start_date,
        end_date=end_date,
        category_id=category_id
    )
    return JSONResponse(
        status_code=200,
        content={
            "status": "success",
            "data": summary,
            "message": None
        }
    )

@router.get("/{expense_id}")
def read_expense(expense_id: int, db: Session = Depends(get_db)):
    db_expense = crud.get_expense(db, expense_id=expense_id)
    if db_expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")
    return JSONResponse(
        status_code=200,
        content={
            "status": "success",
            "data": schemas.Expense.from_orm(db_expense).dict(),
            "message": None
        }
    )

@router.put("/{expense_id}")
def update_expense(expense_id: int, expense: schemas.ExpenseUpdate, db: Session = Depends(get_db)):
    updated = crud.update_expense(db=db, expense_id=expense_id, expense=expense)
    return JSONResponse(
        status_code=200,
        content={
            "status": "success",
            "data": schemas.Expense.from_orm(updated).dict(),
            "message": "Expense updated successfully"
        }
    )

@router.delete("/{expense_id}")
def delete_expense(expense_id: int, db: Session = Depends(get_db)):
    crud.delete_expense(db=db, expense_id=expense_id)
    return JSONResponse(
        status_code=200,
        content={
            "status": "success",
            "data": None,
            "message": "Expense deleted successfully"
        }
    )