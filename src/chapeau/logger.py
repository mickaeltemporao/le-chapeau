"""Real-time local event and chat logging for Le Chapeau experiments."""

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional

DEFAULT_LOG_FILE = Path("data/logs/chat_logs.jsonl")


def get_log_file_path() -> Path:
    """Return the configured path to the JSONL log file."""
    custom = os.getenv("CHAPEAU_LOG_FILE")
    if custom:
        return Path(custom)
    return DEFAULT_LOG_FILE


def log_interaction(
    session_id: str,
    user_id: str,
    group: str,
    prompt: str,
    response: str,
    response_id: Optional[str] = None,
    model: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Append an interaction immediately to the local JSONL log file.
    Guarantees no user chat data is lost during runtime or container termination.
    """
    log_path = get_log_file_path()
    log_path.parent.mkdir(parents=True, exist_ok=True)

    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "session_id": session_id,
        "user_id": user_id,
        "group": group,
        "prompt": prompt,
        "response": response,
        "response_id": response_id,
        "model": model,
        "metadata": metadata or {},
    }

    with open(log_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")

    return record
