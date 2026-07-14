"""
Tests for utility modules.
"""

import pytest
from app.utils.validators import validate_question, validate_python_code, sanitize_query


def test_validate_question_valid():
    """Test validate_question with valid input."""
    question = "What is artificial intelligence and how does it work?"
    assert validate_question(question) is True


def test_validate_question_too_short():
    """Test validate_question with short input."""
    question = "What?"
    with pytest.raises(ValueError):
        validate_question(question)


def test_validate_question_too_long():
    """Test validate_question with long input."""
    question = "a" * 1001
    with pytest.raises(ValueError):
        validate_question(question)


def test_validate_python_code_safe():
    """Test validate_python_code with safe code."""
    code = "result = sum([1, 2, 3])"
    assert validate_python_code(code) is True


def test_validate_python_code_dangerous():
    """Test validate_python_code with dangerous code."""
    code = "import os; os.system('ls')"
    with pytest.raises(ValueError):
        validate_python_code(code)


def test_sanitize_query():
    """Test query sanitization."""
    query = "python   programming   language"
    sanitized = sanitize_query(query)
    
    assert "   " not in sanitized
    assert sanitized == "python programming language"
