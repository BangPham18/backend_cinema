from fastapi import APIRouter
from pydantic import BaseModel, Field
from service.agent_service.memory.memory_factory import get_memory
from service.agent_service.main import app as agent_graph
from app.core.security import get_current_user
from langchain_core.messages import HumanMessage, SystemMessage
from fastapi import Depends
from typing import Optional
router = APIRouter()

# Schema cho input
class MessageInput(BaseModel):
    session_id: str
    message: str
class User(BaseModel):
    ten: str = Field(..., alias="name")
    namsinh: int = Field(..., alias="birthYear")
    gioitinh: Optional[str] = None
    email: str
    model_config = {"populate_by_name": True}
class ChatRequest(BaseModel):
    payload: MessageInput
    user: Optional[User] = None
prompt = """
Trạng thái đăng nhập: `{state}`
Họ tên: `{name}`
Năm sinh: `{birthday}`
Email: `{email}`
Giới tính: `{sex}`
"""

@router.post("/chat")
async def chat_with_agent(request: ChatRequest):
    data = request.payload
    user = request.user
    
    session_id = data.session_id
    user_input = data.message

    memory = get_memory(session_id)

    # Add system message nếu chưa có
    # system_messages = [m for m in memory.messages if isinstance(m, SystemMessage)]
    if user:
        state = "đã đăng nhập"
        name = user.ten
        birthday = user.namsinh
        email= user.email
        sex= user.gioitinh
    else:
        state = "chưa đăng nhập"
        name = "chưa đăng nhập"
        birthday = "chưa đăng nhập"
        email="chưa đăng nhập"
        sex="chưa đăng nhập"

    new_system_msg = SystemMessage(content=prompt.format(state=state, name=name, birthday=birthday, email=email, sex=sex))

    history = memory.messages
    history.append(HumanMessage(content=user_input))
    # system_messages = [m for m in history if isinstance(m, SystemMessage)]
    other_messages = [m for m in history if not isinstance(m, SystemMessage)]
    limited_history = [new_system_msg] + other_messages[-14:]  

    # Gọi Agent
    final_state = agent_graph.invoke({"messages": limited_history})
    ai_response = final_state["messages"][-1]
    # Ở đâu đó trong code hoặc script riêng
    memory.add_messages([HumanMessage(content=user_input), ai_response])
    return {"response": ai_response.content}
