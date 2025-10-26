"""
Verification logic for Value Added Tax (VAT).
"""
from datetime import date
from typing import Dict,Any,Optional
from .base_verifier import BaseTaxVerifier
from .constants import VerificationStatus,ComplianceStatus,FilingMode
from .exceptions import InvalidTPINError

class VATVerifier(BaseTaxVerifier):
    """Verification logic for Value Added Tax (VAT)."""
    FILING_RULES = {
        FilingMode.MANUAL :5,
       FilingMode.ELECTRONIC : 18
    }

    def get_due_date(self, filing_mode: FilingMode, filing_period: date) -> date:
        """ Calculate VAT filing due date based on filing mode
        
        Args: 
            filing_mode: The mode of filing(Manual or electronic)
            filing_period: The tax period(month/year)
            
            Returns: 
                date: The due date for VAT filing
            Raises: 
                ValueError: If filing mode is invalid"""
        
        mode = filing_mode.lower()
        if mode not in self.FILING_RULES:
            raise ValueError(f"Invalid filing mode: {filing_mode}. Must be one of {list(self.FILING_RULES.keys())}")
        day = self.FILING_RULES[mode]
        next_month = (filing_period.month % 12) + 1
        year = filing_period.year + (1 if filing_period.month == 12 else 0)
        
        return date(year, next_month, day)

    def verify(self, tpin: str, filing_mode: FilingMode, filing_period: date, filed_on:Optional[date] = None) -> Dict[str,Any]:
        """Verify VAT compliance for a given TPIN.
        
        Args:
            tpin: Taxpayer Identification Number
            filing_mode: Mode of filing (Manual or electronic)
            filing_period: The tax period (Month/Year)
            filed_on: Optional date when the return was filed
            
            Returns: 
                Dict containing verification results with status and compliance info
        """
        #Validate TPIN format
        try:
            self.validate_tpin(tpin)
        except InvalidTPINError as e:
                return {"tpin": tpin, 
                        "status":VerificationStatus.REJECTED.value,
                        "reason": str(e)}
        #Check VAT registration
        #NOTE: This is a placeholder for actual registration check(against database/API)
        registered_vat = self._check_vat_registration(tpin)
        if not registered_vat:
            return {"tpin": tpin,
                    "status": VerificationStatus.REJECTED.value,
                    "reason": "Not registered for VAT"}
        
        #Calculate due date
        due_date = self.get_due_date(filing_mode, filing_period)

        #If no filing date provided, return pending status
        if filed_on is None:
             return{
                  "tpin":tpin,
                  "status": VerificationStatus.PENDING.value,
                  "compliance": ComplianceStatus.DEFAULT.value,
                  "due_date": due_date.isoformat(),
                  "filing_period": filing_period.isoformat()
             }
        
        #check if filed on time
        if filed_on <= due_date:
            return {
                "tpin": tpin,
                "status": VerificationStatus.VERIFIED.value,
                "compliance": ComplianceStatus.COMPLIANT.value,
                "filed_on": filed_on.isoformat(),
                "due_date": due_date.isoformat(),
                "filing_period": filing_period.isoformat()
            }
        else:
             late_days = (filed_on - due_date).days
             return {
                  "tpin": tpin,
                  "status": VerificationStatus.VERIFIED.value,
                  "compliance": ComplianceStatus.NON_COMPLIANT.value,
                  "filed_on": filed_on.isoformat(),
                  "due_date": due_date.isoformat(),
                  "filing_period": filing_period.isoformat(),
                  "late_by": late_days
             }
    def _check_vat_registration(self, tpin: str) -> bool:
        """Placeholder method to check if TPIN is registered for VAT.
        
        Args:
            tpin: Taxpayer Identification Number
            
            Returns:
                bool: True if registered, False otherwise
        """
        return True
    