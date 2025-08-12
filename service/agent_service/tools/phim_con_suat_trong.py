from sqlalchemy.orm import Session
from app.core.models import Phim, TrangThaiGhe, LichChieu, Ghe, Ve
from pydantic import BaseModel, Field
from langchain.tools import BaseTool
from typing import Type
from app.core.database import get_session
from typing import List, Type
from sqlalchemy import func, cast, DateTime
from datetime import datetime, timedelta

# 4. TOOL KIỂM TRA GHẾ TRỐNG CỦA MỘT SUẤT CHIẾU
# ==============================================================================
class PhimConSuatTrongInput(BaseModel):
    """Input cho công cụ liệt kê các suất còn trống của một hoặc nhiều phim."""
    danh_sach_ten_phim: List[str] = Field(
        description="Danh sách tên các bộ phim cần kiểm tra."
    )

# --- Tool đã được sửa đổi ---


class PhimConSuatTrongTool(BaseTool):
    """Liệt kê TẤT CẢ các suất chiếu (ngày, giờ) CÒN GHẾ TRỐNG của một hoặc nhiều bộ phim trong 7 ngày tới."""
    name: str = "phim_con_suat_trong"
    description: str = (
        """**Sử dụng khi người dùng hỏi lịch chiếu, suất chiếu một phim Không nói rõ ngày giờ?**
        Ví dụ: "lịch chiếu phim Mai" -> phim_con_suat_trong(ten_phim='Mai')
        Ví dụ: "phim Mai còn suất trống không" -> phim_con_suat_trong(ten_phim='Mai')"""
    )
    args_schema: Type[BaseModel] = PhimConSuatTrongInput

    def _run(self, danh_sach_ten_phim: List[str]) -> List[str]:
        session: Session = get_session()
        ket_qua_tong_hop = []
        now = datetime.now()
        seven_days_later = now + timedelta(days=7)

        try:
            for ten_phim in danh_sach_ten_phim:
                # Tìm tất cả suất chiếu trong 7 ngày tới của phim hiện tại
                cac_suat = (
                    session.query(LichChieu)
                    .join(Phim)
                    .filter(
                        Phim.ten_phim == ten_phim,
                        # --- SỬA LỖI Ở ĐÂY ---
                        # Kết hợp ngày và giờ thành một giá trị DATETIME để so sánh
                        cast(func.concat(LichChieu.ngay, ' ', LichChieu.gio), DateTime) >= now,
                        cast(func.concat(LichChieu.ngay, ' ', LichChieu.gio), DateTime) <= seven_days_later
                        # -----------------------
                    )
                    .all()
                )

                if not cac_suat:
                    ket_qua_tong_hop.append(f"Không tìm thấy suất chiếu nào trong 7 ngày tới cho phim '{ten_phim}'.")
                    continue

                ket_qua_phim_hien_tai = []

                for suat in cac_suat:
                    # Truy vấn này có thể được tối ưu hóa, nhưng vẫn đúng về mặt logic
                    tong_ghe = (
                        session.query(func.count(Ghe.ma_ghe))
                        .join(TrangThaiGhe, Ghe.ma_ghe == TrangThaiGhe.ma_ghe)
                        .filter(TrangThaiGhe.ma_phong == suat.ma_phong)
                        .scalar()
                    )

                    ghe_da_dat = (
                        session.query(func.count(Ve.ma_ve))
                        .filter(Ve.ma_lich_chieu == suat.ma_lich_chieu)
                        .scalar()
                    )

                    so_ghe_trong = tong_ghe - (ghe_da_dat or 0)

                    if so_ghe_trong > 0:
                        ket_qua_phim_hien_tai.append(
                            f"- Ngày {suat.ngay.strftime('%d/%m/%Y')} lúc {suat.gio.strftime('%H:%M')} còn {so_ghe_trong} ghế"
                        )

                if not ket_qua_phim_hien_tai:
                    ket_qua_tong_hop.append(f"Tất cả suất chiếu của phim '{ten_phim}' trong 7 ngày tới đều đã hết ghế.")
                else:
                    ket_qua_tong_hop.append(f"Các suất chiếu còn trống của phim '{ten_phim}' trong 7 ngày tới:")
                    ket_qua_tong_hop.extend(ket_qua_phim_hien_tai)

            if not ket_qua_tong_hop:
                return ["Không tìm thấy thông tin cho bất kỳ phim nào được yêu cầu."]
            return ket_qua_tong_hop

        finally:
            session.close()