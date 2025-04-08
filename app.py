import os
import json
from datetime import datetime

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

import prompts  # Local module for greeting, system prompts, and thank you messages

# ─── Environment & UI Configuration ───────────────────────────────────────────

load_dotenv()  # Load environment variables (e.g., fallback GitHub token)

# Set the page title and icon for the Streamlit app
st.set_page_config(page_title="Hiring Assistant", page_icon="💼")

# If the GitHub token is not set in the environment variables, prompt the user to enter it in the sidebar.
with st.sidebar:
    # Request GitHub token input if not preset (hidden text input)
    sidebar_token = st.text_input(
        label="GitHub Token (paste if not pre-configured)",
        help="Enter your GitHub token here if not available in your .env file.",
        key="github_token",
        type="password",
        placeholder="GITHUB_TOKEN"
    )

    # display helpful resource links for getting the github token and source code
    st.markdown("[![Get GPT-4o Key](https://img.shields.io/badge/🔑_Get_OpenAI_GPT--4o_Key-for_free-412991?style=for-the-badge&logo=openai&logoColor=white)](https://github.com/marketplace/models/azure-openai/gpt-4o/playground)")
    st.markdown("[![Or Watch Tutorial](https://img.shields.io/badge/Or_Watch_This_Tutorial-FF0000?style=flat&logo=youtube)](https://www.youtube.com/watch?v=YP8mV_2RDLc)")
    st.markdown("[![GitHub Token Docs](https://img.shields.io/badge/GitHub_Token_Docs-181717?style=flat-square&logo=github)](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens)")
    st.markdown("\n\n")
    st.markdown("[![View the source code](https://img.shields.io/badge/View_the_source_code-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/5umit-chandra/AI-Hiring-Assistant-LLM-Chatbot/blob/main/app.py)")

# Use sidebar token or fallback to the environment
github_token = sidebar_token or os.getenv("GITHUB_TOKEN")
if not github_token:
    st.warning("Please paste your GitHub token in the sidebar.")

# Ensure the submissions directory exists for saving conversations
SAVE_DIR = "submissions"
os.makedirs(SAVE_DIR, exist_ok=True)

# Use session state to set default AI model if not already set
st.session_state.setdefault("openai_model", "gpt-4o-mini")

# Initialize OpenAI client with the fixed base URL and selected token
client = OpenAI(
    base_url="https://models.inference.ai.azure.com",
    api_key=github_token
)

# ─── Chat Interface Components ──────────────────────────────────────────────

def initialize_chat_data():
    """
    Initialize session state:
    - Create chat history with the initial greeting.
    - Set the system prompt for conversation context.
    """
    if "history" not in st.session_state:
        st.session_state.history = [{"role": "assistant", "content": prompts.GREETING}]
    if "system_message" not in st.session_state:
        st.session_state.system_message = {
            "role": "system",
            "content": prompts.SYSTEM_PROMPT
        }


def render_history():
    """Render chat history in the Streamlit UI."""
    for msg in st.session_state.history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])


def check_and_handle_conversation_end():
    """
    If the last message from the assistant indicates the conversation should end,
    save the conversation and return True.
    """
    if st.session_state.history:
        last = st.session_state.history[-1]
        if last["role"] == "assistant" and prompts.THANK_YOU in last["content"]:
            _save_conversation()
            return True
    return False


def handle_user_input(user_input):
    """
    Append user input to history, generate and display the assistant's streamed response,
    and then update chat history.
    """
    # Record user message in the UI and session state
    st.session_state.history.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Compose messages for API: system prompt plus full chat history
    messages_for_api = [st.session_state.system_message] + st.session_state.history

    # Stream and display assistant's response
    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state.openai_model,
            messages=messages_for_api,
            temperature=0.7,
            stream=True
        )
        assistant_reply = st.write_stream(stream)

    # Save assistant reply to chat history
    st.session_state.history.append({
        "role": "assistant",
        "content": assistant_reply
    })

# ─── Save Conversation Functionality ──────────────────────────────────────

def _save_conversation():
    fname = datetime.now().strftime("candidate_%Y%m%d_%H%M%S.json")
    path = os.path.join(SAVE_DIR, fname)
    with open(path, "w") as f:
        json.dump(st.session_state.history, f, indent=2)


# ─── Main Chat Interface Controller ───────────────────────────────────────────

def chat_interface():
    """
    Main controller for the chat interface:
    - Display title, initialize data, render history.
    - Handle conversation termination and process user input.
    """
    st.title("🤖 Hiring Assistant Bot")
    
    initialize_chat_data()
    render_history()
    
    if check_and_handle_conversation_end():
        return

    # Process new user input via chat input widget
    if user_input := st.chat_input("Your response…"):
        handle_user_input(user_input)


# ─── App Entry Point ──────────────────────────────────────────────────────────

# This is the entry point of the Streamlit app.
if __name__ == "__main__":
    chat_interface()
