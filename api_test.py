import asyncio
import aiohttp
import random
from pathlib import Path
import streamlit as st

API_URL = "https://api.openai.com/v1/chat/completions"
API_KEY = st.secrets["OPENAI_API_KEY"]
N = 500

student_prompts = [
    "Peux-tu m'expliquer le concept de la photosynthèse ?",
    "Comment résoudre une équation du second degré ?",
    "Donne-moi un conseil pour mieux gérer mon temps en révisions.",
    "Peux-tu résumer le chapitre sur la Révolution française ?",
    "Comment améliorer mes compétences en programmation Python ?",
    "As-tu des astuces pour mémoriser du vocabulaire en anglais ?",
    "Explique-moi la différence entre masse et poids.",
    "Comment fonctionne le moteur d'une voiture ?",
    "Peux-tu me donner un exemple d'expérience scientifique simple à la maison ?",
    "Quels sont les principes de base de l’économie ?"
]

# Reuse your prompt groups
from prompts import assist, mentor

PROMPT_MAP = {
    "a": "",
    "b": assist,
    "c": mentor,
}

# Load your small user file
def load_users(file="users.txt"):
    users = []
    path = Path(file)
    if path.exists():
        with path.open("r") as f:
            for line in f:
                line = line.strip()
                if line:
                    user, group = line.split(",") if "," in line else (line, "a")
                    users.append((user, group))
    return users


async def simulate_user(session, user, group):
    await asyncio.sleep(random.uniform(0.1, 1.5))
    prompt = random.choice(student_prompts)
    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "developer", "content": PROMPT_MAP.get(group, "")},
            {"role": "user", "content": prompt},
        ],
        "max_tokens": 50,
    }
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

    try:
        async with session.post(API_URL, headers=headers, json=payload) as resp:
            if resp.status != 200:
                return f"{user} ({group}): ERROR {resp.status}"
            data = await resp.json()
            return f"{user} ({group}): {data['choices'][0]['message']['content'].strip()}"
    except Exception as e:
        return f"{user} ({group}): EXCEPTION {e}"


async def main():
    small_user_list = load_users()  # only 10 users
    # randomly choose 500 users with replacement
    simulated_users = [random.choice(small_user_list) for _ in range(N)]

    async with aiohttp.ClientSession() as session:
        tasks = [simulate_user(session, user, group) for user, group in simulated_users]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        for r in results:
            print(r)


if __name__ == "__main__":
    asyncio.run(main())

