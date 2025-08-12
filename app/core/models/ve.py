from sqlalchemy import Column, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from app.core.database import Base

class Ve(Base):
    __tablename__ = 've'
    ma_ve = Column(String(10), primary_key=True)
    ngay_dat = Column(Date)
    ma_lich_chieu = Column(String(10), ForeignKey('lich_chieu.ma_lich_chieu'))
    ma_ghe = Column(String(10), ForeignKey('ghe.ma_ghe'))
    email = Column(String(100), ForeignKey('tai_khoan.email'))

    lich_chieu = relationship("LichChieu", back_populates="ve")
    ghe = relationship("Ghe", back_populates="ve")
    tai_khoan = relationship("TaiKhoan", back_populates="ve")