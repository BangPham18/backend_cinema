# app/api/routes.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.core.database import get_session
from app.core.security import verify_password
from app.core.security import create_access_token
from datetime import timedelta
from sqlalchemy.orm import Session
from app.core.models import TaiKhoan

router = APIRouter()

class LoginRequest(BaseModel):
    username: str
    password: str

@router.post("/login")

def login(data: LoginRequest):
    session: Session = get_session()
    try:
        user = session.query(TaiKhoan).filter(TaiKhoan.email == data.username).first()
        
        if not user:
            raise HTTPException(status_code=401, detail="Sai tên tài khoản")

        if not verify_password(data.password, user.mat_khau):
            raise HTTPException(status_code=401, detail="Sai mật khẩu")

        access_token = create_access_token(
            data={"sub": user.email},
            expires_delta=timedelta(minutes=60)
        )

        dict_if = {
            "access_token": access_token,
            "token_type": "bearer"
        }

        return dict_if
    finally:
        session.close()
