import os
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from app.core.config import settings

def send_email_html(to: str, subject: str, body: str):
    # Cấu hình Brevo API
    configuration = sib_api_v3_sdk.Configuration()
    # Ưu tiên lấy từ env, nếu không có thì lấy từ settings (nếu settings đã load env)
    api_key = os.getenv("BREVO_API_KEY")
    if not api_key:
        print("❌ Lỗi: Chưa cấu hình BREVO_API_KEY")
        return

    configuration.api_key['api-key'] = api_key
    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
    
    sender_email = settings.MAIL_FROM
    sender_name = "Cinema Chatbot"
    
    sender = {"name": sender_name, "email": sender_email}
    to_list = [{"email": to}]
    
    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
        to=to_list,
        sender=sender,
        subject=subject,
        html_content=body
    )

    try:
        api_instance.send_transac_email(send_smtp_email)
        print(f"✅ Đã gửi email đến {to}")
    except ApiException as e:
        print(f"❌ Lỗi gửi email: {e}")

