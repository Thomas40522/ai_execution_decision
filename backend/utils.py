import json
import math

def safe_stage3_output(text):

    try:
        data = json.loads(text)
    except Exception:
        return {
            "respond": "Sorry, something went wrong. Please try again.",
            "error": "invalid_json"
        }

    if not isinstance(data, dict):
        return fallback_stage3("not_dict")

    if "respond" not in data:
        return fallback_stage3("missing_respond")

    if not isinstance(data["respond"], str):
        return fallback_stage3("respond_not_string")

    return data


def fallback_stage3(reason):
    return {
        "respond": "Sorry, I couldn't process that properly. Could you rephrase?",
        "error": reason
    }
    
def safe_stage1_output(text, intent_types, issue_types):

    try:
        data = json.loads(text)
    except:
        return fallback_stage1("invalid_json")

    # structure checks
    try:
        context = data["context"]["context_summary"]
        intent = data["classification"]["intent_type"]
        issues = data["classification"]["issues"]
    except:
        return fallback_stage1("missing_fields")

    # type checks
    if not isinstance(context, str):
        return fallback_stage1("bad_context")

    if intent not in intent_types:
        return fallback_stage1("invalid_intent")

    if not all(i in issue_types for i in issues):
        return fallback_stage1("invalid_issues")

    return data

def safe_stage1_keyword_output(text):
    try:
        data = json.loads(text)
    except:
        return fallback_stage1("invalid_json")
    
    try:
        _ = data["keywords"]
    except:
        return fallback_stage1("missing_fields")
    
    return data
    


def fallback_stage1(reason):
    return {
        "context": {"context_summary": "Context unclear due to parsing error."},
        "classification": {
            "intent_type": "unknown",
            "issues": ["parsing_error"]
        },
        "keywords": [],
        "error": reason
    }
    

def compute_confidence(decision_scores):
    # find minimum score
    min_score = min(decision_scores.values())

    # if negative exists, shift all scores up
    if min_score < 0:
        shifted_scores = {
            k: v - min_score
            for k, v in decision_scores.items()
        }
    else:
        shifted_scores = decision_scores.copy()

    total = sum(shifted_scores.values()) + 1e-6  # avoid divide by zero

    probs = {
        k: v / total
        for k, v in shifted_scores.items()
    }

    best_decision = max(probs, key=probs.get)
    confidence = int(probs[best_decision] * 100)

    return best_decision, confidence, probs