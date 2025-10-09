"""Early descriptive analysis draft."""
import ast
import json
import pandas as pd
from collections import Counter

RESULTS_FILE = "data/logs_index.jsonl"

# Convert strings to dicts if necessary
def ensure_dict(x):
    if isinstance(x, dict):
        return x
    elif isinstance(x, str) and x.strip():
        try:
            return ast.literal_eval(x)
        except Exception:
            return {}
    else:
        return {}


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
    df['metadata'] = df['metadata'].apply(ensure_dict)
    df['user'] = df['metadata'].apply(lambda x: x.get('user', None))
    df['group'] = df['metadata'].apply(lambda x: x.get('group', None))
    df = df.dropna(subset=['user', 'group'])
    df =  df[df['group'].isin(['b', 'c'])]
    # Count requests per user per group
    counts = df.groupby(['group', 'user']).size().reset_index(name='requests')
    avg_requests = counts.groupby('group')['requests'].mean().reset_index(name='avg_requests')
    print(avg_requests)
    total_per_group = df.groupby('group').size().reset_index(name='total_requests')
    print(total_per_group)

