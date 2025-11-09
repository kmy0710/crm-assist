"""
OpenRouter 이미지 생성 API 클라이언트.
OpenRouter의 이미지 엔드포인트를 호출하여 CRM 워크플로우에서 사용할 이미지를 생성합니다.
"""

from __future__ import annotations
import base64
from typing import Any, Dict, List, Optional
import requests
from config import Config

class OpenRouterClient:
    """OpenRouter 이미지 생성용 HTTP 클라이언트."""

    def __init__(self, config: Config):
        """
        Args:
            config: 애플리케이션 설정 인스턴스
        """
        self.config = config
        self.base_url = config.openrouter_base_url.rstrip("/")
        self.api_key = config.openrouter_api_key
        self.image_model = config.openrouter_image_model

        if not self.api_key:
            raise ValueError("OpenRouter API 키가 설정되어 있지 않습니다.")

    def generate_image(
        self,
        prompt: str,
        *,
        model: Optional[str] = None,
        size: str = "1024x1024",
        count: int = 1,
        response_format: str = "b64_json",
        negative_prompt: Optional[str] = None,
        extra_options: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        """
        주어진 프롬프트로 이미지를 생성합니다.

        Args:
            prompt: 이미지 생성에 사용할 프롬프트
            model: 사용할 모델명 (미지정 시 설정의 기본값)
            size: 생성 이미지 크기 (예: "1024x1024")
            count: 생성할 이미지 개수
            response_format: 응답 포맷 ("b64_json", "url" 등)
            negative_prompt: 제외하고 싶은 요소에 대한 네거티브 프롬프트
            extra_options: OpenRouter 이미지 API에서 지원하는 추가 파라미터

        Returns:
            이미지 데이터 딕셔너리 목록
        """
        payload: Dict[str, Any] = {
            "model": model or self.image_model,
            "prompt": prompt,
            "size": size,
            "n": count,
            "response_format": response_format,
        }

        if negative_prompt:
            payload["negative_prompt"] = negative_prompt

        if extra_options:
            payload.update(extra_options)

        response = self._post("/images", json=payload)
        data = response.get("data", [])

        # 응답 포맷이 base64인 경우 디코딩된 bytes도 함께 반환
        if response_format == "b64_json":
            for item in data:
                b64_content = item.get("b64_json")
                if isinstance(b64_content, str):
                    try:
                        item["bytes"] = base64.b64decode(b64_content)
                    except (base64.binascii.Error, ValueError):
                        # 디코딩 실패 시 bytes 키는 제거
                        item.pop("bytes", None)

        return data

    def _post(self, path: str, *, json: Dict[str, Any]) -> Dict[str, Any]:
        """POST 요청을 수행하고 JSON 응답을 반환합니다."""
        url = f"{self.base_url}{path}"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            # OpenRouter는 오픈소스/앱 정보 제공을 권장합니다.
            "HTTP-Referer": "https://crm-assist.local/",
            "X-Title": "CRM Assist",
        }

        try:
            response = requests.post(url, headers=headers, json=json, timeout=60)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as exc:
            error_detail = self._extract_error(response)
            raise RuntimeError(f"OpenRouter API 호출 실패: {error_detail}") from exc
        except requests.exceptions.RequestException as exc:
            raise RuntimeError(f"OpenRouter API 요청 중 오류: {exc}") from exc

    @staticmethod
    def _extract_error(response: requests.Response) -> str:
        """에러 응답에서 사람이 읽을 수 있는 메시지를 추출합니다."""
        try:
            data = response.json()
        except ValueError:
            return f"{response.status_code} {response.reason}"

        if isinstance(data, dict):
            if "error" in data:
                if isinstance(data["error"], dict):
                    return data["error"].get("message") or str(data["error"])
                return str(data["error"])
            if "message" in data:
                return str(data["message"])

        return f"{response.status_code} {response.reason}"


