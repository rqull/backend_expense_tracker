from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from typing import List

from .. import crud, schemas
from ..database import get_db

router = APIRouter(
    prefix="/accounts",
    tags=["Accounts"]
)

@router.post("/")
def create_account(account: schemas.AccountCreate, db: Session = Depends(get_db)):
    new_acc = crud.create_account(db=db, account=account)
    return JSONResponse(
        status_code=201,
        content={
            "status": "success",
            "data": schemas.Account.from_orm(new_acc).dict(),
            "message": "Account created successfully"
        }
    )

@router.get("/")
def read_accounts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    accounts = crud.get_accounts(db, skip=skip, limit=limit)
    return JSONResponse(
        status_code=200,
        content={
            "status": "success",
            "data": {
                "items": [schemas.Account.from_orm(acc).dict() for acc in accounts],
                "total": len(accounts),
                "page": 1,
                "size": len(accounts),
                "pages": 1
            },
            "message": None
        }
    )

@router.get("/{account_id}")
def read_account(account_id: int, db: Session = Depends(get_db)):
    db_account = crud.get_account(db, account_id=account_id)
    if db_account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    return JSONResponse(
        status_code=200,
        content={
            "status": "success",
            "data": schemas.Account.from_orm(db_account).dict(),
            "message": None
        }
    )

@router.put("/{account_id}")
def update_account(account_id: int, account: schemas.AccountUpdate, db: Session = Depends(get_db)):
    updated = crud.update_account(db=db, account_id=account_id, account=account)
    return JSONResponse(
        status_code=200,
        content={
            "status": "success",
            "data": schemas.Account.from_orm(updated).dict(),
            "message": "Account updated successfully"
        }
    )

@router.delete("/{account_id}")
def delete_account(account_id: int, db: Session = Depends(get_db)):
    crud.delete_account(db=db, account_id=account_id)
    return JSONResponse(
        status_code=200,
        content={
            "status": "success",
            "data": None,
            "message": "Account deleted successfully"
        }
    )