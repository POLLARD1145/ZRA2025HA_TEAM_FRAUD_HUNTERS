"""
Tax compliance status handling.
"""
from datetime import datetime, timedelta
from typing import List, Optional, Tuple
from calendar import monthrange

from .models import ComplianceRecord
from ..tax_verification.constants import ComplianceStatus

class ComplianceChecker:
    """Handles tax compliance status checks and verification."""
    
    @staticmethod
    def verify_compliance(
        tpin: str,
        tax_returns: bool = True,
        tax_payments: bool = True,
        penalties: bool = True
    ) -> ComplianceRecord:
        """
        Verify tax compliance status for a given TPIN.
        
        Args:
            tpin: Taxpayer Identification Number
            tax_returns: Check tax returns compliance
            tax_payments: Check tax payments compliance
            penalties: Check outstanding penalties
            
        Returns:
            ComplianceRecord: Updated compliance record
        """
        issues: List[str] = []
        
        # TODO: Implement actual verification logic
        # This is a placeholder implementation
        status = ComplianceStatus.COMPLIANT
        score = 100.0
        
        if tax_returns and not ComplianceChecker._verify_tax_returns(tpin):
            issues.append("Outstanding tax returns")
            status = ComplianceStatus.NON_COMPLIANT
            score -= 30.0
            
        if tax_payments and not ComplianceChecker._verify_tax_payments(tpin):
            issues.append("Outstanding tax payments")
            status = ComplianceStatus.NON_COMPLIANT
            score -= 40.0

        if penalties and not ComplianceChecker._verify_penalties(tpin):
            issues.append("Unpaid penalties")
            status = ComplianceStatus.NON_COMPLIANT
            score -= 30.0

        now = datetime.utcnow()
        #Calculate valid_until as end of next month
        next_month = now.month % 12 + 1
        next_year = now.year + (1 if now.month == 12 else 0)
        last_day = monthrange(next_year, next_month)[1]
        valid_until = datetime(next_year, next_month, last_day, 23, 59, 59)

        return ComplianceRecord(
            status=status,
            last_verified=now,
            valid_until=valid_until,
            issues=issues,
            score= max(0.0, score)
        )
    
    @staticmethod
    def check_compliance_status(record: ComplianceRecord) -> Tuple[bool, str]:
        """
        Check if the compliance record indicates a compliant status.
        
        Args:
            record: ComplianceRecord to check
            Returns:
            tuple:(is_valid, message)
            """
        if not record.is_valid:
            return (False, "Compliance record has expired")
        
        if not record.is_compliant:
            issues_text =" , ".join(record.issues) if record.issues else "Unknown issues"
            return (False, f"Compliance record is not compliant: {issues_text}")

        return (True, "Compliance record is valid and compliant")

    @staticmethod
    def _verify_tax_returns(tpin: str) -> bool:
        """Check if all required tax returns have been filed."""
        # TODO: Implement actual verification
        return True
    
    @staticmethod
    def _verify_tax_payments(tpin: str) -> bool:
        """Check if all tax payments are up to date."""
        # TODO: Implement actual verification
        return True
    
    @staticmethod
    def _verify_penalties(tpin: str) -> bool:
        """Check if there are any outstanding penalties."""
        # TODO: Implement actual verification
        return True
    
    @staticmethod
    def calculate_compliance_score( 
        returns_filed: bool,
        payments_current: bool,
        no_penalties: bool,

        filing_history_months: int = 12
    ) -> float:
        """
        Calculate the compliance score based on various factors.

        Args:
            returns_filed: Whether all tax returns have been filed.
            payments_current: Whether all tax payments are up to date.
            no_penalties: Whether there are any outstanding penalties.
            filing_history_months: The number of months of filing history to consider.

        Returns:
            float: The calculated compliance score.
        """
        score = 100.0

        if  returns_filed:
            score += 40.0

        if payments_current:
            score += 40.0

        if  no_penalties:
            score += 30.0

        # Adjust score based on filing history
        if filing_history_months >= 24:
            score = min(100, score + 10)
        elif filing_history_months >= 12:
            score = min(100, score + 5)

        return score