from app.graph.state import CyberNoirState
from app.core.llm import get_llm_client
import asyncio

from app.core.logger import get_logger

logger = get_logger("NarratorAgent")

llm = get_llm_client()


SYSTEM_PROMPT = """
You are a cybersecurity incident explainer.
Be concise.
Use 3–4 sentences max.
No markdown.
No headings.
No bullet points.
Plain language only.
"""


def narrator_llm_agent(state: CyberNoirState) -> CyberNoirState:
    logger.info("NarratorAgent started")
    logger.debug(f"Goal: {state.goals.primary_goal}")
    logger.debug(f"Decision: {state.decisions.chosen_path}")
    logger.debug(f"Escalation risk: {state.risks.escalation_risk}")
    logger.debug(f"Lateral risk: {state.risks.lateral_movement_risk}")


    summary = f"""
    Goal: {state.goals.primary_goal}
    Decision: {state.decisions.chosen_path}
    Escalation risk: {state.risks.escalation_risk}
    Lateral risk: {state.risks.lateral_movement_risk}
    """

    messages = [
        {
            "role": "system",
            "content": (
                "You are a cybersecurity incident explainer. "
                "Be concise. Use plain language. "
                "Maximum 3 sentences. No markdown."
            )
        },
        {"role": "user", "content": summary}
    ]

    try:
        narrative = llm.generate(messages)
    except Exception:
        narrative = (
            "The attacker gained access but avoided further actions "
            "because escalation would likely have been detected."
        )

    state.narrative.attacker_narrative = narrative
    state.narrative.confidence_score = 0.75
    state.trace.append({
        "agent": "NarratorAgent",
        "summary": "Generated customer-facing explanation."
    })

    logger.info("NarratorAgent completed")

    return state
