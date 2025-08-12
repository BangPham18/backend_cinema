from service.agent_service.state.state import AgentState
from service.agent_service.llm_provider.gemini import llm
from service.agent_service.nodes.message_classifier import MessageClassifier
from langchain_core.messages import SystemMessage
import re

def classify_mesage(state: AgentState):
    # Phân loại tin nhắn
    all_mess = [m for m in state['messages'] if not isinstance(m, SystemMessage)]
    content = [mess.content for mess in all_mess]

    content_str = "\n".join(content)

    classifier_llm = llm.with_structured_output(MessageClassifier)

    result = classifier_llm.invoke([
        {"role":"system",
         "content":"""Bạn là AI phân loại câu nói người dùng ở dòng cuối thành 2 loại là tư vấn và đặt vé.
         - tư vấn: Khi người dùng muốn xem lịch chiếu, phim hot, phim theo thể loại, ...
         - đặt vé: khi người dùng muốn đặt vé"""
        },
        {"role":"user",
         "content": content_str
        }
    ])
    
    return {"classify": result.message_type}