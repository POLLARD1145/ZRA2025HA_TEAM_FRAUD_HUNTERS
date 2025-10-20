"""
Main tax verification service.
"""
from datetime import datetime, date
from typing import Optional, Dict, Any

from .constants import VerificationStatus, TaxType
from .exceptions import (
    TaxVerificationError,
    InvalidTPINError,
    TPINNotFoundError,
    InvalidDocumentError,
    InvalidFilingPeriodError,
    VerificationTimeoutError
)
from .validators import validate_tpin, validate_tax_period
from ..taxpayer.models import Taxpayer, TaxRegistration
from ..taxpayer.status import ComplianceChecker
from .vat_verifier import VATVerifier


class TaxVerificationService:
    """Main service for tax verification operations."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the tax verification service.
        
        Args:
            api_key: Optional API key for ZRA services
        """
        self.api_key = api_key
        self._compliance_checker = ComplianceChecker()
        # Registry of tax-type specific verifiers
        self._verifiers: Dict[TaxType, Any] = {
            TaxType.VAT: VATVerifier()
        }
    
    async def verify_taxpayer(self, tpin: str) -> Taxpayer:
        """
        Verify taxpayer details and status.
        
        Args:
            tpin: Taxpayer Identification Number
            
        Returns:
            Taxpayer: Verified taxpayer information
            
        Raises:
            InvalidTPINError: If TPIN format is invalid
            TPINNotFoundError: If TPIN does not exist
            VerificationTimeoutError: If verification times out
        """
        # Validate TPIN format
        validate_tpin(tpin)
        
        # TODO: Implement actual API call to ZRA services
        # This is a placeholder implementation
        taxpayer_data = await self._get_taxpayer_data(tpin)
        if not taxpayer_data:
            raise TPINNotFoundError(f"TPIN {tpin} not found")
        
        # Verify compliance status
        compliance = self._compliance_checker.verify_compliance(tpin)
        taxpayer_data["compliance"] = compliance
        
        return Taxpayer(**taxpayer_data)
    
    async def verify_tax_registration(
        self,
        tpin: str,
        tax_type: TaxType
    ) -> TaxRegistration:
        """
        Verify tax type registration status.
        
        Args:
            tpin: Taxpayer Identification Number
            tax_type: Type of tax to verify
            
        Returns:
            TaxRegistration: Tax registration details
        """
        validate_tpin(tpin)
        
        # TODO: Implement actual verification
        # This is a placeholder implementation
        registration_data = await self._get_registration_data(tpin, tax_type)
        return TaxRegistration(**registration_data)
    
    async def verify_tax_payment(
        self,
        tpin: str,
        tax_type: TaxType,
        tax_period: str,
        amount: float,
        filing_mode: str = "electronic",
        filed_on: Optional[date] = None,
    ) -> VerificationStatus:
        """
        Verify tax payment for a specific period.
        
        Args:
            tpin: Taxpayer Identification Number
            tax_type: Type of tax
            tax_period: Tax period in YYYY-MM format
            amount: Payment amount to verify
            filing_mode: Filing mode (e.g., "manual" or "electronic") used to determine due date
            filed_on: Optional actual filing/payment date
            
        Returns:
            VerificationStatus: Payment verification status
        """
        validate_tpin(tpin)
        start_date, end_date = validate_tax_period(tax_period)
        
        # Delegate to specific tax-type verifier if available
        verifier = self._verifiers.get(tax_type)
        if verifier is None:
            # For unsupported tax types, default to a basic verified status for now
            return VerificationStatus.PENDING
        
        # The per-tax-type verifier works with date objects and returns a dict
        result = verifier.verify(
            tpin=tpin,
            filing_mode=filing_mode,
            filing_period=start_date.date(),
            filed_on=filed_on,
        )
        # Map the returned status string to the VerificationStatus enum
        status_str = str(result.get("status", "PENDING")).upper()
        mapping = {
            "VERIFIED": VerificationStatus.VERIFIED,
            "PENDING": VerificationStatus.PENDING,
            "REJECTED": VerificationStatus.REJECTED,
            "EXPIRED": VerificationStatus.EXPIRED,
            "NOT_FOUND": VerificationStatus.NOT_FOUND,
        }
        return mapping.get(status_str, VerificationStatus.PENDING)
    
    async def _get_taxpayer_data(self, tpin: str) -> Dict[str, Any]:
        """Get taxpayer data from ZRA services."""
        # TODO: Implement actual API call
        # This is a placeholder implementation
        return {
            "tpin": tpin,
            "name": "Test Taxpayer",
            "registration_date": datetime.utcnow(),
            "address": {
                "street": "Test Street",
                "city": "Lusaka",
                "province": "Lusaka",
                "country": "Zambia"
            },
            "contact": {}
        }
    
    async def _get_registration_data(
        self,
        tpin: str,
        tax_type: TaxType
    ) -> Dict[str, Any]:
        """Get tax registration data from ZRA services."""
        # TODO: Implement actual API call
        # This is a placeholder implementation
        return {
            "tax_type": tax_type,
            "registration_date": datetime.utcnow(),
            "status": True
        }