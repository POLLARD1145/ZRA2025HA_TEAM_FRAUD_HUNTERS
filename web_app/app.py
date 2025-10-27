#!/usr/bin/env python3
"""
Enhanced ZRA Web App - Premium UI with Advanced Features
"""

from flask import Flask, request, jsonify
import sys
import os
import time
from datetime import datetime

# Add the zra_sdk folder to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from api.taxpayer_api import verify_taxpayer, calculate_tax, check_compliance, get_compliance_report
    print("✅ SDK imports successful!")
except ImportError as e:
    print(f"❌ SDK import failed: {e}")
    print("💡 Using mock data for demonstration")
    # Mock implementations for demo
    def verify_taxpayer(tpin):
        taxpayers = {
            '123456789': {'name': 'John Banda', 'business_name': 'Banda Enterprises', 'status': 'Active', 'email': 'john.banda@business.co.zm', 'phone': '+260 97 123 4567', 'registration_date': '2022-05-15', 'tax_center': 'Lusaka Central'},
            '444555666': {'name': 'Ebenezer Kaluba', 'business_name': 'Kaluba Holdings', 'status': 'Suspended', 'email': 'ekaluba@holdings.co.zm', 'phone': '+260 96 654 3210', 'registration_date': '2021-11-20', 'tax_center': 'Ndola'},
            '111222333': {'name': 'Pollard Samba', 'business_name': 'Samba Traders', 'status': 'Active', 'email': 'pollard@sambatraders.co.zm', 'phone': '+260 95 789 1234', 'registration_date': '2023-02-10', 'tax_center': 'Kitwe'},
            '777888999': {'name': 'Saviour Silwamba', 'business_name': 'Silwamba Industries', 'status': 'Active', 'email': 'saviour@silwamba.co.zm', 'phone': '+260 97 456 7890', 'registration_date': '2020-08-05', 'tax_center': 'Livingstone'}
        }
        return type('Taxpayer', (), taxpayers.get(tpin, taxpayers['123456789']))()
    
    def check_compliance(tpin):
        compliance_data = {
            '123456789': {'compliance_status': 'Compliant', 'compliance_score': 95, 'risk_level': 'Low', 'outstanding_returns': 0, 'outstanding_payments': 0, 'compliance_issues': []},
            '444555666': {'compliance_status': 'Non-Compliant', 'compliance_score': 35, 'risk_level': 'High', 'outstanding_returns': 3, 'outstanding_payments': 15000, 'compliance_issues': ['Late VAT returns', 'Unpaid income tax', 'Missing payroll filings']},
            '111222333': {'compliance_status': 'Mostly Compliant', 'compliance_score': 78, 'risk_level': 'Medium', 'outstanding_returns': 1, 'outstanding_payments': 2500, 'compliance_issues': ['Late Q3 VAT return']},
            '777888999': {'compliance_status': 'Compliant', 'compliance_score': 92, 'risk_level': 'Low', 'outstanding_returns': 0, 'outstanding_payments': 0, 'compliance_issues': []}
        }
        return compliance_data.get(tpin, compliance_data['123456789'])
    
    def calculate_tax(income, tax_type='income'):
        rates = {'income': 0.3, 'vat': 0.16, 'corporate': 0.35}
        rate = rates.get(tax_type, 0.3)
        tax_amount = income * rate
        return type('TaxCalc', (), {
            'gross_income': income,
            'tax_amount': tax_amount,
            'effective_tax_rate': rate,
            'tax_breakdown': {'base_tax': tax_amount}
        })()

app = Flask(__name__)

@app.route('/')
def home():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Zambia Revenue Authority - Digital Tax Platform</title>
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
        <style>
            :root {
                --primary: #2c5aa0;
                --primary-dark: #1e3a8a;
                --secondary: #10b981;
                --warning: #f59e0b;
                --danger: #ef4444;
                --light: #f8fafc;
                --dark: #1e293b;
                --gray: #64748b;
                --gradient-primary: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                --gradient-success: linear-gradient(135deg, #10b981, #059669);
                --gradient-warning: linear-gradient(135deg, #f59e0b, #d97706);
                --gradient-danger: linear-gradient(135deg, #ef4444, #dc2626);
            }
            
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
                background: var(--gradient-primary);
                min-height: 100vh;
                padding: 20px;
                line-height: 1.6;
                overflow-x: hidden;
            }
            
            /* Animated Background */
            .bg-animation {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                z-index: -1;
                opacity: 0.1;
            }
            
            .floating-shape {
                position: absolute;
                background: rgba(255, 255, 255, 0.1);
                border-radius: 50%;
                animation: float 6s ease-in-out infinite;
            }
            
            .shape-1 { width: 200px; height: 200px; top: 10%; left: 10%; animation-delay: 0s; }
            .shape-2 { width: 150px; height: 150px; top: 60%; right: 10%; animation-delay: 2s; }
            .shape-3 { width: 100px; height: 100px; bottom: 20%; left: 20%; animation-delay: 4s; }
            
            @keyframes float {
                0%, 100% { transform: translateY(0px) rotate(0deg); }
                50% { transform: translateY(-20px) rotate(180deg); }
            }
            
            .container {
                max-width: 1200px;
                margin: 0 auto;
                position: relative;
            }
            
            /* Enhanced Header */
            .header {
                background: rgba(255, 255, 255, 0.95);
                padding: 40px;
                border-radius: 25px;
                box-shadow: 
                    0 20px 40px rgba(0, 0, 0, 0.1),
                    0 0 0 1px rgba(255, 255, 255, 0.2);
                margin-bottom: 30px;
                text-align: center;
                backdrop-filter: blur(20px);
                position: relative;
                overflow: hidden;
                border: 1px solid rgba(255, 255, 255, 0.3);
            }
            
            .header::before {
                content: '';
                position: absolute;
                top: 0;
                left: -100%;
                width: 100%;
                height: 100%;
                background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
                transition: left 0.5s;
            }
            
            .header:hover::before {
                left: 100%;
            }
            
            .header h1 {
                color: var(--primary);
                font-size: 3em;
                margin-bottom: 10px;
                font-weight: 800;
                background: linear-gradient(135deg, var(--primary), var(--primary-dark));
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
            }
            
            .header p {
                color: var(--dark);
                font-size: 1.3em;
                opacity: 0.8;
                font-weight: 500;
            }
            
            /* Quick Test Section */
            .quick-test {
                background: rgba(255, 255, 255, 0.95);
                padding: 30px;
                border-radius: 20px;
                box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
                margin-bottom: 25px;
                backdrop-filter: blur(15px);
                border: 1px solid rgba(255, 255, 255, 0.3);
            }
            
            .quick-test h3 {
                color: var(--primary);
                margin-bottom: 20px;
                font-size: 1.4em;
                display: flex;
                align-items: center;
                gap: 10px;
            }
            
            .test-buttons {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 15px;
            }
            
            .test-btn {
                background: linear-gradient(135deg, var(--primary), var(--primary-dark));
                color: white;
                padding: 18px;
                border: none;
                border-radius: 12px;
                cursor: pointer;
                font-weight: 600;
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                font-size: 0.95em;
                position: relative;
                overflow: hidden;
            }
            
            .test-btn::before {
                content: '';
                position: absolute;
                top: 0;
                left: -100%;
                width: 100%;
                height: 100%;
                background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
                transition: left 0.5s;
            }
            
            .test-btn:hover {
                transform: translateY(-3px) scale(1.02);
                box-shadow: 0 12px 25px rgba(44, 90, 160, 0.4);
            }
            
            .test-btn:hover::before {
                left: 100%;
            }
            
            /* Input Section */
            .input-section {
                background: rgba(255, 255, 255, 0.95);
                padding: 30px;
                border-radius: 20px;
                box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
                margin-bottom: 25px;
                backdrop-filter: blur(15px);
                border: 1px solid rgba(255, 255, 255, 0.3);
            }
            
            .input-group {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 25px;
                align-items: start;
            }
            
            .input-card {
                background: linear-gradient(135deg, #ffffff, #f8fafc);
                padding: 30px;
                border-radius: 15px;
                border-left: 5px solid var(--primary);
                box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08);
                transition: all 0.3s ease;
                position: relative;
                overflow: hidden;
            }
            
            .input-card::after {
                content: '';
                position: absolute;
                top: 0;
                right: 0;
                width: 80px;
                height: 80px;
                background: var(--primary);
                border-radius: 0 0 0 80px;
                opacity: 0.05;
            }
            
            .input-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 15px 35px rgba(0, 0, 0, 0.15);
            }
            
            .input-card h4 {
                color: var(--primary);
                margin-bottom: 20px;
                font-size: 1.3em;
                display: flex;
                align-items: center;
                gap: 12px;
            }
            
            .form-group {
                margin-bottom: 25px;
                position: relative;
            }
            
            .form-group label {
                display: block;
                margin-bottom: 10px;
                color: var(--dark);
                font-weight: 600;
                font-size: 0.95em;
            }
            
            .form-control {
                width: 100%;
                padding: 15px 20px;
                border: 2px solid #e2e8f0;
                border-radius: 10px;
                font-size: 1em;
                transition: all 0.3s ease;
                background: white;
                font-weight: 500;
            }
            
            .form-control:focus {
                outline: none;
                border-color: var(--primary);
                box-shadow: 0 0 0 4px rgba(44, 90, 160, 0.1);
                transform: translateY(-2px);
            }
            
            .submit-btn {
                background: var(--gradient-success);
                color: white;
                padding: 18px 35px;
                border: none;
                border-radius: 12px;
                cursor: pointer;
                font-weight: 600;
                font-size: 1em;
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                width: 100%;
                position: relative;
                overflow: hidden;
            }
            
            .submit-btn::before {
                content: '';
                position: absolute;
                top: 0;
                left: -100%;
                width: 100%;
                height: 100%;
                background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
                transition: left 0.5s;
            }
            
            .submit-btn:hover {
                transform: translateY(-3px);
                box-shadow: 0 12px 25px rgba(16, 185, 129, 0.4);
            }
            
            .submit-btn:hover::before {
                left: 100%;
            }
            
            .submit-btn:active {
                transform: translateY(-1px);
            }
            
            .tax-inputs {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 20px;
            }
            
            /* Enhanced Results Section */
            #results {
                min-height: 100px;
                transition: all 0.3s ease;
            }
            
            .result-card {
                background: white;
                padding: 30px;
                border-radius: 15px;
                margin-bottom: 25px;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
                border-left: 5px solid var(--success);
                animation: slideInUp 0.5s ease-out;
                position: relative;
                overflow: hidden;
            }
            
            @keyframes slideInUp {
                from {
                    opacity: 0;
                    transform: translateY(30px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }
            
            .result-card::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 4px;
                background: var(--gradient-success);
            }
            
            .result-card.error {
                border-left-color: var(--danger);
                background: linear-gradient(135deg, #fef2f2, #fff);
            }
            
            .result-card.error::before {
                background: var(--gradient-danger);
            }
            
            .result-card.warning {
                border-left-color: var(--warning);
                background: linear-gradient(135deg, #fffbeb, #fff);
            }
            
            .result-card.warning::before {
                background: var(--gradient-warning);
            }
            
            .result-card h4 {
                color: var(--primary);
                margin-bottom: 20px;
                font-size: 1.4em;
                display: flex;
                align-items: center;
                gap: 12px;
            }
            
            .result-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
                gap: 20px;
                margin-top: 20px;
            }
            
            .result-item {
                padding: 15px;
                background: linear-gradient(135deg, #f8fafc, #ffffff);
                border-radius: 10px;
                border: 1px solid #e2e8f0;
                transition: all 0.3s ease;
                position: relative;
                overflow: hidden;
            }
            
            .result-item::before {
                content: '';
                position: absolute;
                left: 0;
                top: 0;
                height: 100%;
                width: 4px;
                background: var(--primary);
                opacity: 0.7;
            }
            
            .result-item:hover {
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
            }
            
            .result-item strong {
                color: var(--dark);
                display: block;
                margin-bottom: 8px;
                font-size: 0.9em;
                opacity: 0.8;
                font-weight: 600;
            }
            
            /* Enhanced Badges */
            .compliance-badge {
                display: inline-flex;
                align-items: center;
                gap: 6px;
                padding: 8px 16px;
                border-radius: 25px;
                font-size: 0.85em;
                font-weight: 600;
                margin-left: 10px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            }
            
            .badge-compliant { 
                background: var(--gradient-success); 
                color: white; 
            }
            .badge-noncompliant { 
                background: var(--gradient-danger); 
                color: white; 
            }
            .badge-mostly { 
                background: var(--gradient-warning); 
                color: white; 
            }
            
            /* Enhanced Loading */
            .loading {
                text-align: center;
                padding: 50px;
                color: var(--primary);
            }
            
            .spinner {
                border: 4px solid rgba(44, 90, 160, 0.2);
                border-top: 4px solid var(--primary);
                border-radius: 50%;
                width: 50px;
                height: 50px;
                animation: spin 1s linear infinite;
                margin: 0 auto 20px;
                box-shadow: 0 0 20px rgba(44, 90, 160, 0.3);
            }
            
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
            
            /* Progress Bar */
            .progress-bar {
                width: 100%;
                height: 6px;
                background: #e2e8f0;
                border-radius: 3px;
                overflow: hidden;
                margin: 10px 0;
            }
            
            .progress-fill {
                height: 100%;
                background: var(--gradient-success);
                border-radius: 3px;
                transition: width 0.5s ease;
            }
            
            /* Stats Cards */
            .stats-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
                gap: 15px;
                margin-top: 20px;
            }
            
            .stat-card {
                background: linear-gradient(135deg, #ffffff, #f8fafc);
                padding: 20px;
                border-radius: 12px;
                text-align: center;
                border: 1px solid #e2e8f0;
                transition: all 0.3s ease;
            }
            
            .stat-card:hover {
                transform: translateY(-3px);
                box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
            }
            
            .stat-value {
                font-size: 2em;
                font-weight: 700;
                color: var(--primary);
                margin-bottom: 5px;
            }
            
            .stat-label {
                font-size: 0.85em;
                color: var(--gray);
                font-weight: 600;
            }
            
            /* Notification System */
            .notification {
                position: fixed;
                top: 20px;
                right: 20px;
                padding: 20px 25px;
                border-radius: 12px;
                color: white;
                font-weight: 600;
                box-shadow: 0 10px 25px rgba(0,0,0,0.2);
                transform: translateX(400px);
                transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                z-index: 1000;
                max-width: 350px;
            }
            
            .notification.show {
                transform: translateX(0);
            }
            
            .notification.success { background: var(--gradient-success); }
            .notification.error { background: var(--gradient-danger); }
            .notification.warning { background: var(--gradient-warning); }
            
            /* Responsive Design */
            @media (max-width: 768px) {
                .input-group {
                    grid-template-columns: 1fr;
                }
                
                .tax-inputs {
                    grid-template-columns: 1fr;
                }
                
                .test-buttons {
                    grid-template-columns: 1fr;
                }
                
                .header h1 {
                    font-size: 2.2em;
                }
                
                .result-grid {
                    grid-template-columns: 1fr;
                }
                
                .stats-grid {
                    grid-template-columns: repeat(2, 1fr);
                }
            }
            
            /* Print Styles */
            @media print {
                .test-buttons, .quick-test {
                    display: none;
                }
                
                .result-card {
                    break-inside: avoid;
                    box-shadow: none;
                    border: 1px solid #ccc;
                }
            }
        </style>
    </head>
    <body>
        <!-- Animated Background -->
        <div class="bg-animation">
            <div class="floating-shape shape-1"></div>
            <div class="floating-shape shape-2"></div>
            <div class="floating-shape shape-3"></div>
        </div>
        
        <div class="container">
            <!-- Enhanced Header -->
            <div class="header">
                <h1><i class="fas fa-landmark"></i> Zambia Revenue Authority</h1>
                <p>Digital Tax Platform • Secure • Efficient • Transparent</p>
            </div>
            
            <!-- Quick Test Section -->
            <div class="quick-test">
                <h3><i class="fas fa-rocket"></i> Quick Test with Sample TPINs</h3>
                <div class="test-buttons">
                    <button class="test-btn" onclick="testTPIN('123456789')">
                        <i class="fas fa-user-check"></i> John Banda (Compliant)
                    </button>
                    <button class="test-btn" onclick="testTPIN('444555666')">
                        <i class="fas fa-user-slash"></i> Ebenezer Kaluba (Non-Compliant)
                    </button>
                    <button class="test-btn" onclick="testTPIN('111222333')">
                        <i class="fas fa-user-clock"></i> Pollard Samba (Minor Issues)
                    </button>
                    <button class="test-btn" onclick="testTPIN('777888999')">
                        <i class="fas fa-user-shield"></i> Saviour Silwamba (Compliant)
                    </button>
                </div>
            </div>
            
            <!-- Input Section -->
            <div class="input-section">
                <div class="input-group">
                    <!-- Taxpayer Verification -->
                    <div class="input-card">
                        <h4><i class="fas fa-search"></i> Taxpayer Verification</h4>
                        <div class="form-group">
                            <label for="tpinInput"><i class="fas fa-fingerprint"></i> TPIN (9 digits):</label>
                            <input type="text" id="tpinInput" class="form-control" placeholder="Enter 9-digit TPIN" maxlength="9" pattern="[0-9]{9}">
                        </div>
                        <button class="submit-btn" onclick="testManualTPIN()">
                            <i class="fas fa-shield-alt"></i> Verify Taxpayer
                        </button>
                    </div>
                    
                    <!-- Tax Calculation -->
                    <div class="input-card">
                        <h4><i class="fas fa-calculator"></i> Tax Calculation</h4>
                        <div class="tax-inputs">
                            <div class="form-group">
                                <label for="incomeInput"><i class="fas fa-money-bill-wave"></i> Income (ZMW):</label>
                                <input type="number" id="incomeInput" class="form-control" placeholder="Enter amount" value="25000" min="0" step="100">
                            </div>
                            <div class="form-group">
                                <label for="taxType"><i class="fas fa-percentage"></i> Tax Type:</label>
                                <select id="taxType" class="form-control">
                                    <option value="income">Income Tax</option>
                                    <option value="vat">VAT</option>
                                    <option value="corporate">Corporate Tax</option>
                                </select>
                            </div>
                        </div>
                        <button class="submit-btn" onclick="calculateTax()">
                            <i class="fas fa-calculator"></i> Calculate Tax
                        </button>
                    </div>
                </div>
            </div>
            
            <!-- Results Section -->
            <div id="results"></div>
        </div>

        <!-- Notification Container -->
        <div id="notificationContainer"></div>

        <script>
            // Notification System
            function showNotification(message, type = 'success') {
                const container = document.getElementById('notificationContainer');
                const notification = document.createElement('div');
                notification.className = `notification ${type}`;
                notification.innerHTML = `
                    <div style="display: flex; align-items: center; gap: 10px;">
                        <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-circle' : 'exclamation-triangle'}"></i>
                        <span>${message}</span>
                    </div>
                `;
                
                container.appendChild(notification);
                
                // Animate in
                setTimeout(() => notification.classList.add('show'), 100);
                
                // Auto remove after 5 seconds
                setTimeout(() => {
                    notification.classList.remove('show');
                    setTimeout(() => notification.remove(), 300);
                }, 5000);
            }

            function testTPIN(tpin) {
                document.getElementById('tpinInput').value = tpin;
                testManualTPIN();
                showNotification(`Testing TPIN: ${tpin}`, 'info');
            }

            async function testManualTPIN() {
                const tpin = document.getElementById('tpinInput').value.trim();
                const results = document.getElementById('results');
                
                if (!tpin || tpin.length !== 9 || !/^\d{9}$/.test(tpin)) {
                    showNotification('Please enter a valid 9-digit TPIN', 'error');
                    showError('Please enter a valid 9-digit TPIN');
                    return;
                }

                showLoading('Verifying taxpayer information...');
                showNotification(`Verifying TPIN: ${tpin}`, 'info');
                
                try {
                    // Test verification
                    const verifyResponse = await fetch('/api/verify', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({tpin: tpin})
                    });
                    const verifyData = await verifyResponse.json();
                    
                    let resultsHTML = '';
                    
                    if (verifyData.success) {
                        const data = verifyData.data;
                        showNotification('Taxpayer verified successfully!', 'success');
                        
                        resultsHTML += `
                            <div class="result-card">
                                <h4><i class="fas fa-user-check"></i> Taxpayer Verified</h4>
                                <div class="result-grid">
                                    <div class="result-item">
                                        <strong>Full Name</strong>
                                        <i class="fas fa-user"></i> ${data.name}
                                    </div>
                                    <div class="result-item">
                                        <strong>Business Name</strong>
                                        <i class="fas fa-building"></i> ${data.business_name}
                                    </div>
                                    <div class="result-item">
                                        <strong>Registration Status</strong>
                                        <i class="fas fa-badge-check"></i> ${data.status}
                                    </div>
                                    <div class="result-item">
                                        <strong>Email Address</strong>
                                        <i class="fas fa-envelope"></i> ${data.email}
                                    </div>
                                    <div class="result-item">
                                        <strong>Phone Number</strong>
                                        <i class="fas fa-phone"></i> ${data.phone}
                                    </div>
                                    <div class="result-item">
                                        <strong>Tax Center</strong>
                                        <i class="fas fa-map-marker-alt"></i> ${data.tax_center}
                                    </div>
                                    <div class="result-item">
                                        <strong>Registration Date</strong>
                                        <i class="fas fa-calendar-alt"></i> ${data.registration_date}
                                    </div>
                                </div>
                            </div>
                        `;
                    } else {
                        showNotification('Verification failed!', 'error');
                        resultsHTML += `<div class="result-card error"><h4><i class="fas fa-exclamation-circle"></i> Verification Error</h4><p>${verifyData.error}</p></div>`;
                    }

                    // Test compliance
                    showLoading('Checking compliance status...');
                    const complianceResponse = await fetch('/api/compliance', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({tpin: tpin})
                    });
                    const complianceData = await complianceResponse.json();
                    
                    if (complianceData.success) {
                        const comp = complianceData.compliance_data;
                        let badgeClass = 'badge-compliant';
                        let cardClass = '';
                        let icon = 'check-circle';
                        
                        if (comp.compliance_status === 'Non-Compliant') {
                            badgeClass = 'badge-noncompliant';
                            cardClass = 'error';
                            icon = 'exclamation-circle';
                            showNotification('Compliance issues detected!', 'warning');
                        } else if (comp.compliance_status === 'Mostly Compliant') {
                            badgeClass = 'badge-mostly';
                            cardClass = 'warning';
                            icon = 'exclamation-triangle';
                            showNotification('Minor compliance issues found', 'warning');
                        } else {
                            showNotification('Taxpayer is fully compliant!', 'success');
                        }
                        
                        let issuesHTML = '';
                        if (comp.compliance_issues && comp.compliance_issues.length > 0) {
                            issuesHTML = `
                                <div class="result-item" style="grid-column: 1 / -1;">
                                    <strong><i class="fas fa-exclamation-triangle"></i> Compliance Issues</strong>
                                    ${comp.compliance_issues.map(issue => '<div style="margin: 5px 0; padding: 8px 12px; background: rgba(239,68,68,0.1); border-radius: 6px; border-left: 3px solid var(--danger);"><i class="fas fa-times-circle" style="color: var(--danger); margin-right: 8px;"></i>' + issue + '</div>').join('')}
                                </div>
                            `;
                        }
                        
                        resultsHTML += `
                            <div class="result-card ${cardClass}">
                                <h4><i class="fas fa-${icon}"></i> Compliance Status 
                                    <span class="compliance-badge ${badgeClass}">
                                        <i class="fas fa-${icon}"></i> ${comp.compliance_status}
                                    </span>
                                </h4>
                                
                                <div class="progress-bar">
                                    <div class="progress-fill" style="width: ${comp.compliance_score}%"></div>
                                </div>
                                <div style="text-align: center; margin: 10px 0; font-weight: 600; color: var(--dark);">
                                    Compliance Score: ${comp.compliance_score}/100
                                </div>
                                
                                <div class="result-grid">
                                    <div class="result-item">
                                        <strong><i class="fas fa-chart-line"></i> Risk Level</strong>
                                        <span style="color: ${
                                            comp.risk_level === 'High' ? 'var(--danger)' : 
                                            comp.risk_level === 'Medium' ? 'var(--warning)' : 'var(--success)'
                                        }; font-weight: 700;">${comp.risk_level}</span>
                                    </div>
                                    <div class="result-item">
                                        <strong><i class="fas fa-file-invoice"></i> Outstanding Returns</strong>
                                        ${comp.outstanding_returns}
                                    </div>
                                    <div class="result-item">
                                        <strong><i class="fas fa-money-bill-wave"></i> Outstanding Payments</strong>
                                        ZMW ${comp.outstanding_payments?.toLocaleString() || '0'}
                                    </div>
                                    ${issuesHTML}
                                </div>
                                
                                <div class="stats-grid">
                                    <div class="stat-card">
                                        <div class="stat-value" style="color: ${comp.compliance_score >= 80 ? 'var(--success)' : comp.compliance_score >= 60 ? 'var(--warning)' : 'var(--danger)'};">${comp.compliance_score}%</div>
                                        <div class="stat-label">Compliance Score</div>
                                    </div>
                                    <div class="stat-card">
                                        <div class="stat-value">${comp.outstanding_returns}</div>
                                        <div class="stat-label">Pending Returns</div>
                                    </div>
                                    <div class="stat-card">
                                        <div class="stat-value">ZMW ${(comp.outstanding_payments || 0).toLocaleString()}</div>
                                        <div class="stat-label">Due Amount</div>
                                    </div>
                                    <div class="stat-card">
                                        <div class="stat-value">${comp.compliance_issues?.length || 0}</div>
                                        <div class="stat-label">Active Issues</div>
                                    </div>
                                </div>
                            </div>
                        `;
                    } else {
                        showNotification('Compliance check failed!', 'error');
                        resultsHTML += `<div class="result-card error"><h4><i class="fas fa-exclamation-circle"></i> Compliance Error</h4><p>${complianceData.error}</p></div>`;
                    }
                    
                    results.innerHTML = resultsHTML;
                    
                } catch (error) {
                    showNotification('Network error occurred!', 'error');
                    showError('Network error: ' + error.message);
                }
            }

            async function calculateTax() {
                const income = parseFloat(document.getElementById('incomeInput').value);
                const taxType = document.getElementById('taxType').value;
                const results = document.getElementById('results');
                
                if (!income || income <= 0) {
                    showNotification('Please enter a valid income amount', 'error');
                    showError('Please enter a valid income amount');
                    return;
                }

                showLoading('Calculating tax obligations...');
                showNotification('Calculating tax...', 'info');
                
                try {
                    const response = await fetch('/api/calculate-tax', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({
                            income: income,
                            tax_type: taxType
                        })
                    });
                    const data = await response.json();
                    
                    if (data.success) {
                        showNotification('Tax calculation completed!', 'success');
                        const taxData = data.data;
                        const taxAmount = taxData.tax_amount || income * 0.3;
                        const netIncome = income - taxAmount;
                        const taxRate = (taxData.effective_tax_rate || taxData.effective_rate || 0.3) * 100;
                        
                        results.innerHTML = `
                            <div class="result-card">
                                <h4><i class="fas fa-calculator"></i> Tax Calculation Result</h4>
                                <div class="result-grid">
                                    <div class="result-item">
                                        <strong><i class="fas fa-money-bill-wave"></i> Gross Income</strong>
                                        ZMW ${taxData.gross_income?.toLocaleString() || income.toLocaleString()}
                                    </div>
                                    <div class="result-item">
                                        <strong><i class="fas fa-receipt"></i> Tax Amount</strong>
                                        <span style="color: var(--danger); font-weight: 700;">ZMW ${taxAmount.toLocaleString()}</span>
                                    </div>
                                    <div class="result-item">
                                        <strong><i class="fas fa-percentage"></i> Effective Tax Rate</strong>
                                        ${taxRate.toFixed(1)}%
                                    </div>
                                    <div class="result-item">
                                        <strong><i class="fas fa-wallet"></i> Net Income</strong>
                                        <span style="color: var(--success); font-weight: 700;">ZMW ${netIncome.toLocaleString()}</span>
                                    </div>
                                </div>
                                
                                <div class="stats-grid">
                                    <div class="stat-card">
                                        <div class="stat-value" style="color: var(--primary);">ZMW ${income.toLocaleString()}</div>
                                        <div class="stat-label">Gross Income</div>
                                    </div>
                                    <div class="stat-card">
                                        <div class="stat-value" style="color: var(--danger);">ZMW ${taxAmount.toLocaleString()}</div>
                                        <div class="stat-label">Tax Payable</div>
                                    </div>
                                    <div class="stat-card">
                                        <div class="stat-value" style="color: var(--success);">ZMW ${netIncome.toLocaleString()}</div>
                                        <div class="stat-label">Net Income</div>
                                    </div>
                                    <div class="stat-card">
                                        <div class="stat-value" style="color: var(--warning);">${taxRate.toFixed(1)}%</div>
                                        <div class="stat-label">Tax Rate</div>
                                    </div>
                                </div>
                            </div>
                        `;
                    } else {
                        showNotification('Tax calculation failed!', 'error');
                        showError('Tax calculation error: ' + data.error);
                    }
                } catch (error) {
                    showNotification('Network error occurred!', 'error');
                    showError('Network error: ' + error.message);
                }
            }

            function showLoading(message) {
                document.getElementById('results').innerHTML = `
                    <div class="loading">
                        <div class="spinner"></div>
                        <div style="font-size: 1.1em; margin-top: 15px;">${message}</div>
                        <div style="margin-top: 10px; opacity: 0.7;">Please wait while we process your request...</div>
                    </div>
                `;
            }

            function showError(message) {
                document.getElementById('results').innerHTML = `
                    <div class="result-card error">
                        <h4><i class="fas fa-exclamation-circle"></i> Error</h4>
                        <p>${message}</p>
                    </div>
                `;
            }

            // Enhanced input handling
            document.getElementById('tpinInput').addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    testManualTPIN();
                }
            });

            document.getElementById('incomeInput').addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    calculateTax();
                }
            });

            // Add input formatting
            document.getElementById('tpinInput').addEventListener('input', function(e) {
                this.value = this.value.replace(/[^0-9]/g, '').slice(0, 9);
            });

            // Add some initial animations
            document.addEventListener('DOMContentLoaded', function() {
                showNotification('Welcome to ZRA Digital Tax Platform!', 'success');
            });
        </script>
    </body>
    </html>
    """

@app.route('/api/verify', methods=['POST'])
def verify():
    data = request.json or {}
    tpin = data.get('tpin', '123456789')
    
    try:
        taxpayer = verify_taxpayer(tpin)
        return jsonify({
            'success': True,
            'data': {
                'name': taxpayer.name,
                'business_name': taxpayer.business_name,
                'status': taxpayer.status,
                'email': taxpayer.email,
                'phone': taxpayer.phone,
                'registration_date': taxpayer.registration_date,
                'tax_center': taxpayer.tax_center
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/compliance', methods=['POST'])
def check_compliance_route():
    data = request.json or {}
    tpin = data.get('tpin', '123456789')
    
    try:
        compliance = check_compliance(tpin)
        return jsonify({
            'success': True,
            'compliance_data': compliance
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/calculate-tax', methods=['POST'])
def calculate_tax_route():
    data = request.json or {}
    income = float(data.get('income', 15000))
    tax_type = data.get('tax_type', 'income')
    
    try:
        tax_calc = calculate_tax(income, tax_type)
        return jsonify({
            'success': True,
            'data': {
                'gross_income': tax_calc.gross_income,
                'tax_amount': tax_calc.tax_amount,
                'effective_tax_rate': tax_calc.effective_tax_rate
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

if __name__ == '__main__':
    print("🚀 ZRA Enhanced Web API Running...")
    print("📍 http://localhost:5000")
    print("✨ Featuring: Advanced Animations • Real-time Notifications • Enhanced UX")
    app.run(debug=True, port=5000)