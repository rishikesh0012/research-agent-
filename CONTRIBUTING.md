# Contributing to Enterprise Research Agent

We welcome contributions! This document provides guidelines for contributing.

## Code Quality

- Use type hints everywhere
- Follow PEP 8 style guide
- Write docstrings for all functions and classes
- Run tests before submitting

## Testing

```bash
pytest -v --cov=app
```

## Development Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install dev dependencies
pip install pytest pytest-asyncio pytest-cov
```

## Pull Request Process

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit pull request

## Reporting Issues

Include:
- Description of the issue
- Steps to reproduce
- Expected behavior
- Actual behavior
- Environment details
