from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, HTMLResponse

from app.schemas.tts import TTSRequest, TTSResponse
from app.services.tts_service import generate_tts, get_provider

_STORAGE_DIR = Path(__file__).resolve().parent.parent / "storage"
_AUDIO_DIR = _STORAGE_DIR / "audio"
_TEMPLATE_DIR = Path(__file__).resolve().parent / "templates"


@asynccontextmanager
async def lifespan(app: FastAPI):
    _AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    yield


app = FastAPI(title="TTS Demo", lifespan=lifespan)


@app.get("/", response_class=HTMLResponse)
async def index():
    html = (_TEMPLATE_DIR / "index.html").read_text(encoding="utf-8")
    return HTMLResponse(content=html)


@app.post("/api/tts/generate", response_model=TTSResponse)
async def tts_generate(request: Request, body: TTSRequest):
    if not body.text.strip():
        raise HTTPException(status_code=400, detail="text 不能为空")

    try:
        get_provider(body.provider)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    base_url = f"{request.url.scheme}://{request.url.netloc}"
    try:
        return await generate_tts(body, base_url)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"TTS 生成失败: {e}")


@app.get("/api/voices")
async def list_voices(provider: str = "edge"):
    try:
        p = get_provider(provider)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return p.list_voices()


@app.get("/audio/{filename}")
async def serve_audio(filename: str):
    file_path = _AUDIO_DIR / filename
    if not file_path.is_file():
        raise HTTPException(status_code=404, detail="音频文件不存在")
    media_type = "audio/wav" if filename.endswith(".wav") else "audio/mpeg"
    return FileResponse(file_path, media_type=media_type)
