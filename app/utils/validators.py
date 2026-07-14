"""
Validation utilities for the Enterprise Research Agent.
Provides input validation and error handling.
"""

import re
from typing import Any, List


def validate_question(question: str) -> bool:
    """
    Validate research question format and length.
    
    Args:
        question: Question string to validate
    
    Returns:
        True if valid, raises ValueError otherwise
    """
    if not isinstance(question, str):
        raise ValueError("Question must be a string")
    
    question = question.strip()
    if len(question) < 10:
        raise ValueError("Question must be at least 10 characters long")
    
    if len(question) > 1000:
        raise ValueError("Question must be less than 1000 characters")
    
    # Check for valid question format
    if not any(c.isalpha() for c in question):
        raise ValueError("Question must contain alphabetic characters")
    
    return True


def validate_python_code(code: str, allowed_imports: List[str] = None) -> bool:
    """
    Validate Python code for safe execution.
    
    Args:
        code: Python code to validate
        allowed_imports: List of allowed import modules
    
    Returns:
        True if safe to execute, raises ValueError otherwise
    """
    if allowed_imports is None:
        allowed_imports = ["pandas", "numpy", "json", "math", "re", "datetime"]
    
    # Dangerous patterns to reject
    dangerous_patterns = [
        r"__import__",
        r"exec\s*\(",
        r"eval\s*\(",
        r"os\.system",
        r"subprocess",
        r"open\s*\(",
        r"input\s*\(",
        r"compile\s*\(",
    ]
    
    for pattern in dangerous_patterns:
        if re.search(pattern, code, re.IGNORECASE):
            raise ValueError(f"Code contains dangerous operation: {pattern}")
    
    # Check imports
    import_pattern = r"from\s+(\w+)|import\s+(\w+)"
    imports = re.findall(import_pattern, code)
    for imp in imports:
        module = imp[0] or imp[1]
        if module not in allowed_imports:
            raise ValueError(f"Import '{module}' is not allowed")
    
    return True


def sanitize_query(query: str, max_length: int = 200) -> str:
    """
    Sanitize search query for tool execution.
    
    Args:
        query: Query to sanitize
        max_length: Maximum query length
    
    Returns:
        Sanitized query
    """
    query = query.strip()
    query = re.sub(r'\s+', ' ', query)  # Collapse multiple spaces
    query = query[:max_length]  # Truncate if too long
    return query
