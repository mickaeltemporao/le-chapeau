"""Export and anonymize study conversation logs into researcher-friendly CSV files."""

import json
import os
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import pandas as pd

DEFAULT_LOG_PATH = Path("data/logs/chat_logs.jsonl")
DEFAULT_EXPORT_PATH = Path("data/exports/chapeau_interactions.csv")
DEFAULT_SALT_PATH = Path("config/salt.txt")
EXAMPLE_SALT_PATH = Path("config/salt.example.txt")


def get_study_salt(salt_path: Optional[Path] = None) -> str:
    """
    Retrieve the persistent study salt used for deterministic pseudonymization.
    Order of precedence:
    1. CHAPEAU_SALT environment variable
    2. config/salt.txt
    3. config/salt.example.txt
    4. Auto-generated persistent salt in config/salt.txt
    """
    env_salt = os.getenv("CHAPEAU_SALT")
    if env_salt:
        return env_salt.strip()

    target = salt_path or DEFAULT_SALT_PATH
    if target.exists():
        content = target.read_text(encoding="utf-8").strip()
        lines = [line for line in content.splitlines() if line and not line.startswith("#")]
        if lines:
            return lines[0].strip()

    if EXAMPLE_SALT_PATH.exists():
        content = EXAMPLE_SALT_PATH.read_text(encoding="utf-8").strip()
        lines = [line for line in content.splitlines() if line and not line.startswith("#")]
        if lines:
            return lines[0].strip()

    # Generate and persist a new random salt
    target.parent.mkdir(parents=True, exist_ok=True)
    generated = uuid.uuid4().hex
    target.write_text(f"# Persistent study salt for Le Chapeau\n{generated}\n", encoding="utf-8")
    return generated


def anonymize_user_id(user_id: str, salt: Optional[str] = None) -> str:
    """
    Deterministically hash an email or identifier into a UUIDv5 using the study salt.
    If the same user enters another study with the same salt, their UUID will be identical,
    allowing cross-study linking while strictly protecting student privacy.
    """
    resolved_salt = salt or get_study_salt()
    study_namespace = uuid.uuid5(uuid.NAMESPACE_DNS, f"chapeau.study.{resolved_salt}")
    cleaned_id = user_id.strip().lower()
    return str(uuid.uuid5(study_namespace, cleaned_id))


def _extract_openai_text(blocks: Any) -> str:
    """Extract and concatenate text from OpenAI Responses API nested blocks."""
    if not isinstance(blocks, list):
        return str(blocks or "")
    texts = []
    for block in blocks:
        if isinstance(block, dict):
            for content in block.get("content", []):
                if isinstance(content, dict) and content.get("type") in {"input_text", "output_text"}:
                    texts.append(content.get("text", ""))
    return " ".join(texts).strip()


def parse_log_line(raw_line: str) -> Optional[Dict[str, Any]]:
    """Parse a single JSON log line (supporting both Chapeau real-time format and OpenAI format)."""
    line = raw_line.strip()
    if not line:
        return None
    try:
        obj = json.loads(line)
    except json.JSONDecodeError:
        return None

    # Format 1: Chapeau native real-time log
    if "prompt" in obj and "user_id" in obj:
        return {
            "timestamp": obj.get("timestamp"),
            "session_id": obj.get("session_id", ""),
            "user_id": obj.get("user_id", ""),
            "group": obj.get("group", "unknown"),
            "prompt": obj.get("prompt", ""),
            "response": obj.get("response", ""),
            "model": obj.get("model", ""),
            "response_id": obj.get("response_id", ""),
        }

    # Format 2: OpenAI responses export format
    if "metadata" in obj and ("input" in obj or "output" in obj):
        metadata = obj.get("metadata", {})
        ts = obj.get("created_at")
        if isinstance(ts, (int, float)):
            ts = datetime.fromtimestamp(ts).isoformat()

        return {
            "timestamp": ts,
            "session_id": obj.get("id", ""),
            "user_id": metadata.get("user", ""),
            "group": metadata.get("group", "unknown"),
            "prompt": _extract_openai_text(obj.get("input")),
            "response": _extract_openai_text(obj.get("output")),
            "model": obj.get("model", ""),
            "response_id": obj.get("id", ""),
        }

    return None


def export_logs_to_dataframe(
    log_file: Optional[Path] = None,
    anonymize: bool = True,
    salt: Optional[str] = None,
) -> pd.DataFrame:
    """Load JSONL logs and return a normalized, optionally anonymized DataFrame."""
    target_log = log_file or DEFAULT_LOG_PATH
    if not target_log.exists():
        return pd.DataFrame()

    resolved_salt = salt or get_study_salt()
    records: List[Dict[str, Any]] = []

    with open(target_log, "r", encoding="utf-8") as f:
        for line in f:
            parsed = parse_log_line(line)
            if not parsed or not parsed["user_id"]:
                continue

            raw_user = parsed["user_id"]
            if anonymize:
                parsed["participant_id"] = anonymize_user_id(raw_user, resolved_salt)
                del parsed["user_id"]
            else:
                parsed["participant_id"] = raw_user

            parsed["prompt_chars"] = len(parsed.get("prompt", ""))
            parsed["response_chars"] = len(parsed.get("response", ""))
            records.append(parsed)

    df = pd.DataFrame(records)
    if not df.empty and "timestamp" in df.columns:
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
        df = df.sort_values(["timestamp"])
    return df


def export_logs_to_csv(
    log_file: Optional[Path] = None,
    output_csv: Optional[Path] = None,
    anonymize: bool = True,
    salt: Optional[str] = None,
) -> Path:
    """
    Export study logs to a tidy CSV file for research analysis.
    Returns the path to the written CSV.
    """
    target_csv = output_csv or DEFAULT_EXPORT_PATH
    df = export_logs_to_dataframe(log_file=log_file, anonymize=anonymize, salt=salt)

    target_csv.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(target_csv, index=False, encoding="utf-8")
    return target_csv
