from langgraph.graph import StateGraph, END

from app.agents.confidence import confidence_calibration_agent
from app.graph.state import CyberNoirState

from app.agents.evidence import evidence_context_agent
from app.agents.recon import recon_reasoning_agent
from app.agents.goals import goal_inference_agent
from app.agents.risk import risk_evaluation_agent
from app.agents.decision import decision_simulation_agent
from app.agents.narrator import narrator_llm_agent


def build_cybernoir_graph():
    graph = StateGraph(CyberNoirState)

    graph.add_node("evidence", evidence_context_agent)
    graph.add_node("recon", recon_reasoning_agent)
    graph.add_node("goals", goal_inference_agent)
    graph.add_node("risk", risk_evaluation_agent)
    graph.add_node("decision", decision_simulation_agent)
    graph.add_node("narrator", narrator_llm_agent)
    graph.add_node("confidence", confidence_calibration_agent)

    graph.set_entry_point("evidence")

    graph.add_edge("evidence", "recon")
    graph.add_edge("recon", "goals")
    graph.add_edge("goals", "risk")
    graph.add_edge("risk", "decision")
    graph.add_edge("decision", "confidence")
    graph.add_edge("confidence", "narrator")
    graph.add_edge("narrator", END)

    return graph.compile()


def run_cybernoir(initial_state: CyberNoirState) -> CyberNoirState:
    graph = build_cybernoir_graph()
    result = graph.invoke(initial_state)
    return CyberNoirState(**result)
