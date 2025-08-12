from langchain_core.messages import ToolMessage
from service.agent_service.state.state import AgentState
from service.agent_service.tools import tools  
from langgraph.prebuilt import ToolNode

tool_executor_dat_ve = ToolNode(tools)