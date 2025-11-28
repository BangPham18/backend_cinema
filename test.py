# python
import asyncio
from service.agent_service.tools.gui_otp import ToolGuiOTP
tool = ToolGuiOTP()
# gọi tool để gửi OTP thử (sẽ raise exception nếu cấu hình sai)
print(asyncio.run(tool._arun(email="phambang@yopmail.com", state="đã đăng nhập")))