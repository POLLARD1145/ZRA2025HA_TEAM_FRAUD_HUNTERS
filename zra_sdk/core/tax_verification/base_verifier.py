"""
Abstract base class for all tax verification types.
"""
from abc import ABC, abstractmethod
from datetime import date
from typing import Dict,Any,Optional
from .validators import validate_tpin
from .constants import FilingMode

class BaseTaxVerifier(ABC):
    """Abstract base class for all tax verification types."""
    def validate_tpin(self, tpin: str) -> None:
        """Check TPIN format validity.
        Args: 
            tpin: The TPIN to validate
        Raises:
            ValueError: If the TPIN is invalid
        """
        validate_tpin(tpin)

    @abstractmethod
    def get_due_date(self, filing_mode:FilingMode, filing_period: date) -> date:
        """ Calculate the due date for tax filing
        Args:
            filing_mode: Mode of filing(Manual or electronic)
            filing_period: The tax period(Month/year)'

            returns: date: Due date for filing
        """
        pass

    @abstractmethod
    def verify(self, tpin: str, filing_mode: FilingMode, filing_period: date, filed_on: Optional[date] = None) -> Dict[str,Any]:
        """Verify tax compliance for a given TPIN.
        Args: tpin: Taxpayer Identification Number
            filing_mode: Mode of filing (Manual or electronic)
            filing_period: The tax period (Month/Year)
            filed_on: Optional date when the return was filed

            Returns: Dict containing verification results with status and compliance info
        """
        pass
