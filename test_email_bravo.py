import asyncio
import os
from dotenv import load_dotenv
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pydantic import EmailStr, BaseModel
from typing import List

# Load environment variables from .env file
load_dotenv()

async def test_send_email():
    print("--- Bắt đầu kiểm tra cấu hình Email (Bravo/Brevo/Gmail) ---")
    
    # 1. Get configuration
    mail_username = os.getenv("MAIL_USERNAME")
    mail_password = os.getenv("MAIL_PASSWORD")
    mail_from = os.getenv("MAIL_FROM")
    # Default to 587 if not set
    mail_port = int(os.getenv("MAIL_PORT", 587))
    mail_server = os.getenv("MAIL_SERVER")
    
    # 2. Print config (debug info)
    print(f"Server:   {mail_server}")
    print(f"Port:     {mail_port}")
    print(f"Username: {mail_username}")
    print(f"From:     {mail_from}")
    
    if mail_password:
        masked_password = mail_password[:2] + '*' * (len(mail_password) - 4) + mail_password[-2:] if len(mail_password) > 4 else "****"
        print(f"Password: {masked_password}")
    else:
        print("Password: [NOT SET] ❌")

    # 3. Determine Security Settings
    # Port 587 -> STARTTLS
    # Port 465 -> SSL/TLS
    default_starttls = str(mail_port == 587)
    default_ssl_tls = str(mail_port == 465)

    mail_starttls = os.getenv("MAIL_STARTTLS", default_starttls).lower() == "true"
    mail_ssl_tls = os.getenv("MAIL_SSL_TLS", default_ssl_tls).lower() == "true"

    print(f"STARTTLS: {mail_starttls}")
    print(f"SSL/TLS:  {mail_ssl_tls}")

    # 4. Configure FastMail
    try:
        conf = ConnectionConfig(
            MAIL_USERNAME=mail_username,
            MAIL_PASSWORD=mail_password,
            MAIL_FROM=mail_from,
            MAIL_PORT=mail_port,
            MAIL_SERVER=mail_server,
            MAIL_STARTTLS=mail_starttls,
            MAIL_SSL_TLS=mail_ssl_tls,
            USE_CREDENTIALS=True,
            VALIDATE_CERTS=True
        )
    except Exception as e:
        print(f"\n❌ Lỗi cấu hình: {e}")
        return

    # 5. Prepare Message
    if not mail_from or "@" not in mail_from:
        print("\n❌ Lỗi: MAIL_FROM không hợp lệ. Hãy kiểm tra file .env")
        return

    # Send to self for testing
    recipient = mail_from 
    
    message = MessageSchema(
        subject="[Test] Kiểm tra gửi OTP (Bravo/Brevo)",
        recipients=[recipient],
        body=f"""
        <h3>Kiểm tra gửi Email thành công!</h3>
        <p>Nếu bạn nhận được email này, cấu hình SMTP của bạn đã hoạt động chính xác.</p>
        <ul>
            <li>Server: {mail_server}</li>
            <li>Port: {mail_port}</li>
        </ul>
        """,
        subtype=MessageType.html
    )

    print(f"\nĐang thử gửi email đến: {recipient} ...")
    
    # 6. Send Email
    try:
        fm = FastMail(conf)
        await fm.send_message(message)
        print("\n✅ Gửi email THÀNH CÔNG!")
        print(f"Hãy kiểm tra hộp thư đến của {recipient}.")
    except Exception as e:
        print(f"\n❌ Gửi email THẤT BẠI.")
        print(f"Lỗi chi tiết: {e}")
        print("\n--- HƯỚNG DẪN KHẮC PHỤC ---")
        if "Authentication failed" in str(e):
            print("1. Sai Username hoặc Password.")
            print("   - Nếu dùng Gmail: Phải dùng 'App Password' (Mật khẩu ứng dụng), KHÔNG dùng mật khẩu đăng nhập Google.")
            print("   - Nếu dùng Brevo: Username là email đăng nhập, Password là SMTP Key (lấy trong Dashboard -> SMTP & API).")
        elif "Timeout" in str(e):
            print("1. Sai Port hoặc bị chặn mạng.")
            print("   - Thử đổi MAIL_PORT thành 587 (thường ổn định hơn 465).")
            print("   - Kiểm tra firewall.")
        elif "ConnectionErrors" in str(e):
            print("1. Không kết nối được đến server.")
            print("   - Kiểm tra lại MAIL_SERVER (ví dụ: smtp.gmail.com hoặc smtp-relay.brevo.com).")

if __name__ == "__main__":
    asyncio.run(test_send_email())
