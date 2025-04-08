import os
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

import prompts

load_dotenv()

st.session_state.setdefault("openai_model", "gpt-4o-mini")

client = OpenAI(
    base_url=os.getenv("OPENAI_API_BASE_URL"),
    api_key=os.getenv("GITHUB_TOKEN")
)

# ─── Chat Interface Components ────────────────────────────────────────────────

def initialize_chat_data():
    if "history" not in st.session_state:
        st.session_state.history = [{"role": "assistant", "content": prompts.GREETING}]
    if "system_message" not in st.session_state:
        st.session_state.system_message = {
            "role": "system",
            "content": prompts.SYSTEM_PROMPT
        }

def render_history():
    for msg in st.session_state.history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

def handle_user_input(user_input):
    st.session_state.history.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    messages_for_api = [st.session_state.system_message] + st.session_state.history

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state.openai_model,
            messages=messages_for_api,
            temperature=0.7,
            stream=True
        )
        assistant_reply = st.write_stream(stream)

# ─── Main Chat Interface ──────────────────────────────────────────────────────

def chat_interface():
    st.title("🤖 Hiring Assistant Bot")   
    initialize_chat_data()
    render_history()
    
    if user_input := st.chat_input("Your response…"):
        handle_user_input(user_input)

# ─── Main ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    chat_interface()
