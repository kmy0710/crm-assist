"""
애플리케이션 설정을 관리하는 모듈입니다.
환경 변수에서 OpenAI 관련 설정을 읽어오거나 기본값을 제공합니다.
"""

from dataclasses import dataclass
import os
from typing import Optional

# 환경 변수에서 OpenAI API 키와 모델을 불러옵니다.
# 키가 설정되어 있지 않은 경우 빈 문자열을 기본값으로 사용합니다.
OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "").strip()
DEFAULT_OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini").strip()


@dataclass(frozen=True)
class Config:
    """OpenAI API 호출에 필요한 설정 정보를 보관합니다."""

    openai_api_key: str
    openai_model: str = DEFAULT_OPENAI_MODEL

    @classmethod
    def from_env(cls, api_key: Optional[str] = None, model: Optional[str] = None) -> "Config":
        """
        환경 변수 또는 전달된 인자를 사용하여 Config 인스턴스를 생성합니다.

        Args:
            api_key: 명시적으로 전달된 OpenAI API 키
            model: 명시적으로 전달된 모델 이름

        Returns:
            Config: 생성된 설정 인스턴스
        """
        resolved_api_key = (api_key or OPENAI_API_KEY).strip()
        resolved_model = (model or DEFAULT_OPENAI_MODEL).strip()

        if not resolved_api_key:
            raise ValueError(
                "OpenAI API 키가 설정되어 있지 않습니다. "
                "환경 변수 OPENAI_API_KEY를 설정하거나 api_key 인자를 제공하세요."
            )

        if not resolved_model:
            raise ValueError(
                "OpenAI 모델이 설정되어 있지 않습니다. "
                "환경 변수 OPENAI_MODEL을 설정하거나 model 인자를 제공하세요."
            )

        return cls(openai_api_key=resolved_api_key, openai_model=resolved_model)


def get_default_config() -> Config:
    """
    기본 환경 설정을 기반으로 Config 인스턴스를 반환합니다.

    Returns:
        Config: 기본 설정이 적용된 인스턴스
    """
    return Config.from_env()


