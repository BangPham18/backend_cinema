from datetime import date
from sqlalchemy.orm import Session
from app.core.models import LichChieu, Phim
from sqlalchemy import func, desc
from pydantic import BaseModel, Field
from langchain.tools import BaseTool
from typing import List
from app.core.database import get_session

# 3. TOOL LẤY PHIM HOT
# ==============================================================================

class PhimHotInput(BaseModel):
    """Input cho công cụ lấy phim hot. Không yêu cầu tham số."""
    pass

class GetPhimHotTool(BaseTool):
    """Công cụ lấy danh sách các phim nổi bật có nhiều suất chiếu nhất tính từ hôm nay."""
    name: str = "get_phim_hot"
    description: str = (
        "Sử dụng công cụ này khi người dùng hỏi về 'phim hot', 'phim nổi bật', 'phim được xem nhiều'."
    )
    args_schema: type[BaseModel] = PhimHotInput

    def _run(self) -> List[str]:
        today = date.today()
        session: Session = get_session() # Hàm này để lấy session kết nối DB
        try:
            results = (
                session.query(
                    Phim.ten_phim, 
                    func.count(LichChieu.ma_lich_chieu).label("so_suat")
                )
                .join(LichChieu, LichChieu.ma_phim == Phim.ma_phim)
                # THAY ĐỔI: Lọc các lịch chiếu từ hôm nay trở về sau
                .filter(LichChieu.ngay >= today) 
                .group_by(Phim.ten_phim)
                .order_by(desc("so_suat")) # Sắp xếp theo số suất chiếu giảm dần
                .limit(5)
                .all()
            )
            
            if not results:
                return ["Hiện tại chưa có lịch chiếu cho phim nào sắp tới."]
            
            # Format output cho dễ đọc
            return [f"{ten_phim}" for ten_phim in results]
        
        finally:
            session.close()
