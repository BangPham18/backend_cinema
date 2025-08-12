from datetime import datetime, date
from typing import Optional
from sqlalchemy.orm import Session
from app.core.models import LichChieu, Phim, PhongPhim
from pydantic import BaseModel, Field
from langchain.tools import BaseTool
from typing import List, Type, Optional
from app.core.database import get_session

# 1. TOOL TRA CỨU LỊCH CHIẾU
# ==============================================================================

class LichChieuInput(BaseModel):
    """Input cho công cụ tra cứu lịch chiếu."""
    ngay: str = Field(description="Ngày cần tra cứu lịch chiếu theo định dạng DD/MM/YYYY.")
    ten_phim: Optional[str] = Field(default=None, description="Tên phim cụ thể để lọc kết quả.")
    ma_phong: Optional[str] = Field(default=None, description="Mã phòng chiếu cụ thể để lọc kết quả.")

class TraCuuLichChieuTool(BaseTool):
    """Công cụ để tra cứu lịch chiếu phim trong một ngày cụ thể."""
    name: str = "tra_cuu_lich_chieu"
    description: str = (
        """**Sử dụng công cụ này khi người dùng muốn biết 'lịch chiếu', 'suất chiếu', hoặc 'chiếu lúc mấy giờ'.** BẮT BUỘC phải có tham số 'ngay'.
        Ví dụ: "Lịch chiếu phim Mai hôm nay" -> get_lich_chieu(ngay='22/7/2025', ten_phim='Mai')
        Ví dụ: "Lịch chiếu phim ngày 29/7/2025" -> get_lich_chieu(ngay='29/7/2025')
        """
    )   
    args_schema: Type[BaseModel] = LichChieuInput

    def _run(self, ngay: str, ten_phim: Optional[str] = None, ma_phong: Optional[str] = None) -> List[dict]:
        try:
            ngay_dt = datetime.strptime(datetime.strptime(ngay, "%d/%m/%Y").strftime("%Y-%m-%d"), "%Y-%m-%d").date()
        except ValueError:
            return [f"Định dạng ngày không hợp lệ. Vui lòng dùng DD/MM/YYYY."]

        session: Session = get_session()
        try:
            query = session.query(LichChieu).join(Phim).join(PhongPhim)
            query = query.filter(LichChieu.ngay == ngay_dt)

            if ten_phim:
                query = query.filter(Phim.ten_phim.ilike(f"%{ten_phim}%"))
            if ma_phong:
                query = query.filter(PhongPhim.ma_phong == ma_phong)

            results = query.all()
            if not results:
                return ["Không tìm thấy lịch chiếu phù hợp với điều kiện."]

            return [
                {
                    "ngay": lc.ngay.isoformat(),
                    "gio": lc.gio.strftime("%H:%M"),
                    "ten_phim": lc.phim.ten_phim,
                    "ten_phong": lc.phong_phim.ten_phong,
                }
                for lc in results
            ]
        finally:
            session.close()