"""
CRM 이미지 생성 모듈
OpenRouter 응답을 해석하고 CRM에서 활용할 수 있는 이미지 데이터를 제공합니다.
"""

from __future__ import annotations

import base64
import json
import tkinter as tk
from typing import Any, Dict, List, Optional

from config import Config
from api.openrouter_api import OpenRouterClient


class CRMImageGenerator:
    """CRM 시나리오에서 사용할 이미지를 생성하고 표시하는 헬퍼 클래스."""

    def __init__(self, config: Config):
        self.config = config
        self.client = OpenRouterClient(config)

    def generate(
        self,
        prompt: str,
        *,
        model: Optional[str] = None,
        modalities: Optional[List[str]] = None,
        extra_options: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        """
        OpenRouter Chat Completions 엔드포인트를 사용해 이미지를 생성합니다.

        Args:
            prompt: 이미지 생성 프롬프트
            model: 사용할 모델명 (기본값은 설정의 이미지 모델)
            modalities: 사용할 모달리티 목록 (기본값 ["image"])
            extra_options: OpenRouter API에서 요구하는 추가 파라미터

        Returns:
            이미지 관련 정보를 담은 딕셔너리 리스트
        """
        payload: Dict[str, Any] = {
            "model": model or self.client.image_model,
            "messages": [
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            "modalities": modalities or ["image", "text"],
        }

        if extra_options:
            payload.update(extra_options)

        response = self.client.create_chat_completion(payload)

        if "choices" not in response or not response["choices"]:
            raw = response.get("raw")
            detail = json.dumps(response, indent=2, ensure_ascii=False) if not raw else raw
            raise RuntimeError(f"OpenRouter가 이미지 선택지를 반환하지 않았습니다.\n{detail}")

        images: List[Dict[str, Any]] = []
        for choice in response["choices"]:
            message = choice.get("message", {})
            for image in message.get("images", []):
                images.append(image)

        if not images:
            raise RuntimeError("OpenRouter 응답에 이미지 데이터가 포함되어 있지 않습니다.")

        return images

    def show_image_from_data_url(self, data_url: str) -> None:
        """
        data URL 또는 base64 문자열로 전달된 이미지를 화면에 표시합니다.
        """
        if not data_url:
            print("이미지 데이터를 찾을 수 없습니다.")
            return

        base64_data = data_url
        if data_url.startswith("data:"):
            try:
                _, base64_data = data_url.split(",", 1)
            except ValueError:
                print("유효하지 않은 이미지 데이터 형식입니다.")
                return

        try:
            base64.b64decode(base64_data, validate=True)
        except (base64.binascii.Error, ValueError):
            print("Base64 디코딩에 실패했습니다.")
            return

        root = tk.Tk()
        root.title("Generated Image")

        photo = tk.PhotoImage(data=base64_data)
        label = tk.Label(root, image=photo)
        label.image = photo
        label.pack()

        root.mainloop()
