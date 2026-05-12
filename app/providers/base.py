"""TTS Provider 抽象基类。

定义所有 TTS Provider 必须实现的接口。

注：CosyVoice 未来预留实现，可能需要 GPU 资源、模型加载、异步队列等。
当前仅提供 edge-tts 作为轻量级在线 TTS 方案。
"""

from abc import ABC, abstractmethod


class TTSProvider(ABC):
    """TTS Provider 抽象基类。"""

    @abstractmethod
    def list_voices(self) -> list[str]:
        """返回该 provider 支持的音色列表。"""
        ...

    @abstractmethod
    async def generate(self, text: str, voice: str) -> tuple[bytes, int]:
        """生成语音音频。

        Args:
            text: 要转换的文本。
            voice: 语音标识（如 "zh-CN-XiaoxiaoNeural"）。

        Returns:
            (mp3 音频数据 bytes, 耗时毫秒)
        """
        ...
