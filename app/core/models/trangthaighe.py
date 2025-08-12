from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class TrangThaiGhe(Base):
    __tablename__ = 'trang_thai_ghe'
    ma_phong = Column(String(10), ForeignKey('phong_phim.ma_phong'), primary_key=True)
    ma_ghe = Column(String(10), ForeignKey('ghe.ma_ghe'), primary_key=True)

    phong_phim = relationship("PhongPhim", back_populates="trang_thai_ghe")
    ghe = relationship("Ghe", back_populates="trang_thai")