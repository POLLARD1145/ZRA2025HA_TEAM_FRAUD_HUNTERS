from flask import Flask, render_template, request, jsonify
import sys
import os
import json

# Add project directories to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../web_app'))

# Try to import your actual API, fallback to mock data
try:
    # Try different import paths
    try:
        from api.taxpayer_api import verify_taxpayer, calculate_tax
    except ImportError:
        from taxpayer_api import verify_taxpayer, calculate_tax
except ImportError as e:
    print(f"Import warning: {e}")
    # Mock implementation for deployment
    def verify_taxpayer(tpin):
        return {
            "tpin": tpin,
            "business_name": f"Demo Business {tpin}",
            "registration_date": "2023-01-01",
            "status": "Active",
            "address": "123 Demo Street, Lusaka",
            "compliance_status": "Compliant"
        }
    
    def calculate_tax(amount, tax_type="income"):
        rates = {"income": 0.3, "vat": 0.16, "corporate": 0.35}
        tax_due = amount * rates.get(tax_type, 0.3)
        return {
            "amount": amount,
            "tax_type": tax_type,
            "rate": rates.get(tax_type, 0.3),
            "tax_due": round(tax_due, 2),
            "breakdown": {
                "base_amount": amount,
                "tax_rate": rates.get(tax_type, 0.3),
                "calculated_tax": round(tax_due, 2)
            }
        }

app = Flask(__name__, 
    template_folder=os.path.join(os.path.dirname(__file__), '../web_app/templates'),
    static_folder=os.path.join(os.path.dirname(__file__), '../web_app/static')
)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/verify-taxpayer', methods=['POST', 'GET'])
def verify_taxpayer_route():
    if request.method == 'GET':
        tpin = request.args.get('tpin', '123456789')
    else:
        data = request.get_json()
        tpin = data.get('tpin', '123456789') if data else '123456789'
    
    result = verify_taxpayer(tpin)
    return jsonify(result)

@app.route('/api/calculate-tax', methods=['POST', 'GET'])
def calculate_tax_route():
    if request.method == 'GET':
        amount = float(request.args.get('amount', 25000))
        tax_type = request.args.get('tax_type', 'income')
    else:
        data = request.get_json()
        amount = float(data.get('amount', 25000)) if data else 25000
        tax_type = data.get('tax_type', 'income') if data else 'income'
    
    result = calculate_tax(amount, tax_type)
    return jsonify(result)

@app.route('/api/health')
def health_check():
    return jsonify({"status": "healthy", "service": "ZRA SDK API"})

# Vercel serverless handler
def handler(request, context):
    with app.app_context():
        return app(request.environ, lambda status, headers: None)
