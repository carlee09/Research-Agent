# Contributing to Research Agent

Thank you for your interest in contributing to Research Agent! This document provides guidelines for contributing to the project.

## How to Contribute

### Reporting Bugs

If you find a bug, please create an issue with:
- A clear description of the bug
- Steps to reproduce
- Expected vs. actual behavior
- Your environment (OS, Python version, etc.)

### Suggesting Features

Feature suggestions are welcome! Please:
- Check if the feature has already been suggested
- Provide a clear use case
- Explain why this feature would be useful

### Pull Requests

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/your-feature-name`
3. **Make your changes**
4. **Add tests** if applicable
5. **Update documentation** if needed
6. **Commit your changes**: `git commit -m "Add feature: description"`
7. **Push to your fork**: `git push origin feature/your-feature-name`
8. **Create a Pull Request**

## Development Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/research-agent.git
cd research-agent

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -e .

# Copy environment variables
cp .env.example .env
# Edit .env with your API keys

# Run tests
pytest tests/
```

## Code Style

- Follow PEP 8 guidelines
- Use type hints where appropriate
- Add docstrings to all public functions
- Keep functions focused and single-purpose
- Use meaningful variable names

## Code Quality Tools

```bash
# Format code
black src/ tests/

# Lint code
flake8 src/ tests/

# Type checking
mypy src/
```

## Testing

- Write tests for new features
- Ensure all tests pass before submitting PR
- Aim for >80% code coverage

```bash
# Run tests
pytest tests/

# Run with coverage
pytest --cov=src tests/
```

## Commit Messages

Use clear, descriptive commit messages:
- Start with a verb (Add, Fix, Update, Remove, etc.)
- Keep the first line under 50 characters
- Add detailed description if needed

Examples:
```
Add web collector retry logic
Fix markdown formatting in reports
Update Claude API to latest version
```

## Questions?

Feel free to open an issue for any questions or concerns!
