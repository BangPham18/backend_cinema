from service.agent_service.tools import tools  
from .gemini import llm

llm_with_tool = llm.bind_tools(tools)
