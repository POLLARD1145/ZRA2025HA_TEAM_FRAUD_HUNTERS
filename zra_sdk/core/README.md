# ZRA SDK Core Module

## Overview

The core module provides the foundational functionality for ZRA tax verification and taxpayer management. It includes tax verification logic, taxpayer data models, and compliance checking.

## Structure

```
core/
├── tax_verification/       # Tax verification and compliance checking
│   ├── base_verifier.py   # Abstract base class for all tax verifiers
│   ├── vat_verifier.py    # VAT-specific verification logic
│   ├── paye_verifier.py   # PAYE-specific verification logic (TODO)
│   ├── verifier.py        # Main tax verification service
│   ├── constants.py       # Enums and constants
│   ├── validators.py      # Input validation functions
│   └── exceptions.py      # Custom exception classes
│
└── taxpayer/              # Taxpayer domain logic
    ├── models.py          # Re-exports from models package
    └── status.py          # Compliance checking logic
```

## Features

### 1. Tax Verification

Verify tax filings and payments for different tax types:

- ✅ **VAT (Value Added Tax)**
- 🚧 **PAYE (Pay As You Earn)** - In progress
- 📋 **WHT (Withholding Tax)** - Planned
- 📋 **ITX (Income Tax)** - Planned

### 2. TPIN Validation

Validates Zambian Taxpayer Identification Numbers:

- Format validation (10 digits)
- Prefix validation (must start with 1, 2, or 3)
- Checksum validation (placeholder - awaiting ZRA specification)

### 3. Due Date Calculation

Calculates tax filing due dates based on:

- Tax type
- Filing mode (manual vs electronic)
- Filing period

### 4. Compliance Checking

Monitors taxpayer compliance status:

- Tax returns filing status
- Payment history
- Outstanding penalties
- Compliance score (0-100)

## Usage Examples

### Basic Tax Verification

```python
from zra_sdk.core.tax_verification import TaxVerificationService
from zra_sdk.core.tax_verification.constants import TaxType, FilingMode
from datetime import date

# Initialize service
service = TaxVerificationService(api_key="your_api_key")

# Verify VAT payment
result = await service.verify_tax_payment(
    tpin="1234567890",
    tax_type=TaxType.VAT,
    tax_period="2025-09",
    amount=5000.00,
    filing_mode="electronic",
    filed_on=date(2025, 10, 15)
)

print(result)
# Output:
# {
#     "tpin": "1234567890",
#     "status": "VERIFIED",
#     "compliance": "COMPLIANT",
#     "filed_on": "2025-10-15",
#     "due_date": "2025-10-18",
#     "tax_type": "Value Added Tax",
#     "tax_period": "2025-09",
#     "amount": 5000.00
# }
```

### TPIN Validation

```python
from zra_sdk.core.tax_verification.validators import validate_tpin
from zra_sdk.core.tax_verification.exceptions import InvalidTPINError

try:
    validate_tpin("1234567890")  # Valid TPIN
    print("TPIN is valid")
except InvalidTPINError as e:
    print(f"Invalid TPIN: {e}")
```

### Compliance Checking

```python
from zra_sdk.core.taxpayer import ComplianceChecker

checker = ComplianceChecker()
compliance = checker.verify_compliance(
    tpin="1234567890",
    tax_returns=True,
    tax_payments=True,
    penalties=True
)

print(f"Status: {compliance.status.value}")
print(f"Score: {compliance.score}/100")
print(f"Issues: {compliance.issues}")
```

### Using Tax Verifiers Directly

```python
from zra_sdk.core.tax_verification import VATVerifier
from zra_sdk.core.tax_verification.constants import FilingMode
from datetime import date

verifier = VATVerifier()

# Calculate due date
due_date = verifier.get_due_date(
    filing_mode=FilingMode.ELECTRONIC,
    filing_period=date(2025, 9, 1)
)
print(f"Due date: {due_date}")  # 2025-10-18

# Verify filing
result = verifier.verify(
    tpin="1234567890",
    filing_mode=FilingMode.ELECTRONIC,
    filing_period=date(2025, 9, 1),
    filed_on=date(2025, 10, 15)
)
```

## Tax Types and Filing Rules

### VAT (Value Added Tax)

| Filing Mode | Due Date Rule      |
| ----------- | ------------------ |
| Manual      | 5th of next month  |
| Electronic  | 18th of next month |

**Example**: For September 2025 (filing period):

- Manual filing due: October 5, 2025
- Electronic filing due: October 18, 2025

### PAYE (Pay As You Earn)

🚧 **In Development**

## Data Models

All data models are defined in `models/taxpayer.py` and re-exported through `core/taxpayer/models.py`.

### Key Models

- **`Taxpayer`** - Complete taxpayer information
- **`TaxRegistration`** - Tax type registration details
- **`ComplianceRecord`** - Compliance status and history
- **`Address`** - Physical/postal address
- **`Contact`** - Contact information

See `models/README.md` for detailed model documentation.

## Constants and Enums

### Tax Types

```python
from zra_sdk.core.tax_verification.constants import TaxType

TaxType.VAT      # Value Added Tax
TaxType.PAYE     # Pay As You Earn
TaxType.WHT      # Withholding Tax
TaxType.ITX      # Income Tax
TaxType.PTT      # Property Transfer Tax
TaxType.TLEVY    # Tourism Levy
TaxType.MINRYL   # Mineral Royalty
```

### Verification Status

```python
from zra_sdk.core.tax_verification.constants import VerificationStatus

VerificationStatus.VERIFIED    # Successfully verified
VerificationStatus.PENDING     # Awaiting verification
VerificationStatus.REJECTED    # Verification failed
VerificationStatus.EXPIRED     # Verification expired
VerificationStatus.NOT_FOUND   # Record not found
```

### Compliance Status

```python
from zra_sdk.core.tax_verification.constants import ComplianceStatus

ComplianceStatus.COMPLIANT            # Fully compliant
ComplianceStatus.NON_COMPLIANT        # Non-compliant
ComplianceStatus.UNDER_INVESTIGATION  # Under investigation
ComplianceStatus.DEFAULTER            # Defaulter status
```

### Filing Mode

```python
from zra_sdk.core.tax_verification.constants import FilingMode

FilingMode.MANUAL       # Manual filing
FilingMode.ELECTRONIC   # Electronic filing
```

## Exception Handling

All exceptions inherit from `TaxVerificationError`:

```python
from zra_sdk.core.tax_verification.exceptions import (
    TaxVerificationError,      # Base exception
    InvalidTPINError,          # Invalid TPIN format
    TPINNotFoundError,         # TPIN not found
    InvalidDocumentError,      # Invalid document/period
    TaxComplianceError,        # Compliance issues
    VerificationTimeoutError,  # Verification timeout
    RateLimitExceededError,    # Rate limit exceeded
    AuthenticationError,       # API authentication failed
)

try:
    result = await service.verify_taxpayer("invalid")
except InvalidTPINError as e:
    print(f"TPIN validation failed: {e}")
except TPINNotFoundError as e:
    print(f"TPIN not found: {e}")
except TaxVerificationError as e:
    print(f"Verification error: {e}")
```

## Configuration

Key configuration constants in `constants.py`:

```python
TPIN_LENGTH = 10                          # TPIN length
TPIN_PREFIX = ["1", "2", "3"]            # Valid prefixes
VAT_REGISTRATION_THRESHOLD = 800_000      # ZMW threshold
VERIFICATION_TIMEOUT = 30                 # Seconds
CACHE_TIMEOUT = 3600                      # 1 hour
MAX_REQUESTS_PER_MINUTE = 60             # Rate limit
MAX_REQUESTS_PER_DAY = 1000              # Daily rate limit
```

## Testing

Run tests for the core module:

```bash
# Run all core tests
pytest zra_sdk/tests/core/

# Run specific test file
pytest zra_sdk/tests/core/test_validators.py

# Run with coverage
pytest --cov=zra_sdk.core --cov-report=html
```

## TODO / Roadmap

### High Priority

- [ ] Implement actual ZRA API integration
- [ ] Complete PAYE verifier implementation
- [ ] Add WHT (Withholding Tax) verifier
- [ ] Implement TPIN checksum validation (awaiting ZRA spec)
- [ ] Add caching layer for verification results

### Medium Priority

- [ ] Add ITX (Income Tax) verifier
- [ ] Implement rate limiting
- [ ] Add retry logic for API calls
- [ ] Enhanced error messages and logging

### Low Priority

- [ ] Add PTT (Property Transfer Tax) verifier
- [ ] Add Tourism Levy verifier
- [ ] Add Mineral Royalty verifier
- [ ] Performance optimization

## Contributing

When contributing to the core module:

1. **Follow the pattern**: Use `BaseTaxVerifier` for new tax types
2. **Write tests**: Add tests for all new functionality
3. **Update docs**: Update this README with new features
4. **Type hints**: Always include proper type hints
5. **Error handling**: Use appropriate custom exceptions
6. **Validation**: Validate all inputs

### Adding a New Tax Verifier

```python
# 1. Create verifier class
from .base_verifier import BaseTaxVerifier
from .constants import FilingMode

class NewTaxVerifier(BaseTaxVerifier):
    FILING_RULES = {
        FilingMode.MANUAL: 10,
        FilingMode.ELECTRONIC: 20
    }

    def get_due_date(self, filing_mode: FilingMode, filing_period: date) -> date:
        # Implement due date logic
        pass

    def verify(self, tpin: str, filing_mode: FilingMode,
               filing_period: date, filed_on: Optional[date] = None) -> Dict[str, Any]:
        # Implement verification logic
        pass

# 2. Register in TaxVerificationService
self._verifiers[TaxType.NEW_TAX] = NewTaxVerifier()
```

## Architecture Notes

### Design Patterns Used

1. **Abstract Base Class Pattern** - `BaseTaxVerifier` ensures consistent interface
2. **Strategy Pattern** - Different verifiers for different tax types
3. **Service Layer Pattern** - `TaxVerificationService` orchestrates operations
4. **Repository Pattern** - Models separated from business logic

### Separation of Concerns

- **Validation** - `validators.py` handles all input validation
- **Business Logic** - Verifiers handle tax-specific logic
- **Data Models** - `models/` contains all data structures
- **Exceptions** - `exceptions.py` defines all error types

## References

- [ZRA Official Website](https://www.zra.org.zm)
- [ZRA e-Services Portal](https://www.zra.org.zm/eservices)
- ZRA API Documentation (internal)

## Questions or Issues?

Contact the development team or create an issue in the repository.

---

**Last Updated**: 2025-10-17  
**Module Version**: 0.1.0  
**Maintained by**: Team Fraud Hunters
