from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class Taxpayer:
    """Taxpayer data model"""
    tpin: str
    name: str
    business_name: str
    email: str
    phone: str
    status: str  # Active, Inactive, Suspended
    registration_date: str
    last_filing_date: Optional[str] = None
    tax_center: Optional[str] = None
    
    @classmethod
    def from_json(cls, data: dict) -> 'Taxpayer':
        """Create Taxpayer instance from JSON response"""
        return cls(
            tpin=data.get('tpin', ''),
            name=data.get('name', ''),
            business_name=data.get('business_name', ''),
            email=data.get('email', ''),
            phone=data.get('phone', ''),
            status=data.get('status', 'Unknown'),
            registration_date=data.get('registration_date', ''),
            last_filing_date=data.get('last_filing_date'),
            tax_center=data.get('tax_center')
        )

@dataclass
class TaxCalculation:
    """Tax calculation result model"""
    gross_income: float
    taxable_income: float
    tax_amount: float
    tax_breakdown: dict
    effective_tax_rate: float
