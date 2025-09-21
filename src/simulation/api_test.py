import argparse
import aiohttp
import asyncio
import json
import random
# import requests
import streamlit as st

from datetime import datetime
from pathlib import Path
from prompts import assist, mentor, bad_1, bad_2, bad_doc

# 1️⃣ Set up the argument parser
parser = argparse.ArgumentParser(description="Enter Number of requests.")
parser.add_argument(
    "N",                     # The name of the argument
    type=int,                 # Convert input to integer
    help="An integer value for N"
)

# 2️⃣ Parse the arguments
args = parser.parse_args()

MODEL = "gpt-5-mini-2025-08-07"
API_URL = "https://api.openai.com/v1/responses"
API_KEY = st.secrets["OPENAI_API_KEY"]
OUTPUT_FILE = f"simulation_results_{datetime.now().strftime("%Y%m%d_%H%M%S")}.jsonl"
N = args.N


student_prompts = [
"Peux-tu résumer ce texte de Robert Badinter sur la peine de mort en 5 phrases claires ?/n" + bad_1,
"Quels sont les arguments principaux que Badinter utilise contre la peine de mort ?/n" + bad_2,
"Peux-tu identifier la thèse défendue par Badinter et la formuler simplement ?/n" + bad_doc,
"Quels exemples ou références historiques Badinter utilise-t-il dans son discours ?/n" + bad_1,
"Reformule ce passage difficile en termes plus simples pour que je sois sûr de le comprendre./n" + bad_2,
"Quels procédés rhétoriques (émotion, raison, morale) Badinter emploie-t-il dans son texte ?/n" + bad_doc,
"Peux-tu me donner un plan en deux ou trois parties pour résumer ce texte efficacement ?/n" + bad_1,
"Quelle est la conclusion de Badinter et comment la relie-t-il à son argumentation ?/n" + bad_2,
"Si je devais présenter ce texte à l’oral en 2 minutes, comment pourrais-je structurer mon résumé ?/n" + bad_doc,
"Quelles sont les phrases clés à retenir de ce discours pour comprendre son message ?/n" + bad_1,
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
    await asyncio.sleep(random.uniform(0.25, 5))
    prompt = random.choice(student_prompts)
    payload = {
        "model":MODEL,
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
            return user, group, 1, data
    except Exception as e:
        return user, group, 0, e


async def main():
    small_user_list = load_users()  # only 10 users
    # randomly choose 500 users with replacement
    simulated_users = [random.choice(small_user_list) for _ in range(N)]

    async with aiohttp.ClientSession() as session:
        tasks = [simulate_user(session, user, group) for user, group in simulated_users]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        # for r in results:
        #     print(r)

    # Write results to file as JSONL
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for r in results:
            f.write(json.dumps({"raw": str(r)}) + "\n")

    print(f"✅ Results written to {OUTPUT_FILE}")

if __name__ == "__main__":
    asyncio.run(main())

