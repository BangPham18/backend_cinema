from service.agent_service.state.state import AgentState
from langchain_core.messages import AIMessage

def kiem_tra_dang_nhap(state: AgentState) -> bool:
    dangNhap = state['dang_nhap']
    if dangNhap == 'đã đăng nhập':
        return True
    else:
        state['messages'].append(AIMessage(content="Bạn không thể đặt vé. Vui lòng đăng nhập."))
        return False