# CosyVoice 独立服务集成

TTS Demo 需要接入开源 TTS 模型以验证本地部署语音合成能力。选择 CosyVoice 2（阿里开源）作为开源模型 provider，通过 httpx 调用其独立部署的 FastAPI 推理服务，仅使用 SFT 模式（预置音色）。

## Considered Options

1. **Python SDK 直连** — 将 CosyVoice 和 PyTorch 装进 TTS Demo 进程，直接调用模型推理。简单但引入重依赖，与现有轻量架构冲突。
2. **独立推理服务 + httpx 调用** — CosyVoice 单独部署为 FastAPI 服务，TTS Demo 通过 HTTP 调用。保持 TTS Demo 轻量，模型常驻无需每次冷启动。
3. **Docker 容器部署** — 用官方 Dockerfile 部署 CosyVoice。部署干净但需要 nvidia-container-toolkit，增加环境配置复杂度。

## Decision

选择方案 2。理由：

- TTS Demo 不引入 PyTorch 等重依赖，保持项目轻量
- 模型加载一次常驻，避免每次请求冷启动（首次加载需几十秒）
- 与 edge-tts provider 的调用模式一致（异步等待外部服务返回结果）
- 未来可平滑切换为 Docker 或远程部署，只需改配置 URL

CosyVoice 返回 raw PCM 数据（int16, 22050 Hz），在 provider 中转换为 WAV 格式。不引入 pydub/ffmpeg，WAV 转换仅需添加 44 字节 header。
