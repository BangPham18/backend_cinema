from service.agent_service.state.state import AgentState

def dat_ve_hay_tu_van(state: AgentState) -> bool:
    classify = state['classify']
    if classify == 'tư vấn':
        return True
    else:
        return False
