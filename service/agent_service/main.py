from langgraph.graph import StateGraph, END
from service.agent_service.state.state import AgentState
from service.agent_service.nodes.call_model_tu_van import call_model_tu_van
from service.agent_service.nodes.call_model_dat_ve import call_model_dat_ve
from service.agent_service.nodes.call_tool_tu_van import tool_executor_tu_van
from service.agent_service.nodes.call_tool_dat_ve import tool_executor_dat_ve
from service.agent_service.nodes.should_continue import should_continue
from service.agent_service.nodes.classify_mesage import classify_mesage
from service.agent_service.nodes.dat_ve_hay_tu_van import dat_ve_hay_tu_van
from service.agent_service.nodes.kiem_tra_dang_nhap import kiem_tra_dang_nhap
from service.agent_service.nodes.dang_nhap import dang_nhap
# --- 4. Xây dựng Graph ---
workflow = StateGraph(AgentState)

workflow.add_node("classifier", classify_mesage)
workflow.add_node("agent_tu_van", call_model_tu_van)
workflow.add_node("agent_dat_ve", call_model_dat_ve)
workflow.add_node("action_tu_van", tool_executor_tu_van)
workflow.add_node("action_dat_ve", tool_executor_dat_ve)
workflow.add_node("kiem_tra_dang_nhap", kiem_tra_dang_nhap)
workflow.add_node("dang_nhap", dang_nhap)

workflow.set_entry_point("classifier")

workflow.add_conditional_edges(
    "classifier",
    dat_ve_hay_tu_van,
    {
        True: "agent_tu_van",
        False: "dang_nhap"
    }
)

workflow.add_conditional_edges(
    "dang_nhap",
    kiem_tra_dang_nhap,
    {
        True: "agent_dat_ve",
        False: END
    }
)

workflow.add_conditional_edges(
    "agent_tu_van",
    should_continue,
    {
        True: "action_tu_van",
        False: END
    }
)

workflow.add_conditional_edges(
    "agent_dat_ve",
    should_continue,
    {
        True: "action_dat_ve",
        False: END
    }
)

workflow.add_edge("action_tu_van", "agent_tu_van")
workflow.add_edge("action_dat_ve", "agent_dat_ve")

app = workflow.compile()
