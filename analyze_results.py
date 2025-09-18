import json
import pandas as pd
from collections import Counter

RESULTS_FILE = "simulation_results.jsonl"

def load_results(file_path=RESULTS_FILE):
    """Load JSONL results into a pandas DataFrame."""
    rows = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:
                pass
    return pd.DataFrame(rows)

def analyze(df):
    df['error'] = df['text'].str.contains("ERROR", case=False, na=False)
    df["type"] = df[df['error']==True]['text'].str.extract(r'ERROR\s*(.*)')[0]
    error_counts = df['type'].value_counts()
    error_counts
    # Count occurrences per group
    group_counts = df[df['error']]['group'].value_counts()
    print("Total Errors:", df['error'].sum())
    print("\nError Counts:", error_counts)
    print("\nGroup Counts:", group_counts)

if __name__ == "__main__":
    df = load_results()
    df[["user", "group", "text"]] = df["raw"].str.extract(r'^(.*?) \((.*?)\):\s*(.*)$')
    if df.empty:
        print("No results loaded. Did you run the simulation?")
    else:
        print(analyze(df))


