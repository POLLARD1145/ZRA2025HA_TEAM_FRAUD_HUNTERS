#!/usr/bin/env python3
"""
Basic demonstration of ZRA SDK usage
"""

import sys
import os

# FIX: Add the current directory to Python path so it can find the modules
sys.path.insert(0, os.getcwd())

# FIX: Import directly from the submodules instead of top-level package
from api.taxpayer_api import verify_taxpayer, calculate_tax

def main():
    print("🚀 ZRA SDK Basic Demo")
    print("=" * 50)
    
    # Verify a taxpayer
    taxpayer = verify_taxpayer("123456789")
    print(f"Taxpayer: {taxpayer.name}")
    print(f"Status: {taxpayer.status}")
    print(f"Business: {taxpayer.business_name}")
    print(f"Email: {taxpayer.email}")
    
    print("\n" + "-" * 50)
    
    # Calculate tax
    tax_calc = calculate_tax(15000, "income")
    print(f"Tax Amount: ZMW {tax_calc.tax_amount}")
    print(f"Gross Income: ZMW {tax_calc.gross_income:,.2f}")
    print(f"Effective Tax Rate: {tax_calc.effective_tax_rate}%")

if __name__ == "__main__":
    main()