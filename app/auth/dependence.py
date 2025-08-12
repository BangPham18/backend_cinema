# # auth/dependencies.py

# from fastapi import Depends, HTTPException
# from fastapi.security import OAuth2PasswordBearer
# from jose import jwt, JWTError
# import os

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")  # hoặc "token" nếu bạn dùng /token để login

# SECRET_KEY = os.environ.get("SECRET_KEY")
# ALGORITHM = "HS256"

# def get_current_user(token: str = Depends(oauth2_scheme)):
    
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         return {
#             "user_id": payload.get("sub"),
#             "email": payload.get("email"),
#             "name": payload.get("name"),
#         }
#     except JWTError:
#         raise HTTPException(status_code=401, detail="Invalid token")
