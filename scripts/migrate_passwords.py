# scripts/migrate_passwords.py

from app.core.database import get_connection
from app.core.security import hash_password

def migrate_passwords():
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("SELECT email, mat_khau FROM tai_khoan")
        users = cur.fetchall()

        for user in users:
            user_id = user["email"]
            plain_password = user["mat_khau"]
            hashed = hash_password(plain_password)

            cur.execute("UPDATE tai_khoan SET mat_khau = %s WHERE email = %s", (hashed, user_id))

        conn.commit()
        print("✅ Đã mã hóa và cập nhật tất cả mật khẩu.")

if __name__ == "__main__":
    migrate_passwords()
