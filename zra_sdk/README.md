# ZRA SDK - Developer Guide

## Overview
The ZRA SDK is a Python-based software development kit that simplifies integration with Zambia Revenue Authority services. This SDK provides developers with easy-to-use tools for taxpayer verification, tax calculations, compliance checks, and other ZRA services. Whether you're building a financial application, tax management system, or business automation tool, the ZRA SDK streamlines your integration with ZRA's official services.

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
from typing import Optional, Dict


def verify_taxpayer(tpin: str) -> Dict:
    """
    Verify taxpayer details using their TPIN (Taxpayer Identification Number).
    
    Args:
        tpin: Taxpayer Identification Number
        
    Returns:
        Dictionary containing taxpayer information including name, status, and compliance details
        
    Raises:
        ValueError: If TPIN format is invalid
        APIError: If verification fails
    """
    if not tpin or len(tpin) != 10:
        raise ValueError("TPIN must be a 10-digit number")
    
    # Taxpayer verification logic here
    return {
        "tpin": tpin,
        "name": "Business Name",
        "status": "active",
        "compliant": True
    }
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
# tests/test_taxpayer_verification.py
import pytest
from zra_sdk.core.taxpayer import verify_taxpayer


def test_verify_taxpayer_valid_tpin():
    """Test taxpayer verification with valid TPIN."""
    result = verify_taxpayer("1000123456")
    assert isinstance(result, dict)
    assert "tpin" in result
    assert "status" in result


def test_verify_taxpayer_invalid_tpin():
    """Test taxpayer verification with invalid TPIN."""
    with pytest.raises(ValueError):
        verify_taxpayer("123")
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
Core functionality for ZRA service integrations including taxpayer verification, tax calculations, and compliance checks.

#### `zra_sdk.models`
Data models and schemas for taxpayers, transactions, tax returns, and compliance reports.

#### `zra_sdk.utils`
Utility functions for TPIN validation, data formatting, currency conversions, and API request handling.

#### `zra_sdk.api`
FastAPI endpoints for exposing SDK functionality as REST API.

### Example Usage

```python
from zra_sdk import ZRAClient

# Initialize client
client = ZRAClient(api_key="your-api-key")

# Verify a taxpayer
taxpayer = client.verify_taxpayer(tpin="1000123456")
print(f"Taxpayer Name: {taxpayer.name}")
print(f"Status: {taxpayer.status}")
print(f"Compliant: {taxpayer.compliant}")

# Calculate tax
tax_result = client.calculate_tax(
    amount=50000.00,
    tax_type="VAT"
)
print(f"Tax Amount: {tax_result.tax_amount}")
print(f"Total: {tax_result.total}")
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
