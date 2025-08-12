from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from app.core.database import Base

class PhongPhim(Base):
    __tablename__ = 'phong_phim'
    ma_phong = Column(String(10), primary_key=True)
    ten_phong = Column(String(100))
    so_luong_ghe = Column(Integer)

    lich_chieu = relationship("LichChieu", back_populates="phong_phim")
    trang_thai_ghe = relationship("TrangThaiGhe", back_populates="phong_phim")