"""
Constants and configurations for tax verification.
"""
from enum import Enum, auto

class TaxType(Enum):
    """Types of taxes in the Zambian tax system."""
    VAT = "Value Added Tax"
    PAYE = "Pay As You Earn"
    WHT = "Withholding Tax"
    ITX = "Income Tax"
    PTT = "Property Transfer Tax"
    TLEVY = "Tourism Levy"
    MINRYL = "Mineral Royalty"

class VerificationStatus(Enum):
    """Status codes for tax verification results."""
    VERIFIED = "VERIFIED"
    PENDING = "PENDING"
    REJECTED = "REJECTED"
    EXPIRED = "EXPIRED"
    NOT_FOUND = "NOT_FOUND"

class ComplianceStatus(Enum):
    """Tax compliance status codes."""
    COMPLIANT = "COMPLIANT"
    NON_COMPLIANT = "NON_COMPLIANT"
    UNDER_INVESTIGATION = "UNDER_INVESTIGATION"
    DEFAULTER = "DEFAULTER"

class FilingMode(Enum):
    """Filing modes for tax submissions."""
    MANUAL = "manual"
    ELECTRONIC = "electronic"
    
# TPIN Configuration
TPIN_LENGTH = 10
TPIN_PREFIX = ["1", "2", "3"]  # Valid TPIN starting numbers
TPIN_REGEX = r"^[1-3]\d{9}$"  # Regex pattern for TPIN validation

# Tax Thresholds (2025 values in ZMW)
VAT_REGISTRATION_THRESHOLD = 800_000  # Annual turnover threshold for VAT registration
PAYE_THRESHOLDS = {
    "BAND_1": 4_500,    # 0% tax
    "BAND_2": 4_800,    # 25% tax
    "BAND_3": 6_900,    # 30% tax
    "BAND_4": float('inf')  # 37.5% tax
}

# Verification Timeouts (in seconds)
VERIFICATION_TIMEOUT = 30
CACHE_TIMEOUT = 3600  # 1 hour

# API Rate Limits
MAX_REQUESTS_PER_MINUTE = 60
MAX_REQUESTS_PER_DAY = 1000