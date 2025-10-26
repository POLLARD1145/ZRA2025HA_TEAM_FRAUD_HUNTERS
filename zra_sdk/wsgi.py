'# Create wsgi.py in your project root
@'
import sys
import os

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from api.app import app

if __name__ == "__main__":
    app.run()
'@ | Set-Content -Path "wsgi.py" -Encoding utf8
