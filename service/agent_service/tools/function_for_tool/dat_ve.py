from sqlalchemy.orm import Session
from app.core.models import Phim, TrangThaiGhe, LichChieu, Ghe, Ve
from uuid import uuid4
from datetime import datetime
from typing import List
from app.core.database import get_session
import asyncio

def dat_ve(
    email: str,
    ten_phim: str,
    ngay: str,
    gio: str,
    ghe: List[str]
) -> List[str] | str:
    session: Session = get_session()
    try:
        ngay_chieu = datetime.strptime(ngay, "%d/%m/%Y").date()
        gio_chieu = datetime.strptime(gio, "%H:%M").time()

        lich_chieu = (
            session.query(LichChieu)
            .join(Phim)
            .filter(
                Phim.ten_phim == ten_phim,
                LichChieu.ngay == ngay_chieu,
                LichChieu.gio == gio_chieu
            )
            .first()
        )
        if not lich_chieu:
            return "Không tìm thấy suất chiếu phù hợp."

        ve_da_dat = []

        for ten_ghe in ghe:
            ghe_obj = (
                session.query(Ghe)
                .filter_by(ten_ghe=ten_ghe)
                .join(TrangThaiGhe)
                .filter(TrangThaiGhe.ma_phong == lich_chieu.ma_phong)
                .first()
            )
            if not ghe_obj:
                return f"Ghế {ten_ghe} không tồn tại trong phòng chiếu."

            da_dat = (
                session.query(Ve)
                .filter_by(ma_lich_chieu=lich_chieu.ma_lich_chieu, ma_ghe=ghe_obj.ma_ghe)
                .first()
            )
            if da_dat:
                return f"Ghế {ten_ghe} đã được người khác đặt."

            ma_ve = uuid4().hex[:5].upper()
            ve = Ve(
                ma_ve=ma_ve,
                ngay_dat=datetime.now().date(),
                ma_lich_chieu=lich_chieu.ma_lich_chieu,
                ma_ghe=ghe_obj.ma_ghe,
                email=email
            )
            session.add(ve)
            ve_da_dat.append(ma_ve)

        session.commit()
        return ve_da_dat
    except Exception as e:
        session.rollback()
        return f"Lỗi: {str(e)}"
    finally:
        session.close()
