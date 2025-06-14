from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from fastapi.responses import JSONResponse

from .. import crud, schemas
from ..database import get_db

router = APIRouter(
    prefix="/categories",
    tags=["Categories"]
)

@router.post("/")
def create_category(category: schemas.CategoryCreate, db: Session = Depends(get_db)):
    new_cat = crud.create_category(db=db, category=category)
    return JSONResponse(
        status_code=201,
        content={
            "status": "success",
            "data": schemas.Category.from_orm(new_cat).dict(),
            "message": "Category created successfully"
        }
    )

@router.get("/")
def read_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    categories = crud.get_categories(db, skip=skip, limit=limit)
    return JSONResponse(
        status_code=200,
        content={
            "status": "success",
            "data": {
                "items": [schemas.Category.from_orm(cat).dict() for cat in categories],
                "total": len(categories),
                "page": 1,
                "size": len(categories),
                "pages": 1
            },
            "message": None
        }
    )

@router.get("/{category_id}")
def read_category(category_id: int, db: Session = Depends(get_db)):
    db_category = crud.get_category(db, category_id=category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return JSONResponse(
        status_code=200,
        content={
            "status": "success",
            "data": schemas.Category.from_orm(db_category).dict(),
            "message": None
        }
    )

@router.put("/{category_id}")
def update_category(category_id: int, category: schemas.CategoryUpdate, db: Session = Depends(get_db)):
    updated = crud.update_category(db=db, category_id=category_id, category=category)
    return JSONResponse(
        status_code=200,
        content={
            "status": "success",
            "data": schemas.Category.from_orm(updated).dict(),
            "message": "Category updated successfully"
        }
    )

@router.delete("/{category_id}")
def delete_category(category_id: int, db: Session = Depends(get_db)):
    crud.delete_category(db=db, category_id=category_id)
    return JSONResponse(
        status_code=200,
        content={
            "status": "success",
            "data": None,
            "message": "Category deleted successfully"
        }
    )