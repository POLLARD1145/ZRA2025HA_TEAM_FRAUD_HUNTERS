"""
Canonical taxpayer data models for ZRA SDK.
"""
from datetime import datetime, date
from typing import Any, Optional, List,Dict
from pydantic import BaseModel, Field, validator
from enum import Enum

from ..core.tax_verification.constants import TaxType, ComplianceStatus


class Address(BaseModel):
    """Physical address of a taxpayer."""
    street: str = Field(..., description="Street address")
    city: str = Field(..., description="City")
    province: str = Field(..., description="Province")
    postal_code: Optional[str] = Field(None, description="Postal code")
    country: str = Field("Zambia", description="Country")
    class Config:
        """Pydantic model configuration."""
        json_schema_extra = {
            "example": {
                "street": "123 Cairo Road",
                "city": "Lusaka",
                "province": "Lusaka",
                "postal_code": "10101",
                "country": "Zambia",
            }
        }

class Contact(BaseModel):
    """Contact information for a taxpayer."""
    email: Optional[str] = Field(None, description="Email address")
    phone: Optional[str] = Field(None, description="Phone number")
    mobile: Optional[str] = Field(None, description="Mobile number")
    fax: Optional[str] = Field(None, description="Fax number")  
    class Config:
        """Pydantic model configuration."""
        json_schema_extra = {
            "example": {
                "email": "taxpayer@example.com",
                "phone": "+260211234567",
                "mobile": "+260971234567",
                "fax": "+260211234568",
            }
        }

class TaxRegistration(BaseModel):
    """Tax type registration details."""
    tax_type: TaxType = Field(..., description="Type of tax")
    registration_date: datetime = Field(..., description="Date of registration")
    registration_number: str = Field(..., description="Registration number")
    status: bool = Field(True, description="Registration status")
    last_filing_date: Optional[datetime] = Field(None, description="Date of last filing")
    next_filing_due: Optional[datetime] = Field(None, description="Date of next filing due")
    class Config:
        """Pydantic model configuration."""
        json_schema_extra = {
            "example": {
                "tax_type": "VAT",
                "registration_date": "2023-01-15T00:00:00",
                "registration_number": "VAT123456",
                "status": True,
                "last_filing_date": "2023-05-31T00:00:00",
                "next_filing_due": "2023-08-18T00:00:00",
            }
        }


class ComplianceRecord(BaseModel):
    """Tax compliance record."""
    status: ComplianceStatus = Field(..., description="Compliance status")
    last_verified: datetime = Field(..., description="Last verified date")
    valid_until: datetime = Field(..., description="Validity period until")
    issues: List[str] = Field(default_factory=list, description="List of compliance issues")
    score: Optional[float] = Field(None, description="Compliance score")
    
    class Config:
        """Pydantic model configuration."""
        json_schema_extra = {
            "example": {
                "status": "COMPLIANT",
                "last_verified": "2023-06-01T00:00:00",
                "valid_until": "2023-07-01T00:00:00",
                "issues": [],
                "score": 95.5
            }
        }
        @property
        def is_valid(self) -> bool:
            """Check if the compliance record is still valid."""
            return datetime.utcnow() < self.valid_until
        @property
        def is_compliant(self) -> bool:
            """Check if the taxpayer is compliant."""
            return self.status == ComplianceStatus.COMPLIANT

class BusinessCategory(str, Enum):
    """Business Category Classification."""
    SOLE_PROPRIETORSHIP = "Sole Proprietorship"
    PARTNERSHIP = "Partnership"
    CORPORATION = "Corporation"
    COOPERATIVE = "Cooperative"
    TRUST = "Trust"
    NON_PROFIT = "Non-Profit Organization"
    OTHER = "Other"


class Taxpayer(BaseModel):
    """Main taxpayer model."""
    tpin: str = Field(..., description="Taxpayer Identification Number")
    name: str  = Field(..., description="Full name of the taxpayer")
    business_name: Optional[str] = Field(None, description="Business name of the taxpayer")
    business_category: Optional[BusinessCategory] = Field(None, description="Business category classification")
    
    registration_date: datetime = Field(..., description="Date of registration")
    
    address: Address = Field(..., description="Address of the taxpayer")
    contact: Contact = Field(..., description="Contact information of the taxpayer")
    tax_registrations: List[TaxRegistration] = Field(default_factory=list, description="List of tax registrations")
    compliance: Optional[ComplianceRecord] = Field(None, description="Tax compliance record")
    
    is_active: bool = Field(True, description="Indicates if the taxpayer is active")
    is_verified: bool = Field(False, description="Indicates if the taxpayer has been verified")

    meta_data: Dict[str,Any] = Field(default_factory=dict, description="Additional metadata about the taxpayer")
    
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Record creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Record last update timestamp")
    
    
    class Config:
        """Pydantic model configuration."""
        json_schema_extra = {
            "example": {
                "tpin": "1234567890",
                "name": "John Doe",
                "business_name": "JD Enterprises",
                "business_category": "Sole Proprietorship",
                "registration_date": "2025-01-01T00:00:00",
                "address": {
                    "street": "123 Cairo Road",
                    "city": "Lusaka",
                    "province": "Lusaka",
                    "postal_code": "10101",
                    "country": "Zambia",
                },
                "contact": {
                    "email": "john.doe@example.com",
                    "phone": "+260211234567",
                    "mobile": "+260971234567",
                },
                "tax_registrations": [
                    {
                        "tax_type": "VAT",
                        "registration_date": "2023-01-15T00:00:00",
                        "registration_number": "VAT123456",
                        "status": True,
                        "last_filing_date": "2023-05-31T00:00:00",
                        "next_filing_due": "2023-08-18T00:00:00",
                    }
                ],
                "is_active": True,
                "is_verified": False,
            }
        }
    @validator("tpin")
    def validate_tpin_format(cls, v):
        """ Validate TPIN format."""
        if not v.isdigit() or len(v) != 10:
            raise ValueError("TPIN must be a 10-digit numeric string.")
        if v[0] not in ['1','2','3']:
            raise ValueError("TPIN must start with a valid prefix digit.")
        return v
    def get_tax_registration(self, tax_type: TaxType) -> Optional[TaxRegistration]:
        """Retrieve tax registration for a specific tax type."""
        for registration in self.tax_registrations:
            if registration.tax_type == tax_type:
                return registration
        return None
    
    def is_registered_for(self, tax_type: TaxType) -> bool:
        """Check if taxpayer is registered for a specific tax type."""
        registration = self.get_tax_registration(tax_type)
        return registration is not None and registration.status
    
    def update_compliance(self, compliance_record: ComplianceRecord) -> None:
        """Update the taxpayer's compliance record."""
        self.compliance = compliance_record
        self.updated_at = datetime.utcnow()

    @property
    def is_compliant(self) -> bool:
        """Check if the taxpayer is compliant."""
        return self.compliance.is_compliant if self.compliance else False
    
__all__ = ["Taxpayer", "TaxRegistration", "Address", "Contact", "ComplianceRecord", "BusinessCategory"]