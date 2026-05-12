"""edge-tts Provider 实现。"""

import time

import edge_tts

from .base import TTSProvider


class EdgeTTSProvider(TTSProvider):
    """基于 edge-tts 的 TTS Provider。"""

    def list_voices(self) -> list[str]:
        return [
            "zh-CN-XiaoxiaoNeural",
            "zh-CN-YunxiNeural",
            "zh-CN-YunjianNeural",
            "zh-CN-XiaoyiNeural",
        ]

    async def generate(self, text: str, voice: str) -> tuple[bytes, int]:
        """使用 edge-tts 生成语音音频。

        Args:
            text: 要转换的文本。
            voice: 语音标识。

        Returns:
            (mp3 音频数据 bytes, 耗时毫秒)

        Raises:
            RuntimeError: 生成音频失败时抛出。
        """
        start = time.perf_counter()

        try:
            communicate = edge_tts.Communicate(text, voice)
            audio_data = bytearray()
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    audio_data.extend(chunk["data"])
        except Exception as e:
            raise RuntimeError(f"edge-tts 生成音频失败: {e}") from e

        elapsed_ms = int((time.perf_counter() - start) * 1000)
        return bytes(audio_data), elapsed_ms
