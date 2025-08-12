from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_session
from app.core.models import Ve
from typing import Optional

router = APIRouter()

@router.get("/ve")
def get_ve_by_email(
    email: Optional[str] = Query(None, description="Email khách hàng"),
    session: Session = Depends(get_session)
):
    query = session.query(Ve)

    if email:
        query = query.filter(Ve.email == email)

    ve_list = query.all()
    
    result = []

    if not ve_list:
        return result
    
    for ve in ve_list:
        phim = ve.lich_chieu.phim
        phong = ve.lich_chieu.phong_phim
        ghe = ve.ghe

        result.append({
            "ma_ve": ve.ma_ve,
            "ten_phim": phim.ten_phim if phim else None,
            "phong_phim": phong.ten_phong if phong else None,
            "ngay": str(ve.lich_chieu.ngay),
            "gio": str(ve.lich_chieu.gio),
            "ghe": ghe.ten_ghe if ghe else None,
            "poster": phim.poster if phim else None,
        })

    return result
