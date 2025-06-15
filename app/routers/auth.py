from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from .. import crud, schemas
from ..database import get_db
from ..utils.security import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    create_access_token,
    verify_password,
    get_password_hash,
    oauth2_scheme,
    verify_token
)

router = APIRouter(
    tags=["Authentication"]
)

@router.post("/auth/register")
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        # Check if user exists
        db_user = crud.get_user_by_username(db, username=user.username)
        if db_user:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "status": "error",
                    "data": None,
                    "message": "Username already registered"
                }
            )
        
        # Check if email exists
        db_user = crud.get_user_by_email(db, email=user.email)
        if db_user:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "status": "error",
                    "data": None,
                    "message": "Email already registered"
                }
            )
        
        # Create new user
        hashed_password = get_password_hash(user.password)
        new_user = crud.create_user(db=db, user=user, hashed_password=hashed_password)
        
        # Convert user to dict and format datetime
        user_dict = schemas.User.from_orm(new_user).model_dump()
        user_dict["created_at"] = user_dict["created_at"].isoformat()
        user_dict["updated_at"] = user_dict["updated_at"].isoformat()
        
        return JSONResponse(
            status_code=201,
            content={
                "status": "success",
                "data": user_dict,
                "message": "User registered successfully"
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "status": "error",
                "data": None,
                "message": str(e)
            }
        )

@router.post("/auth/token")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    try:
        # Authenticate user
        user = crud.get_user_by_username(db, username=form_data.username)
        if not user or not verify_password(form_data.password, user.hashed_password):
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={
                    "status": "error",
                    "data": None,
                    "message": "Incorrect username or password"
                }
            )
        
        # Create access token
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username},
            expires_delta=access_token_expires
        )
        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "data": {
                    "access_token": access_token,
                    "token_type": "bearer",
                    "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60
                },
                "message": "Successfully logged in"
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "status": "error",
                "data": None,
                "message": str(e)
            }
        )

@router.get("/auth/me")
async def read_users_me(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    try:
        payload = verify_token(token)
        username: str = payload.get("sub")
        if username is None:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={
                    "status": "error",
                    "data": None,
                    "message": "Could not validate credentials"
                }
            )
        
        user = crud.get_user_by_username(db, username=username)
        if user is None:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={
                    "status": "error",
                    "data": None,
                    "message": "User not found"
                }
            )
        
        # Convert user to dict and format datetime
        user_dict = schemas.User.from_orm(user).model_dump()
        user_dict["created_at"] = user_dict["created_at"].isoformat()
        user_dict["updated_at"] = user_dict["updated_at"].isoformat()
        
        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "data": user_dict,
                "message": None
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "status": "error",
                "data": None,
                "message": str(e)
            }
        )

@router.put("/auth/me")
async def update_user_profile(
    user_update: schemas.UserUpdate,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    try:
        payload = verify_token(token)
        username: str = payload.get("sub")
        if username is None:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={
                    "status": "error",
                    "data": None,
                    "message": "Could not validate credentials"
                }
            )
        
        user = crud.get_user_by_username(db, username=username)
        if user is None:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={
                    "status": "error",
                    "data": None,
                    "message": "User not found"
                }
            )

        # Verify current password if provided
        if user_update.password:
            if not verify_password(user_update.password, user.hashed_password):
                return JSONResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content={
                        "status": "error",
                        "data": None,
                        "message": "Current password is incorrect"
                    }
                )
        
        # Update user
        updated_user = crud.update_user(db=db, user_id=user.id, user=user_update)
        
        # Convert user to dict and format datetime
        user_dict = schemas.User.from_orm(updated_user).model_dump()
        user_dict["created_at"] = user_dict["created_at"].isoformat()
        user_dict["updated_at"] = user_dict["updated_at"].isoformat()
        
        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "data": user_dict,
                "message": "Profile updated successfully"
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "status": "error",
                "data": None,
                "message": str(e)
            }
        )
