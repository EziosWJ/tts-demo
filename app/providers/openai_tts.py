"""OpenAI TTS Provider。"""

import time

import openai

from app.config import OPENAI_TTS_BASE_URL, OPENAI_TTS_API_KEY, OPENAI_TTS_MODEL, OPENAI_TTS_VOICE
from app.providers.base import TTSProvider


class OpenAITTSProvider(TTSProvider):
    """OpenAI TTS Provider。"""

    def __init__(self) -> None:
        if not OPENAI_TTS_API_KEY:
            raise ValueError(
                "OpenAI TTS provider 需要配置 OPENAI_TTS_API_KEY，请在 .env 文件中设置"
            )
        self._client = openai.AsyncOpenAI(
            api_key=OPENAI_TTS_API_KEY,
            base_url=OPENAI_TTS_BASE_URL or None,
        )
        self._model = OPENAI_TTS_MODEL

    def list_voices(self) -> list[str]:
        return ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]

    async def generate(self, text: str, voice: str) -> tuple[bytes, int]:
        start = time.perf_counter()

        response = await self._client.audio.speech.create(
            model=self._model,
            voice=voice or OPENAI_TTS_VOICE,
            input=text,
        )
        audio_data = response.content

        elapsed_ms = int((time.perf_counter() - start) * 1000)
        return audio_data, elapsed_ms
