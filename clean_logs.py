import json
from pathlib import Path

INDEX_FILE = Path("logs_index.jsonl")
TEMP_FILE = Path("logs_index_cleaned.jsonl")

seen_ids = set()
total_in = 0
total_out = 0

with INDEX_FILE.open("r", encoding="utf8") as f_in, TEMP_FILE.open("w", encoding="utf8") as f_out:
    for line in f_in:
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue  # skip bad lines
        rid = obj.get("id")
        if not rid:
            continue
        total_in += 1
        if rid not in seen_ids:
            seen_ids.add(rid)
            f_out.write(json.dumps(obj, ensure_ascii=False) + "\n")
            total_out += 1

print(f"Total lines read: {total_in}")
print(f"Total lines after dedup: {total_out}")
print(f"Duplicates removed: {total_in - total_out}")

# Optional: replace original file
INDEX_FILE.unlink()        # delete old file
TEMP_FILE.rename(INDEX_FILE)  # rename cleaned file
print("Deduplicated index saved.")
