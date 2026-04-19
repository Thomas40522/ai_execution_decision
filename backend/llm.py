import os
import json
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def call_llm(action, message, history, signals):
    prompt = f"""
You are an execution decision engine.

Action: {action}
User message: {message}
History: {history}
Signals: {signals}

Decide one:
EXECUTE_SILENTLY
EXECUTE_AND_NOTIFY
CONFIRM_BEFORE
ASK_CLARIFICATION
REFUSE

Return JSON:
{{
  "decision": "...",
  "rationale": "...",
  "confidence": 0-1
}}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        content = response.choices[0].message.content
        return json.loads(content)

    except Exception as e:
        return {
            "decision": "CONFIRM_BEFORE",
            "rationale": f"LLM failure: {str(e)}",
            "confidence": 0
        }