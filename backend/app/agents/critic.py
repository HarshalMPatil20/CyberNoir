from app.graph.state import CyberNoirState
from app.core.llm_clients import get_llm_client

llm = get_llm_client()


CRITIC_PROMPT = """
You are reviewing a cybersecurity explanation.
Critique clarity, tone, and uncertainty.
Do NOT introduce new facts.
"""


def critic_agent(state: CyberNoirState) -> CyberNoirState:
    messages = [
        {"role": "system", "content": CRITIC_PROMPT},
        {"role": "user", "content": state.narrative.attacker_narrative}
    ]

    print("[Critic] Enter")

    critique = llm.generate(messages)
    state.narrative.revision_notes = critique

    print("[Critic] Exit")
    return state
