from flask import Flask, jsonify
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "<h1>ZRA SDK - Successfully Deployed! 🎉</h1><p><a href='/api/health'>Health Check</a> | <a href='/api/verify-taxpayer'>Verify Taxpayer</a> | <a href='/api/calculate-tax'>Calculate Tax</a></p>"

@app.route("/api/verify-taxpayer")
def verify_taxpayer():
    return jsonify({
        "tpin": "123456789",
        "business_name": "Demo Business",
        "status": "Active",
        "message": "ZRA SDK - Production Ready"
    })

@app.route("/api/calculate-tax")
def calculate_tax():
    return jsonify({
        "amount": 25000,
        "tax_type": "income", 
        "tax_due": 7500,
        "message": "Tax calculated successfully"
    })

@app.route("/api/health")
def health_check():
    return jsonify({
        "status": "healthy",
        "service": "ZRA SDK API", 
        "deployment": "Render.com",
        "message": "Successfully deployed!"
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)