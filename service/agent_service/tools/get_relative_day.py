"""
Get Relative Date Tool (ngày dạng DD/MM/YYYY)
"""
import json
from datetime import datetime, timedelta
from typing import Type

from langchain.tools import BaseTool
from pydantic import BaseModel, Field


class GetRelativeDateInput(BaseModel):
    """Input cho tool lấy ngày tương đối"""
    relative_day: str = Field(
        description="Một trong các giá trị: 'hôm qua', 'hôm kia', 'ngày mai', 'ngày kia'"
    )


class GetRelativeDateTool(BaseTool):
    """Tool để xác định ngày tương đối: hôm qua, hôm kia, ngày mai, ngày kia"""
    name: str = "get_relative_date"
    description:str = """Sử dụng khi người dùng nhắc đến các ngày như 'hôm qua', 'hôm kia', 'ngày mai', 'ngày kia'"""

    args_schema: Type[BaseModel] = GetRelativeDateInput

    def _run(self, relative_day: str) -> str:
        try:
            today = datetime.today().date()
            relative_day = relative_day.strip().lower()

            mapping = {
                "hôm qua": -1,
                "hôm kia": -2,
                "ngày mai": 1,
                "ngày kia": 2
            }

            if relative_day not in mapping:
                return f"Lỗi: '{relative_day}' không hợp lệ. Vui lòng dùng 'hôm qua', 'hôm kia', 'ngày mai', 'ngày kia'."

            offset = mapping[relative_day]
            result_date = today + timedelta(days=offset)

            return json.dumps({
                "relative_day": relative_day,
                "date": result_date.strftime("%d/%m/%Y")
            }, ensure_ascii=False, indent=2)

        except Exception as e:
            return f"Lỗi khi xử lý ngày: {str(e)}"
