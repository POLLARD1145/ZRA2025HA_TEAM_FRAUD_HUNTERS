import os
from dotenv import load_dotenv

load_dotenv()

class ZRAConfig:
    """Configuration manager for ZRA SDK"""
    
    BASE_URL = os.getenv('ZRA_BASE_URL', 'https://api-sandbox.zra.org.zm')
    API_KEY = os.getenv('ZRA_API_KEY', '')
    TIMEOUT = int(os.getenv('ZRA_TIMEOUT', '30'))
    
    # Endpoints
    VERIFY_TAXPAYER = '/v1/taxpayer/verify'
    CALCULATE_TAX = '/v1/tax/calculate'
    
    @classmethod
    def validate(cls):
        """Validate required configuration"""
        if not cls.API_KEY:
            raise ValueError("ZRA_API_KEY environment variable is required")