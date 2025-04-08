import os
import json
from datetime import datetime

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

import prompts

# ─── Configuration ─────────────────────────────────────────────────────────────

load_dotenv()
    
st.set_page_config(page_title="Hiring Assistant", page_icon="💼")

with st.sidebar:
    sidebar_token = st.text_input(
        label="GitHub Token (paste if not pre-configured)",
        help="Enter your GitHub token here if it's not already available in your .env file. The token from .env will be used if you leave this field empty.",
        key="github_token",
        type="password",
        placeholder="GITHUB_TOKEN"
    )
    
    st.markdown("[![Get GPT-4o Key](https://img.shields.io/badge/🔑_Get_OpenAI_GPT--4o_Key-for_free-412991?style=for-the-badge&logo=openai&logoColor=white)](https://github.com/marketplace/models/azure-openai/gpt-4o/playground)")
    st.markdown("[![Or Watch Tutorial](https://img.shields.io/badge/Or_Watch_This_Tutorial-FF0000?style=flat&logo=youtube)](https://www.youtube.com/watch?v=YP8mV_2RDLc)")
    st.markdown("[![GitHub Token Docs](https://img.shields.io/badge/GitHub_Token_Docs-181717?style=flat-square&logo=github)](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens)")
    st.markdown("")
    st.markdown("")
    st.markdown("")
    st.markdown("[![View the source code](https://img.shields.io/badge/View_the_source_code-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/5umit-chandra/AI-Hiring-Assistant-LLM-Chatbot/blob/main/app.py)")

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
    st.title("🤖 Hiring Assistant ChatBot")
    
    initialize_chat_data()
    render_history()
    
    if check_and_handle_conversation_end():
        return

    if user_input := st.chat_input("Your response…"):
        handle_user_input(user_input)

# ─── Main ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    chat_interface()
