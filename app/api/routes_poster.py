from fastapi import Query, APIRouter, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional
from app.core.database import get_session
from app.core.models import Phim  

router = APIRouter()

@router.get("/poster")
def get_poster_by_title(title: Optional[str] = Query(None)):
    session: Session = get_session()
    try:
        movie = session.query(Phim).filter(func.lower(Phim.text) == title.lower()).first()

        if not movie:
            raise HTTPException(status_code=404, detail="Không tìm thấy poster cho phim")

        return {"poster": movie.poster}
    finally:
        session.close()
