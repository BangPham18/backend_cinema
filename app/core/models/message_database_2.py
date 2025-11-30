from sqlalchemy import Column, String, Integer
from app.core.database import Base
from sqlalchemy.dialects.postgresql import JSONB


class MessageDatabase2(Base):
    __tablename__ = 'message_database_2'
    id = Column(Integer, primary_key=True)
    session_id = Column(String(100))
    message = Column(JSONB)