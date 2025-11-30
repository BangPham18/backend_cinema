from pydantic import EmailStr
import traceback
from sqlalchemy.orm import Session
from app.core.database import get_session
from app.core.models import Ve, LichChieu, Phim, Ghe
from scripts.send_email import send_email_html
from typing import List

def gui_lai_ve(email: EmailStr, ma_ves: List[str]) -> str:
    db: Session = get_session()
    try:
        ve_list = db.query(Ve).filter(Ve.ma_ve.in_(ma_ves), Ve.email == email).all()
        if not ve_list:
            return "❌ Không tìm thấy vé nào phù hợp với danh sách mã vé và email."

        rows = ""
        for ve in ve_list:
            lc = db.query(LichChieu).filter_by(ma_lich_chieu=ve.ma_lich_chieu).first()
            phim = db.query(Phim).filter_by(ma_phim=lc.ma_phim).first()
            ghe = db.query(Ghe).filter_by(ma_ghe=ve.ma_ghe).first()

            rows += f"""
            <tr>
                <td>{phim.ten_phim}</td>
                <td>{lc.gio}</td>
                <td>{ghe.ten_ghe}</td>
                <td><b>{ve.ma_ve}</b></td>
            </tr>
            """

        subject = f"🎫 Gửi lại {len(ve_list)} vé đã đặt thành công"
        body = f"""
        <html>
          <body>
            <div style="font-family: Arial, sans-serif; max-width: 600px; margin: auto; border: 1px solid #ddd; padding: 20px; border-radius: 10px;">
              <h2 style="text-align: center; color: #2b2b2b;">🎬 Thông tin vé của bạn</h2>
              <p>Xin chào <b>{email}</b>,</p>
              <p>Bạn đã yêu cầu gửi lại các vé đã đặt. Dưới đây là thông tin:</p>
              <table style="width: 100%; border-collapse: collapse;" border="1">
                <tr>
                  <th>Tên phim</th>
                  <th>Thời gian chiếu</th>
                  <th>Ghế</th>
                  <th>Mã vé</th>
                </tr>
                {rows}
              </table>
              <br/>
              <p style="text-align: center;">🎉 Cảm ơn bạn đã sử dụng dịch vụ của chúng tôi!</p>
            </div>
          </body>
        </html>
        """
        send_email_html(to=email, subject=subject, body=body)
        return f"✅ Đã gửi lại {len(ve_list)} vé qua email."
    except Exception as e:
        traceback.print_exc()
        print(f"❌ DEBUG ERROR (gui_ve): {str(e)}")
        return f"❌ Lỗi khi gửi lại vé: {str(e)}"
    finally:
        db.close()
