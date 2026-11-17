import json
import os
from typing import Any
from genai import Any

from google import genai
from google.genai import types

FAQ_FILE = "faqs.json"
def load_faqs():
    if not os.path.exists(FAQ_FILE):
        return []

    with open(FAQ_FILE, "r", encoding="utf-8") as file:
        return json.load(file)

def get_gemini_client():
    api_key = st.secrets.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return None
    return genai.Client(api_key=api_key)

def get_answer(question):
    client = get_gemini_client()
    if not client:
        return "⚠️ `GEMINI_API_KEY` is missing. Please add it to your Streamlit Secrets."

    faqs = load_faqs()
    faq_context = json.dumps(faqs, indent=2)

    system_instruction = f"""
    You are CampusBot, the official AI Campus Assistant for The National College, Basavanagudi (NCB), Bengaluru.
    Answer student and visitor questions clearly, politely, and concisely.
    
    Use the following official Campus FAQ data as your primary source of truth:
    {faq_context}
    
    Rules:
    - If the answer can be found or inferred from the FAQ data, answer accurately based on it.
    - If the user asks a greeting or casual conversational question, respond warmly and helpfully.
    - If a specific college detail is NOT in the FAQ data, politely state that you don't have that specific information in your current records and advise contacting the college administration office (Phone: 080-26674441, Email: info@ncbgudi.com).
    """

    # Build conversation history from Streamlit session state for multi-turn memory
    formatted_contents = []
    if "messages" in st.session_state:
        history = st.session_state.messages[:-1] if len(st.session_state.messages) > 0 else []
        for msg in history[-6:]:  # Keep last 6 messages for conversational context
            role = "user" if msg["role"] == "user" else "model"
            formatted_contents.append(
                types.Content(role=role, parts=[types.Part.from_text(text=msg["content"])])
            )

    formatted_contents.append(
        types.Content(role="user", parts=[types.Part.from_text(text=question)])
    )

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=formatted_contents,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.3,
            ),
        )
        return response.text
    except Exception as e:
        return f"Sorry, I ran into an error connecting to the AI service: {e}"
