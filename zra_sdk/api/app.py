# Update zra_sdk/api/app.py template paths
@'
from flask import Flask, render_template, request, jsonify
import os
import sys

# Get the current directory (zra_sdk/api/)
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..'))

# Set template and static paths
template_dir = os.path.join(project_root, 'web_app', 'templates')
static_dir = os.path.join(project_root, 'web_app', 'static')

print(f"Project root: {project_root}")
print(f"Template dir: {template_dir}")
print(f"Static dir: {static_dir}")

# Mock implementations
def verify_taxpayer(tpin):
    return {
        "tpin": tpin,
        "business_name": f"Demo Business {tpin}",
        "registration_date": "2023-01-01",
        "status": "Active",
        "address": "123 Demo Street, Lusaka",
        "compliance_status": "Compliant",
        "message": "ZRA SDK - Production Ready on Render"
    }

def calculate_tax(amount, tax_type="income"):
    rates = {"income": 0.3, "vat": 0.16, "corporate": 0.35}
    tax_due = amount * rates.get(tax_type, 0.3)
    return {
        "amount": amount,
        "tax_type": tax_type,
        "rate": rates.get(tax_type, 0.3),
        "tax_due": round(tax_due, 2),
        "message": f"Tax calculated for {tax_type} tax"
    }

# Create Flask app
app = Flask(__name__,
    template_folder=template_dir,
    static_folder=static_dir
)

@app.route('/')
def home():
    try:
        return render_template('index.html')
    except Exception as e:
        return f'''
        <html>
            <body>
                <h1>ZRA SDK Demo - LIVE! 🚀</h1>
                <p>Template system loading... but API is working!</p>
                <p>Test these endpoints:</p>
                <ul>
                    <li><a href="/api/health">Health Check</a></li>
                    <li><a href="/api/verify-taxpayer?tpin=123456789">Verify Taxpayer</a></li>
                    <li><a href="/api/calculate-tax?amount=25000">Calculate Tax</a></li>
                </ul>
                <p><small>Error: {str(e)}</small></p>
            </body>
        </html>
        '''

@app.route('/api/verify-taxpayer', methods=['GET'])
def verify_taxpayer_route():
    tpin = request.args.get('tpin', '123456789')
    result = verify_taxpayer(tpin)
    return jsonify(result)

@app.route('/api/calculate-tax', methods=['GET'])
def calculate_tax_route():
    try:
        amount = float(request.args.get('amount', 25000))
    except:
        amount = 25000
    tax_type = request.args.get('tax_type', 'income')
    result = calculate_tax(amount, tax_type)
    return jsonify(result)

@app.route('/api/health')
def health_check():
    return jsonify({
        "status": "healthy", 
        "service": "ZRA SDK API",
        "deployment": "Render.com",
        "message": "Successfully deployed! 🎉"
    })

# Production server
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
'@ | Set-Content -Path "zra_sdk/api/app.py" -Encoding utf8