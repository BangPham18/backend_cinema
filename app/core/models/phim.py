from sqlalchemy import Column, String, Text
from sqlalchemy.orm import relationship
from app.core.database import Base

class Phim(Base):
    __tablename__ = 'phim'
    ma_phim = Column(String(10), primary_key=True)
    ten_phim = Column(String(255))
    NSX = Column(String(100))
    nhan = Column(Text)
    the_loai = Column(String(100))
    poster = Column(String(100))
    
    lich_chieu = relationship("LichChieu", back_populates="phim")