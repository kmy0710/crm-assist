"""
Qlik API 모듈
Qlik API를 통해 데이터를 가져오고 처리합니다.
"""
import requests
from typing import Dict, Any, List, Optional
from config import Config


class QlikClient:
    """Qlik API 클라이언트"""
    
    def __init__(self, config: Config):
        """Qlik 클라이언트를 초기화합니다."""
        self.config = config
        self.base_url = config.qlik_server
        self.app_id = config.qlik_app_id
        self.api_key = config.qlik_api_key
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def get_device_data(self, device_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        디바이스 데이터를 Qlik에서 가져옵니다.
        
        Args:
            device_id: 특정 디바이스 ID (선택사항)
        
        Returns:
            디바이스 데이터 리스트
        """
        try:
            url = f"{self.base_url}/api/v1/apps/{self.app_id}/data"
            
            params = {}
            if device_id:
                params["device_id"] = device_id
            
            response = requests.get(
                url,
                headers=self.headers,
                params=params,
                timeout=30
            )
            response.raise_for_status()
            
            return response.json().get("data", [])
            
        except requests.exceptions.RequestException as e:
            print(f"Qlik API 호출 오류: {str(e)}")
            return []
    
    def get_customer_data(self, customer_id: str) -> Optional[Dict[str, Any]]:
        """
        고객 데이터를 Qlik에서 가져옵니다.
        
        Args:
            customer_id: 고객 ID
        
        Returns:
            고객 데이터 딕셔너리 또는 None
        """
        try:
            url = f"{self.base_url}/api/v1/apps/{self.app_id}/customers/{customer_id}"
            
            response = requests.get(
                url,
                headers=self.headers,
                timeout=30
            )
            response.raise_for_status()
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            print(f"Qlik API 호출 오류: {str(e)}")
            return None

