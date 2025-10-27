
from flask import Flask, request, jsonify
import sys
import os

# Fix paths for deployment
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.insert(0, project_root)

app = Flask(__name__)

# Mock functions for demonstration
def verify_taxpayer(tpin):
    return {
        'name': 'John Banda',
        'business_name': f'Demo Business {tpin}',
        'status': 'Active',
        'email': 'john.banda@business.co.zm',
        'phone': '+260 97 123 4567',
        'registration_date': '2022-05-15',
        'tax_center': 'Lusaka Central',
        'address': '123 Business Ave, Lusaka'
    }

def calculate_tax(income, tax_type='income'):
    rates = {'income': 0.3, 'vat': 0.16, 'corporate': 0.35}
    rate = rates.get(tax_type, 0.3)
    tax_amount = income * rate
    
    return {
        'gross_income': income,
        'tax_amount': tax_amount,
        'effective_tax_rate': rate,
        'tax_breakdown': {
            'base_income': income,
            'tax_rate': rate,
            'tax_amount': tax_amount,
            'net_income': income - tax_amount
        }
    }

def check_compliance(tpin):
    return {
        'status': 'Compliant',
        'score': 95,
        'last_filing': '2024-01-15',
        'next_deadline': '2024-04-30',
        'outstanding_returns': 0
    }

@app.route('/')
def index():
    """Home page with beautiful UI"""
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>ZRA SDK - Tax Services Platform</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; padding: 20px; }
            .container { max-width: 1200px; margin: 0 auto; }
            .header { background: rgba(255, 255, 255, 0.95); padding: 30px; border-radius: 15px; box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2); margin-bottom: 30px; text-align: center; }
            .header h1 { color: #2c3e50; font-size: 2.5em; margin-bottom: 10px; }
            .header p { color: #7f8c8d; font-size: 1.2em; }
            .services-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); gap: 25px; margin-bottom: 30px; }
            .service-card { background: rgba(255, 255, 255, 0.95); padding: 30px; border-radius: 15px; box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1); transition: transform 0.3s ease; }
            .service-card:hover { transform: translateY(-5px); }
            .service-card h3 { color: #2c3e50; font-size: 1.5em; margin-bottom: 15px; }
            .service-card p { color: #7f8c8d; margin-bottom: 20px; line-height: 1.6; }
            .btn { background: linear-gradient(135deg, #3498db, #2980b9); color: white; padding: 12px 25px; text-decoration: none; border-radius: 8px; display: inline-block; font-weight: 600; transition: all 0.3s ease; border: none; cursor: pointer; }
            .btn:hover { background: linear-gradient(135deg, #2980b9, #3498db); transform: translateY(-2px); }
            .api-test { background: rgba(255, 255, 255, 0.95); padding: 25px; border-radius: 15px; margin-top: 30px; }
            .test-links { display: flex; gap: 15px; flex-wrap: wrap; }
            .success-banner { background: linear-gradient(135deg, #27ae60, #2ecc71); color: white; padding: 20px; border-radius: 10px; text-align: center; margin-bottom: 25px; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🏢 ZRA SDK Tax Services Platform</h1>
                <p>Production-Ready Tax Service Integration</p>
            </div>
            
            <div class="success-banner">
                <h2>🚀 Successfully Deployed on Render.com!</h2>
                <p>Your ZRA SDK is now live and serving tax services</p>
            </div>
            
            <div class="services-grid">
                <div class="service-card">
                    <h3>📋 Taxpayer Verification</h3>
                    <p>Verify business registration details and compliance status using TPIN validation.</p>
                    <button class="btn" onclick="testVerification()">Test Verification API</button>
                </div>
                
                <div class="service-card">
                    <h3>💰 Tax Calculation</h3>
                    <p>Calculate income tax, VAT, and corporate tax with detailed breakdowns.</p>
                    <button class="btn" onclick="testTaxCalculation()">Test Tax Calculator</button>
                </div>
                
                <div class="service-card">
                    <h3>📊 Compliance Check</h3>
                    <p>Check taxpayer compliance status and filing history.</p>
                    <button class="btn" onclick="testCompliance()">Test Compliance API</button>
                </div>
            </div>
            
            <div class="api-test">
                <h3>API Test Results</h3>
                <div id="results" style="margin-top: 15px; padding: 15px; background: #f8f9fa; border-radius: 8px; min-height: 100px;"></div>
            </div>
        </div>

        <script>
            function testVerification() {
                fetch('/api/verify?tpin=123456789')
                    .then(response => response.json())
                    .then(data => {
                        document.getElementById('results').innerHTML = '<h4>✅ Taxpayer Verification Result:</h4><pre>' + JSON.stringify(data, null, 2) + '</pre>';
                    });
            }

            function testTaxCalculation() {
                fetch('/api/calculate-tax?income=50000&tax_type=income')
                    .then(response => response.json())
                    .then(data => {
                        document.getElementById('results').innerHTML = '<h4>✅ Tax Calculation Result:</h4><pre>' + JSON.stringify(data, null, 2) + '</pre>';
                    });
            }

            function testCompliance() {
                fetch('/api/compliance?tpin=123456789')
                    .then(response => response.json())
                    .then(data => {
                        document.getElementById('results').innerHTML = '<h4>✅ Compliance Check Result:</h4><pre>' + JSON.stringify(data, null, 2) + '</pre>';
                    });
            }
        </script>
    </body>
    </html>
    """

@app.route('/api/verify', methods=['GET'])
def verify_taxpayer_api():
    """API endpoint to verify taxpayer"""
    tpin = request.args.get('tpin', '123456789')
    taxpayer = verify_taxpayer(tpin)
    return jsonify({
        'success': True,
        'data': taxpayer
    })

@app.route('/api/calculate-tax', methods=['GET'])
def calculate_tax_api():
    """API endpoint to calculate tax"""
    income = float(request.args.get('income', 25000))
    tax_type = request.args.get('tax_type', 'income')
    tax_calc = calculate_tax(income, tax_type)
    return jsonify({
        'success': True,
        'data': tax_calc
    })

@app.route('/api/compliance', methods=['GET'])
def check_compliance_api():
    """API endpoint to check taxpayer compliance"""
    tpin = request.args.get('tpin', '123456789')
    compliance = check_compliance(tpin)
    return jsonify({
        'success': True,
        'compliance_data': compliance
    })

@app.route('/api/health')
def health_check():
    return jsonify({
        'status': 'healthy',
        'service': 'ZRA SDK Web App',
        'deployment': 'Render.com',
        'message': 'Full UI is now working! 🎉'
    })

if __name__ == '__main__':
    print("🚀 ZRA SDK Web App Starting...")
    app.run(debug=True, host='0.0.0.0', port=5000)
