#!/usr/bin/env python3
"""
Test compliance checking functionality
"""

import sys
import os
sys.path.insert(0, os.getcwd())

from api.taxpayer_api import check_compliance, get_compliance_report, verify_taxpayer

def test_compliance_check():
    """Test compliance checking for all taxpayers"""
    taxpayers = [
        "123456789",  # John Banda - Fully Compliant
        "111222333",  # Pollard Samba - Minor Issues  
        "444555666",  # Ebenezer Kaluba - Non-Compliant
        "777888999",  # Saviour Silwamba - Fully Compliant
        "222333444",  # Pethias Kasempa - Under Review
        "555666777",  # Lawrence Thor - Minor Issues
    ]
    
    print("🔍 ZRA SDK - Compliance Check Demo")
    print("=" * 70)
    
    for tpin in taxpayers:
        try:
            # Get taxpayer info
            taxpayer = verify_taxpayer(tpin)
            
            # Check compliance
            compliance = check_compliance(tpin)
            
            print(f"\n📋 TPIN: {tpin}")
            print(f"   👤 {taxpayer.name} - {taxpayer.business_name}")
            print(f"   🎯 Compliance Status: {compliance['compliance_status']}")
            print(f"   📊 Compliance Score: {compliance['compliance_score']}/100")
            print(f"   ⚠️  Risk Level: {compliance['risk_level']}")
            print(f"   📝 Outstanding Returns: {compliance['outstanding_returns']}")
            print(f"   💰 Outstanding Payments: ZMW {compliance['outstanding_payments']:,.2f}")
            print(f"   💸 Penalties: ZMW {compliance['penalties']:,.2f}")
            
            if compliance['compliance_issues']:
                print(f"   ❌ Issues: {', '.join(compliance['compliance_issues'])}")
            else:
                print(f"   ✅ No compliance issues")
                
        except Exception as e:
            print(f"❌ Error with TPIN {tpin}: {e}")

def test_comprehensive_report():
    """Test comprehensive compliance reporting"""
    print("\n" + "=" * 70)
    print("📊 COMPREHENSIVE COMPLIANCE REPORTS")
    print("=" * 70)
    
    test_tpins = ["444555666", "123456789"]  # Non-compliant vs Compliant
    
    for tpin in test_tpins:
        report = get_compliance_report(tpin)
        
        print(f"\n📄 Compliance Report for: {report['taxpayer_info']['name']}")
        print(f"   Business: {report['taxpayer_info']['business_name']}")
        print(f"   TPIN: {report['taxpayer_info']['tpin']}")
        print(f"   📍 Tax Center: {report['taxpayer_info']['tax_center']}")
        
        comp = report['compliance_summary']
        print(f"\n   🎯 COMPLIANCE SUMMARY:")
        print(f"      Status: {comp['compliance_status']}")
        print(f"      Score: {comp['compliance_score']}/100")
        print(f"      Risk: {comp['risk_level']}")
        print(f"      Outstanding Returns: {comp['outstanding_returns']}")
        print(f"      Outstanding Payments: ZMW {comp['outstanding_payments']:,.2f}")
        
        print(f"\n   💡 RECOMMENDATIONS:")
        for i, recommendation in enumerate(report['recommendations'], 1):
            print(f"      {i}. {recommendation}")
        
        print(f"   📅 Report Generated: {report['report_generated']}")

if __name__ == "__main__":
    test_compliance_check()
    test_comprehensive_report()
    print("\n🎉 Compliance checking demo completed!")