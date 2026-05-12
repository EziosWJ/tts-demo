# tts-demo

极简本地 TTS Demo，用于验证 AI 面试系统中的"文本生成语音并播放"能力。

## 技术栈

- Python 3.12+
- FastAPI + uvicorn
- edge-tts（默认 TTS 引擎）
- openai（OpenAI-compatible TTS 支持）
- CosyVoice 2（开源语音合成模型，独立部署）
- httpx（HTTP 客户端，用于调用 CosyVoice 服务）
- uv（依赖管理）

## 安装依赖

```bash
cd tts-demo
uv sync
```

## 启动服务

```bash
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 浏览器测试

访问 http://localhost:8000，输入文本，点击"生成语音"按钮即可试听。

## CLI 测试

```bash
# 使用默认配置
uv run python -m app.cli "请你做一个自我介绍"

# 指定 provider 和音色
uv run python -m app.cli "请你做一个自我介绍" --provider edge --voice zh-CN-YunxiNeural
```

## .env 配置说明

复制 `.env.example` 为 `.env`，按需修改：

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `TTS_PROVIDER` | `edge` | 默认 TTS 引擎，可选 `edge` / `openai` / `cosyvoice` |
| `OPENAI_TTS_BASE_URL` | 空 | OpenAI-compatible 服务的 base URL |
| `OPENAI_TTS_API_KEY` | 空 | OpenAI-compatible 服务的 API Key |
| `OPENAI_TTS_MODEL` | `tts-1` | OpenAI TTS 模型名 |
| `OPENAI_TTS_VOICE` | `alloy` | OpenAI TTS 音色 |
| `COSYVOICE_BASE_URL` | `http://localhost:50000` | CosyVoice 推理服务地址 |
| `COSYVOICE_DEFAULT_VOICE` | `中文女` | CosyVoice 默认音色 |

## edge-tts 说明

[edge-tts](https://github.com/rany2/edge-tts) 是微软 Edge 浏览器 TTS 接口的 Python 封装：

- **完全免费**，无需 API Key
- 支持多种中文音色，如 `zh-CN-XiaoxiaoNeural`、`zh-CN-YunxiNeural`
- 本项目默认使用此引擎

常用中文音色：

| 音色 | 描述 |
|------|------|
| `zh-CN-XiaoxiaoNeural` | 女声（默认） |
| `zh-CN-YunxiNeural` | 男声 |
| `zh-CN-XiaoyiNeural` | 女声（台湾腔） |
| `zh-CN-YunjianNeural` | 男声（新闻播报） |

查看所有可用音色：

```bash
uv run edge-tts --list-voices | grep zh-CN
```

## OpenAI-compatible Provider 说明

支持任何兼容 OpenAI TTS API 的服务（如本地部署的 Whisper/ChatTTS 等）。

配置方式：在 `.env` 中设置：

```
TTS_PROVIDER=openai
OPENAI_TTS_BASE_URL=http://your-server:8080/v1
OPENAI_TTS_API_KEY=sk-xxx
OPENAI_TTS_MODEL=tts-1
OPENAI_TTS_VOICE=alloy
```

## CosyVoice Provider 说明

[CosyVoice 2](https://github.com/FunAudioLLM/CosyVoice) 是阿里开源的语音合成模型，支持多语言、多音色的高质量语音合成。

### 部署 CosyVoice 推理服务

CosyVoice 作为独立服务部署，TTS Demo 通过 HTTP 调用。仅支持 SFT 模式（预置音色）。

```bash
# 1. 克隆 CosyVoice 仓库
git clone https://github.com/FunAudioLLM/CosyVoice.git
cd CosyVoice

# 2. 安装依赖（需要 GPU 环境）
pip install -r requirements.txt

# 3. 启动 FastAPI 推理服务（默认端口 50000）
python runtime/python/fastapi/server.py --port 50000
```

服务启动后，可用以下命令测试：

```bash
curl -X GET "http://localhost:50000/inference_sft?tts_text=你好世界&spk_id=中文女" --output test.wav
```

### 配置 TTS Demo 使用 CosyVoice

在 `.env` 中设置：

```
TTS_PROVIDER=cosyvoice
COSYVOICE_BASE_URL=http://localhost:50000
COSYVOICE_DEFAULT_VOICE=中文女
```

### 可用音色

SFT 模式下预置音色：`中文女`、`中文男`、`英文女`、`英文男`、`日语男`、`粤语女`、`韩语女`。

页面上选择 CosyVoice provider 后，音色列表会自动从后端获取。

## 项目结构

```
tts-demo/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI 应用入口
│   ├── cli.py               # CLI 命令行入口
│   ├── config.py            # 环境变量配置
│   ├── providers/           # TTS Provider 实现
│   │   ├── __init__.py
│   │   ├── base.py          # Provider 基类
│   │   ├── edge_tts.py      # edge-tts 实现
│   │   ├── openai_tts.py    # OpenAI-compatible 实现
│   │   └── cosyvoice_provider.py  # CosyVoice 预留
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── tts.py           # 请求/响应数据模型
│   ├── services/
│   │   ├── __init__.py
│   │   └── tts_service.py   # TTS 业务逻辑
│   └── templates/
│       └── index.html        # Web 前端页面
├── storage/
│   └── audio/                # 生成的音频文件存储目录
├── .env.example
├── .gitignore
├── pyproject.toml
└── uv.lock
```

## 常见问题

**Q: 生成音频时报错 "edge-tts not found"？**

A: 确保已执行 `uv sync` 安装依赖。如果仍有问题，尝试 `uv sync --reinstall`。

**Q: 如何更换中文音色？**

A: CLI 中使用 `--voice` 参数指定，如 `--voice zh-CN-YunxiNeural`。Web 页面中在音色输入框填入音色名即可。

**Q: 生成的音频文件在哪里？**

A: 在 `storage/audio/` 目录下，文件名格式为 `tts_日期时间_随机ID.mp3`。

**Q: 能否使用其他 OpenAI-compatible 的 TTS 服务？**

A: 可以。在 `.env` 中将 `TTS_PROVIDER` 设为 `openai`，并配置对应的 `OPENAI_TTS_BASE_URL` 和 `OPENAI_TTS_API_KEY` 即可。
