from sqlalchemy.orm import Session
from app.core.models import Phim
from pydantic import BaseModel, Field
from langchain.tools import BaseTool
from typing import Type
from app.core.database import get_session
import unicodedata
import re
from sqlalchemy import func, desc
from .get_phim_hot import GetPhimHotTool

def normalize_string(s: str) -> str:
    if not s:
        return ""
    s = s.lower()
    s = ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')
    s = re.sub(r'[^a-z0-9\s]', '', s)
    s = re.sub(r'\s+', ' ', s).strip()
    return s

class KiemTraPhimInput(BaseModel):
    """Input cho công cụ kiểm tra phim."""
    ten_phim: str = Field(description="Tên phim mà người dùng cung cấp để kiểm tra.")

class KiemTraPhimTonTaiTool(BaseTool):
    """
    Công cụ kiểm tra xem một phim có trong hệ thống không dựa trên so khớp tên và trả về tên chính xác của phim.
    Nếu không tìm thấy, công cụ sẽ tự động gợi ý các phim đang hot.
    """
    name: str = "kiem_tra_phim_ton_tai"
    description: str = (
        """**Sử dụng khi người dùng có nhắc về tên phim sau đó sử dụng các tool khác.**
        Ví dụ: "đặt vé phim connan" -> kiem_tra_phim_ton_tai(ten_phim='connan') -> phim connan: thám tử lừng danh có tồn tại -> Làm theo QUY TRÌNH ĐẶT VÉ
        Ví dụ: "lịch chiếu phim connan" -> kiem_tra_phim_ton_tai(ten_phim='connan') -> phim connan: thám tử lừng danh có tồn tại -> phim_con_suat_trong(ten_phim='connan: thám tử lừng danh')
        Ví dụ: "tôi muốn xem phim superman" -> kiem_tra_phim_ton_tai(ten_phim='superman') -> hiện tại rạp có chiếu phim superman 1, superman 2, bạn muốn xem phim nào"""
    )
    args_schema: Type[BaseModel] = KiemTraPhimInput

    def _run(self, ten_phim: str) -> str:
        SIMILARITY_THRESHOLD = 0.15 # Ngưỡng tương đồng để coi là khớp
        session: Session = get_session()

        try:
            # Chuẩn hóa chuỗi input để tìm kiếm tốt hơn (bỏ dấu, viết thường,...)
            normalized_input = normalize_string(ten_phim)

            # --- Logic truy vấn thực tế với PostgreSQL ---
            # Hàm unaccent để bỏ dấu tiếng Việt, similarity để đo độ tương đồng
            similarity_score = func.similarity(func.unaccent(Phim.ten_phim), normalized_input)
            result = (
                session.query(Phim)
                .filter(similarity_score > SIMILARITY_THRESHOLD)
                .order_by(desc(similarity_score))
                .all() # Lấy kết quả khớp nhất
            )
            if result:
                # Nếu tìm thấy phim, trả về thông báo xác nhận
                return f"Phim '{', '.join([phim.ten_phim for phim in result])}' có trong hệ thống. Bạn muốn biết lịch chiếu phim này chứ?"
            else:
                # Nếu không tìm thấy, gọi tool get_phim_hot
                print(f"Không tìm thấy phim '{ten_phim}'. Đang tìm phim hot để gợi ý...")
                hot_movies_tool = GetPhimHotTool()
                hot_movies_list = hot_movies_tool._run() # Chạy tool để lấy danh sách phim hot

                # Chuyển danh sách thành chuỗi để hiển thị
                hot_movies_str = ", ".join(hot_movies_list)

                return (
                    f"Hiện tại chúng tôi không chiếu phim '{ten_phim}'. "
                    f"Có thể bạn sẽ thích các phim đang hot sau đây: {hot_movies_str}."
                )
        finally:
            session.close()