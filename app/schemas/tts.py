from pydantic import BaseModel, Field


class TTSRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=1000)
    provider: str = "edge"
    voice: str = "zh-CN-XiaoxiaoNeural"


class TTSResponse(BaseModel):
    id: str
    provider: str
    voice: str
    audio_url: str
    filename: str
    duration_ms: int
    created_at: str
