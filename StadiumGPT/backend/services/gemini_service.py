from __future__ import annotations
import json
import logging
from typing import Any
from fastapi import HTTPException
from google import genai
from google.genai import types
from utils.security import settings

logger = logging.getLogger("stadiumgpt.ai")

class GeminiService:
    def __init__(self) -> None:
        self._client = genai.Client(api_key=settings.gemini_api_key) if settings.gemini_api_key else None

    def _require_client(self) -> genai.Client:
        if self._client is None:
            raise HTTPException(503, "Gemini is not configured. Set GEMINI_API_KEY in .env.")
        return self._client

    def generate_text(self, prompt: str) -> str:
        try:
            response = self._require_client().models.generate_content(
                model=settings.gemini_model, contents=prompt,
                config=types.GenerateContentConfig(temperature=0.25),
            )
            text = (response.text or "").strip()
            if not text:
                raise RuntimeError("Gemini returned an empty response")
            return text
        except HTTPException:
            raise
        except Exception as exc:
            logger.exception("Gemini text generation failed")
            raise HTTPException(503, "The AI assistant is temporarily unavailable.") from exc

    def generate_json(self, prompt: str) -> dict[str, Any]:
        try:
            response = self._require_client().models.generate_content(
                model=settings.gemini_model, contents=prompt,
                config=types.GenerateContentConfig(temperature=0.15, response_mime_type="application/json"),
            )
            text = (response.text or "").strip()
            payload = json.loads(text)
            if not isinstance(payload, dict):
                raise ValueError("Gemini response was not a JSON object")
            return payload
        except HTTPException:
            raise
        except Exception as exc:
            logger.exception("Gemini structured generation failed")
            raise HTTPException(503, "The AI assistant is temporarily unavailable.") from exc

gemini_service = GeminiService()