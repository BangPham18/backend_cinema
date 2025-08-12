from sqlalchemy import Column, String
from app.core.database import Base
from sqlalchemy.dialects.postgresql import JSONB


class MessageDatabase2(Base):
    __tablename__ = 'message_database_2'
    id = Column(String(10000), primary_key=True)
    session_id = Column(String(100))
    message = Column(JSONB)