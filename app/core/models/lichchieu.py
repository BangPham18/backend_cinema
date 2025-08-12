from sqlalchemy import Column, String, Time, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class LichChieu(Base):
    __tablename__ = 'lich_chieu'
    ma_lich_chieu = Column(String(10), primary_key=True)
    gio = Column(Time)
    ngay = Column(Date)
    ma_phim = Column(String(10), ForeignKey('phim.ma_phim'))
    ma_phong = Column(String(10), ForeignKey('phong_phim.ma_phong'))

    phim = relationship("Phim", back_populates="lich_chieu")
    phong_phim = relationship("PhongPhim", back_populates="lich_chieu")
    ve = relationship("Ve", back_populates="lich_chieu")