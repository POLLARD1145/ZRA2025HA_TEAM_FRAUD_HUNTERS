#!/usr/bin/env python3
"""
Enhanced ZRA Web App - Professional UI with User Input
"""

from flask import Flask, request, jsonify
import sys
import os

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
        <title>ZRA Tax Services Platform</title>
        <style>
            :root {
                --primary: #2c5aa0;
                --secondary: #1e3a8a;
                --success: #10b981;
                --warning: #f59e0b;
                --danger: #ef4444;
                --light: #f8fafc;
                --dark: #1e293b;
            }
            
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 20px;
                line-height: 1.6;
            }
            
            .container {
                max-width: 1200px;
                margin: 0 auto;
            }
            
            .header {
                background: rgba(255, 255, 255, 0.95);
                padding: 40px;
                border-radius: 20px;
                box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
                margin-bottom: 30px;
                text-align: center;
                backdrop-filter: blur(10px);
            }
            
            .header h1 {
                color: var(--primary);
                font-size: 2.8em;
                margin-bottom: 10px;
                font-weight: 700;
            }
            
            .header p {
                color: var(--dark);
                font-size: 1.3em;
                opacity: 0.8;
            }
            
            .quick-test {
                background: rgba(255, 255, 255, 0.95);
                padding: 30px;
                border-radius: 15px;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
                margin-bottom: 25px;
            }
            
            .quick-test h3 {
                color: var(--primary);
                margin-bottom: 20px;
                font-size: 1.4em;
            }
            
            .test-buttons {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 12px;
            }
            
            .test-btn {
                background: linear-gradient(135deg, var(--primary), var(--secondary));
                color: white;
                padding: 15px;
                border: none;
                border-radius: 10px;
                cursor: pointer;
                font-weight: 600;
                transition: all 0.3s ease;
                font-size: 0.95em;
            }
            
            .test-btn:hover {
                transform: translateY(-2px);
                box-shadow: 0 8px 20px rgba(44, 90, 160, 0.3);
            }
            
            .input-section {
                background: rgba(255, 255, 255, 0.95);
                padding: 30px;
                border-radius: 15px;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
                margin-bottom: 25px;
            }
            
            .input-group {
                display: grid;
                grid-template-columns: 1fr 2fr;
                gap: 20px;
                align-items: start;
            }
            
            .input-card {
                background: var(--light);
                padding: 25px;
                border-radius: 12px;
                border-left: 4px solid var(--primary);
            }
            
            .input-card h4 {
                color: var(--primary);
                margin-bottom: 15px;
                font-size: 1.2em;
            }
            
            .form-group {
                margin-bottom: 20px;
            }
            
            .form-group label {
                display: block;
                margin-bottom: 8px;
                color: var(--dark);
                font-weight: 600;
            }
            
            .form-control {
                width: 100%;
                padding: 12px 15px;
                border: 2px solid #e2e8f0;
                border-radius: 8px;
                font-size: 1em;
                transition: border-color 0.3s ease;
            }
            
            .form-control:focus {
                outline: none;
                border-color: var(--primary);
                box-shadow: 0 0 0 3px rgba(44, 90, 160, 0.1);
            }
            
            .submit-btn {
                background: linear-gradient(135deg, var(--success), #059669);
                color: white;
                padding: 15px 30px;
                border: none;
                border-radius: 10px;
                cursor: pointer;
                font-weight: 600;
                font-size: 1em;
                transition: all 0.3s ease;
                width: 100%;
            }
            
            .submit-btn:hover {
                transform: translateY(-2px);
                box-shadow: 0 8px 20px rgba(16, 185, 129, 0.3);
            }
            
            .tax-inputs {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 15px;
            }
            
            #results {
                min-height: 100px;
            }
            
            .result-card {
                background: white;
                padding: 25px;
                border-radius: 12px;
                margin-bottom: 20px;
                box-shadow: 0 5px 15px rgba(0, 0, 0, 0.08);
                border-left: 4px solid var(--success);
            }
            
            .result-card.error {
                border-left-color: var(--danger);
                background: #fef2f2;
            }
            
            .result-card.warning {
                border-left-color: var(--warning);
                background: #fffbeb;
            }
            
            .result-card h4 {
                color: var(--primary);
                margin-bottom: 15px;
                font-size: 1.3em;
                display: flex;
                align-items: center;
                gap: 10px;
            }
            
            .result-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 15px;
                margin-top: 15px;
            }
            
            .result-item {
                padding: 12px;
                background: var(--light);
                border-radius: 8px;
            }
            
            .result-item strong {
                color: var(--dark);
                display: block;
                margin-bottom: 5px;
                font-size: 0.9em;
                opacity: 0.8;
            }
            
            .compliance-badge {
                display: inline-block;
                padding: 6px 12px;
                border-radius: 20px;
                font-size: 0.8em;
                font-weight: 600;
                margin-left: 10px;
            }
            
            .badge-compliant { background: var(--success); color: white; }
            .badge-noncompliant { background: var(--danger); color: white; }
            .badge-mostly { background: var(--warning); color: white; }
            
            .loading {
                text-align: center;
                padding: 30px;
                color: var(--primary);
            }
            
            .spinner {
                border: 3px solid #f3f3f3;
                border-top: 3px solid var(--primary);
                border-radius: 50%;
                width: 30px;
                height: 30px;
                animation: spin 1s linear infinite;
                margin: 0 auto 15px;
            }
            
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
            
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
            }
        </style>
    </head>
    <body>
        <div class="container">
            <!-- Header -->
            <div class="header">
                <h1>🏢 ZRA Tax Services Platform</h1>
                <p>Verify Taxpayers • Calculate Taxes • Check Compliance</p>
            </div>
            
            <!-- Quick Test Section -->
            <div class="quick-test">
                <h3>🚀 Quick Test with Sample TPINs</h3>
                <div class="test-buttons">
                    <button class="test-btn" onclick="testTPIN('123456789')">John Banda (Compliant)</button>
                    <button class="test-btn" onclick="testTPIN('444555666')">Ebenezer Kaluba (Non-Compliant)</button>
                    <button class="test-btn" onclick="testTPIN('111222333')">Pollard Samba (Minor Issues)</button>
                    <button class="test-btn" onclick="testTPIN('777888999')">Saviour Silwamba (Compliant)</button>
                </div>
            </div>
            
            <!-- Input Section -->
            <div class="input-section">
                <div class="input-group">
                    <!-- Taxpayer Verification -->
                    <div class="input-card">
                        <h4>📋 Taxpayer Verification</h4>
                        <div class="form-group">
                            <label for="tpinInput">TPIN (9 digits):</label>
                            <input type="text" id="tpinInput" class="form-control" placeholder="Enter TPIN" maxlength="9" pattern="[0-9]{9}">
                        </div>
                        <button class="submit-btn" onclick="testManualTPIN()">Verify Taxpayer</button>
                    </div>
                    
                    <!-- Tax Calculation -->
                    <div class="input-card">
                        <h4>💰 Tax Calculation</h4>
                        <div class="tax-inputs">
                            <div class="form-group">
                                <label for="incomeInput">Income (ZMW):</label>
                                <input type="number" id="incomeInput" class="form-control" placeholder="Enter amount" value="25000">
                            </div>
                            <div class="form-group">
                                <label for="taxType">Tax Type:</label>
                                <select id="taxType" class="form-control">
                                    <option value="income">Income Tax</option>
                                    <option value="vat">VAT</option>
                                    <option value="corporate">Corporate Tax</option>
                                </select>
                            </div>
                        </div>
                        <button class="submit-btn" onclick="calculateTax()">Calculate Tax</button>
                    </div>
                </div>
            </div>
            
            <!-- Results Section -->
            <div id="results"></div>
        </div>

        <script>
            function testTPIN(tpin) {
                document.getElementById('tpinInput').value = tpin;
                testManualTPIN();
            }

            async function testManualTPIN() {
                const tpin = document.getElementById('tpinInput').value.trim();
                const results = document.getElementById('results');
                
                if (!tpin || tpin.length !== 9 || !/^\d{9}$/.test(tpin)) {
                    showError('Please enter a valid 9-digit TPIN');
                    return;
                }

                showLoading('Testing TPIN: ' + tpin);
                
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
                        resultsHTML += `
                            <div class="result-card">
                                <h4>✅ Taxpayer Verified</h4>
                                <div class="result-grid">
                                    <div class="result-item">
                                        <strong>Name</strong>
                                        ${data.name}
                                    </div>
                                    <div class="result-item">
                                        <strong>Business</strong>
                                        ${data.business_name}
                                    </div>
                                    <div class="result-item">
                                        <strong>Status</strong>
                                        ${data.status}
                                    </div>
                                    <div class="result-item">
                                        <strong>Email</strong>
                                        ${data.email}
                                    </div>
                                    <div class="result-item">
                                        <strong>Phone</strong>
                                        ${data.phone}
                                    </div>
                                    <div class="result-item">
                                        <strong>Tax Center</strong>
                                        ${data.tax_center}
                                    </div>
                                </div>
                            </div>
                        `;
                    } else {
                        resultsHTML += `<div class="result-card error">Verification Error: ${verifyData.error}</div>`;
                    }

                    // Test compliance
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
                        
                        if (comp.compliance_status === 'Non-Compliant') {
                            badgeClass = 'badge-noncompliant';
                            cardClass = 'error';
                        } else if (comp.compliance_status === 'Mostly Compliant') {
                            badgeClass = 'badge-mostly';
                            cardClass = 'warning';
                        }
                        
                        let issuesHTML = '';
                        if (comp.compliance_issues && comp.compliance_issues.length > 0) {
                            issuesHTML = `
                                <div class="result-item" style="grid-column: 1 / -1;">
                                    <strong>Compliance Issues</strong>
                                    ${comp.compliance_issues.map(issue => '• ' + issue).join('<br>')}
                                </div>
                            `;
                        }
                        
                        resultsHTML += `
                            <div class="result-card ${cardClass}">
                                <h4>🔍 Compliance Status 
                                    <span class="compliance-badge ${badgeClass}">${comp.compliance_status}</span>
                                </h4>
                                <div class="result-grid">
                                    <div class="result-item">
                                        <strong>Compliance Score</strong>
                                        ${comp.compliance_score}/100
                                    </div>
                                    <div class="result-item">
                                        <strong>Risk Level</strong>
                                        ${comp.risk_level}
                                    </div>
                                    <div class="result-item">
                                        <strong>Outstanding Returns</strong>
                                        ${comp.outstanding_returns}
                                    </div>
                                    <div class="result-item">
                                        <strong>Outstanding Payments</strong>
                                        ZMW ${comp.outstanding_payments?.toLocaleString() || '0'}
                                    </div>
                                    ${issuesHTML}
                                </div>
                            </div>
                        `;
                    } else {
                        resultsHTML += `<div class="result-card error">Compliance Error: ${complianceData.error}</div>`;
                    }
                    
                    results.innerHTML = resultsHTML;
                    
                } catch (error) {
                    showError('Network error: ' + error.message);
                }
            }

            async function calculateTax() {
                const income = parseFloat(document.getElementById('incomeInput').value);
                const taxType = document.getElementById('taxType').value;
                const results = document.getElementById('results');
                
                if (!income || income <= 0) {
                    showError('Please enter a valid income amount');
                    return;
                }

                showLoading('Calculating tax...');
                
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
                        const taxData = data.data;
                        results.innerHTML = `
                            <div class="result-card">
                                <h4>💰 Tax Calculation Result</h4>
                                <div class="result-grid">
                                    <div class="result-item">
                                        <strong>Gross Income</strong>
                                        ZMW ${taxData.gross_income?.toLocaleString() || income.toLocaleString()}
                                    </div>
                                    <div class="result-item">
                                        <strong>Tax Amount</strong>
                                        ZMW ${taxData.tax_amount?.toLocaleString() || (income * 0.3).toLocaleString()}
                                    </div>
                                    <div class="result-item">
                                        <strong>Effective Tax Rate</strong>
                                        ${((taxData.effective_tax_rate || taxData.effective_rate || 0.3) * 100).toFixed(1)}%
                                    </div>
                                    <div class="result-item">
                                        <strong>Net Income</strong>
                                        ZMW ${(income - (taxData.tax_amount || income * 0.3)).toLocaleString()}
                                    </div>
                                </div>
                            </div>
                        `;
                    } else {
                        showError('Tax calculation error: ' + data.error);
                    }
                } catch (error) {
                    showError('Network error: ' + error.message);
                }
            }

            function showLoading(message) {
                document.getElementById('results').innerHTML = `
                    <div class="loading">
                        <div class="spinner"></div>
                        <div>${message}</div>
                    </div>
                `;
            }

            function showError(message) {
                document.getElementById('results').innerHTML = `
                    <div class="result-card error">
                        <h4>❌ Error</h4>
                        <p>${message}</p>
                    </div>
                `;
            }

            // Allow Enter key to submit TPIN
            document.getElementById('tpinInput').addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    testManualTPIN();
                }
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
    print("🚀 ZRA SDK Web API Running...")
    print("📍 http://localhost:5000")
    app.run(debug=True, port=5000)