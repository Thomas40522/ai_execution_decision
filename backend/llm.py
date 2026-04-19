import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def call_llm(prompt, model="gpt-4o-mini", max_retries=3, timeout=10):
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You output valid JSON only."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0,
                timeout=timeout
            )

            content = response.choices[0].message.content

            if not content:
                raise ValueError("Empty response from LLM")

            return content

        except Exception as e:
            print(f"[LLM ERROR] Attempt {attempt+1}: {e}")

            if attempt == max_retries - 1:
                return None 