from typing import Optional, Dict, Any, List
from models.taxpayer import Taxpayer, TaxCalculation
from utils.validators import validate_tpin
import random
from datetime import datetime

def verify_taxpayer(tpin: str) -> Taxpayer:
    """
    Verify taxpayer information using TPIN
    """
    if not validate_tpin(tpin):
        raise ValueError("Invalid TPIN format. Must be 9 digits.")
    
    # Mock database of taxpayers
    taxpayer_database = {
        "123456789": {
            "tpin": "123456789",
            "name": "John Banda",
            "business_name": "Banda Enterprises Ltd",
            "email": "john.banda@bandaenterprises.co.zm",
            "phone": "+260977123456",
            "status": "Active",
            "registration_date": "2022-01-15",
            "last_filing_date": "2024-01-10",
            "tax_center": "Lusaka"
        },
        "111222333": {
            "tpin": "111222333",
            "name": "Pollard Samba",
            "business_name": "Samba Tech Solutions",
            "email": "pollard.samba@sambatech.co.zm",
            "phone": "+260966789123",
            "status": "Active",
            "registration_date": "2021-03-20",
            "last_filing_date": "2024-02-15",
            "tax_center": "Ndola"
        },
        "444555666": {
            "tpin": "444555666",
            "name": "Ebenezer Kaluba",
            "business_name": "Kaluba Holdings Limited",
            "email": "e.kaluba@kalubaholdings.co.zm",
            "phone": "+260955456789",
            "status": "Active",
            "registration_date": "2020-11-08",
            "last_filing_date": "2024-03-01",
            "tax_center": "Kitwe"
        },
        "777888999": {
            "tpin": "777888999",
            "name": "Saviour Silwamba",
            "business_name": "Silwamba Legal Practitioners",
            "email": "saviour@silwambalaw.co.zm",
            "phone": "+260978321654",
            "status": "Active",
            "registration_date": "2019-07-12",
            "last_filing_date": "2024-01-25",
            "tax_center": "Lusaka"
        },
        "222333444": {
            "tpin": "222333444",
            "name": "Pethias Kasempa",
            "business_name": "Kasempa Mining Supplies",
            "email": "p.kasempa@kasempamining.co.zm",
            "phone": "+260967852741",
            "status": "Active",
            "registration_date": "2023-05-30",
            "last_filing_date": "2024-02-28",
            "tax_center": "Chingola"
        },
        "555666777": {
            "tpin": "555666777",
            "name": "Lawrence Thor",
            "business_name": "ThorLabs Innovations",
            "email": "lawrence.thor@thorlabs.co.zm",
            "phone": "+260965123789",
            "status": "Active",
            "registration_date": "2022-09-14",
            "last_filing_date": "2024-03-10",
            "tax_center": "Livingstone"
        }
    }
    
    if tpin in taxpayer_database:
        mock_response = taxpayer_database[tpin]
    else:
        mock_response = {
            "tpin": tpin,
            "name": "Taxpayer Name",
            "business_name": "Registered Business",
            "email": f"taxpayer{tpin}@business.co.zm",
            "phone": "+260900000000",
            "status": "Active",
            "registration_date": "2023-01-01",
            "last_filing_date": "2024-01-01",
            "tax_center": "Lusaka"
        }
    
    return Taxpayer.from_json(mock_response)

def calculate_tax(income: float, tax_type: str = "income") -> TaxCalculation:
    """
    Calculate tax amount based on income and tax type
    """
    if income < 0:
        raise ValueError("Income must be positive")
    
    if tax_type == "income":
        if income <= 4800:
            tax_amount = 0
        elif income <= 6000:
            tax_amount = (income - 4800) * 0.25
        elif income <= 12000:
            tax_amount = 300 + (income - 6000) * 0.30
        else:
            tax_amount = 2100 + (income - 12000) * 0.37
    else:
        tax_amount = income * 0.16
    
    return TaxCalculation(
        gross_income=income,
        taxable_income=income,
        tax_amount=round(tax_amount, 2),
        tax_breakdown={"base_tax": tax_amount},
        effective_tax_rate=round((tax_amount / income) * 100, 2) if income > 0 else 0
    )

def check_compliance(tpin: str) -> Dict[str, Any]:
    """
    Check taxpayer compliance status
    """
    if not validate_tpin(tpin):
        raise ValueError("Invalid TPIN format. Must be 9 digits.")
    
    compliance_data = {
        "123456789": {
            "compliance_status": "Fully Compliant",
            "compliance_score": 95,
            "outstanding_returns": 0,
            "outstanding_payments": 0.0,
            "last_audit_date": "2023-11-15",
            "next_audit_due": "2024-11-15",
            "risk_level": "Low",
            "compliance_issues": [],
            "penalties": 0.0
        },
        "111222333": {
            "compliance_status": "Mostly Compliant",
            "compliance_score": 78,
            "outstanding_returns": 1,
            "outstanding_payments": 1500.0,
            "last_audit_date": "2023-09-20",
            "next_audit_due": "2024-09-20",
            "risk_level": "Medium",
            "compliance_issues": ["Q4 2023 VAT Return overdue"],
            "penalties": 250.0
        },
        "444555666": {
            "compliance_status": "Non-Compliant",
            "compliance_score": 45,
            "outstanding_returns": 3,
            "outstanding_payments": 12500.0,
            "last_audit_date": "2022-12-10",
            "next_audit_due": "2024-06-10",
            "risk_level": "High",
            "compliance_issues": [
                "Q3 2023 Income Tax overdue",
                "Q4 2023 VAT Return overdue", 
                "Q1 2024 PAYE Return overdue"
            ],
            "penalties": 1800.0
        },
        "777888999": {
            "compliance_status": "Fully Compliant", 
            "compliance_score": 98,
            "outstanding_returns": 0,
            "outstanding_payments": 0.0,
            "last_audit_date": "2024-01-05",
            "next_audit_due": "2025-01-05",
            "risk_level": "Low",
            "compliance_issues": [],
            "penalties": 0.0
        },
        "222333444": {
            "compliance_status": "Under Review",
            "compliance_score": 65,
            "outstanding_returns": 2,
            "outstanding_payments": 7500.0,
            "last_audit_date": "2023-08-15",
            "next_audit_due": "2024-08-15", 
            "risk_level": "Medium",
            "compliance_issues": [
                "Q4 2023 Income Tax overdue",
                "Discrepancy in Q1 2024 filing"
            ],
            "penalties": 500.0
        },
        "555666777": {
            "compliance_status": "Mostly Compliant",
            "compliance_score": 82,
            "outstanding_returns": 0,
            "outstanding_payments": 3200.0,
            "last_audit_date": "2023-10-22",
            "next_audit_due": "2024-10-22",
            "risk_level": "Low",
            "compliance_issues": ["Outstanding VAT payment"],
            "penalties": 150.0
        }
    }
    
    if tpin in compliance_data:
        return compliance_data[tpin]
    else:
        status_options = ["Fully Compliant", "Mostly Compliant", "Non-Compliant", "Under Review"]
        risk_options = ["Low", "Medium", "High"]
        
        return {
            "compliance_status": random.choice(status_options),
            "compliance_score": random.randint(30, 95),
            "outstanding_returns": random.randint(0, 4),
            "outstanding_payments": round(random.uniform(0, 20000), 2),
            "last_audit_date": "2023-12-01",
            "next_audit_due": "2024-12-01",
            "risk_level": random.choice(risk_options),
            "compliance_issues": ["No data available"] if random.random() > 0.5 else [],
            "penalties": round(random.uniform(0, 1000), 2)
        }

def generate_compliance_recommendations(compliance_data: Dict) -> List[str]:
    """Generate recommendations based on compliance status"""
    recommendations = []
    
    if compliance_data["outstanding_returns"] > 0:
        recommendations.append(f"Submit {compliance_data['outstanding_returns']} outstanding tax returns")
    
    if compliance_data["outstanding_payments"] > 0:
        recommendations.append(f"Clear outstanding payment of ZMW {compliance_data['outstanding_payments']:,.2f}")
    
    if compliance_data["compliance_score"] < 70:
        recommendations.append("Schedule meeting with tax consultant to review compliance status")
    
    if compliance_data["risk_level"] == "High":
        recommendations.append("Urgent: Address compliance issues to avoid penalties")
    
    if not recommendations:
        recommendations.append("Maintain current compliance practices")
    
    return recommendations

def get_compliance_report(tpin: str) -> Dict[str, Any]:
    """
    Generate a comprehensive compliance report
    """
    taxpayer = verify_taxpayer(tpin)
    compliance = check_compliance(tpin)
    
    return {
        "taxpayer_info": {
            "name": taxpayer.name,
            "business_name": taxpayer.business_name,
            "tpin": taxpayer.tpin,
            "tax_center": taxpayer.tax_center
        },
        "compliance_summary": compliance,
        "recommendations": generate_compliance_recommendations(compliance),
        "report_generated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

def submit_tax_return(tax_data: Dict) -> Dict:
    """Submit tax return data"""
    return {
        "success": True,
        "submission_id": f"TRX{random.randint(100000, 999999)}",
        "message": "Tax return submitted successfully",
        "submission_date": datetime.now().strftime("%Y-%m-%d"),
        "receipt_number": f"ZRA{random.randint(1000000, 9999999)}"
    }