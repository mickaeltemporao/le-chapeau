"""User authentication, group assignment, and roster management for Le Chapeau."""

import os
import random
from collections import Counter
from pathlib import Path
from typing import Dict, Optional, Set, Tuple

DEFAULT_USERS_FILE = Path("data/users.txt")
EXAMPLE_USERS_FILE = Path("data/users.example.txt")


def get_users_file_path() -> Path:
    """Return the resolved path to the participant roster file."""
    custom = os.getenv("CHAPEAU_USERS_FILE")
    if custom:
        return Path(custom)
    if DEFAULT_USERS_FILE.exists():
        return DEFAULT_USERS_FILE
    if EXAMPLE_USERS_FILE.exists():
        return EXAMPLE_USERS_FILE
    return DEFAULT_USERS_FILE


def load_roster(filepath: Optional[Path] = None) -> Dict[str, str]:
    """
    Load users and their assigned groups from a CSV/text file.
    Lines starting with '#' or empty lines are ignored.
    """
    target = filepath or get_users_file_path()
    roster: Dict[str, str] = {}
    if not target.exists():
        return roster

    with open(target, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = [p.strip() for p in line.split(",")]
            user = parts[0].lower()
            group = parts[1].lower() if len(parts) > 1 else "a"
            roster[user] = group

    return roster


def is_auto_enroll_enabled() -> bool:
    """Check if auto-enrollment for unknown users is enabled."""
    val = os.getenv("CHAPEAU_AUTO_ENROLL", "false").lower()
    return val in {"1", "true", "yes", "y", "on"}


def assign_balanced_group(roster: Dict[str, str], available_groups: Tuple[str, ...] = ("a", "b", "c")) -> str:
    """Assign the user to the group with the fewest participants to maintain study balance."""
    counts = Counter({g: 0 for g in available_groups})
    counts.update([g for g in roster.values() if g in available_groups])
    # Find group(s) with minimum count
    min_count = min(counts.values())
    least_groups = [g for g, count in counts.items() if count == min_count]
    return random.choice(least_groups)


def auto_enroll_user(user: str, filepath: Optional[Path] = None) -> str:
    """
    Enroll an unknown user on-the-fly, assign a balanced group,
    and persist the assignment to disk.
    """
    target = filepath or get_users_file_path()
    roster = load_roster(target)
    if user in roster:
        return roster[user]

    assigned_group = assign_balanced_group(roster)
    target.parent.mkdir(parents=True, exist_ok=True)

    with open(target, "a", encoding="utf-8") as f:
        f.write(f"{user},{assigned_group}\n")

    return assigned_group


def clean_user_identifier(raw_input: str) -> str:
    """Normalize user input (strip whitespace, lowercase)."""
    return raw_input.strip().lower()


class StudyAuth:
    """Authentication and group resolution helper."""

    def __init__(self, users_file: Optional[Path] = None, auto_enroll: Optional[bool] = None):
        self.users_file = users_file or get_users_file_path()
        self.auto_enroll = auto_enroll if auto_enroll is not None else is_auto_enroll_enabled()
        self.roster = load_roster(self.users_file)

    def reload(self) -> None:
        """Reload roster from disk."""
        self.roster = load_roster(self.users_file)

    def authenticate(self, user_id: str) -> Tuple[bool, Optional[str]]:
        """
        Authenticate a user identifier.
        Returns (is_authenticated, group).
        """
        user = clean_user_identifier(user_id)
        if not user:
            return False, None

        # Check existing roster
        if user in self.roster:
            return True, self.roster[user]

        # Check disk in case file changed
        self.reload()
        if user in self.roster:
            return True, self.roster[user]

        # If auto-enrollment is enabled, enroll them
        if self.auto_enroll:
            group = auto_enroll_user(user, self.users_file)
            self.reload()
            return True, group

        return False, None
