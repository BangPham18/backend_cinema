import random
import traceback
from pydantic import BaseModel, EmailStr, Field
from typing import Type
from langchain.tools import BaseTool
from scripts.redis_client import set_otp  
import asyncio
from dotenv import load_dotenv
import os
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException

load_dotenv()

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

                # Cấu hình Brevo API
                configuration = sib_api_v3_sdk.Configuration()
                api_key = os.getenv("BREVO_API_KEY")
                if not api_key:
                    return "Lỗi: Chưa cấu hình BREVO_API_KEY"
                
                configuration.api_key['api-key'] = api_key
                api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
                
                sender_email = os.getenv("MAIL_FROM", "no-reply@example.com")
                sender_name = "Cinema Chatbot"
                
                subject = "Mã OTP xác nhận đặt vé 🎟️"
                html_content = f"""
                <html>
                    <body>
                        <h3>Mã OTP của bạn là: <strong style="font-size: 24px; color: #4CAF50;">{otp}</strong></h3>
                        <p>Vui lòng cung cấp mã này để xác nhận đặt vé.</p>
                        <p>Mã có hiệu lực trong 5 phút.</p>
                    </body>
                </html>
                """
                
                sender = {"name": sender_name, "email": sender_email}
                to = [{"email": email}]
                
                send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
                    to=to,
                    sender=sender,
                    subject=subject,
                    html_content=html_content
                )

                try:
                    api_response = api_instance.send_transac_email(send_smtp_email)
                    print(f"Brevo Response: {api_response}")
                    return "Đã gửi mã OTP đến email của bạn. Vui lòng xác nhận."
                except ApiException as e:
                    print(f"Exception when calling TransactionalEmailsApi->send_transac_email: {e}")
                    return f"Lỗi gửi OTP qua API: {e}"

        except Exception as e:
            traceback.print_exc()
            print(f"❌ DEBUG ERROR: {str(e)}")
            return f"Lỗi gửi OTP: {str(e)}"
