import json
import re
from pathlib import Path
from typing import List, Dict

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from tqdm import tqdm
import nltk
from nltk.tokenize import word_tokenize

nltk.download("punkt")
nltk.download('punkt_tab')

########################################
# 1. Loading and cleaning
########################################

def load_jsonl(filepath: Path) -> List[Dict]:
    """
    Load a JSONL file line by line.
    Malformed lines are skipped but logged.
    """
    rows = []
    with open(filepath, "r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:
                print(f"Skipping malformed line {i}")
    return rows


def extract_text(blocks: List[Dict]) -> str:
    """
    Extract and concatenate text fields from nested content blocks.
    """
    texts = []
    if not isinstance(blocks, list):
        return ""
    for block in blocks:
        for content in block.get("content", []):
            if content.get("type") in {"input_text", "output_text"}:
                texts.append(content.get("text", ""))
    return " ".join(texts).strip()


def normalize_rows(raw_rows: List[Dict]) -> pd.DataFrame:
    """
    Flatten JSON rows into a tabular DataFrame.
    """
    records = []

    for row in raw_rows:
        try:
            record = {
                "timestamp": row.get("created_at"),
                "user_id": row.get("metadata", {}).get("user"),
                "prompt": extract_text(row.get("input")),
                "response": extract_text(row.get("output")),
                "input_tokens": row.get("usage", {}).get("input_tokens"),
                "output_tokens": row.get("usage", {}).get("output_tokens"),
                "total_tokens": row.get("usage", {}).get("total_tokens"),
            }
            records.append(record)
        except Exception:
            continue

    df = pd.DataFrame(records)
    df = df.dropna(subset=["user_id", "prompt"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s", errors="coerce")
    return df


########################################
# 2. User-level descriptive statistics
########################################

def user_level_stats(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute per-user usage statistics.
    """
    agg = df.groupby("user_id").agg(
        n_requests=("prompt", "count"),
        total_input_tokens=("input_tokens", "sum"),
        avg_input_tokens=("input_tokens", "mean"),
        total_output_tokens=("output_tokens", "sum"),
        avg_output_tokens=("output_tokens", "mean"),
    )
    return agg.sort_values("n_requests", ascending=False)


########################################
# 3. Session-level metrics
########################################

def add_sessions(df: pd.DataFrame, gap_minutes: int = 30) -> pd.DataFrame:
    """
    Define sessions using inactivity gaps.
    """
    df = df.sort_values(["user_id", "timestamp"])
    df["prev_time"] = df.groupby("user_id")["timestamp"].shift(1)
    df["gap_minutes"] = (
        (df["timestamp"] - df["prev_time"]).dt.total_seconds() / 60
    )
    df["new_session"] = (df["gap_minutes"] > gap_minutes) | df["gap_minutes"].isna()
    df["session_id"] = df.groupby("user_id")["new_session"].cumsum()
    return df


########################################
# 4. Prompt-level analysis
########################################

def prompt_length_features(df: pd.DataFrame) -> pd.DataFrame:
    df["prompt_chars"] = df["prompt"].str.len()
    df["prompt_tokens"] = df["prompt"].apply(lambda x: len(word_tokenize(x)))
    return df


########################################
# 5. Learning-style classification
########################################

DIRECT_PATTERNS = [
    r"^what is",
    r"^give me",
    r"^define",
    r"^answer",
    r"résume",
    r"donne la réponse"
]

TUTORING_PATTERNS = [
    r"explain",
    r"why",
    r"how does",
    r"walk me through",
    r"step by step",
    r"pourquoi",
    r"explique"
]


def classify_learning_style(prompt: str) -> str:
    """
    Rule-based, transparent classification.
    """
    text = prompt.lower().strip()

    for p in TUTORING_PATTERNS:
        if re.search(p, text):
            return "tutoring_oriented"

    for p in DIRECT_PATTERNS:
        if re.search(p, text):
            return "direct_answer"

    return "other"


def add_learning_style(df: pd.DataFrame) -> pd.DataFrame:
    df["learning_style"] = df["prompt"].apply(classify_learning_style)
    return df


########################################
# 6. Additional insights
########################################

def prompt_sophistication_over_time(df: pd.DataFrame) -> pd.DataFrame:
    """
    Track average prompt length per user over time.
    """
    df["date"] = df["timestamp"].dt.date
    return (
        df.groupby(["user_id", "date"])
        .agg(avg_prompt_tokens=("prompt_tokens", "mean"))
        .reset_index()
    )


########################################
# 7. Visualizations
########################################

def plot_distributions(df: pd.DataFrame):
    sns.histplot(df["prompt_tokens"], bins=50)
    plt.title("Distribution of Prompt Lengths (Tokens)")
    plt.show()

    sns.countplot(data=df, x="learning_style")
    plt.title("Learning Style Classification")
    plt.show()


########################################
# 8. Visualizations
########################################
def compute_time_on_task(df: pd.DataFrame) -> pd.DataFrame:
    """
    Estimate time-on-task per user using:
    last_prompt_time - first_prompt_time

    Returns time in minutes and hours.
    """
    time_df = (
        df.groupby("user_id")
        .agg(
            first_prompt=("timestamp", "min"),
            last_prompt=("timestamp", "max"),
            n_requests=("timestamp", "count"),
        )
        .reset_index()
    )

    time_df["time_spent_minutes"] = (
        (time_df["last_prompt"] - time_df["first_prompt"])
        .dt.total_seconds() / 60
    )

    time_df["time_spent_hours"] = time_df["time_spent_minutes"] / 60

    return time_df



########################################
# 9. Main execution
########################################
# jsonl_path = "data/logs_index.jsonl"
def main(jsonl_path: str):
    raw = load_jsonl(Path(jsonl_path))
    df = normalize_rows(raw)
    df = add_sessions(df)
    df = prompt_length_features(df)
    df = add_learning_style(df)

    user_stats = user_level_stats(df)
    sophistication = prompt_sophistication_over_time(df)
    time_on_task = compute_time_on_task(df)
    time_on_task = time_on_task[time_on_task["n_requests"] > 1]

    print("Estimated time-on-task per user:")
    print(time_on_task.sort_values("time_spent_minutes", ascending=False).head())
    print("User-level statistics:")
    print(user_stats.head())

    plot_distributions(df)

    return df, user_stats, sophistication


if __name__ == "__main__":
    df, user_stats, sophistication = main("data/logs_index.jsonl")
