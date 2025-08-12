import smtplib
from email.mime.text import MIMEText

def send_email_html(to: str, subject: str, body: str):
    msg = MIMEText(body, "html")
    msg["Subject"] = subject
    msg["From"] = "pbang4589@gmail.com"
    msg["To"] = to

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login("pbang4589@gmail.com", "nhwe vhxx ofdb zfcz")
        server.sendmail(msg["From"], [msg["To"]], msg.as_string())
