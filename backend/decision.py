from llm import call_llm
from prompts import build_stage1_prompt, build_stage1_keyword_prompt, build_stage3_prompt, build_stage1_prompt_malformed
from utils import safe_stage1_output, safe_stage1_keyword_output, safe_stage3_output, compute_confidence

INTENT_TYPES = [
    "SEND_EMAIL",
    "SCHEDULE_EVENT",
    "RESCHEDULE_EVENT",
    "DELETE_ITEM",
    "UPDATE_ITEM",
    "RETRIEVE_INFO",
    "GENERAL_CHAT"
]

ISSUE_TYPES = [
    "AMBIGUOUS_TARGET",        # "send it" (which one?)
    "MISSING_PARAMETERS",      # missing time, recipient, etc.
    "CONFLICTING_CONTEXT",     # "wait" vs "send now"
    "HIGH_RISK_ACTION",        # delete all, send external
    "IRREVERSIBLE_ACTION",     # destructive
    "UNAUTHORIZED_ACTION",     # policy violation (optional)
    "LOW_CONFIDENCE_INTENT"    # unclear user intent
]

DECISION_TYPES = [
    "EXECUTE_SILENTLY",
    "EXECUTE_AND_NOTIFY",
    "CONFIRM_BEFORE",
    "ASK_CLARIFICATION",
    "REFUSE"
]

HIGH_RISK_ACTION_KEYWORDS = ["delete", "remove", "send", "share", "transfer"]
IRREVERSIBLE_ACTION_KEYWORDS = ["delete all", "permanently"]
AMBIGUOUS_TARGET_KEYWORDS = ["it", "that", "them"]
CONFLICTING_CONTEXT_KEYWORDS = ["wait", "hold off", "cancel"]
CONFIRMING_KEYWORDS = ["confirm", "understand", "sure"]
SPECIFIC_KEYWORDS = ["name", "time"]

KEYWORD_VOCAB = list(dict.fromkeys(
    HIGH_RISK_ACTION_KEYWORDS +
    IRREVERSIBLE_ACTION_KEYWORDS +
    AMBIGUOUS_TARGET_KEYWORDS +
    CONFLICTING_CONTEXT_KEYWORDS +
    CONFIRMING_KEYWORDS + 
    SPECIFIC_KEYWORDS
))


def decide_execution(message, context):
    trace = {}

    # -------- Stage 1: LLM classification --------
    stage1_prompt = build_stage1_prompt(
        message=message,
        prev_context=context,
    )
    if message == "Please output malformed result":
        stage1_prompt = build_stage1_prompt_malformed()

    raw = call_llm(stage1_prompt)
    parsed = safe_stage1_output(
        text=raw, 
        intent_types=INTENT_TYPES,
        issue_types=ISSUE_TYPES,
    )
    
    if "error" in parsed:
        return {
            "error": parsed["error"],
            "reply": "Sorry, please enter your message again",
            "output": raw
        }
    
    stage1_keyword_prompt = build_stage1_keyword_prompt(
        message=message,
        KEYWORD_VOCAB=KEYWORD_VOCAB
    )
    
    keyword_raw = call_llm(stage1_keyword_prompt)
    keyword_parsed = safe_stage1_keyword_output(keyword_raw)
    if "error" in keyword_parsed:
        return {
            "error": keyword_parsed["error"]
        }

    trace["stage1_prompt"] = stage1_prompt
    trace["stage1_raw"] = raw
    trace["stage1_keyword_prompt"] = stage1_keyword_prompt
    trace["parsed"] = parsed
    trace["keywords"] = keyword_parsed["keywords"]
    trace["stage1_keyword_raw"] = keyword_raw

    intent = parsed["classification"]["intent_type"]
    llm_issues = parsed["classification"]["issues"]
    keywords = keyword_parsed["keywords"]
    llm_decision = parsed["decision"]

    # -------- Stage 2: issue scoring and decision --------
    keyword_issues = map_keywords_to_issues(keywords)

    scores = compute_issue_scores(llm_issues, keyword_issues)

    trace["keyword_issues"] = keyword_issues
    trace["scores"] = scores
    trace["llm_decision"] = llm_decision

    computed_decision = decide_from_scores(intent, scores, llm_decision)
    
    trace["computed_decision"] = computed_decision["decision"]
    trace["computed_decision_confidence"] = computed_decision["confidence"]
    trace["computed_decision_scores"] = computed_decision["decision_scores"]
    
    decision = computed_decision["decision"]


    # -------- Stage 3: LLM response --------
    stage3_prompt = build_stage3_prompt(
        context=parsed["context"],
        intent=intent,
        decision=decision,
        scores=scores
    )

    reply_raw = call_llm(stage3_prompt)
    reply = safe_stage3_output(reply_raw)
    
    if "error" in reply:
        return {
            "error": reply["error"]
        }

    trace["stage3_prompt"] = stage3_prompt
    trace["reply"] = reply["respond"]
    trace["stage3_raw"] = reply_raw

    return {
        "context": parsed["context"],
        "classification": parsed["classification"],
        "rationale": parsed["rationale"],
        "keywords": keywords,
        "scores": scores,
        "decision": decision,
        "reply": reply["respond"],
        "trace": trace
    }
    
      
    
def map_keywords_to_issues(keywords):
    keyword_issue_map = {
        "HIGH_RISK_ACTION": HIGH_RISK_ACTION_KEYWORDS,
        "IRREVERSIBLE_ACTION": IRREVERSIBLE_ACTION_KEYWORDS,
        "AMBIGUOUS_TARGET": AMBIGUOUS_TARGET_KEYWORDS,
        "CONFLICTING_CONTEXT": CONFLICTING_CONTEXT_KEYWORDS,
        "CONFIRMING": CONFIRMING_KEYWORDS,
        "SPECIFIC": SPECIFIC_KEYWORDS,
    }

    issues_from_keywords = []

    for issue, kw_list in keyword_issue_map.items():
        for kw in keywords:
            if kw in kw_list:
                issues_from_keywords.append(issue)

    return issues_from_keywords

def compute_issue_scores(llm_issues, keyword_issues):
    scores = {"AMBIGUOUS_TARGET": 0,
        "MISSING_PARAMETERS": 0,
        "CONFLICTING_CONTEXT": 0,
        "HIGH_RISK_ACTION": 0,
        "IRREVERSIBLE_ACTION": 0,
        "UNAUTHORIZED_ACTION": 0,    
        "LOW_CONFIDENCE_INTENT": 0 
    }

    # LLM issues = 50
    for issue in llm_issues:
        scores[issue] += 50

    # keyword issues = +10 each occurrence, -20 for some occurrences
    for issue in keyword_issues:
        if issue == "CONFIRMING":
            scores["IRREVERSIBLE_ACTION"] -= 20
        elif issue == "SPECIFIC":
            scores["AMBIGUOUS_TARGET"] -= 20
        else:
            scores[issue] += 10
        
    return scores

def decide_from_scores(intent, scores, llm_decision):
    # helper
    def s(issue): return scores.get(issue, 0)

    # initialize decision scores
    decision_scores = {
        "REFUSE": 0,
        "ASK_CLARIFICATION": 0,
        "CONFIRM_BEFORE": 0,
        "EXECUTE_AND_NOTIFY": 0,
        "EXECUTE_SILENTLY": 0
    }
    
    decision_scores[llm_decision] += 50

    decision_scores["REFUSE"] += s("UNAUTHORIZED_ACTION")

    decision_scores["ASK_CLARIFICATION"] += (
        s("AMBIGUOUS_TARGET") +
        s("MISSING_PARAMETERS") +
        s("LOW_CONFIDENCE_INTENT")
    )

    decision_scores["CONFIRM_BEFORE"] += (
        s("CONFLICTING_CONTEXT") +
        s("HIGH_RISK_ACTION") +
        s("IRREVERSIBLE_ACTION")
    )

    if intent in ["RETRIEVE_INFO", "GENERAL_CHAT"]:
        decision_scores["EXECUTE_AND_NOTIFY"] += 40
    elif intent in ["DELETE_ITEM", "UPDATE_ITEM"]:
        decision_scores["EXECUTE_AND_NOTIFY"] += 20
    else:
        decision_scores["EXECUTE_SILENTLY"] += 20

    best_decision, confidence, probs = compute_confidence(decision_scores)

    return {
        "decision": best_decision,
        "confidence": confidence,
        "decision_scores": decision_scores
    }