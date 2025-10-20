import re

def validate_tpin(tpin: str) -> bool:
    """
    Validate Taxpayer Identification Number format
    TPIN format: 9 digits (according to ZRA standards)
    """
    if not tpin or not isinstance(tpin, str):
        return False
    
    # Remove any spaces or dashes
    clean_tpin = re.sub(r'[\s-]', '', tpin)
    
    # Check if it's exactly 9 digits
    return len(clean_tpin) == 9 and clean_tpin.isdigit()

def validate_phone(phone: str) -> bool:
    """Validate Zambian phone number format"""
    pattern = r'^(\+260|0)[0-9]{9}$'
    return bool(re.match(pattern, phone))

def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))