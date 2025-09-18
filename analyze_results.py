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

def analyze(df: pd.DataFrame):
    print("===== Basic Info =====")
    print(df.info())
    print("\nFirst few rows:")
    print(df.head(), "\n")

    # Latency stats
    if "latency" in df.columns:
        print("===== Latency (seconds) =====")
        print(df["latency"].describe(), "\n")

    # Error analysis
    if "error" in df.columns:
        errors = df["error"].dropna()
        if not errors.empty:
            print("===== Errors =====")
            print(errors.value_counts().head(10), "\n")

    # Status code distribution
    if "status" in df.columns:
        print("===== Status Codes =====")
        print(df["status"].value_counts(), "\n")

    # Group-level analysis
    if "group" in df.columns and "latency" in df.columns:
        print("===== Average Latency by Group =====")
        print(df.groupby("group")["latency"].mean(), "\n")

    # Response lengths (as proxy for richness)
    if "response" in df.columns:
        df["response_length"] = df["response"].dropna().apply(len)
        print("===== Response Length (characters) =====")
        print(df["response_length"].describe(), "\n")

if __name__ == "__main__":
    df = load_results()
    if df.empty:
        print("No results loaded. Did you run the simulation?")
    else:
        analyze(df)
