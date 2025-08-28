import os
import random
import streamlit as st
import time

from openai import OpenAI
from pathlib import Path
from typing import Optional
from uuid import uuid4


# Session state keys
SESSION_ID_KEY = "session_id"
PASSWORD_KEY = "password"
GROUP_KEY = "group"
PROMPTS_KEY = "prompts"
RESPONSES_KEY = "responses"
SESSION_DIR = "chat_sessions"
TITLE = "Interface Prototype - LLM"
MODEL = "gpt-4o-mini"

# Configuration
PASSWORD_FILE = Path("passwords.txt")
DATA_DIR = Path("data")
os.makedirs(SESSION_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)

dev_prompt_A = """Act as if you were Super Mario!"""
dev_prompt_B = """Act as if you were Batman!"""
dev_prompt_C = """You are an historian."""

def check_password(word):
    """Check if password is valid."""
    with PASSWORD_FILE.open('r') as pass_file:
        contents = pass_file.read().splitlines()
    if word in contents:
        return word
    else:
        return False


def get_group(password: str) -> Optional[str]:
    """Get or assign the group for a user."""
    folders = [f for f in DATA_DIR.iterdir() if f.is_dir()]
    users = [f.name.rsplit('_', 1)[0] for f in folders]
    pattern = f"{password}_*"
    if password in users:
        path = [f for f in DATA_DIR.glob(pattern) if f.is_dir()][0]
    else:
        group = random.choice(["control", "test"])
        path = Path(DATA_DIR) / f"{password}_{group}"
        path.mkdir(parents=True, exist_ok=True)
    return path, path.name.split("_")[-1]


def modify_prompt(prompt: str) -> str:
    """Modify prompt for test group."""
    return f"Please act with empathy. User's question: {prompt}"

def get_help(user_prompt: str, dev_prompt: str, client, MODEL):
    response = client.responses.create(
        model=MODEL,
        # reasoning={"effort": "low"},
        input=[
            {
                "role": "developer",
                "content": dev_prompt,
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": user_prompt,
                    },
                ]
            }
        ]
    )
    return response

def stream_text(stream):
    for event in stream:
        if event.type == "response.created":
            st.session_state["last_response_id"] = event.response.id
        elif event.type == "response.output_text.delta":
            yield event.delta

def main():

    from openai import OpenAI
    import streamlit as st

    st.set_page_config(page_title=f"{TITLE}", page_icon="🤖")
    st.title(f"🤖 {TITLE}")

    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = MODEL

    if "last_response_id" not in st.session_state:
        st.session_state["last_response_id"] = None

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Comment puis-je t'aider?"}
        ]

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Entrez votre requête ici..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            with client.responses.create(
                # model=st.session_state["openai_model"],
                model=st.session_state["openai_model"] = MODEL
,
                # reasoning={"effort": "low"},
                input=[
                    {
                        "role": "developer",
                        "content": dev_prompt_C,
                    },
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "input_text",
                                "text": prompt,
                            },
                        ]
                    }
                ],
                stream=True,
                previous_response_id=st.session_state["last_response_id"],
            ) as stream:
                response = st.write_stream(
                    stream_text(stream)
                )

        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()
