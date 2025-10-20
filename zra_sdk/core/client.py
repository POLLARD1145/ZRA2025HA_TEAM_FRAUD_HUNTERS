import requests
import json
from typing import Optional, Dict, Any
from .config import ZRAConfig

class ZRAClient:
    """HTTP client for ZRA API communication"""
    
    def __init__(self):
        self.base_url = ZRAConfig.BASE_URL
        self.api_key = ZRAConfig.API_KEY
        self.timeout = ZRAConfig.TIMEOUT
        self.session = requests.Session()
        self._setup_session()
    
    def _setup_session(self):
        """Setup session with default headers"""
        self.session.headers.update({
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json',
            'User-Agent': 'ZRA-SDK/1.0.0'
        })
    
    def request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Dict[str, Any]:
        """Make API request to ZRA services"""
        url = f"{self.base_url}{endpoint}"
        
        try:
            response = self.session.request(
                method=method,
                url=url,
                json=data,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise ZRAAPIError(f"API request failed: {str(e)}")

class ZRAAPIError(Exception):
    """Custom exception for ZRA API errors"""
    pass