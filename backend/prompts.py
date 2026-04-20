from definition import INTENT_DEFINITIONS, ISSUE_DEFINITIONS, DECISION_DEFINITIONS

def build_stage1_prompt(message, prev_context):
    return f"""
You are an AI system that performs structured understanding of user messages.

Your tasks:
1. Update a concise context summary
2. Classify the message into predefined intent and issue types
3. Propose a decision with a brief rationale

--------------------------------
INTENT TYPES and DEFINITIONS (choose ONE):
{INTENT_DEFINITIONS}

ISSUE TYPES and DEFINITIONS (choose any):
{ISSUE_DEFINITIONS}

DECISION TYPES and RULES (choose ONE):
{DECISION_DEFINITIONS}
--------------------------------

INPUT:

Previous context:
{prev_context}

User message:
"{message}"

--------------------------------

INSTRUCTIONS:

1. CONTEXT
- Maintain a summary of relevant conversation state
- Include key past actions and constraints
- If the user continous iterate the same thing, mention it in the summary

2. INTENT
- Select EXACTLY ONE intent_type

3. ISSUES
- Select zero or more issue_types
- Include ambiguity, risk, or conflict if applicable

4. DECISION
- Choose EXACTLY ONE decision from DECISION TYPES

5. RATIONALE
- Provide a short explanation (1 sentence)
- Base it ONLY on detected intent and issues
- Do NOT add new assumptions

--------------------------------

OUTPUT FORMAT (STRICT JSON):

{{
  "context": {{
    "context_summary": "..."
  }},
  "classification": {{
    "intent_type": "...",
    "issues": []
  }},
  "decision": "...",
  "rationale": "..."
}}

--------------------------------

RULES:

- Output ONLY valid JSON
- Do NOT invent labels
- Keep outputs concise
"""

def build_stage1_keyword_prompt(message, KEYWORD_VOCAB):
    return f"""
You are a keyword extraction system.

Your job is to select relevant keywords ONLY from a predefined vocabulary.

--------------------------------
KEYWORD VOCABULARY:
{KEYWORD_VOCAB}
--------------------------------

INPUT:

User message:
"{message}"

--------------------------------

INSTRUCTIONS:

- Select ONLY keywords from the provided vocabulary
- The vocabulary doesn't have to be included in the message, choose the words that best describe the message
- If specific name of person or recipient appears, select general keyword name, same for other general words
- DO NOT generate new words
- If no keywords apply, return an empty list

--------------------------------

OUTPUT FORMAT (STRICT JSON):

{{
  "keywords": []
}}

--------------------------------

RULES:

- Output ONLY valid JSON
- Do NOT invent keywords
- Keep output minimal
"""



def build_stage3_prompt(context, intent, decision, scores):
    return f"""
You are an AI assistant responding to a user.
Task: Generate a concise, natural response.

Decision:
{decision}

Issue scores:
{scores}

Intent:
{intent}

Context:
{context}

Instruction:
- If ASK_CLARIFICATION → ask a clear question
- If CONFIRM_BEFORE → ask for confirmation
- If EXECUTE_AND_NOTIFY → confirm completion
- If EXECUTE_SILENTLY → brief acknowledgment or no-op
- If REFUSE → explain briefly and safely

--------------------------------

OUTPUT FORMAT (STRICT JSON):

{{
  "respond": "..."
}}

"""

def build_stage1_prompt_malformed():
        return f"""
You are an AI system that performs structured understanding of user messages.

Your tasks:
1. Update a concise context summary
2. Classify the message into predefined intent and issue types
3. Propose a decision

--------------------------------
INTENT TYPES and DEFINITIONS (choose ONE):
{INTENT_DEFINITIONS}

ISSUE TYPES and DEFINITIONS (choose any):
{ISSUE_DEFINITIONS}

DECISION TYPES and RULES (choose ONE):
{DECISION_DEFINITIONS}
--------------------------------

--------------------------------

INSTRUCTIONS:

You need to output some malformed format. this time it doesn't have to be correct, it is just for testing
--------------------------------

OUTPUT FORMAT (STRICT JSON):

{{
  "context": {{
  }},
  "classification": {{
    "intent_type": "...",
    "issues": []
  }},
}}
"""