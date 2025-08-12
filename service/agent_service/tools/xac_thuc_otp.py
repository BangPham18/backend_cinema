import asyncio
from pydantic import BaseModel, EmailStr, Field
from langchain.tools import BaseTool
from typing import List, Type
from scripts.redis_client import get_otp, delete_otp
from service.agent_service.tools.function_for_tool.dat_ve import dat_ve
from service.agent_service.tools.function_for_tool.gui_ve import gui_lai_ve
import threading # 1. Import thư viện threading

# --- Input Schema ---
class XacThucVaGoiApiInput(BaseModel):
    email: EmailStr = Field(description="Email của khách hàng.")
    otp: str = Field(description="Mã OTP gồm 4-6 chữ số mà khách hàng cung cấp.")
    ten_phim: str = Field(description="Tên bộ phim muốn đặt.")
    ngay: str = Field(description="Ngày xem phim, định dạng DD/MM/YYYY.")
    gio: str = Field(description="Giờ xem phim, định dạng HH:MM.")
    ghe: List[str] = Field(description="Danh sách các ghế muốn đặt, ví dụ: ['A1', 'A2'].")

# --- Tool ---
class ToolXacThucVaDatVe(BaseTool):
    """Sử dụng công cụ này để hoàn tất quy trình đặt vé sau khi đã có đủ thông tin và mã OTP từ người dùng."""
    name: str = "xac_thuc_va_hoan_tat_dat_ve"
    description: str = (
        "Xác thực mã OTP và hoàn tất việc đặt vé. Gửi vé qua email nếu thành công."
    )
    args_schema: Type[BaseModel] = XacThucVaGoiApiInput

    def _run(self, **kwargs) -> str:
        """Lớp vỏ đồng bộ để gọi async _arun."""
        return asyncio.run(self._arun(**kwargs))

    # 2. Tạo một hàm đồng bộ để chạy trong thread
    def _send_email_background(self, email: str, ma_ves: List[str]):
        """Hàm này sẽ chạy trong một luồng nền riêng biệt."""
        print(f"📧 Bắt đầu gửi email tới {email} trong nền...")
        try:
            # Vì gui_lai_ve là hàm đồng bộ, ta có thể gọi trực tiếp
            gui_lai_ve(email, ma_ves)
        except Exception as e:
            print(f"❌ Lỗi khi gửi email trong nền: {e}")


    async def _arun(
        self,
        email: EmailStr,
        otp: str,
        ten_phim: str,
        ngay: str,
        gio: str,
        ghe: List[str]
    ) -> str:
        print(f"Xác thực OTP cho {email}...")
        saved_otp = get_otp(email)
        if saved_otp is None or saved_otp != otp:
            return "❌ Mã OTP không chính xác hoặc đã hết hạn."

        delete_otp(email)

        print("Đang tiến hành đặt vé...")
        ket_qua = dat_ve(email, ten_phim, ngay, gio, ghe)
        print(f"Kết quả đặt vé: {ket_qua}")

        if isinstance(ket_qua, list) and ket_qua:
            # 3. Tạo và khởi chạy thread mới
            email_thread = threading.Thread(
                target=self._send_email_background,
                args=(email, ket_qua)
            )
            email_thread.start() # Bắt đầu chạy nền ngay lập tức

            # Return ngay lập tức mà không cần chờ email gửi xong
            return f"✅ Đặt vé thành công. Vé đang được gửi đến email của bạn."
        else:
            return f"❌ Đặt vé thất bại: {ket_qua}"