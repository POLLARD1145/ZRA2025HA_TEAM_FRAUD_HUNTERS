# ZRA SDK Data Models

## Overview

This package contains all Pydantic data models used throughout the ZRA SDK. These models provide type safety, validation, and serialization for taxpayer information, tax registrations, and compliance records.

## Models

### Taxpayer

Complete taxpayer information model.

```python
from zra_sdk.models import Taxpayer

taxpayer = Taxpayer(
    tpin="1234567890",
    name="Example Business Ltd",
    business_name="Example Trading",
    business_category="Company",
    registration_date="2024-01-15T00:00:00",
    address={
        "street": "Independence Avenue",
        "city": "Lusaka",
        "province": "Lusaka",
        "country": "Zambia"
    },
    contact={
        "email": "info@example.zm",
        "phone": "+260211123456"
    }
)

# Check if registered for VAT
is_vat_registered = taxpayer.is_registered_for(TaxType.VAT)

# Check compliance status
if taxpayer.is_compliant:
    print("Taxpayer is compliant")
```

**Fields:**

- `tpin` (str) - 10-digit Taxpayer Identification Number
- `name` (str) - Legal or trading name
- `business_name` (Optional[str]) - Business or trading name
- `business_category` (Optional[BusinessCategory]) - Business category
- `registration_date` (datetime) - TPIN registration date
- `address` (Address) - Physical address
- `postal_address` (Optional[Address]) - Postal address
- `contact` (Contact) - Contact information
- `tax_registrations` (List[TaxRegistration]) - List of tax type registrations
- `compliance` (Optional[ComplianceRecord]) - Compliance status
- `is_active` (bool) - Account active status
- `is_verified` (bool) - Verification status
- `metadata` (Dict[str, Any]) - Additional metadata

**Methods:**

- `get_tax_registration(tax_type)` - Get registration for specific tax type
- `is_registered_for(tax_type)` - Check if registered for tax type
- `update_compliance(compliance)` - Update compliance record

**Properties:**

- `is_compliant` - Check if currently compliant

### Address

Physical or postal address information.

```python
from zra_sdk.models import Address

address = Address(
    street="Independence Avenue",
    city="Lusaka",
    province="Lusaka",
    postal_code="10101",
    country="Zambia"
)
```

**Fields:**

- `street` (str) - Street address
- `city` (str) - City or town
- `province` (str) - Province
- `postal_code` (Optional[str]) - Postal code
- `country` (str) - Country (default: "Zambia")

### Contact

Contact information for taxpayer.

```python
from zra_sdk.models import Contact

contact = Contact(
    email="taxpayer@example.com",
    phone="+260211123456",
    mobile="+260977123456"
)
```

**Fields:**

- `email` (Optional[str]) - Email address
- `phone` (Optional[str]) - Phone number
- `mobile` (Optional[str]) - Mobile number
- `fax` (Optional[str]) - Fax number

### TaxRegistration

Tax type registration details.

```python
from zra_sdk.models import TaxRegistration
from zra_sdk.core.tax_verification.constants import TaxType

registration = TaxRegistration(
    tax_type=TaxType.VAT,
    registration_date="2024-01-15T00:00:00",
    registration_number="VAT123456",
    status=True
)
```

**Fields:**

- `tax_type` (TaxType) - Type of tax
- `registration_date` (datetime) - Date of registration
- `registration_number` (Optional[str]) - Registration number
- `status` (bool) - Active status
- `expiry_date` (Optional[date]) - Registration expiry date

### ComplianceRecord

Tax compliance record and status.

```python
from zra_sdk.models import ComplianceRecord
from zra_sdk.core.tax_verification.constants import ComplianceStatus

compliance = ComplianceRecord(
    status=ComplianceStatus.COMPLIANT,
    last_verified="2025-10-16T10:00:00",
    valid_until="2025-11-01T00:00:00",
    issues=[],
    score=95
)

# Check validity
if compliance.is_valid:
    print("Compliance record is still valid")

if compliance.is_compliant:
    print("Taxpayer is compliant")
```

**Fields:**

- `status` (ComplianceStatus) - Compliance status
- `last_verified` (datetime) - Last verification timestamp
- `valid_until` (datetime) - Validity expiration
- `issues` (List[str]) - List of compliance issues
- `score` (Optional[int]) - Compliance score (0-100)

**Properties:**

- `is_valid` - Check if record is still valid
- `is_compliant` - Check if taxpayer is compliant

### BusinessCategory

Enumeration of business categories.

```python
from zra_sdk.models import BusinessCategory

category = BusinessCategory.COMPANY

# Available categories:
# - SOLE_PROPRIETOR
# - PARTNERSHIP
# - COMPANY
# - TRUST
# - COOPERATIVE
# - NGO
# - GOVERNMENT
# - OTHER
```

## Validation

All models include automatic validation:

### TPIN Validation

```python
from zra_sdk.models import Taxpayer

# Valid TPIN
taxpayer = Taxpayer(tpin="1234567890", ...)  # OK

# Invalid - too short
taxpayer = Taxpayer(tpin="123", ...)
# ValueError: TPIN must be exactly 10 digits

# Invalid - wrong prefix
taxpayer = Taxpayer(tpin="9234567890", ...)
# ValueError: TPIN must start with 1, 2, or 3

# Invalid - non-numeric
taxpayer = Taxpayer(tpin="123ABC7890", ...)
# ValueError: TPIN must contain only digits
```

### Field Validation

```python
from zra_sdk.models import ComplianceRecord

# Valid score
record = ComplianceRecord(score=95, ...)  # OK

# Invalid score
record = ComplianceRecord(score=150, ...)
# ValidationError: score must be <= 100
```

## Serialization

All models support JSON serialization:

```python
from zra_sdk.models import Taxpayer

# Create taxpayer
taxpayer = Taxpayer(...)

# Serialize to dict
data = taxpayer.dict()

# Serialize to JSON
json_str = taxpayer.json()

# Deserialize from dict
taxpayer = Taxpayer(**data)

# Deserialize from JSON
taxpayer = Taxpayer.parse_raw(json_str)
```

## Usage with API

Models are designed to work seamlessly with API responses:

```python
# API response
response_data = {
    "tpin": "1234567890",
    "name": "Example Business Ltd",
    "address": {...},
    "contact": {...}
}

# Create model from API response
taxpayer = Taxpayer(**response_data)

# Use model
if taxpayer.is_active:
    print(f"Taxpayer {taxpayer.name} is active")
```

## Best Practices

### 1. Always Use Type Hints

```python
from zra_sdk.models import Taxpayer, TaxRegistration
from typing import List

def process_taxpayers(taxpayers: List[Taxpayer]) -> None:
    for taxpayer in taxpayers:
        print(taxpayer.name)
```

### 2. Handle Validation Errors

```python
from pydantic import ValidationError
from zra_sdk.models import Taxpayer

try:
    taxpayer = Taxpayer(**data)
except ValidationError as e:
    print(f"Validation failed: {e}")
```

### 3. Use Model Methods

```python
# Good - use built-in methods
if taxpayer.is_registered_for(TaxType.VAT):
    registration = taxpayer.get_tax_registration(TaxType.VAT)

# Avoid - manual iteration
for reg in taxpayer.tax_registrations:
    if reg.tax_type == TaxType.VAT:
        ...
```

### 4. Update Models Properly

```python
# Good - use update methods
taxpayer.update_compliance(new_compliance)

# Also good - direct assignment with updated_at
taxpayer.compliance = new_compliance
taxpayer.updated_at = datetime.utcnow()
```

## Testing

Example test for models:

```python
import pytest
from zra_sdk.models import Taxpayer, Address, Contact
from pydantic import ValidationError

def test_taxpayer_creation():
    taxpayer = Taxpayer(
        tpin="1234567890",
        name="Test Business",
        registration_date="2024-01-15T00:00:00",
        address=Address(
            street="Test St",
            city="Lusaka",
            province="Lusaka"
        ),
        contact=Contact(email="test@example.com")
    )
    assert taxpayer.tpin == "1234567890"
    assert taxpayer.is_active

def test_invalid_tpin():
    with pytest.raises(ValidationError):
        Taxpayer(
            tpin="123",  # Too short
            name="Test",
            registration_date="2024-01-15T00:00:00",
            address=Address(...),
            contact=Contact()
        )
```

## Model Schema

All models provide JSON schema:

```python
from zra_sdk.models import Taxpayer

# Get JSON schema
schema = Taxpayer.schema()
print(schema)
```

## Dependencies

Models use [Pydantic](https://docs.pydantic.dev/) for validation and serialization:

- Automatic validation
- Type safety
- JSON serialization
- Schema generation
- IDE support

---

**Last Updated**: 2025-10-17  
**Package Version**: 0.1.0  
**Maintained by**: Team Fraud Hunters
