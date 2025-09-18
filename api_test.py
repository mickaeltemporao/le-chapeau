import aiohttp
import asyncio
import json
import random
# import requests
import streamlit as st

from pathlib import Path
from prompts import assist, mentor, bad_1, bad_2, bad_doc


API_URL = "https://api.openai.com/v1/responses"
API_KEY = st.secrets["OPENAI_API_KEY"]
N = 500
OUTPUT_FILE = "simulation_results.jsonl"

student_prompts = [
    "Peux-tu m'expliquer le concept de la photosynthèse ?",
    "Comment résoudre une équation du second degré ?",
    bad_1,
    "Peux-tu résumer le chapitre sur la Révolution française ?",
    "Explique-moi la différence entre masse et poids.",
    "Comment fonctionne le moteur d'une voiture ?",
    "Peux-tu me donner un exemple d'expérience scientifique simple à la maison ?",
    bad_2,
    "Quels sont les principes de base de l’économie ?",
    bad_doc,
]

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
        with path.open("r",  encoding='utf-8-sig') as f:
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
        "input": [
            {"role": "developer", "content": PROMPT_MAP.get(group, "")},
            {"role": "user", "content": prompt},
        ],
        "metadata": {"user": user, "group": group},
    }
    # print(json.dumps(payload, indent=2, ensure_ascii=False))

    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

    # response = requests.post(API_URL, headers=headers, json=payload)
    # data = response.json()
    # data["output"][0]["content"][0]['text'].strip()

    try:
        async with session.post(API_URL, headers=headers, json=payload) as resp:
            if resp.status != 200:
                return f"{user} ({group}): ERROR {resp.status}"
            data = await resp.json()
            return f"{user} ({group}): {data["output"][0]["content"][0]['text'].strip()}"
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

    # Write results to file as JSONL
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for r in results:
            # If simulate_user returns metadata dict
            if isinstance(r, dict):
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
            else:
                # In case it returns a string or exception
                f.write(json.dumps({"raw": str(r)}) + "\n")

    print(f"✅ Results written to {OUTPUT_FILE}")

if __name__ == "__main__":
    asyncio.run(main())

