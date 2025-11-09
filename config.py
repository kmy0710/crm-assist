"""
애플리케이션 설정을 관리하는 모듈입니다.
환경 변수에서 OpenAI 및 Qlik 관련 설정을 읽어오거나 기본값을 제공합니다.
"""

import os
from dataclasses import dataclass, field
from typing import Dict, Optional

# 환경 변수에서 설정값을 읽어오고 공백을 제거합니다.
DEFAULTS = {
    "OPENAI_API_KEY": "test-openai-api-key",
    "OPENAI_MODEL": "gpt-4o-mini",
    "QLIK_SERVER": "https://qlik.local",
    "QLIK_APP_ID": "demo-app-id",
    "QLIK_API_KEY": "test-qlik-api-key",
    "CRM_API_URL": "https://crm.local/api",
    "OPENROUTER_API_KEY": "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",
    "OPENROUTER_BASE_URL": "https://openrouter.ai/api/v1",
    "OPENROUTER_IMAGE_MODEL": "stabilityai/sdxl-lightning",
}

def _get_env(name: str) -> str:
    """환경 변수 값을 읽고, 없으면 DEFAULT 값을 반환합니다."""
    value = os.getenv(name, "").strip()
    return value if value else DEFAULTS[name]

OPENAI_API_KEY: str = _get_env("OPENAI_API_KEY")
_raw_openai_model = _get_env("OPENAI_MODEL")
DEFAULT_OPENAI_MODEL: str = _raw_openai_model if _raw_openai_model else DEFAULTS["OPENAI_MODEL"]

QLIK_SERVER: str = _get_env("QLIK_SERVER")
QLIK_APP_ID: str = _get_env("QLIK_APP_ID")
QLIK_API_KEY: str = _get_env("QLIK_API_KEY")

CRM_API_URL: str = _get_env("CRM_API_URL")

OPENROUTER_API_KEY: str = _get_env("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL: str = _get_env("OPENROUTER_BASE_URL")
OPENROUTER_IMAGE_MODEL: str = _get_env("OPENROUTER_IMAGE_MODEL")

@dataclass
class Config:
    """애플리케이션 전반에 사용되는 설정 값을 보관합니다."""

    openai_api_key: str = field(default=OPENAI_API_KEY)
    openai_model: str = field(default=DEFAULT_OPENAI_MODEL)

    qlik_server: str = field(default=QLIK_SERVER)
    qlik_app_id: str = field(default=QLIK_APP_ID)
    qlik_api_key: str = field(default=QLIK_API_KEY)

    crm_api_url: str = field(default=CRM_API_URL)

    openrouter_api_key: str = field(default=OPENROUTER_API_KEY)
    openrouter_base_url: str = field(default=OPENROUTER_BASE_URL)
    openrouter_image_model: str = field(default=OPENROUTER_IMAGE_MODEL)

    def __post_init__(self) -> None:
        """모든 문자열 필드의 공백을 제거합니다."""
        for attr, value in self.__dict__.items():
            if isinstance(value, str):
                setattr(self, attr, value.strip())

        # OpenAI 모델은 기본값을 보존하도록 보정합니다.
        if not self.openai_model:
            self.openai_model = DEFAULT_OPENAI_MODEL

    def validate(self) -> bool:
        """
        필수 환경 변수들이 모두 채워져 있는지 확인합니다.

        Returns:
            bool: 필수 값이 모두 존재하면 True, 아니면 False
        """
        required_fields = {
            "openai_api_key": self.openai_api_key,
            "qlik_server": self.qlik_server,
            "qlik_app_id": self.qlik_app_id,
            "qlik_api_key": self.qlik_api_key,
            "crm_api_url": self.crm_api_url,
        }

        for field_name, value in required_fields.items():
            if not value:
                return False

            # DEFAULT 값이 사용된 경우에도 안내 가능하도록 최소한의 형식 검증을 수행합니다.
            if value == DEFAULTS[field_name.upper()]:
                continue

        return True

    def missing_keys(self) -> Dict[str, str]:
        """
        누락된 설정 항목을 확인합니다.

        Returns:
            Dict[str, str]: 누락된 항목 이름과 가이드를 담은 딕셔너리
        """
        missing: Dict[str, str] = {}
        def _is_default(name: str, value: str) -> bool:
            return value == DEFAULTS[name]

        if not self.openai_api_key:
            missing["OPENAI_API_KEY"] = "OpenAI API 인증을 위해 필요합니다."
        elif _is_default("OPENAI_API_KEY", self.openai_api_key):
            missing["OPENAI_API_KEY"] = "환경 변수로 실제 키를 설정하세요. 현재는 기본 테스트 값입니다."

        if not self.qlik_server:
            missing["QLIK_SERVER"] = "Qlik 서버 URL을 지정해주세요."
        elif _is_default("QLIK_SERVER", self.qlik_server):
            missing["QLIK_SERVER"] = "환경 변수로 실제 서버 URL을 설정하세요. 현재는 기본 테스트 값입니다."

        if not self.qlik_app_id:
            missing["QLIK_APP_ID"] = "Qlik 애플리케이션 ID가 필요합니다."
        elif _is_default("QLIK_APP_ID", self.qlik_app_id):
            missing["QLIK_APP_ID"] = "환경 변수로 실제 앱 ID를 설정하세요. 현재는 기본 테스트 값입니다."

        if not self.qlik_api_key:
            missing["QLIK_API_KEY"] = "Qlik API 인증을 위해 필요합니다."
        elif _is_default("QLIK_API_KEY", self.qlik_api_key):
            missing["QLIK_API_KEY"] = "환경 변수로 실제 API 키를 설정하세요. 현재는 기본 테스트 값입니다."

        if not self.crm_api_url:
            missing["CRM_API_URL"] = "CRM API 호출을 위한 엔드포인트가 필요합니다."
        elif _is_default("CRM_API_URL", self.crm_api_url):
            missing["CRM_API_URL"] = "환경 변수로 실제 엔드포인트를 설정하세요. 현재는 기본 테스트 값입니다."

        if not self.openrouter_api_key:
            missing["OPENROUTER_API_KEY"] = "OpenRouter API 인증을 위해 필요합니다."
        elif _is_default("OPENROUTER_API_KEY", self.openrouter_api_key):
            missing["OPENROUTER_API_KEY"] = "환경 변수로 실제 OpenRouter API 키를 설정하세요. 현재는 기본 테스트 값입니다."

        if not self.openrouter_base_url:
            missing["OPENROUTER_BASE_URL"] = "OpenRouter API 기본 URL이 필요합니다."
        elif _is_default("OPENROUTER_BASE_URL", self.openrouter_base_url):
            missing["OPENROUTER_BASE_URL"] = "환경 변수로 OpenRouter API URL을 설정하세요. 현재는 기본 테스트 값입니다."

        if not self.openrouter_image_model:
            missing["OPENROUTER_IMAGE_MODEL"] = "이미지 생성을 위한 OpenRouter 모델명이 필요합니다."
        elif _is_default("OPENROUTER_IMAGE_MODEL", self.openrouter_image_model):
            missing["OPENROUTER_IMAGE_MODEL"] = "환경 변수로 사용할 이미지 생성 모델을 설정하세요. 현재는 기본 테스트 값입니다."

        return missing

    def ensure_valid(self) -> None:
        """
        필수 설정값이 모두 존재하는지 확인하고, 누락 시 예외를 발생시킵니다.

        Raises:
            ValueError: 필수 설정값이 하나라도 누락된 경우
        """
        missing = self.missing_keys()
        if missing:
            missing_list = ", ".join(missing.keys())
            raise ValueError(f"필수 설정값이 누락되었습니다: {missing_list}")

    @classmethod
    def from_env(
        cls,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        qlik_server: Optional[str] = None,
        qlik_app_id: Optional[str] = None,
        qlik_api_key: Optional[str] = None,
        crm_api_url: Optional[str] = None,
        openrouter_api_key: Optional[str] = None,
        openrouter_base_url: Optional[str] = None,
        openrouter_image_model: Optional[str] = None,
        ensure: bool = True,
    ) -> "Config":
        """
        환경 변수 또는 전달된 인자를 사용하여 Config 인스턴스를 생성합니다.

        Args:
            api_key: 명시적으로 전달된 OpenAI API 키
            model: 명시적으로 전달된 모델 이름
            qlik_server: Qlik 서버 URL
            qlik_app_id: Qlik 애플리케이션 ID
            qlik_api_key: Qlik API 키
            crm_api_url: CRM API 엔드포인트
            ensure: True인 경우 필수값 검증 (기본값)

        Returns:
            Config: 생성된 설정 인스턴스
        """
        config = cls(
            openai_api_key=api_key or OPENAI_API_KEY,
            openai_model=model or DEFAULT_OPENAI_MODEL,
            qlik_server=qlik_server or QLIK_SERVER,
            qlik_app_id=qlik_app_id or QLIK_APP_ID,
            qlik_api_key=qlik_api_key or QLIK_API_KEY,
            crm_api_url=crm_api_url or CRM_API_URL,
            openrouter_api_key=openrouter_api_key or OPENROUTER_API_KEY,
            openrouter_base_url=openrouter_base_url or OPENROUTER_BASE_URL,
            openrouter_image_model=openrouter_image_model or OPENROUTER_IMAGE_MODEL,
        )

        if ensure:
            config.ensure_valid()

        return config


def get_default_config(ensure: bool = True) -> Config:
    """
    기본 환경 설정을 기반으로 Config 인스턴스를 반환합니다.

    Args:
        ensure: True인 경우 필수값 검증을 수행합니다.

    Returns:
        Config: 기본 설정이 적용된 인스턴스
    """
    return Config.from_env(ensure=ensure)


