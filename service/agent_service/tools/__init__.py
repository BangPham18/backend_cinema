from .get_phim_hot import GetPhimHotTool
from .goi_y_phim_theo_so_thich import GoiYPhimTool
from .get_lich_chieu import TraCuuLichChieuTool
from .phim_con_suat_trong import PhimConSuatTrongTool
from .kiem_tra_ghe_trong import GheTrongTool
from .kiem_tra_phim import KiemTraPhimTonTaiTool
from .get_time_week import GetFutureDateFromWeekdayTool
from .get_time import GetCurrentTimeTool
from .gui_otp import ToolGuiOTP
from .xac_thuc_otp import ToolXacThucVaDatVe
from .kiem_tra_ngay_dat import KiemTraNgayDatTool
from .get_relative_day import GetRelativeDateTool

tools = [
    GetPhimHotTool(),
    GoiYPhimTool(),
    TraCuuLichChieuTool(),
    GheTrongTool(),
    PhimConSuatTrongTool(),
    KiemTraPhimTonTaiTool(),
    GetFutureDateFromWeekdayTool(),
    GetCurrentTimeTool(),
    ToolGuiOTP(),
    ToolXacThucVaDatVe(),
    KiemTraNgayDatTool(),
    GetRelativeDateTool()
]
