import os
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

import prompts

load_dotenv()

st.set_page_config(page_title="Hiring Assistant", page_icon="💼")

if "openai_model" not in st.session_state:
    st.session_state.openai_model = "gpt-4o-mini"

client = OpenAI(
    base_url=os.getenv("OPENAI_API_BASE_URL"),
    api_key=os.getenv("GITHUB_TOKEN")
)


# ─── Chat Interface ────────────────────────────────────────────────────────────

def chat_interface():
    st.title("🤖 Hiring Assistant Bot")

    if "history" not in st.session_state:
        st.session_state.history = [
            {"role": "assistant", "content": prompts.GREETING}
        ]
    if "system_message" not in st.session_state:
        st.session_state.system_message = {
            "role": "system",
            "content": prompts.SYSTEM_PROMPT
        }

    for msg in st.session_state.history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    last = st.session_state.history[-1]
    if last["role"] == "assistant" and prompts.THANK_YOU in last["content"]:
        _save_conversation()
        return

    if user_input := st.chat_input("Your response…"):
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

        st.session_state.history.append({
            "role": "assistant",
            "content": assistant_reply
        })

# ─── Main ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    chat_interface()
