from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import routes, routes_tai_khoan, routes_thong_tin_kh, routes_dang_ky, routes_poster, routes_lay_ve, routes_thay_doi_id

app = FastAPI(title="CGV Agent API")

# Cho phép frontend truy cập (nếu có)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Đổi thành domain frontend nếu cần bảo mật hơn
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Đăng ký router
app.include_router(routes.router)

app.include_router(routes_tai_khoan.router)

app.include_router(routes_thong_tin_kh.router)

app.include_router(routes_dang_ky.router)

app.include_router(routes_poster.router)

app.include_router(routes_lay_ve.router)

app.include_router(routes_thay_doi_id.router)

