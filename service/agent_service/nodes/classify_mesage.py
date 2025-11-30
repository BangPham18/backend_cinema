from service.agent_service.state.state import AgentState
from service.agent_service.llm_provider.gemini import llm
from service.agent_service.nodes.message_classifier import MessageClassifier
from langchain_core.messages import SystemMessage
import re

def classify_mesage(state: AgentState):
    # Phân loại tin nhắn
    all_mess = [m for m in state['messages'] if not isinstance(m, SystemMessage)]
    
    content_list = []
    for mess in all_mess:
        if isinstance(mess.content, str):
            content_list.append(mess.content)
        elif isinstance(mess.content, list):
            # Handle list content (e.g., from Gemini with text parts)
            text_parts = []
            for item in mess.content:
                if isinstance(item, dict) and 'text' in item:
                    text_parts.append(item['text'])
                elif isinstance(item, str):
                    text_parts.append(item)
            content_list.append(" ".join(text_parts))
            
    content_str = "\n".join(content_list)

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