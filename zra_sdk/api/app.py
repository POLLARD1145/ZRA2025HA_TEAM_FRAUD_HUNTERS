# Update zra_sdk/api/app.py to use the new web_app
import sys
import os

# Add the project path to access your web_app
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..', '..'))

# Add both possible paths
sys.path.insert(0, project_root)
sys.path.insert(0, os.path.join(project_root, 'web_app'))

print("Loading ZRA SDK Web Application...")

# Import your actual web app
try:
    from app import app
    print("✅ Successfully imported web_app.app")
except ImportError as e:
    print(f"❌ Import error: {e}")
    # Fallback
    from flask import Flask, jsonify
    app = Flask(__name__)
    
    @app.route("/")
    def home():
        return "ZRA SDK - Please check web_app setup"
    
    @app.route("/api/health")
    def health():
        return jsonify({"status": "web_app import failed"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
