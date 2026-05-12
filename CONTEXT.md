# TTS Demo

极简本地 TTS Demo 项目，用于验证 AI 面试系统中的"文本生成语音并播放"能力。这是一个纯 demo，不做前后端分离，不做生产级抽象。

## Language

**Provider**:
TTS 语音合成服务的提供方。本项目支持三种 provider：edge-tts（完整）、OpenAI-compatible（完整）、CosyVoice（完整）。
_Avoid_: engine, backend, service (这些词太泛)

**Voice**:
TTS 合成时使用的音色标识符，格式如 `zh-CN-XiaoxiaoNeural`。每个 provider 支持的音色不同。
_Avoid_: speaker, voice model

**Audio**:
TTS 生成的音频文件。edge-tts 和 OpenAI provider 生成 mp3，CosyVoice 生成 wav。保存在 `storage/audio/` 目录下，文件名格式为 `tts_时间戳_随机ID.mp3`（或 `.wav`）。
_Avoid_: sound, recording

**SFT 模式**:
CosyVoice 的预置音色推理模式。传入文本和音色 ID（如 `中文女`），直接生成音频。不需要参考音频或音色克隆。
_Avoid_: preset mode, default mode

**PCM 音频**:
CosyVoice 推理服务返回的原始音频格式（int16 PCM，22050 Hz）。没有文件头，需要在 provider 中转换为 WAV 格式才能被浏览器播放。
_Avoid_: raw audio, uncompressed audio

**Record**:
一次 TTS 生成的完整记录，包含文本、provider、voice、音频路径、耗时等。以 JSONL 格式追加写入 `storage/tts_records.jsonl`。
_Avoid_: log, entry

**Duration**:
TTS 调用的实际耗时（毫秒），用 `time.perf_counter()` 计算，不包括文件保存和日志写入。
_Avoid_: latency, time

## Relationships

- 一次 **TTS 生成** 使用一个 **Provider** 和一个 **Voice**
- 一次 **TTS 生成** 产生一个 **Audio** 文件和一条 **Record**
- 一个 **Provider** 支持多个 **Voice**
- **Audio** 文件的元数据（文本、provider、voice、耗时）存储在对应的 **Record** 中

## Design decisions

### Provider 范围

edge-tts、OpenAI-compatible、CosyVoice 三种 provider 均已完整实现。CosyVoice 通过 httpx 调用独立部署的 CosyVoice 推理服务（FastAPI server，默认端口 50000），仅支持 SFT 模式。

### 前端技术

纯原生 HTML + JS，不使用 React/Vue。页面由 FastAPI 直接返回。

### 配置管理

使用 `os.getenv()` 读取环境变量，不用 pydantic-settings。配置放在 `app/config.py`。

### 错误处理

极简策略，使用 FastAPI 的 `HTTPException`。不搞自定义异常类和全局异常处理器。

### 代码复用

CLI 和 Web 共享同一个 `tts_service.py`。CLI 是薄壳，调用 service 层。

### 数据模型

只用两个 Pydantic 模型：`TTSRequest` 和 `TTSResponse`，放在 `schemas/tts.py`。

### 文件存储

文件操作逻辑放在 `tts_service.py`，用 `pathlib`。不需要单独的 `audio_store.py`。

### CosyVoice 集成方式

CosyVoice 作为独立推理服务部署，TTS Demo 通过 httpx 调用其 FastAPI 端点（`/inference_sft`）。CosyVoice 返回 raw PCM 数据，在 provider 中转换为 WAV 格式。不将 PyTorch 等重依赖引入 TTS Demo。

### 音色管理

每个 provider 独立维护音色列表，通过 `list_voices()` 方法返回 `list[str]`。前端通过 `/api/voices?provider=xxx` 接口动态获取音色列表，切换 provider 时自动刷新下拉框。

## Example dialogue

> **Dev:** "edge-tts 和 OpenAI provider 的调用方式差异很大，怎么统一接口？"
> **Domain expert:** "用抽象基类定义统一接口，但实现可以完全不同。edge-tts 是异步调用，OpenAI 是 HTTP 请求，但对外都是 `generate(text, voice) -> bytes`。"

> **Dev:** "页面上需要显示历史生成记录吗？"
> **Domain expert:** "不需要。页面只做输入→生成→播放。JSONL 只是后端日志，不暴露给前端。"
