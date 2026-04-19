from llm import call_llm

def compute_signals(action, message, history):
    action_lower = action.lower()

    risk_keywords = ["delete", "send", "transfer"]
    high_risk = any(k in action_lower for k in risk_keywords)

    return {
        "intent_resolved": len(message.strip()) > 0,
        "has_all_parameters": "?" not in message,
        "risk_level": "high" if high_risk else "low",
        "reversibility": "irreversible" if "delete" in action_lower else "reversible",
        "policy_blocked": False,
        "user_confirmation_history": "none"
    }


def apply_guardrails(decision, signals):
    if signals["policy_blocked"]:
        return "REFUSE"

    if signals["risk_level"] == "high" and decision == "EXECUTE_SILENTLY":
        return "CONFIRM_BEFORE"

    return decision


def decide_execution(action, message, history, user_state):
    signals = compute_signals(action, message, history)

    llm_response = call_llm(action, message, history, signals)

    decision = llm_response.get("decision", "CONFIRM_BEFORE")

    final_decision = apply_guardrails(decision, signals)

    return {
        "inputs": {
            "action": action,
            "message": message,
            "history": history
        },
        "signals": signals,
        "llm_output": llm_response,
        "final_decision": final_decision
    }