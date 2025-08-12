from fastapi import APIRouter, Depends
from app.core.security import get_current_user

router = APIRouter()

@router.get("/me")
def get_user_info(current_user: dict = Depends(get_current_user)):
    return {
        "ten": current_user["ten"],
        "namsinh": current_user["namsinh"],
        "gioitinh": current_user["gioitinh"],
        "email": current_user["email"]
    }
