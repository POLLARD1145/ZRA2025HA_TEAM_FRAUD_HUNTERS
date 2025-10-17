"""
ZRA SDK - Fraud Detection SDK for Zambia Revenue Authority
"""

__version__ = "0.1.0"
__author__ = "Team Fraud Hunters"

# Public API
from .client import ZRAClient  # noqa: E402,F401

__all__ = [
    "ZRAClient",
    "__version__",
    "__author__",
]
