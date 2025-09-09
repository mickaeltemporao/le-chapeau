import os
import random
import streamlit as st

from openai import OpenAI
from pathlib import Path
from typing import Optional, Dict, Set
from uuid import uuid4


# Session Configuration
SESSION_ID_KEY = "session_id"
USER_ID_KEY = "user_id"
GROUP_KEY = "group"
TITLE = "Le Chapeau"
# MODEL = "gpt-5-mini"
MODEL = "gpt-4o-mini"
# PASSWORD_FILE = Path("passwords.txt")
PASSWORD_FILE = Path("users.txt")
PROMPT_MAP = {
    # 'a': "Act as if you were Angela Merkel",
    # 'b': "Act as if you were Emmanuel Macron",
    # 'c': "Act as if you were Ursula von der Leyen",
    'a': """Act as if you were Super Mario.""",
    'b': """Act as if you were Batman.""",
    'c': """Act as if you were Tinker Bell.""",
}
TEXT_ID = """
            Votre identifiant correspond à la partie de votre adresse e-mail étudiante **avant le symbole @**.

            **Exemple :**
            Si votre adresse e-mail est **jeanne-marie.redon@etu.u-bordeaux.fr**,
            votre identifiant est **jeanne-marie.redon**.

            Saisissez-le dans le champ ci-dessous, puis CLIQUEZ sur le bouton **"Se connecter"**.
"""
TEXT_ID = """
            Votre identifiant correspond à la partie de votre adresse e-mail étudiante **avant le symbole @**.

            **Exemple :**
            Si votre adresse e-mail est **jeanne-marie.redon@scpobx.fr**,
            votre identifiant est **jeanne-marie.redon**.

            Saisissez-le dans le champ ci-dessous, puis CLIQUEZ sur le bouton **"Se connecter"**.
"""




def load_passwords_and_groups() -> Dict[str, str]:
    """Load passwords and their groups from file into a dictionary."""
    passwords = {}
    if PASSWORD_FILE.exists():
        with PASSWORD_FILE.open('r') as pass_file:
            for line in pass_file:
                line = line.strip()
                if line:
                    password, group = line.split(',') if ',' in line else (line, None)
                    passwords[password] = group
    return passwords


# Load passwords and groups at startup
PASSWORDS: Dict[str, str] = load_passwords_and_groups()
VALID_PASSWORDS: Set[str] = set(PASSWORDS.keys())


def get_prompt_for_group(group: str, default=None):
    return PROMPT_MAP.get(group, default)


def clean_input(user_name):
    return user_name.strip().lower()


def get_group(password: str) -> Optional[str]:
    """Get the group for a user (already loaded in PASSWORDS)."""
    return PASSWORDS.get(password)


def check_password(word):
    """Check if password is valid (in-memory)."""
    return word in VALID_PASSWORDS


def stream_text(stream):
    for event in stream:
        if event.type == "response.completed":
            st.session_state["last_response_id"] = event.response.id
        elif event.type == "response.output_text.delta":
            yield event.delta


def get_response(user, user_input, group, client):
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
                },
            ],
            stream=True,
            previous_response_id=st.session_state["last_response_id"],
            metadata={"user": user, "group": group},
        ) as stream:
            response = st.write_stream(
                stream_text(stream)
            )

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})


def main():

    st.set_page_config(
        page_title=f"{TITLE}",
        page_icon="🎓"
    )

    st.title(f"🎓 {TITLE}")

    # Initialize session state
    if not st.session_state.get(SESSION_ID_KEY):
        st.session_state[SESSION_ID_KEY] = str(uuid4())
        st.session_state[GROUP_KEY] = None

    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        st.header("🔐 Identification")

        st.write(TEXT_ID)

        input_password = st.text_input("Entrez votre identifiant", type="password")
        # st.write(f"Utilisez un des noms suivants: {', '.join(PASSWORDS.keys())}.")
        authenticate_button = st.button("Se connecter")

        if authenticate_button:
            username = clean_input(input_password)
            if check_password(username):
                st.session_state.authenticated = True
                st.session_state[USER_ID_KEY] = username
                st.session_state[GROUP_KEY] = get_group(username)
                st.success(f"Authentification réussie !")
                st.rerun()
            else:
                st.error("Veuillez entrer votre identifiant.")
        return

    st.success(
        # f"Bonjour {st.session_state[USER_ID_KEY].title()}, Tu es dans le groupe '{st.session_state[GROUP_KEY].upper()}'."
        # f"Bonjour {st.session_state[USER_ID_KEY].title()}, tu es dans le groupe '{st.session_state[GROUP_KEY].upper()}'."
        f"Bonjour {st.session_state[USER_ID_KEY].title()}."
    )
    st.write("Bienvenue dans blabla 🚗 et non ce n'est pas une voiture... Bref c'est de blabla.")
    # st.write("You use the chat interface below to ask me a question?")
    st.caption("Utilisez la boîte de dialogue en bas de page pour interagir avec cet outil.")

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

    if prompt := st.chat_input(
        "Enter you request here...",
    ):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.spinner("Thinking..."):
            get_response(
                st.session_state[USER_ID_KEY],
                prompt,
                st.session_state[GROUP_KEY],
                client
            )

if __name__ == "__main__":
    main()
