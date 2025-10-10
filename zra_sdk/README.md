# ZRA SDK - Developer Guide

## Overview
The ZRA SDK is a Python-based software development kit for fraud detection functionality in the Zambia Revenue Authority system. This SDK provides core utilities, models, and API integrations for fraud detection and analysis.

## Table of Contents
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Code Standards](#code-standards)
- [Testing](#testing)
- [API Documentation](#api-documentation)

## Project Structure

```
zra_sdk/
├── __init__.py           # Package initialization
├── core/                 # Core functionality
│   └── __init__.py
├── models/               # Data models and schemas
│   └── __init__.py
├── utils/                # Utility functions
│   └── __init__.py
├── api/                  # API endpoints and handlers
│   └── __init__.py
├── tests/                # Test suite
│   └── __init__.py
├── requirements.txt      # Python dependencies
├── setup.py             # Package setup configuration
├── pyproject.toml       # Modern Python project config
├── .env.example         # Environment variables template
└── README.md            # This file
```

## Getting Started

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment tool (venv, virtualenv, or conda)

### Installation

1. **Clone the repository** (if not already done):
   ```bash
   git clone https://github.com/POLLARD1145/ZRA2025HA_TEAM_FRAUD_HUNTERS.git
   cd ZRA2025HA_TEAM_FRAUD_HUNTERS/zra_sdk
   ```

2. **Create a virtual environment**:
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # Linux/Mac
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   ```bash
   # Copy the example file
   cp .env.example .env
   
   # Edit .env with your actual configuration
   ```

## Development Setup

### Running in Development Mode

To run the SDK in development mode:

```bash
# Install in editable mode
pip install -e .

# Run tests
pytest

# Run with coverage
pytest --cov=zra_sdk --cov-report=html
```

### Code Formatting

This project uses **Black** for code formatting and **Flake8** for linting:

```bash
# Format code
black .

# Check linting
flake8 .

# Type checking (optional)
mypy .
```

## Code Standards

### Style Guide
- Follow **PEP 8** Python style guide
- Use **Black** formatter with 100 character line length
- Use type hints where appropriate
- Write docstrings for all public functions and classes

### Example Code Style

```python
from typing import Optional, List


def detect_fraud(transaction_id: str, amount: float) -> bool:
    """
    Detect potential fraud in a transaction.
    
    Args:
        transaction_id: Unique identifier for the transaction
        amount: Transaction amount in ZMW
        
    Returns:
        True if fraud is detected, False otherwise
        
    Raises:
        ValueError: If transaction_id is empty or amount is negative
    """
    if not transaction_id:
        raise ValueError("Transaction ID cannot be empty")
    if amount < 0:
        raise ValueError("Amount cannot be negative")
    
    # Your fraud detection logic here
    return False
```

### Naming Conventions
- **Modules**: `lowercase_with_underscores.py`
- **Classes**: `PascalCase`
- **Functions/Variables**: `snake_case`
- **Constants**: `UPPER_CASE_WITH_UNDERSCORES`

## Testing

### Writing Tests

Tests are located in the `tests/` directory. Use **pytest** for writing tests:

```python
# tests/test_fraud_detection.py
import pytest
from zra_sdk.core.fraud_detector import detect_fraud


def test_detect_fraud_valid_transaction():
    """Test fraud detection with valid transaction."""
    result = detect_fraud("TXN123", 1000.00)
    assert isinstance(result, bool)


def test_detect_fraud_invalid_amount():
    """Test fraud detection with negative amount."""
    with pytest.raises(ValueError):
        detect_fraud("TXN123", -100.00)
```

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_fraud_detection.py

# Run with verbose output
pytest -v

# Run with coverage report
pytest --cov=zra_sdk --cov-report=html
```

## API Documentation

### Core Modules

#### `zra_sdk.core`
Core functionality for fraud detection algorithms.

#### `zra_sdk.models`
Data models and schemas for transactions, users, and fraud reports.

#### `zra_sdk.utils`
Utility functions for data processing, validation, and formatting.

#### `zra_sdk.api`
FastAPI endpoints for exposing SDK functionality as REST API.

### Example Usage

```python
from zra_sdk import FraudDetector

# Initialize detector
detector = FraudDetector(api_key="your-api-key")

# Analyze transaction
result = detector.analyze_transaction(
    transaction_id="TXN123",
    amount=5000.00,
    user_id="USER456"
)

print(f"Fraud Risk: {result.risk_score}")
print(f"Is Fraudulent: {result.is_fraud}")
```

## Building and Distribution

### Building the Package

```bash
# Build distribution files
python setup.py sdist bdist_wheel
```

### Installing Locally

```bash
# Install in development mode
pip install -e .

# Install normally
pip install .
```

## Troubleshooting

### Common Issues

**Import errors**: Make sure you've activated your virtual environment and installed all dependencies.

**Test failures**: Ensure your environment variables are set correctly in `.env`.

**Module not found**: Install the package in editable mode: `pip install -e .`

## Additional Resources

- [Python Official Documentation](https://docs.python.org/3/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pytest Documentation](https://docs.pytest.org/)
- [Black Code Formatter](https://black.readthedocs.io/)

## Support

For questions or issues, please contact the team or create an issue in the GitHub repository.

---

**Last Updated**: 2025-10-10  
**Maintained by**: Team Fraud Hunters
