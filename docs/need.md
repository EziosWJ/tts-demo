你是一名资深 Python 全栈开发工程师，请实现一个极简本地 TTS Demo 项目，用于验证 AI 面试系统中的“文本生成语音并播放”能力。

项目名称：tts-demo

核心目标：
1. 本地启动一个 Python 服务。
2. 浏览器打开页面后，可以输入中文文本。
3. 点击按钮后调用 TTS 生成 mp3。
4. 页面自动播放生成的音频。
5. 音频保存到本地目录。
6. 生成记录写入 jsonl 日志。
7. 同时提供 CLI 命令测试入口。
8. 暂时不做前后端分离，不创建 Vite/React 独立前端项目。

技术要求：
- Python 3.12+
- 使用 uv 管理依赖
- FastAPI
- uvicorn
- edge-tts 作为默认 TTS Provider
- pydantic-settings 可选
- 页面由 FastAPI 直接返回 HTML
- 前端可以使用原生 HTML + JS；如确实需要 React/JSX，可通过 CDN 写在单个 HTML 页面中
- 不使用 pipenv、poetry
- 不需要登录、鉴权、token
- 不需要 WebRTC
- 不需要实时流式播放
- 不需要 STT
- 不需要数字人
- 不需要完整 AI 面试流程

建议项目结构：
tts-demo/
  app/
    main.py
    cli.py
    core/
      config.py
    schemas/
      tts.py
    services/
      tts_service.py
      providers/
        base.py
        edge_tts_provider.py
        openai_tts_provider.py
        cosyvoice_provider.py
    utils/
      audio_store.py
    templates/
      index.html
  storage/
    audio/
    tts_records.jsonl
  docs/
    TTS_DEMO_IMPLEMENTATION_SUMMARY.md
  .env.example
  pyproject.toml
  README.md

后端接口：
1. GET /
返回一个简单 HTML 测试页面。

2. POST /api/tts/generate
请求示例：
{
  "text": "请你用自然、专业的语气，邀请候选人做一个一分钟的自我介绍。",
  "provider": "edge",
  "voice": "zh-CN-XiaoxiaoNeural"
}

响应示例：
{
  "id": "xxx",
  "provider": "edge",
  "voice": "zh-CN-XiaoxiaoNeural",
  "audio_url": "http://localhost:8000/audio/xxx.mp3",
  "filename": "xxx.mp3",
  "duration_ms": 1234,
  "created_at": "2026-05-10 12:00:00"
}

3. GET /audio/{filename}
用于浏览器播放生成的 mp3 文件。

页面功能：
- 一个文本输入框
- Provider 选择框，默认 edge
- 音色选择框
- 生成按钮
- loading 状态
- 错误提示
- 生成成功后自动播放
- 显示 audio 控件，可重复播放
- 显示音频 URL
- 显示生成耗时
- 默认文本：请你用自然、专业的语气，邀请候选人做一个一分钟的自我介绍。

默认音色：
- zh-CN-XiaoxiaoNeural
- zh-CN-YunxiNeural
- zh-CN-YunjianNeural
- zh-CN-XiaoyiNeural

Provider 设计：
1. base.py 定义统一 TTS Provider 接口。
2. edge_tts_provider.py 必须可用，是第一版默认实现。
3. openai_tts_provider.py 只需要预留基础结构，支持从 .env 读取配置；配置缺失时返回明确错误。
4. cosyvoice_provider.py 只需要预留占位结构和说明，暂不强制实现本地模型推理。
5. Provider 选择错误时，应返回清晰错误信息。

.env.example 示例：
TTS_PROVIDER=edge
OPENAI_TTS_BASE_URL=
OPENAI_TTS_API_KEY=
OPENAI_TTS_MODEL=
OPENAI_TTS_VOICE=

文件保存：
- 生成的 mp3 保存到 storage/audio/
- 文件名格式建议：tts_年月日时分秒_随机ID.mp3
- 程序启动或生成前应自动创建 storage/audio 目录

日志要求：
每次生成成功后，追加写入 storage/tts_records.jsonl。
每行一个 JSON，记录：
{
  "id": "xxx",
  "provider": "edge",
  "voice": "zh-CN-XiaoxiaoNeural",
  "text": "原始文本",
  "audio_path": "storage/audio/xxx.mp3",
  "audio_url": "http://localhost:8000/audio/xxx.mp3",
  "duration_ms": 1234,
  "created_at": "2026-05-10 12:00:00"
}

CLI 要求：
支持命令行生成语音：
uv run python -m app.cli "请你做一个自我介绍"

可选参数：
--provider edge
--voice zh-CN-XiaoxiaoNeural

CLI 输出：
- 是否成功
- provider
- voice
- 音频文件路径
- 生成耗时

错误处理：
必须处理以下情况：
- text 为空
- text 过长
- provider 不支持
- voice 为空
- TTS 调用失败
- 文件保存失败
- OpenAI-compatible 配置缺失

运行方式：
后端启动：
cd tts-demo
uv sync
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

浏览器访问：
http://localhost:8000

CLI 测试：
uv run python -m app.cli "请你做一个自我介绍"

README 要求：
README.md 必须包含：
1. 项目用途
2. 技术栈
3. 安装依赖
4. 启动服务
5. 浏览器测试方式
6. CLI 测试方式
7. .env 配置说明
8. edge-tts 说明
9. OpenAI-compatible Provider 说明
10. CosyVoice 预留说明
11. 常见问题

验收标准：
1. uv sync 成功。
2. FastAPI 服务可启动。
3. 打开 http://localhost:8000 能看到测试页面。
4. 输入中文文本后能生成 mp3。
5. 页面能自动播放 mp3。
6. storage/audio 下能看到生成的音频文件。
7. storage/tts_records.jsonl 能看到生成记录。
8. CLI 能成功生成音频。
9. edge provider 可用。
10. openai/cosyvoice provider 有清晰预留结构和错误说明。
11. README 能指导新人跑通项目。

代码要求：
- 代码清晰、模块化
- Python 尽量使用类型标注
- 不要把全部逻辑写在 main.py
- 不要硬编码绝对路径
- 不提交真实 API Key
- .env.example 只放示例
- 生成失败不要写入成功日志
- 页面保持简洁工具型，不做花哨 UI

最后要求：
完成后必须在 docs/TTS_DEMO_IMPLEMENTATION_SUMMARY.md 写入总结，包含：
1. 修改文件
2. 实现内容
3. 运行方式
4. 验证结果
5. 未完成事项
6. 后续建议

最终回复也必须总结：
1. 修改了哪些文件
2. 实现了哪些功能
3. 如何运行验证
4. 是否有未完成或需要人工确认的事项