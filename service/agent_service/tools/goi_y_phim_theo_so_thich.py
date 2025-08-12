from sqlalchemy.orm import Session
from app.core.models import Phim, LichChieu
from sqlalchemy import or_, and_
from app.core.database import get_session
from pydantic import BaseModel, Field
from langchain.tools import BaseTool
from typing import List, Type
from datetime import date

# 2. TOOL GỢI Ý PHIM THEO SỞ THÍCH
# ==============================================================================

class GoiYPhimInput(BaseModel):
    """Input cho công cụ gợi ý phim."""
    so_thich: str = Field(description="Từ khóa mô tả sở thích, thể loại, hoặc đối tượng xem phim (ví dụ: 'phim ma', 'phim cho người yêu', 'phim hài hước').")

class GoiYPhimTool(BaseTool):
    """Công cụ gợi ý phim dựa trên sở thích do người dùng cung cấp."""
    name: str = "goi_y_phim_theo_so_thich"
    description: str = (
        """Sử dụng công cụ này khi người dùng không biết xem phim gì và cần một vài gợi ý.
        Ví dụ: "tôi muốn xem phim hành động" -> sử dụng goi_y_phim_theo_so_thich("hành động") -> hiện tại chúng tôi có những phim hành động sau,...."""
    )
    args_schema: Type[BaseModel] = GoiYPhimInput

    def _run(self, so_thich: str) -> List[str]:
        mapping = {
            "người yêu": ["tình cảm", "lãng mạn"],
            "ma": ["kinh dị"],
            "trẻ con": ["hoạt hình", "gia đình", "thiếu nhi"],
            "hài": ["hài"],
            "hành động": ["hành động"],
            "viễn tưởng": ["khoa học viễn tưởng"],
        }
        matched_tags = []
        for keyword, tags in mapping.items():
            if keyword in so_thich.lower():
                matched_tags.extend(tags)

        if not matched_tags:
            return ["Không rõ sở thích bạn đề cập đến là gì. Vui lòng nói rõ hơn."]

        session: Session = get_session()
        try:
            current_date = date.today()
            
            # Lấy danh sách ma_phim đang chiếu (ngày chiếu >= hiện tại)
            ma_phim_dang_chieu = session.query(LichChieu.ma_phim).filter(LichChieu.ngay >= current_date).distinct().all()
            ma_phim_dang_chieu = [ma_phim[0] for ma_phim in ma_phim_dang_chieu]
            
            if not ma_phim_dang_chieu:
                return ["Hiện tại không có phim nào đang được chiếu."]

            # Lọc phim theo thể loại và chỉ lấy những phim đang chiếu
            results = (
                session.query(Phim)
                .filter(
                    and_(
                        or_(*[Phim.the_loai.ilike(f"%{tag}%") for tag in matched_tags]),
                        Phim.ma_phim.in_(ma_phim_dang_chieu)
                    )
                )
                .all()
            )
            
            if not results:
                return [f"Không tìm thấy phim phù hợp với sở thích '{so_thich}' đang chiếu."]
            
            return [phim.ten_phim for phim in results]
        finally:
            session.close()