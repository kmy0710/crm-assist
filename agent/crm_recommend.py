"""
CRM 추천 모듈
CRM 데이터를 기반으로 디바이스 추천 로직을 처리합니다.
"""
from typing import Dict, Any, List, Optional
from api.openai_api import OpenAIClient
from api.qlik_api import QlikClient

class CRMRecommendationEngine:
    """CRM 기반 디바이스 추천 엔진"""
    
    def __init__(self, openai_client: OpenAIClient, qlik_client: QlikClient):
        """CRM 추천 엔진을 초기화합니다."""
        self.openai_client = openai_client
        self.qlik_client = qlik_client
    
    def recommend_devices_for_customer(
        self, 
        customer_id: str
    ) -> Optional[Dict[str, Any]]:
        """
        고객에게 적합한 디바이스를 추천합니다.
        
        Args:
            customer_id: 고객 ID
        
        Returns:
            추천 결과 딕셔너리 또는 None
        """
        # 고객 데이터 가져오기
        customer_data = self.qlik_client.get_customer_data(customer_id)
        if not customer_data:
            print(f"고객 데이터를 가져올 수 없습니다: {customer_id}")
            return None
        
        # 디바이스 데이터 가져오기
        device_list = self.qlik_client.get_device_data()
        if not device_list:
            print("디바이스 데이터를 가져올 수 없습니다.")
            return None
        
        # 각 디바이스에 대해 추천 생성
        recommendations = []
        for device in device_list:
            recommendation = self.openai_client.generate_recommendation(
                device_data=device,
                customer_context=customer_data
            )
            
            if recommendation:
                recommendations.append({
                    "device_id": device.get("id"),
                    "device_name": device.get("name"),
                    "recommendation": recommendation,
                    "score": self._calculate_recommendation_score(device, customer_data)
                })
        
        # 점수 기준으로 정렬
        recommendations.sort(key=lambda x: x["score"], reverse=True)
        
        return {
            "customer_id": customer_id,
            "recommendations": recommendations[:5]  # 상위 5개만 반환
        }
    
    def _calculate_recommendation_score(
        self, 
        device: Dict[str, Any], 
        customer: Dict[str, Any]
    ) -> float:
        """
        디바이스와 고객 정보를 기반으로 추천 점수를 계산합니다.
        
        Args:
            device: 디바이스 정보
            customer: 고객 정보
        
        Returns:
            추천 점수 (0.0 ~ 1.0)
        """
        # 간단한 점수 계산 로직 (실제로는 더 복잡한 알고리즘 사용 가능)
        score = 0.5  # 기본 점수
        
        # 고객 선호도와 디바이스 특성 매칭
        customer_preferences = customer.get("preferences", {})
        device_features = device.get("features", {})
        
        # 매칭되는 특성 수에 따라 점수 증가
        matching_features = sum(
            1 for key in customer_preferences 
            if key in device_features and customer_preferences[key] == device_features[key]
        )
        
        score += min(matching_features * 0.1, 0.5)  # 최대 0.5까지 추가
        
        return min(score, 1.0)

