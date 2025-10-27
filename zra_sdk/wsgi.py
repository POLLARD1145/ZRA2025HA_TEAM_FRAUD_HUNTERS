# Update zra_sdk/wsgi.py to handle the new import path
@'
import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import from the correct location
from api.app import app

if __name__ == "__main__":
    app.run()
'@ | Set-Content -Path "zra_sdk/wsgi.py" -Encoding utf8