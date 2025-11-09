"""
CRM 이미지 생성 모듈
OpenRouter 이미지를 사용해 CRM 캠페인에서 활용할 시각 자료를 생성합니다.
"""

from typing import Any, Dict, List, Optional

from config import Config
from api.openrouter_api import OpenRouterClient


class CRMImageGenerator:
    """CRM 시나리오에서 사용할 이미지를 생성하는 래퍼 클래스."""

    def __init__(self, config: Config):
        self.client = OpenRouterClient(config)

    def generate(
        self,
        prompt: str,
        *,
        model: Optional[str] = None,
        extra_options: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        """
        캠페인 메시지에 사용할 이미지를 생성합니다.

        Args:
            prompt: 이미지 생성 프롬프트
            model: 사용할 모델명 (기본값은 설정의 이미지 모델)
            extra_options: OpenRouter 이미지 API가 지원하는 추가 인자
        """
        return self.client.generate_image(
            prompt,
            model=model,
            extra_options=extra_options,
        )
