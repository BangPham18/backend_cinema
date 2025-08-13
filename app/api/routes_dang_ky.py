from app.core.models import TaiKhoan, KhachHang
from app.core.security import hash_password
import re
import uuid
from pydantic import BaseModel, EmailStr
from app.core.database import get_session
from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from typing import Optional

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    ten: str
    nam_sinh: Optional[int] = None
    gioi_tinh: Optional[str] = None
    dia_chi: Optional[str] = None

router = APIRouter()

@router.post("/register")
def register(data: RegisterRequest):
    session: Session = get_session()
    try:

        # 2. Kiểm tra email đã tồn tại chưa
        existing_user = session.query(TaiKhoan).filter(TaiKhoan.email == data.email).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Email đã được sử dụng")

        # 3. Tạo mã khách hàng (ma_kh) đơn giản: UUID rút gọn hoặc tự sinh
        ma_kh = str(uuid.uuid4())[:8]  # ví dụ: 'a1b2c3d4'

        # 4. Tạo đối tượng KhachHang
        khach_hang = KhachHang(
            ma_kh=ma_kh,
            ten=data.ten,
            nam_sinh=data.nam_sinh,
            gioi_tinh=data.gioi_tinh,
            dia_chi=data.dia_chi
        )

        # 5. Tạo tài khoản và hash mật khẩu
        tai_khoan = TaiKhoan(
            email=data.email,
            mat_khau=hash_password(data.password),
            ma_kh=ma_kh
        )

        # 6. Thêm vào session và commit
        session.add(khach_hang)
        session.add(tai_khoan)
        session.commit()

        return {"message": "Đăng ký thành công"}
    finally:
        session.close()
