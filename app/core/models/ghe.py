from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from app.core.database import Base

class Ghe(Base):
    __tablename__ = 'ghe'
    ma_ghe = Column(String(10), primary_key=True)
    ten_ghe = Column(String(10))

    trang_thai = relationship("TrangThaiGhe", back_populates="ghe")
    ve = relationship("Ve", back_populates="ghe")