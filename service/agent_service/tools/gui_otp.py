import random
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pydantic import BaseModel, EmailStr, Field
from typing import Type
from langchain.tools import BaseTool
from scripts.redis_client import set_otp  
import asyncio
from dotenv import load_dotenv
import os

load_dotenv()
conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
    MAIL_FROM=os.getenv("MAIL_FROM"),
    MAIL_PORT=int(os.getenv("MAIL_PORT")),
    MAIL_SERVER=os.getenv("MAIL_SERVER"),
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True
)

class GuiOTPInput(BaseModel):
    email: EmailStr = Field(description="Email khách hàng để gửi mã OTP")
    state: str = Field(description='Trạng thái đăng nhập của khách hàng')
class ToolGuiOTP(BaseTool):
    name:str = "gui_otp"
    description:str = """Khi khách hàng xác nhận đặt vé. Gửi mã OTP đến email khách hàng để xác nhận đặt vé.
    ví dụ: `AI`: Bạn muốn đặt 5 vé ghế D1, D2, D3, D4, D5 phim Hitman suất 10h sáng ngày 07/08/2025 đúng không ạ? Bạn có muốn xác nhận đặt vé không?
            `người dùng`: có
            **Sử dụng tool gui_otp()"""
    args_schema: Type[BaseModel] = GuiOTPInput

    def _run(self,**kwargs) -> str:
        """Thực thi đồng bộ (bắt buộc phải có)."""
        # Sử dụng asyncio để chạy phiên bản async từ trong hàm sync
        return asyncio.run(self._arun(**kwargs))
    
    async def _arun(self, email: str, state: str) -> str:
        try:
            print(state)
            if state == 'chưa đăng nhập':
                return "chưa đăng nhập"
            else:
                print("đã gửi otp")
                otp = str(random.randint(1000, 9999))
                set_otp(email, otp, expire_seconds=300)  # Lưu vào Redis 5 phút

                message = MessageSchema(
                    subject="Mã OTP xác nhận đặt vé 🎟️",
                    recipients=[email],
                    body=f"Mã OTP của bạn là: {otp}. Vui lòng cung cấp mã này để xác nhận đặt vé.",
                    subtype="plain"
                )
                fm = FastMail(conf)
                await fm.send_message(message)
                return "Đã gửi mã OTP đến email của bạn. Vui lòng xác nhận."
        except Exception as e:
            return f"Lỗi gửi OTP: {str(e)}"
