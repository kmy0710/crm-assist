"""
OpenAI API 모듈
OpenAI API를 호출하고 응답을 처리합니다.
"""
import openai
from typing import Dict, Any, Optional
from config import Config, OPENAI_API_KEY

class OpenAIClient:
    """OpenAI API 클라이언트"""
    
    def __init__(self, config: Config):
        """OpenAI 클라이언트를 초기화합니다."""
        self.config = config
        openai.api_key = config.openai_api_key
        self.model = config.openai_model
    
    def generate_recommendation(
        self, 
        device_data: Dict[str, Any], 
        customer_context: Dict[str, Any]
    ) -> Optional[str]:
        """
        디바이스 추천을 위한 프롬프트를 생성하고 OpenAI API를 호출합니다.
        
        Args:
            device_data: 디바이스 정보 딕셔너리
            customer_context: 고객 컨텍스트 정보 딕셔너리
        
        Returns:
            OpenAI API 응답 텍스트 또는 None
        """
        try:
            prompt = self._build_prompt(device_data, customer_context)
            
            response = openai.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "당신은 CRM 기반 디바이스 마케팅 전문가입니다."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"OpenAI API 호출 오류: {str(e)}")
            return None
    
    def _build_prompt(
        self, 
        device_data: Dict[str, Any], 
        customer_context: Dict[str, Any]
    ) -> str:
        """디바이스 데이터와 고객 컨텍스트를 기반으로 프롬프트를 생성합니다."""
        prompt = f"""
        다음 정보를 바탕으로 고객에게 적합한 디바이스 추천을 제공해주세요.
        
        디바이스 정보:
        {device_data}
        
        고객 정보:
        {customer_context}
        
        위 정보를 분석하여 고객에게 가장 적합한 디바이스 추천과 이유를 설명해주세요.
        """
        return prompt


def generate_marketing_copy(product: str, target: str, purpose: str) -> Optional[str]:
    """
    OpenAI ChatGPT API를 사용하여 마케팅 카피를 생성합니다.
    
    Args:
        product: 제품명
        target: 타겟 고객층
        purpose: 마케팅 목적
    
    Returns:
        생성된 마케팅 카피 텍스트 또는 None
    """
    try:
        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        
        prompt = f"""
        다음 정보를 바탕으로 효과적인 마케팅 카피를 작성해주세요.
        
        제품명: {product}
        타겟 고객층: {target}
        마케팅 목적: {purpose}
        
        위 정보를 바탕으로 타겟 고객층에게 어필할 수 있는 매력적이고 설득력 있는 마케팅 카피를 작성해주세요.
        """
        
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "당신은 전문 마케팅 카피라이터입니다."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        print(f"OpenAI API 호출 오류: {str(e)}")
        return None

