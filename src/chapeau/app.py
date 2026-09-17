"""Streamlit Web Application for Le Chapeau Educational AI Experiments."""

import os
from pathlib import Path
from uuid import uuid4

import streamlit as st
from openai import OpenAI

from chapeau.auth import StudyAuth, clean_user_identifier
from chapeau.logger import log_interaction
from chapeau.prompts import get_prompt_for_group

SESSION_ID_KEY = "session_id"
USER_ID_KEY = "user_id"
GROUP_KEY = "group"
TITLE = "Le Chapeau"
DEFAULT_MODEL = os.getenv("CHAPEAU_MODEL", "gpt-4o-mini")

TEXT_ID = """
1. Votre identifiant est votre adresse e-mail étudiante de l'**Université de Bordeaux** (ou votre identifiant d'expérience).
2. Appuyez sur Entrée ⏎ pour valider.
"""

TEXT_ID2 = """
**Exemple :**
- identifiant = **prenom.nom@etu.u-bordeaux.fr**
"""


def get_openai_api_key() -> str:
    """Retrieve OpenAI API key from Streamlit secrets or environment variables."""
    if "OPENAI_API_KEY" in st.secrets:
        return st.secrets["OPENAI_API_KEY"]
    env_key = os.getenv("OPENAI_API_KEY")
    if env_key:
        return env_key
    return ""


def stream_text(stream):
    """Yield text chunks from OpenAI Responses API stream."""
    for event in stream:
        if event.type == "response.completed":
            st.session_state["last_response_id"] = event.response.id
        elif event.type == "response.output_text.delta":
            yield event.delta


def generate_response(user: str, user_input: str, group: str, client: OpenAI) -> None:
    """Generate assistant response, display stream in chat container, and log to disk."""
    dev_prompt = get_prompt_for_group(group)

    with st.chat_message("assistant"):
        try:
            with client.responses.create(
                model=st.session_state["openai_model"],
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
                        ],
                    },
                ],
                stream=True,
                previous_response_id=st.session_state.get("last_response_id"),
                metadata={"user": user, "group": group},
            ) as stream:
                full_response = st.write_stream(stream_text(stream))

        except Exception as e:
            # Fallback to standard chat completions if responses endpoint fails
            try:
                messages = []
                if dev_prompt:
                    messages.append({"role": "system", "content": dev_prompt})
                for m in st.session_state.messages:
                    messages.append({"role": m["role"], "content": m["content"]})
                messages.append({"role": "user", "content": user_input})

                completion = client.chat.completions.create(
                    model=st.session_state["openai_model"],
                    messages=messages,
                    stream=True,
                )
                full_response = st.write_stream(chunk.choices[0].delta.content or "" for chunk in completion)
            except Exception as inner_e:
                st.error(f"Erreur de communication avec l'IA: {inner_e}")
                return

    # Add assistant response to in-memory chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})

    # Real-time local disk persistence: guarantees no data loss
    log_interaction(
        session_id=st.session_state[SESSION_ID_KEY],
        user_id=user,
        group=group,
        prompt=user_input,
        response=full_response,
        response_id=st.session_state.get("last_response_id"),
        model=st.session_state["openai_model"],
    )


def main():
    st.set_page_config(
        page_title=f"{TITLE}",
        page_icon="🎓",
        layout="centered",
    )

    st.title(f"🎓 {TITLE}")
    st.caption("Plateforme d'expérimentation pédagogique")
    st.warning(
        "Cet outil est expérimental. En cas de blocage, vous pouvez relancer votre requête ou rafraîchir la page.",
        icon="⚠️",
    )

    # Initialize session state
    if SESSION_ID_KEY not in st.session_state:
        st.session_state[SESSION_ID_KEY] = str(uuid4())
        st.session_state[GROUP_KEY] = None

    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    auth_manager = StudyAuth()

    # Participant login gate
    if not st.session_state.authenticated:
        st.header("🔐 Identification")
        st.write(TEXT_ID)

        input_id = st.text_input("Entrez votre identifiant :")
        st.write(TEXT_ID2)

        if input_id:
            clean_id = clean_user_identifier(input_id)
            is_valid, group = auth_manager.authenticate(clean_id)

            if is_valid and group:
                st.session_state.authenticated = True
                st.session_state[USER_ID_KEY] = clean_id
                st.session_state[GROUP_KEY] = group
                st.success("Authentification réussie !")
                st.rerun()
            else:
                st.error(
                    "Identifiant non reconnu. Veuillez vérifier l'orthographe ou contacter l'enseignant/chercheur."
                )
        return

    # User is authenticated
    st.success("Vous êtes connecté(e). Utilisez la boîte de dialogue en bas de page pour vos échanges.")

    api_key = get_openai_api_key()
    if not api_key:
        st.error(
            "Clé API OpenAI manquante. Veuillez configurer OPENAI_API_KEY dans les variables d'environnement ou .streamlit/secrets.toml."
        )
        return

    client = OpenAI(api_key=api_key)

    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = DEFAULT_MODEL

    if "last_response_id" not in st.session_state:
        st.session_state["last_response_id"] = None

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Bonjour ! Comment puis-je t'aider aujourd'hui ?"}
        ]

    # Render previous conversation history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Handle incoming user prompt
    if prompt := st.chat_input("Entrez votre demande ici..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.spinner("Je réfléchis, un instant..."):
            generate_response(
                user=st.session_state[USER_ID_KEY],
                user_input=prompt,
                group=st.session_state[GROUP_KEY],
                client=client,
            )


if __name__ == "__main__":
    main()
