"""CosyVoice TTS Provider。

CosyVoice 是阿里开源的语音合成模型，支持多语言、多音色的高质量语音合成。
通过本地 HTTP 推理服务提供 TTS 能力。
"""

import struct
import time

import httpx

from app.config import COSYVOICE_BASE_URL
from app.providers.base import TTSProvider


def pcm_to_wav(pcm_data: bytes, sample_rate: int = 22050) -> bytes:
    """将原始 PCM 音频数据转换为 WAV 格式。

    Args:
        pcm_data: 原始 int16 PCM 音频数据。
        sample_rate: 采样率，默认 22050 Hz。

    Returns:
        包含 44 字节 WAV 头的完整 WAV 音频数据。
    """
    num_channels = 1
    bits_per_sample = 16
    byte_rate = sample_rate * num_channels * bits_per_sample // 8
    block_align = num_channels * bits_per_sample // 8
    data_size = len(pcm_data)
    file_size = 36 + data_size

    header = struct.pack(
        "<4sI4s4sIHHIIHH4sI",
        b"RIFF",
        file_size,
        b"WAVE",
        b"fmt ",
        16,  # fmt subchunk size
        1,  # audio format: PCM
        num_channels,
        sample_rate,
        byte_rate,
        block_align,
        bits_per_sample,
        b"data",
        data_size,
    )
    return header + pcm_data


class CosyVoiceProvider(TTSProvider):
    """CosyVoice TTS Provider。

    通过本地 CosyVoice 推理服务生成语音音频。

    Attributes:
        _base_url: CosyVoice 推理服务地址。
        _client: httpx 异步 HTTP 客户端。
    """

    def __init__(self) -> None:
        self._base_url = COSYVOICE_BASE_URL
        self._client = httpx.AsyncClient(timeout=30)

    async def generate(self, text: str, voice: str) -> tuple[bytes, int]:
        """生成语音音频。

        Args:
            text: 要转换的文本。
            voice: 语音标识（如 "中文女"）。

        Returns:
            (wav 音频数据 bytes, 耗时毫秒)

        Raises:
            RuntimeError: CosyVoice 服务不可用时抛出。
        """
        start = time.perf_counter()
        try:
            response = await self._client.get(
                f"{self._base_url}/inference_sft",
                params={"tts_text": text, "spk_id": voice},
            )
            response.raise_for_status()
        except httpx.HTTPError as e:
            raise RuntimeError(
                f"CosyVoice 服务不可用: {e}"
            ) from e

        pcm_data = response.content
        wav_data = pcm_to_wav(pcm_data)
        elapsed_ms = int((time.perf_counter() - start) * 1000)
        return wav_data, elapsed_ms

    def list_voices(self) -> list[str]:
        """返回支持的语音列表。"""
        return ["中文女", "中文男", "英文女", "英文男", "日语男", "粤语女", "韩语女"]
