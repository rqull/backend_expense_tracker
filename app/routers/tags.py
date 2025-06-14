from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse

from .. import crud, schemas
from ..database import get_db

router = APIRouter(
    prefix="/tags",
    tags=["Tags"]
)

@router.post("/")
def create_tag(tag: schemas.TagCreate, db: Session = Depends(get_db)):
    new_tag = crud.create_tag(db=db, tag=tag)
    return JSONResponse(
        status_code=201,
        content={
            "status": "success",
            "data": schemas.Tag.from_orm(new_tag).dict(),
            "message": "Tag created successfully"
        }
    )

@router.get("/")
def read_tags(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    tags = crud.get_tags(db, skip=skip, limit=limit)
    return JSONResponse(
        status_code=200,
        content={
            "status": "success",
            "data": {
                "items": [schemas.Tag.from_orm(tag).dict() for tag in tags],
                "total": len(tags),
                "page": 1,
                "size": len(tags),
                "pages": 1
            },
            "message": None
        }
    )

@router.get("/{tag_id}")
def read_tag(tag_id: int, db: Session = Depends(get_db)):
    db_tag = crud.get_tag(db, tag_id=tag_id)
    if db_tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")
    return JSONResponse(
        status_code=200,
        content={
            "status": "success",
            "data": schemas.Tag.from_orm(db_tag).dict(),
            "message": None
        }
    )

@router.put("/{tag_id}")
def update_tag(tag_id: int, tag: schemas.TagUpdate, db: Session = Depends(get_db)):
    updated = crud.update_tag(db=db, tag_id=tag_id, tag=tag)
    return JSONResponse(
        status_code=200,
        content={
            "status": "success",
            "data": schemas.Tag.from_orm(updated).dict(),
            "message": "Tag updated successfully"
        }
    )

@router.delete("/{tag_id}")
def delete_tag(tag_id: int, db: Session = Depends(get_db)):
    crud.delete_tag(db=db, tag_id=tag_id)
    return JSONResponse(
        status_code=200,
        content={
            "status": "success",
            "data": None,
            "message": "Tag deleted successfully"
        }
    )