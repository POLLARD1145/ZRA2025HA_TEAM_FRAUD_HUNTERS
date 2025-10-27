# Update wsgi.py in root to import from zra_sdk
@'
import sys
import os

# Add the zra_sdk folder to Python path
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'zra_sdk'))

# Import from zra_sdk.api.app
from zra_sdk.api.app import app

if __name__ == "__main__":
    app.run()
'@ | Set-Content -Path "wsgi.py" -Encoding utf8