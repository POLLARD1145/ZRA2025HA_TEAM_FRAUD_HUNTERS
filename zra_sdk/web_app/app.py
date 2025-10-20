#!/usr/bin/env python3
"""
ZRA SDK Web Application - Vercel Deployment with Compliance Features
"""

try:
    from flask import Flask, request, jsonify, render_template
    import sys
    import os

    # Add the parent directory (zra_sdk) to Python path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    sys.path.insert(0, parent_dir)

    # Import APIs
    from api.taxpayer_api import verify_taxpayer, calculate_tax, check_compliance, get_compliance_report

    app = Flask(__name__)

    @app.route('/')
    def index():
        """Home page with web interface"""
        return render_template('index.html')

    @app.route('/api/verify', methods=['POST'])
    def verify_taxpayer_api():
        """API endpoint to verify taxpayer"""
        try:
            data = request.get_json()
            if not data:
                return jsonify({'error': 'No JSON data provided'}), 400

            tpin = data.get('tpin')
            if not tpin:
                return jsonify({'error': 'TPIN is required'}), 400

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

    @app.route('/api/calculate-tax', methods=['POST'])
    def calculate_tax_api():
        """API endpoint to calculate tax"""
        try:
            data = request.get_json()
            if not data:
                return jsonify({'error': 'No JSON data provided'}), 400

            income = float(data.get('income', 0))
            tax_type = data.get('tax_type', 'income')
            if income <= 0:
                return jsonify({'error': 'Income must be positive'}), 400

            tax_calc = calculate_tax(income, tax_type)
            return jsonify({
                'success': True,
                'data': {
                    'gross_income': tax_calc.gross_income,
                    'tax_amount': tax_calc.tax_amount,
                    'effective_tax_rate': tax_calc.effective_tax_rate,
                    'tax_breakdown': tax_calc.tax_breakdown
                }
            })
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 400

    @app.route('/api/compliance', methods=['POST'])
    def check_compliance_api():
        """API endpoint to check taxpayer compliance"""
        try:
            data = request.get_json()
            if not data:
                return jsonify({'error': 'No JSON data provided'}), 400

            tpin = data.get('tpin')
            if not tpin:
                return jsonify({'error': 'TPIN is required'}), 400

            compliance = check_compliance(tpin)
            return jsonify({
                'success': True,
                'compliance_data': compliance
            })
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 400

    @app.route('/api/compliance-report', methods=['POST'])
    def compliance_report_api():
        """API endpoint to get comprehensive compliance report"""
        try:
            data = request.get_json()
            if not data:
                return jsonify({'error': 'No JSON data provided'}), 400

            tpin = data.get('tpin')
            if not tpin:
                return jsonify({'error': 'TPIN is required'}), 400

            report = get_compliance_report(tpin)
            return jsonify({
                'success': True,
                'compliance_report': report
            })
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 400

    # Vercel compatibility
    if __name__ == '__main__':
        print("🚀 ZRA SDK Web App with Compliance Features Starting...")
        print("📍 Access at: http://localhost:5000")
        app.run(debug=True, host='0.0.0.0', port=5000)
    else:
        # For Vercel serverless deployment
        application = app

except ImportError as e:
    print(f"❌ Import Error: {e}")
    print("💡 Please check that:")
    print("   1. You're running from the web_app folder")
    print("   2. The parent zra_sdk folder has api/, models/, utils/ folders")
    print("   3. All required Python files exist")
    
    # For Vercel deployment
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
else:
    # This is required for Vercel
    application = app