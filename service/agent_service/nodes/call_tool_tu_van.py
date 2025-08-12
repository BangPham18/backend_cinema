from langchain_core.messages import ToolMessage
from service.agent_service.state.state import AgentState
from service.agent_service.tools import tools  
from langgraph.prebuilt import ToolNode

tool_executor_tu_van = ToolNode(tools)