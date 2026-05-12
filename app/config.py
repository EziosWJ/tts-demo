import os

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

TTS_PROVIDER: str = os.getenv("TTS_PROVIDER", "edge")
OPENAI_TTS_BASE_URL: str = os.getenv("OPENAI_TTS_BASE_URL", "")
OPENAI_TTS_API_KEY: str = os.getenv("OPENAI_TTS_API_KEY", "")
OPENAI_TTS_MODEL: str = os.getenv("OPENAI_TTS_MODEL", "tts-1")
OPENAI_TTS_VOICE: str = os.getenv("OPENAI_TTS_VOICE", "alloy")

COSYVOICE_BASE_URL: str = os.getenv("COSYVOICE_BASE_URL", "http://localhost:50000")
COSYVOICE_DEFAULT_VOICE: str = os.getenv("COSYVOICE_DEFAULT_VOICE", "中文女")
