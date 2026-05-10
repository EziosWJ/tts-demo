"""TTS CLI 命令行入口。"""

import argparse
import asyncio
import time

from app.schemas.tts import TTSRequest
from app.services.tts_service import generate_tts


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="TTS 文本转语音命令行工具")
    parser.add_argument("text", help="要合成的文本")
    parser.add_argument("--provider", default="edge", help="TTS provider (默认: edge)")
    parser.add_argument(
        "--voice",
        default="zh-CN-XiaoxiaoNeural",
        help="音色 (默认: zh-CN-XiaoxiaoNeural)",
    )
    return parser.parse_args()


async def run(args: argparse.Namespace) -> None:
    request = TTSRequest(text=args.text, provider=args.provider, voice=args.voice)

    start = time.monotonic()
    try:
        response = await generate_tts(request, base_url="http://localhost:8001")
    except Exception as e:
        print(f"❌ 生成失败: {e}")
        return

    elapsed_ms = int((time.monotonic() - start) * 1000)
    print("✅ 生成成功")
    print(f"Provider: {response.provider}")
    print(f"Voice: {response.voice}")
    print(f"音频文件: storage/audio/{response.filename}")
    print(f"耗时: {elapsed_ms}ms")


def main() -> None:
    args = parse_args()
    asyncio.run(run(args))


if __name__ == "__main__":
    main()
