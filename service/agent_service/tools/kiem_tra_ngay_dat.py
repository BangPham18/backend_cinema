from sqlalchemy.orm import Session
from app.core.models import LichChieu
from app.core.database import get_session
from pydantic import BaseModel, Field
from langchain.tools import BaseTool
from typing import Type
from datetime import datetime


# Schema input
class KiemTraNgayDatInput(BaseModel):
    """Input cho công cụ kiểm tra ngày đặt vé"""
    ngay_dat: str = Field(..., description="Ngày người dùng muốn đặt vé (định dạng: DD/MM/YYYY)")


# Tool kiểm tra ngày đặt
class KiemTraNgayDatTool(BaseTool):
    """Công cụ kiểm tra tính hợp lệ của ngày đặt vé."""
    name: str = "kiem_tra_ngay_dat"
    description: str = (
        """Kiểm tra xem ngày người dùng muốn đặt vé có hợp lệ không: "
        1) không phải là ngày quá khứ, 
        2) có nằm trong danh sách lịch chiếu.
        Ví dụ: "tôi muốn đặt vé ngày 1/8/2025 -> kiem_tra_ngay_dat() -> Bạn không thể đặt vé trong quá khứ"""
    )
    args_schema: Type[BaseModel] = KiemTraNgayDatInput

    def _run(self, ngay_dat: str) -> str:
        try:
            # Chuyển định dạng DD-MM-YYYY -> datetime.date
            user_date = datetime.strptime(datetime.strptime(ngay_dat, "%d/%m/%Y").strftime("%Y-%m-%d"), "%Y-%m-%d").date()
            today = datetime.today().date()

            # 1. Kiểm tra ngày quá khứ
            if user_date < today:
                print('hehe')
                return "Bạn không thể đặt vé cho ngày trong quá khứ."

            # 2. Kiểm tra ngày có lịch chiếu không
            session: Session = get_session()
            try:
                exists = session.query(LichChieu).filter(LichChieu.ngay == user_date).first()
                if not exists:
                    return f"Hiện tại không có lịch chiếu nào vào ngày {ngay_dat}."
                return f"Ngày {ngay_dat} hợp lệ. Bạn có thể tiếp tục đặt vé."
            finally:
                session.close()

        except ValueError:
            return "Định dạng ngày không hợp lệ. Vui lòng nhập theo dạng DD-MM-YYYY."
        except Exception as e:
            return f"Lỗi khi kiểm tra ngày đặt: {str(e)}"
