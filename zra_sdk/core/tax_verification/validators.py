"""
Validation functions for tax verification.
"""
import re
from datetime import datetime,date
from typing import Optional, Tuple

from .constants import TPIN_LENGTH, TPIN_PREFIX, TPIN_REGEX
from .exceptions import InvalidTPINError, InvalidDocumentError

def validate_tpin(tpin: str) -> None:
    """
    Validate TPIN format and checksum.
    
    Args:
        tpin: The TPIN to validate
        
    Raises:
        InvalidTPINError: If TPIN format is invalid
    """
    if not isinstance(tpin, str):
        raise InvalidTPINError("TPIN must be a string")
    
    if len(tpin) != TPIN_LENGTH:
        raise InvalidTPINError(f"TPIN must be {TPIN_LENGTH} digits long")
    
    if not tpin[0] in TPIN_PREFIX:
        raise InvalidTPINError(f"TPIN must start with one of {TPIN_PREFIX}")
    
    if not re.match(TPIN_REGEX, tpin):
        raise InvalidTPINError("TPIN must contain only digits")
    
    # TODO: Implement checksum validation
    return True

def validate_tax_period(tax_period: str) -> tuple[datetime, datetime]:
    """
    Validate tax period format (YYYY-MM).
    
    Args:
        tax_period: The tax period in YYYY-MM format
        
    Returns:
        tuple: Start and end dates of the tax period
        
    Raises:
        InvalidDocumentError: If tax period format is invalid
    """
    try:
        period_date = datetime.strptime(tax_period, "%Y-%m")
        start_date = datetime(period_date.year, period_date.month, 1)
        if period_date.month == 12:
            end_date = datetime(period_date.year + 1, 1, 1)
        else:
            end_date = datetime(period_date.year, period_date.month + 1, 1)
        return start_date, end_date
    except ValueError as e:
        raise InvalidDocumentError(f"Invalid tax period format. Use YYYY-MM: {e}")

def validate_amount(amount: float, minimum: Optional[float] = 0) -> None:
    """
    Validate tax amount.
    
    Args:
        amount: The amount to validate
        minimum: Optional minimum allowed amount
        
    Returns:
        bool: True if amount is valid
        
    Raises:
        ValueError: If amount is invalid
    """
    if not isinstance(amount, (int, float)):
        raise ValueError("Amount must be a number")
    
    if amount < minimum:
        raise ValueError(f"Amount must be greater than {minimum}")
    
def validate_filing_period(filing_period: date) -> None:
    """
    Validate filing period is not in the future.
    
    Args:
        filing_period: The filing period date
    Raises:
        ValueError: If filing period is in the future"""
    if not isinstance(filing_period, date):
        raise ValueError("Filing period must be a date object")
    if filing_period > date.today():
        raise ValueError("Filing period cannot be in the future")