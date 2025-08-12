"""
Get Current Time Tool for AI Agent
"""
import json
from datetime import datetime
from typing import Type

from langchain.tools import BaseTool
from pydantic import BaseModel, Field


class GetCurrentTimeInput(BaseModel):
    """Input for get current time tool"""
    timezone: str = Field(default="UTC", description="Múi giờ để lấy thời gian hiện tại (mặc định: UTC)")


class GetCurrentTimeTool(BaseTool):
    """Tool to get current date and time"""
    name: str = "get_current_time"
    description: str = """**Sử dụng khi người dùng có nhắc về ngày hôm nay, hiện tại, ... sau đó sử dụng các tool khác.**
                        Ví dụ:Ví dụ: "lịch chiếu phim ngày mai" -> dùng get_current_time() xác định hôm nay -> xác định ngày mai """
    args_schema: Type[BaseModel] = GetCurrentTimeInput

    def _run(self, timezone: str = "UTC") -> str:
        """Execute the tool"""
        try:
            current_time = datetime.now()

            # Format time info
            time_info = {
                "current_datetime": current_time.isoformat(),
                "formatted_time": current_time.strftime("%Y-%m-%d %H:%M:%S"),
                "day_of_week": current_time.strftime("%A"),
                "date": current_time.strftime("%Y-%m-%d"),
                "time": current_time.strftime("%H:%M:%S"),
                "timezone": timezone,
                "timestamp": current_time.timestamp()
            }

            return json.dumps(time_info, indent=2)

        except Exception as e:
            return f"Error getting current time: {str(e)}"