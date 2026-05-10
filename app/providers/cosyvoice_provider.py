"""CosyVoice TTS Provider 占位模块。

CosyVoice 是阿里开源的语音合成模型，支持多语言、多音色的高质量语音合成。

未来实现需要：
- 本地模型推理（CosyVoice 模型文件）
- GPU 资源（CUDA 推理加速）
- 模型加载与初始化（可能需要 cosyvoice SDK 或自定义推理服务）

当前版本不做实现，仅预留接口。
"""

from app.providers.base import TTSProvider


class CosyVoiceProvider(TTSProvider):
    """CosyVoice TTS Provider 占位类。

    阿里开源语音合成模型 CosyVoice 的 Provider 实现占位。
    当前仅定义接口，不做实际实现。

    Attributes:
        None - 当前为占位类，无实际属性。
    """

    async def generate(self, text: str, voice: str) -> tuple[bytes, int]:
        """生成语音音频（未实现）。

        Args:
            text: 要转换的文本。
            voice: 语音标识。

        Returns:
            (mp3 音频数据 bytes, 耗时毫秒)

        Raises:
            NotImplementedError: 当前版本未实现此方法。
        """
        raise NotImplementedError(
            "CosyVoice provider 尚未实现。"
            "需要本地模型推理、GPU 资源和模型加载。"
        )
