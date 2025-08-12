from service.agent_service.state.state import AgentState
from service.agent_service.llm_provider.gemini import llm
from service.agent_service.nodes.message_classifier import MessageClassifier
from langchain_core.messages import SystemMessage
import re

def dang_nhap(state: AgentState):
    # Kiểm tra đăng nhập
    sys_mess = [m for m in state['messages'] if isinstance(m, SystemMessage)][0]
    sys_content = sys_mess.content
    pattern = r'`(.*?)`'
    matches = re.findall(pattern, sys_content)

    # Gán vào biến
    dang_nhap, name, birthday, email, sex = matches
    print(dang_nhap, name, birthday, email, sex)
    return {"dang_nhap": dang_nhap,
            "name": name,
            "birthday": birthday,
            "email": email,
            "sex": sex}