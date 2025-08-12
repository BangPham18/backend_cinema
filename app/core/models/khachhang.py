from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from app.core.database import Base

class KhachHang(Base):
    __tablename__ = 'khach_hang'
    ma_kh = Column(String(10), primary_key=True)
    ten = Column(String(100))
    nam_sinh = Column(Integer)
    gioi_tinh = Column(String(10))
    dia_chi = Column(String(255))

    tai_khoan = relationship("TaiKhoan", back_populates="khach_hang", uselist=False)
