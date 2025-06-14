from fastapi import Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError, OperationalError
from typing import Union, Dict, Any

class AppException(Exception):
    def __init__(
        self,
        status_code: int,
        detail: Union[str, Dict[str, Any]],
        headers: Dict[str, str] = None
    ):
        self.status_code = status_code
        self.detail = detail
        self.headers = headers

async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
        headers=exc.headers
    )

async def integrity_error_handler(request: Request, exc: IntegrityError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "detail": "Database constraint violation",
            "message": str(exc)
        }
    )

async def operational_error_handler(request: Request, exc: OperationalError):
    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content={
            "detail": "Database operation failed",
            "message": str(exc)
        }
    )

async def validation_error_handler(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": "Validation error",
            "message": str(exc)
        }
    )
