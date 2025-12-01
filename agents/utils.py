import os
from typing import Optional
try:
    import openai
except ImportError:
    openai = None

try:
    import google.generativeai as genai
except ImportError:
    genai = None

def get_llm_response(prompt: str, system_prompt: str = "You are a helpful assistant.") -> str:
    # 1. Try Gemini
    gemini_key = os.getenv("GEMINI_API_KEY")
    if gemini_key and genai:
        try:
            genai.configure(api_key=gemini_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            # Gemini doesn't have system prompt in the same way, but we can prepend it.
            full_prompt = f"{system_prompt}\n\n{prompt}"
            response = model.generate_content(full_prompt)
            return response.text
        except Exception as e:
            print(f"Gemini Error: {e}, trying OpenAI...")

    # 2. Try OpenAI
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key and openai:
        try:
            client = openai.OpenAI(api_key=api_key)
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"OpenAI Error: {e}, falling back to mock.")
    
    # 3. Fallback / Simulation Mode
    print(f"--- MOCK LLM CALL ---\nSystem: {system_prompt}\nUser: {prompt}\n----------------")
    if "research" in prompt.lower():
        return "Found recent news: Company raised Series B. Key contact: Jane Doe (CTO). Tech stack: React, Python."
    if "email" in prompt.lower():
        return "Subject: Partnership Opportunity\n\nHi Jane,\n\nI saw you recently raised Series B. We'd love to discuss..."
    return "Processed."
