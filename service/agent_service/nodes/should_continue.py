from service.agent_service.state.state import AgentState

def should_continue(state: AgentState) -> bool:
    last_message = state['messages'][-1]
    return bool(last_message.tool_calls)
