"""
OpenRouter 이미지 생성 API 클라이언트.
OpenRouter의 이미지 엔드포인트를 호출하여 CRM 워크플로우에서 사용할 이미지를 생성합니다.
"""

from __future__ import annotations
import base64
from typing import Any, Dict, List, Optional
import requests
from config import Config
import json
import tkinter as tk
from tkinter import messagebox

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

    def show_image_from_data_url(self, data_url: str) -> None:
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

    def generate_image(
        self,
        prompt: str,
        *,
        model: Optional[str] = None,
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
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload: Dict[str, Any] = {
            "model": model or self.image_model,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "modalities": ["image", "text"]
        }
        response = requests.post(self.base_url, headers=headers, json=payload)
        result = response.json()

        # The generated image will be in the assistant message
        if result.get("choices"):
            message = result["choices"][0]["message"]
            if message.get("images"):
                for image in message["images"]:
                    image_url = image["image_url"]["url"]
                    self.show_image_from_data_url(image_url)
            else:
                print("이미지 응답이 포함되어 있지 않습니다.")
        else:
            print(json.dumps(result, indent=2, ensure_ascii=False))

