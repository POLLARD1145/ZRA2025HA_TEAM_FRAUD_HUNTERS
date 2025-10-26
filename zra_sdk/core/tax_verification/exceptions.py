"""
Custom exceptions for tax verification.
"""
from typing import List

class TaxVerificationError(Exception):
    """Base exception for all tax verification errors."""
    pass

class InvalidTPINError(TaxVerificationError):
    """Raised when TPIN format is invalid."""
    pass

class TPINNotFoundError(TaxVerificationError):
    """Raised when TPIN does not exist in the system."""
    pass

class VerificationTimeoutError(TaxVerificationError):
    """Raised when verification request times out."""
    pass

class TaxComplianceError(TaxVerificationError):
    """Raised when there are tax compliance issues."""
    def __init__(self, tpin: str, issues: List[str]):
        self.tpin = tpin
        self.issues = issues
        message = f"Tax compliance issues found for TPIN {tpin}: {', '.join(issues)}"
        super().__init__(message)

class RateLimitExceededError(TaxVerificationError):
    """Raised when API rate limit is exceeded."""
    def __init__(self, limit_type: str, retry_after: int):
        self.limit_type = limit_type
        self.retry_after = retry_after
        message = f"{limit_type} rate limit exceeded. Try again after {retry_after} seconds."
        super().__init__(message)

class InvalidDocumentError(TaxVerificationError):
    """Raised when tax document is invalid or expired."""
    pass

class AuthenticationError(TaxVerificationError):
    """Raised when API authentication fails."""
    pass
class InvalidFilingPeriodError(TaxVerificationError):
    """Raised when the filing period is invalid."""
    pass