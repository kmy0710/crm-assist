"""
OpenRouter HTTP 클라이언트.
이미지 생성과 같은 도메인 로직은 상위 레이어에서 처리하고,
이 모듈은 OpenRouter API 호출을 위한 공통 기능만 제공합니다.
"""

from __future__ import annotations

from typing import Any, Dict, Optional

import requests

from config import Config


class OpenRouterClient:
    """OpenRouter HTTP 클라이언트."""

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

    def post(self, path: str, *, json: Dict[str, Any], timeout: int = 60) -> Dict[str, Any]:
        """
        OpenRouter API에 POST 요청을 전송합니다.

        Args:
            path: 호출할 엔드포인트 경로 (예: "/chat/completions")
            json: 전송할 JSON 페이로드
            timeout: 요청 타임아웃 (초)

        Returns:
            dict: 파싱된 JSON 응답

        Raises:
            RuntimeError: HTTP 에러 또는 요청 예외 발생 시
        """
        url = f"{self.base_url}{path}"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        response: Optional[requests.Response] = None
        try:
            response = requests.post(url, headers=headers, json=json, timeout=timeout)
            return self._parse_json(response)
        except requests.exceptions.HTTPError as exc:
            error_detail = self._extract_error(response or exc.response)
            raise RuntimeError(f"OpenRouter API 호출 실패: {error_detail}") from exc
        except requests.exceptions.RequestException as exc:
            raise RuntimeError(f"OpenRouter API 요청 중 오류: {exc}") from exc

    def create_chat_completion(self, payload: Dict[str, Any], *, timeout: int = 60) -> Dict[str, Any]:
        """
        OpenRouter의 Chat Completions 엔드포인트를 호출합니다.

        Args:
            payload: OpenRouter Chat Completion 형식의 JSON 페이로드
            timeout: 요청 타임아웃 (초)
        """
        return self.post("/chat/completions", json=payload, timeout=timeout)

    @staticmethod
    def _parse_json(response: requests.Response) -> Dict[str, Any]:
        """
        JSON 응답을 파싱합니다. 비어 있거나 JSON이 아닐 경우 원문 텍스트를 raw 키에 담습니다.
        """
        try:
            return response.json()
        except ValueError:
            text = response.text.strip()
            if not text:
                return {}
            return {"raw": text}

    @staticmethod
    def _extract_error(response: Optional[requests.Response]) -> str:
        """에러 응답에서 사람이 읽을 수 있는 메시지를 추출합니다."""
        if response is None:
            return "응답 객체를 받을 수 없습니다."

        try:
            data = response.json()
        except ValueError:
            text = response.text.strip()
            if text:
                return text
            return f"{response.status_code} {response.reason}"

        if isinstance(data, dict):
            error = data.get("error")
            if isinstance(error, dict):
                return error.get("message") or str(error)
            if error:
                return str(error)
            message = data.get("message")
            if message:
                return str(message)

        return f"{response.status_code} {response.reason}"

