from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.core.database import get_session
from app.core.models import MessageDatabase2

router = APIRouter()

class ReplaceSessionRequest(BaseModel):
    old_session_id: str
    new_session_id: str

@router.put("/replaceid")
def replace_session(
    data: ReplaceSessionRequest,
    db: Session = Depends(get_session)
):
    try:
        # Lấy tất cả message có old_session_id
        messages = db.query(MessageDatabase2).filter(MessageDatabase2.session_id == data.old_session_id).all()

        if not messages:
            # raise HTTPException(status_code=404, detail="Không tìm thấy session_id cần thay thế.")
            return "lỗi"

        # Cập nhật session_id cho từng bản ghi
        for msg in messages:
            msg.session_id = data.new_session_id

        db.commit()

        return {
            "message": f"Đã thay thế {len(messages)} bản ghi từ session_id '{data.old_session_id}' sang '{data.new_session_id}'."
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Lỗi máy chủ: {str(e)}")

    finally:
        db.close()
