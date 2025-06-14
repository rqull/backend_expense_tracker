from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter(
    prefix="/health",
    tags=["Health"]
)

@router.get("/")
def health_check():
    return JSONResponse(content={"status": "ok"})

@router.get("/ping")
def ping():
    return JSONResponse(content={"ping": "pong"})   