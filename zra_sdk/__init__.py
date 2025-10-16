
"""
ZRA SDK - Zambia Revenue Authority Software Development Kit
A Python toolkit for integrating with ZRA services.
"""

__version__ = "1.0.0"
__author__ = "Team Fraud Hunters"

from zra_sdk.api.taxpayer_api import verify_taxpayer, calculate_tax
from zra_sdk.models.taxpayer import Taxpayer

__all__ = ['verify_taxpayer', 'calculate_tax', 'Taxpayer']