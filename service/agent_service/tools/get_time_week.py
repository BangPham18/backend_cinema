from datetime import datetime, timedelta
from typing import Type
from langchain.tools import BaseTool
from pydantic import BaseModel, Field


class GetFutureDateFromWeekdayInput(BaseModel):
    """Input cho tool tính ngày từ thứ và số tuần"""
    weekday_name: str = Field(..., description="Tên thứ (e.g. Monday, Thursday)")
    week_offset: int = Field(default=0, description="Số tuần hiện tại (0 = tuần này, 1 = tuần sau, v.v.)")


class GetFutureDateFromWeekdayTool(BaseTool):
    """Tool tính ngày tương ứng với thứ trong tuần và khoảng cách tuần"""
    name: str = "get_date_from_weekday_with_offset"
    description: str = """***Sử dụng Khi người dùng có nhắc về ngày, thứ, tuần (người dùng có thể viết tắt như: T7 (thứ bảy), CN (chú nhật), T2(thứ hai), tuần sau, tuần mốt, ngày mai, ngày mốt.... sau đó sử dụng các tool khác.***
                        Ví dụ: "lịch chiếu phim CN tuần này" -> get_date_from_weekday_with_offset("Sunday",0) là 3/8/2025-> get_lich_chieu(ngay='3/8/2025')"""
    args_schema: Type[BaseModel] = GetFutureDateFromWeekdayInput

    def _run(self, weekday_name: str, week_offset: int = 0) -> str:
        try:
            today = datetime.now()
            weekdays = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
            weekday_name_lower = weekday_name.strip().lower()

            if weekday_name_lower not in weekdays:
                return f"Invalid weekday name: {weekday_name}"

            target_weekday = weekdays.index(weekday_name_lower)

            # Lấy ngày thứ Hai của tuần hiện tại
            start_of_week = today - timedelta(days=today.weekday())

            # Tính ngày tương ứng trong tuần offset
            target_date = start_of_week + timedelta(weeks=week_offset, days=target_weekday)

            return f"{weekday_name.capitalize()} tuần {'này' if week_offset == 0 else f'sau {week_offset} tuần' if week_offset > 1 else 'sau'} là ngày {target_date.strftime('%d/%m/%Y')}"

        except Exception as e:
            return f"Error: {str(e)}"
