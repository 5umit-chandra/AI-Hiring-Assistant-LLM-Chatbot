import os
import json
from datetime import datetime

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

import prompts

load_dotenv()

st.set_page_config(page_title="Hiring Assistant", page_icon="💼")

with st.sidebar:
    sidebar_token = st.text_input(
        "GITHUB_TOKEN",
        key="github_token",
        type="password",
        placeholder="Paste your GitHub token here"
    )

if sidebar_token:
    github_token = sidebar_token
else:
    github_token = os.getenv("GITHUB_TOKEN")

if not github_token:
    st.warning("Please paste your GitHub token in the sidebar.")

st.session_state.setdefault("openai_model", "gpt-4o-mini")

SAVE_DIR = "submissions"
os.makedirs(SAVE_DIR, exist_ok=True)

client = OpenAI(
    base_url="https://models.inference.ai.azure.com",
    api_key=github_token
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

def check_and_handle_conversation_end():
    """Check if conversation should end and save it if completed."""
    if st.session_state.history:
        last = st.session_state.history[-1]
        if last["role"] == "assistant" and prompts.THANK_YOU in last["content"]:
            _save_conversation()
            return True
    return False

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
        
def _save_conversation():
    """Save the full chat history to a timestamped JSON file."""
    fname = datetime.now().strftime("candidate_%Y%m%d_%H%M%S.json")
    path = os.path.join(SAVE_DIR, fname)
    with open(path, "w") as f:
        json.dump(st.session_state.history, f, indent=2)

# ─── Main Chat Interface ──────────────────────────────────────────────────────

def chat_interface():
    st.title("🤖 Hiring Assistant Bot")
    
    initialize_chat_data()
    render_history()
    
    if check_and_handle_conversation_end():
        return

    if user_input := st.chat_input("Your response…"):
        handle_user_input(user_input)

# ─── Main ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    chat_interface()
