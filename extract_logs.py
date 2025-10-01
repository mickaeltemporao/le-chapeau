import os, time, json, sys
from pathlib import Path
import requests
from requests.adapters import HTTPAdapter, Retry

# ----------------- CONFIG -----------------
OUT_INDEX = Path("logs_index.jsonl")
OUT_INDEX.parent.mkdir(exist_ok=True)
BASE = "https://api.openai.com/v1/responses"
PAGE_PARAMS = {"input_item_limit": 1, "output_item_limit": 1}
SLEEP_BETWEEN = 0.05  # polite delay between requests

# ----------------- AUTH -----------------
config_path = "env.json"
with open(config_path) as f:
    config = json.load(f)

BEARER = config.get("bearer")
ORG = config.get("org")
PROJ = config.get("proj")

if not BEARER:
    print("ERROR: set OPENAI_BEARER environment variable.")
    sys.exit(1)

HEADERS = {
    "Authorization": f"{BEARER}",
    "OpenAI-Organization": F"{ORG}",
    "OpenAI-Project": f"{PROJ}",
    "OpenAI-Beta": "responses=v1",
    "User-Agent": "Mozilla/5.0",  # not strictly needed, but fine
}


# ----------------- SESSION -----------------
sess = requests.Session()
retries = Retry(total=5, backoff_factor=1,
                status_forcelist=(429, 500, 502, 503, 504),
                allowed_methods=frozenset(["GET"]))
sess.mount("https://", HTTPAdapter(max_retries=retries))

# ----------------- HELPER -----------------
def write_line(obj):
    with OUT_INDEX.open("a", encoding="utf8") as f:
        f.write(json.dumps(obj, ensure_ascii=False) + "\n")

def get_last_saved_id():
    """Return last saved log id if file exists, else None"""
    if not OUT_INDEX.exists() or OUT_INDEX.stat().st_size == 0:
        return None
    last_id = None
    with OUT_INDEX.open("r", encoding="utf8") as f:
        for line in f:
            if not line.strip():
                continue
            try:
                obj = json.loads(line)
                last_id = obj.get("id")
            except Exception:
                continue
    return last_id

# ----------------- MAIN LOOP -----------------
def fetch_all():
    after = get_last_saved_id()
    total_saved = 0
    if after:
        print(f"Resuming from last saved id: {after}")
    else:
        print("Starting from the beginning.")

    while True:
        params = dict(PAGE_PARAMS)
        if after:
            params["after"] = after

        try:
            r = sess.get(BASE, headers=HEADERS, params=params, timeout=30)
            if r.status_code == 401:
                raise SystemExit("Unauthorized (401). Check your session token/headers.")
            r.raise_for_status()
        except Exception as e:
            print("Request failed:", e)
            print("Sleeping 5s before retry...")
            time.sleep(5)
            continue

        j = r.json()
        items = j.get("data", [])
        if not items:
            print("No items returned, stopping.")
            break

        for it in items:
            write_line(it)
            total_saved += 1

        print(f"Saved {len(items)} items this page, total {total_saved}, last_id={j['last_id']}")

        if not j.get("has_more"):
            print("All pages fetched.")
            break

        after = j["last_id"]
        time.sleep(SLEEP_BETWEEN)

# ----------------- RUN -----------------
if __name__ == "__main__":
    fetch_all()
