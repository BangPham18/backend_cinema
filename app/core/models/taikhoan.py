from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class TaiKhoan(Base):
    __tablename__ = 'tai_khoan'
    email = Column(String(100), primary_key=True)
    mat_khau = Column(String(100), nullable=False)
    ma_kh = Column(String(10), ForeignKey('khach_hang.ma_kh'))
    
    khach_hang = relationship("KhachHang", back_populates="tai_khoan")
    ve = relationship("Ve", back_populates="tai_khoan", uselist=False)