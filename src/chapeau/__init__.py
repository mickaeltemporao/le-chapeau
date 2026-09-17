"""
Le Chapeau: An A/B Testing Toolbox for Socratic Educational AI Agents.
"""

from chapeau.auth import StudyAuth
from chapeau.export import anonymize_user_id, export_logs_to_csv, export_logs_to_dataframe
from chapeau.logger import log_interaction
from chapeau.prompts import assist, get_prompt_for_group, mentor

__version__ = "0.1.0"

__all__ = [
    "assist",
    "mentor",
    "get_prompt_for_group",
    "StudyAuth",
    "log_interaction",
    "anonymize_user_id",
    "export_logs_to_csv",
    "export_logs_to_dataframe",
    "__version__",
]
