"""Text preparation helpers used by both training and inference."""
from __future__ import annotations
import re
from typing import Any

_WHITESPACE_RE = re.compile(r"\s+")

def clean_text(value: Any) -> str:
    """Normalize text; preserve punctuation that may carry email context."""
    if value is None:
        return ""
    try:
        if value != value:  # NaN without importing pandas
            return ""
    except (TypeError, ValueError):
        pass
    return _WHITESPACE_RE.sub(" ", str(value).lower()).strip()

def combine_email_text(subject: Any, body: Any) -> str:
    """Combine subject and body using the same normalization path."""
    parts = [clean_text(subject), clean_text(body)]
    return " ".join(part for part in parts if part)
