from typing import List, Type
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from datetime import datetime, time
from app.core.models import Phim, LichChieu, Ve, Ghe, TrangThaiGhe
from app.core.database import get_session
from langchain.tools import BaseTool

# --- Schema input ---
class GheTrongInput(BaseModel):
    ten_phim: str = Field(..., description="Tên bộ phim cần kiểm tra")
    ngay: str = Field(..., description="Ngày chiếu (format: DD/MM/YYYY)")  # changed from date to str
    gio: time = Field(..., description="Giờ chiếu (format: HH:MM:SS)")

# --- Tool ---
class GheTrongTool(BaseTool):
    name: str = "kiem_tra_ghe_trong"
    description: str = """Sử dụng Khi người dùng muốn Đặt Vé phim cụ thể.
                        Ví dụ: "Phim Mai suất 7 giờ tối nay còn ghế không?" -> kiem_tra_ghe_trong(ten_phim='Mai', ngay_chieu='21/7/2025', gio_chieu='19:00')
                        Ví dụ: tôi muốn đặt vé Phim Mai suất 7 giờ tối nay => Dùng kiem_tra_ghe_trong(ten_phim='Mai', ngay_chieu='21/7/2025', gio_chieu='19:00') -> đưa ra ghế còn trống của suất phim đó -> gui_otp() -> xac_thuc_va_hoan_tat_dat_ve()"""
    args_schema: Type[BaseModel] = GheTrongInput

    def _run(self, ten_phim: str, ngay: str, gio: time) -> List[str]:
        session: Session = get_session()
        try:
            # Ép kiểu ngày từ chuỗi sang datetime.date
            try:
                ngay_date = datetime.strptime(datetime.strptime(ngay, "%d/%m/%Y").strftime("%Y-%m-%d"), "%Y-%m-%d").date()
            except ValueError:
                return [f"Định dạng ngày không hợp lệ. Hãy nhập theo định dạng DD-MM-YYYY (VD: 05-08-2025)"]

            # 1. Tìm suất chiếu
            suat = (
                session.query(LichChieu)
                .join(Phim, LichChieu.ma_phim == Phim.ma_phim)
                .filter(
                    Phim.ten_phim == ten_phim,
                    LichChieu.ngay == ngay_date,
                    LichChieu.gio == gio
                )
                .first()
            )

            if not suat:
                return [f"Không tìm thấy suất chiếu cho phim '{ten_phim}' vào lúc {gio.strftime('%H:%M')} ngày {ngay}"]

            # 2. Lấy tất cả ghế trong phòng chiếu đó
            ghe_trong_phong = (
                session.query(Ghe)
                .join(TrangThaiGhe, TrangThaiGhe.ma_ghe == Ghe.ma_ghe)
                .filter(TrangThaiGhe.ma_phong == suat.ma_phong)
                .all()
            )

            # 3. Lấy danh sách ghế đã đặt trong suất chiếu đó
            ghe_da_dat = (
                session.query(Ve.ma_ghe)
                .filter(Ve.ma_lich_chieu == suat.ma_lich_chieu)
                .all()
            )
            ds_ghe_da_dat = {g[0] for g in ghe_da_dat}

            # 4. Lọc ghế còn trống
            ghe_con_trong = [ghe.ten_ghe for ghe in ghe_trong_phong if ghe.ma_ghe not in ds_ghe_da_dat]

            if not ghe_con_trong:
                return [f"Tất cả ghế của suất chiếu phim '{ten_phim}' vào {gio.strftime('%H:%M')} ngày {ngay} đã được đặt."]
            
            return [
                f"Các ghế còn trống của phim '{ten_phim}' vào {gio.strftime('%H:%M')} ngày {ngay}:"
            ] + ghe_con_trong
        finally:
            session.close()
