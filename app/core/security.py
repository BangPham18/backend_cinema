from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
import os
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.core.models import TaiKhoan
from app.core.database import get_session


SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60  # Token hết hạn sau 60 phút

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    
    # Thiết lập thời gian hết hạn token
    expire = datetime.now(timezone.utc) + (expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    
    # Tạo JWT token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login", auto_error=False)
def get_current_user(token: str = Depends(oauth2_scheme)):
    session: Session = get_session()
    if not token or len(token.split(".")) != 3:
        return None
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        user = session.query(TaiKhoan).filter(TaiKhoan.email == email).first()
        dict_if = {"ten": user.khach_hang.ten,
                   "namsinh": user.khach_hang.nam_sinh,
                   "gioitinh": user.khach_hang.gioi_tinh,
                   "email": user.email}
        return dict_if
    finally:
        session.close()
