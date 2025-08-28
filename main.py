import os
import random
import streamlit as st
import time

from openai import OpenAI
from pathlib import Path
from typing import Optional
from uuid import uuid4


# Session Configuration
SESSION_ID_KEY = "session_id"
USER_ID_KEY = "user_id"
GROUP_KEY = "group"
SESSION_DIR = "chat_sessions"
TITLE = "Interface Prototype - LLM"
MODEL = "gpt-4o-mini"
PASSWORD_FILE = Path("passwords.txt")
DATA_DIR = Path("data")

PROMPT_MAP = {
    'a': """Act as if you were Super Mario.""",
    'b': """Act as if you were Batman.""",
    'c': """Act as a Emmanuel Macron.""",
}

os.makedirs(SESSION_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)


def get_prompt_for_group(group: str, default=None):
    return PROMPT_MAP.get(group, default)


def clean_input(user_name):
    return user_name.strip().lower()


def get_group(password: str) -> Optional[str]:
    """Get or assign the group for a user."""
    folders = [f for f in DATA_DIR.iterdir() if f.is_dir()]
    users = [f.name.rsplit('_', 1)[0] for f in folders]
    pattern = f"{password}_*"
    if password in users:
        path = [f for f in DATA_DIR.glob(pattern) if f.is_dir()][0]
    else:
        group = random.choice(PROMPT_MAP.keys())
        path = Path(DATA_DIR) / f"{password}_{group}"
        path.mkdir(parents=True, exist_ok=True)
    return path.name.split("_")[-1]


def check_password(word):
    """Check if password is valid."""
    with PASSWORD_FILE.open('r') as pass_file:
        contents = pass_file.read().splitlines()
    if word in contents:
        return word
    else:
        return False


def stream_text(stream):
    for event in stream:
        if event.type == "response.created":
            st.session_state["last_response_id"] = event.response.id
        elif event.type == "response.output_text.delta":
            yield event.delta


def get_response(user_input, group, client):
    dev_prompt = get_prompt_for_group(group)
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        with client.responses.create(
            model=st.session_state["openai_model"],
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
                            "text": user_input,
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


def main():

    st.set_page_config(
        page_title=f"{TITLE}",
        page_icon="🤖"
    )

    st.title(f"🤖 {TITLE}")

    # Initialize session state
    if not st.session_state.get(SESSION_ID_KEY):
        st.session_state[SESSION_ID_KEY] = str(uuid4())
        st.session_state[GROUP_KEY] = None

    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        st.header("🔐 Authentication")
        input_password = st.text_input("Enter your password:", type="password")
        authenticate_button = st.button("Authenticate")

        if authenticate_button:
            username = clean_input(input_password)
            if check_password(username):
                st.session_state.authenticated = True
                st.session_state[USER_ID_KEY] = username
                st.session_state[GROUP_KEY] = get_group(username)
                st.success(f"Authentication successful!")
                st.rerun()
            else:
                st.error("Please enter a password.")
        return

    st.success(
        f"Bonjour {st.session_state[USER_ID_KEY]}, Tu es dans le groupe '{st.session_state[GROUP_KEY]}'!."
    )
    st.write("Bienvenue dans blabla 🚗 et non ce n'est pas une voiture... Bref beaucoup de blabla.")
    st.caption("Et surtout ... encore du blabla.")

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

        get_response(prompt, st.session_state[GROUP_KEY], client)

if __name__ == "__main__":
    main()
