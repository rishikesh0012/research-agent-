"""Data serialization and formatting utilities."""

import json
from typing import Any, Dict
from datetime import datetime


def serialize_for_json(obj: Any) -> Any:
    """
    Convert objects to JSON-serializable format.
    
    Args:
        obj: Object to serialize
    
    Returns:
        JSON-serializable object
    """
    if isinstance(obj, datetime):
        return obj.isoformat()
    elif isinstance(obj, dict):
        return {k: serialize_for_json(v) for k, v in obj.items()}
    elif isinstance(obj, (list, tuple)):
        return [serialize_for_json(item) for item in obj]
    elif hasattr(obj, "dict"):
        return obj.dict()
    else:
        return obj


def format_markdown_table(data: list[Dict[str, Any]], headers: list[str] = None) -> str:
    """
    Format data as markdown table.
    
    Args:
        data: List of dictionaries
        headers: Column headers (optional)
    
    Returns:
        Markdown table string
    """
    if not data:
        return ""
    
    if headers is None:
        headers = list(data[0].keys())
    
    # Create header row
    table = "| " + " | ".join(headers) + " |\n"
    table += "|" + "---|" * len(headers) + "\n"
    
    # Add data rows
    for row in data:
        values = [str(row.get(header, "")) for header in headers]
        table += "| " + " | ".join(values) + " |\n"
    
    return table


def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """
    Truncate text to max length.
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix to add if truncated
    
    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix
