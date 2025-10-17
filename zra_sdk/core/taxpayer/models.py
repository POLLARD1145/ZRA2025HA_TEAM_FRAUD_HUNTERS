"""
Compatibility layer re-exporting taxpayer models from zra_sdk.models.
"""
from ...models.taxpayer import (
    Address,
    Contact,
    TaxRegistration,
    ComplianceRecord,
    BusinessCategory,
    Taxpayer,
)

__all__ = [
    "Address",
    "Contact",
    "TaxRegistration",
    "ComplianceRecord",
    "Taxpayer",
    "BusinessCategory",
]