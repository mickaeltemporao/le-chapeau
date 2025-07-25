import streamlit as st
from pathlib import Path
from typing import Dict, Optional, List
import json
import os
import random
from datetime import datetime
from pydantic import BaseModel, Field
from uuid import uuid4

# Setup logging
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Pydantic model for session storage
class ChatSession(BaseModel):
    session_id: str
    password: str
    group: str
    prompts: List[str]
    responses: List[str]
    timestamp: datetime = Field(default_factory=datetime.now)


# Session state keys
SESSION_ID_KEY = "session_id"
PASSWORD_KEY = "password"
GROUP_KEY = "group"
PROMPTS_KEY = "prompts"
RESPONSES_KEY = "responses"
SESSION_DIR = "chat_sessions"

# Configuration
PASSWORD_FILE = Path("passwords.txt")
DATA_DIR = Path("data")
os.makedirs(SESSION_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)


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


def mock_chatgpt_api(prompt: str) -> str:
    """Simulate a ChatGPT API response."""
    logger.info(f"Mock ChatGPT API called with prompt: {prompt}")
    return f"Mock response for: '{prompt}'"


def save_session(session: ChatSession) -> None:
    """Save session data to file."""
    file_path = os.path.join(SESSION_DIR, f"{session.session_id}.json")
    with open(file_path, "w") as f:
        json.dump(session.dict(), f, indent=4)
    logger.info(f"Session saved for {session.session_id}")


def load_session(session_id: str) -> Optional[ChatSession]:
    """Load session data from file."""
    file_path = os.path.join(SESSION_DIR, f"{session_id}.json")
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            data = json.load(f)
            return ChatSession(**data)
    return None


def modify_prompt(prompt: str) -> str:
    """Modify prompt for test group."""
    return f"Please act with empathy. User's question: {prompt}"


def main():
    st.set_page_config(
        page_title="ChatGPT Experiment Interface",
        page_icon="🤖"
    )

    st.title("🤖 ChatGPT Experiment Interface")
    # Initialize session state
    if not st.session_state.get(SESSION_ID_KEY):
        st.session_state[SESSION_ID_KEY] = str(uuid4())
        st.session_state[PASSWORD_KEY] = None
        st.session_state[GROUP_KEY] = None
        st.session_state[PROMPTS_KEY] = []
        st.session_state[RESPONSES_KEY] = []

    session_id = st.session_state[SESSION_ID_KEY]
    group = st.session_state[GROUP_KEY]
    prompts = st.session_state[PROMPTS_KEY]
    responses = st.session_state[RESPONSES_KEY]
    password = st.session_state[PASSWORD_KEY]

    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        st.header("🔐 Authentication")
        input_password = st.text_input("Enter your password:", type="password")
        authenticate_button = st.button("Authenticate")

        if authenticate_button:
            if check_password(input_password):
                path, group = get_group(input_password)
                # Load previous session if exists
                session_data = load_session(session_id)
                if session_data:
                    prompts = session_data.prompts
                    responses = session_data.responses
                else:
                    prompts = []
                    responses = []
                # Update session state
                st.session_state.authenticated = True
                st.session_state[PASSWORD_KEY] = input_password
                st.session_state[GROUP_KEY] = group
                st.session_state[PROMPTS_KEY] = prompts
                st.session_state[RESPONSES_KEY] = responses
                st.success(f"Authentication successful! You are in the '{group}' group.")
                st.rerun()
            else:
                st.error("Please enter a password.")
        return

    st.success(f"Welcome back! You are in the '{group}' group. Session ID: {session_id}")

    # Display chat history
    st.subheader("Chat History")
    for i in range(len(prompts)):
        st.markdown(f"**You:** {prompts[i]}")
        st.markdown(f"**Assistant:** {responses[i]}")
        st.markdown("---")

    # Chat interface
    user_input = st.text_input("Enter your prompt:", key="user_input")
    send_button = st.button("Send")

    if send_button and user_input:
        if group == "test":
            modified_prompt = modify_prompt(user_input)
        else:
            modified_prompt = user_input

        response = mock_chatgpt_api(modified_prompt)

        prompts.append(user_input)
        responses.append(response)

        st.session_state[PROMPTS_KEY] = prompts
        st.session_state[RESPONSES_KEY] = responses

    # Save and exit
    if st.button("Save and Exit"):
        session_data = ChatSession(
            session_id=session_id,
            password=st.session_state[PASSWORD_KEY],
            group=group,
            prompts=prompts,
            responses=responses,
            timestamp=datetime.now(),
        )
        save_session(session_data)
        st.success("Session saved. Thank you for participating!")
        st.session_state.authenticated = False
        st.rerun()

if __name__ == "__main__":
    main()

