import streamlit as st
from typing import Dict, List, Optional, Tuple
import random
import json
import logging
from datetime import datetime
from pydantic import BaseModel, Field
import os
import uuid

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Mock ChatGPT API (You can replace with actual API call)
def mock_chatgpt_api(prompt: str) -> str:
    """Simulate a ChatGPT API response."""
    logger.info(f"Mock ChatGPT API called with prompt: {prompt}")
    return f"Mock response for: '{prompt}'"

# Pydantic models for data storage
class ChatSession(BaseModel):
    session_id: str
    group: str
    prompts: List[str]
    responses: List[str]
    timestamp: datetime = Field(default_factory=datetime.now)

class UserSessionData(BaseModel):
    session_id: str
    group: str
    prompts: List[str]
    responses: List[str]
    timestamp: datetime

# Session state keys
SESSION_ID_KEY = "session_id"
GROUP_KEY = "group"
PROMPTS_KEY = "prompts"
RESPONSES_KEY = "responses"

# Configuration
PASSCODE = "secret123"
OUTPUT_DIR = "chat_sessions"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def authenticate_user(passcode: str) -> bool:
    """Validate user passcode."""
    return passcode == PASSCODE

def assign_group() -> str:
    """Randomly assign the user to 'control' or 'test' group."""
    return random.choice(["control", "test"])

def save_session(session_data: UserSessionData) -> None:
    """Save user session data to a JSON file."""
    file_path = os.path.join(OUTPUT_DIR, f"{session_data.session_id}.json")
    with open(file_path, "w") as f:
        json.dump(session_data.dict(), f, indent=4)
    logger.info(f"Saved session data for {session_data.session_id} in {file_path}")

def load_session(session_id: str) -> Optional[UserSessionData]:
    """Load a previous session if it exists."""
    file_path = os.path.join(OUTPUT_DIR, f"{session_id}.json")
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            data = json.load(f)
            return UserSessionData(**data)
    return None

def initialize_session() -> None:
    """Initialize session state for a new user."""
    session_id = str(uuid.uuid4())
    group = assign_group()
    st.session_state[SESSION_ID_KEY] = session_id
    st.session_state[GROUP_KEY] = group
    st.session_state[PROMPTS_KEY] = []
    st.session_state[RESPONSES_KEY] = []
    logger.info(f"New session initialized for {session_id} in {group} group")

def get_modified_prompt(prompt: str) -> str:
    """Return modified prompt for test group."""
    return f"Please act as an assistant with empathy. User's question: {prompt}"

def main():
    st.set_page_config(page_title="ChatGPT Experiment Interface", page_icon="🤖")

    # Initialize session state
    if not st.session_state.get(SESSION_ID_KEY):
        initialize_session()

    session_id = st.session_state[SESSION_ID_KEY]
    group = st.session_state[GROUP_KEY]
    prompts = st.session_state[PROMPTS_KEY]
    responses = st.session_state[RESPONSES_KEY]

    st.title("🤖 ChatGPT Experiment Interface")

    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        st.header("🔐 Authentication")
        passcode = st.text_input("Enter passcode:", type="password")
        authenticate_button = st.button("Authenticate")

        if authenticate_button:
            if authenticate_user(passcode):
                st.session_state.authenticated = True
                st.success("Authentication successful!")
                st.rerun()
            else:
                st.error("Incorrect passcode. Please try again.")
        return

    st.success(f"Welcome! You are in the '{group}' group. Session ID: {session_id}")

    # Chat interface
    user_input = st.text_input("Enter your prompt:", key="user_input")
    send_button = st.button("Send")

    if send_button and user_input:
        if group == "test":
            modified_prompt = get_modified_prompt(user_input)
        else:
            modified_prompt = user_input

        response = mock_chatgpt_api(modified_prompt)

        prompts.append(user_input)
        responses.append(response)

        st.session_state[PROMPTS_KEY] = prompts
        st.session_state[RESPONSES_KEY] = responses

    # Display chat history
    st.subheader("📜 Chat History")
    for i in range(len(prompts)):
        st.markdown(f"**You:** {prompts[i]}")
        st.markdown(f"**Assistant:** {responses[i]}")
        st.markdown("---")

    # Save session and exit
    if st.button("Save and Exit"):
        session_data = UserSessionData(
            session_id=session_id,
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
