"""TTS 核心业务逻辑。"""

import json
import uuid
from datetime import datetime
from pathlib import Path

from app.providers.base import TTSProvider
from app.providers.edge_tts import EdgeTTSProvider
from app.schemas.tts import TTSRequest, TTSResponse

_STORAGE_DIR = Path(__file__).resolve().parent.parent.parent / "storage"
_AUDIO_DIR = _STORAGE_DIR / "audio"
_RECORDS_FILE = _STORAGE_DIR / "tts_records.jsonl"

# Provider 注册表
_registry: dict[str, TTSProvider] = {
    "edge": EdgeTTSProvider(),
}


def get_provider(name: str) -> TTSProvider:
    """获取指定名称的 TTS Provider。

    Raises:
        ValueError: provider 不存在时抛出。
    """
    provider = _registry.get(name)
    if provider is None:
        available = ", ".join(_registry.keys())
        raise ValueError(f"未知的 TTS provider: '{name}'，可用: {available}")
    return provider


async def generate_tts(
    request: TTSRequest,
    base_url: str = "http://localhost:8000",
) -> TTSResponse:
    """生成 TTS 音频并返回结果。"""
    provider = get_provider(request.provider)
    audio_data, duration_ms = await provider.generate(request.text, request.voice)

    now = datetime.now()
    rand_id = uuid.uuid4().hex[:8]
    filename = f"tts_{now:%Y%m%d_%H%M%S}_{rand_id}.mp3"

    _AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    (_AUDIO_DIR / filename).write_bytes(audio_data)

    response = TTSResponse(
        id=str(uuid.uuid4()),
        provider=request.provider,
        voice=request.voice,
        audio_url=f"{base_url}/audio/{filename}",
        filename=filename,
        duration_ms=duration_ms,
        created_at=now.strftime("%Y-%m-%d %H:%M:%S"),
    )

    # 追加写入记录
    _STORAGE_DIR.mkdir(parents=True, exist_ok=True)
    with _RECORDS_FILE.open("a", encoding="utf-8") as f:
        f.write(response.model_dump_json() + "\n")

    return response
