# 🔧 双 API 配置指南

## 📌 配置方案

本项目支持同时使用两个不同的服务：

| 功能 | 服务提供商 | API Key 类型 | 环境变量 |
|-----|----------|-------------|---------|
| **LLM 推理** | ModelScope | `ms-` 开头 | `OPENAI_API_KEY` |
| **TTS 语音** | DashScope | `sk-` 开头 | `DASHSCOPE_API_KEY` |

---

## 🎯 为什么需要两个 API Key？

1. **ModelScope** 提供免费的大模型推理服务（如 Qwen2.5）
2. **DashScope** 提供高质量的语音合成服务（TTS）
3. 两者是不同的服务，需要不同的 API Key

---

## ⚙️ 配置步骤

### 1️⃣ 获取 ModelScope Token

用于 LLM 推理（玩家发言、投票决策等）

1. 访问：https://www.modelscope.cn/my/myaccesstoken
2. 登录并获取 token（格式：`ms-xxxxxxx`）
3. 在 `.env` 中配置：

```ini
OPENAI_API_KEY=ms-your-modelscope-token-here
OPENAI_API_BASE=https://api-inference.modelscope.cn/v1/
OPENAI_MODEL=Qwen/Qwen2.5-32B-Instruct
LLM_PROVIDER=openai
```

### 2️⃣ 获取 DashScope API Key

用于 TTS 语音合成（文字转语音）

1. 访问：https://dashscope.console.aliyun.com/apiKey
2. 登录阿里云并创建 API Key（格式：`sk-xxxxxxx`）
3. 在 `.env` 中配置：

```ini
DASHSCOPE_API_KEY=sk-your-dashscope-api-key-here
TTS_ENABLED=true
TTS_VOICE=longxiaochun
```

---

## 📋 完整的 .env 配置示例

```ini
# ============================================================
# LLM 对话模型配置（使用 ModelScope）
# ============================================================

# ModelScope API 配置 (ms- 开头)
OPENAI_API_KEY=ms-593358a7-2adf-xxxx-xxxx-xxxxxxxxxxxx
OPENAI_API_BASE=https://api-inference.modelscope.cn/v1/
OPENAI_MODEL=Qwen/Qwen2.5-32B-Instruct
LLM_PROVIDER=openai

# LLM 参数配置
LLM_TEMPERATURE=0.8
LLM_MAX_TOKENS=500

# ============================================================
# TTS 语音合成配置（使用阿里云 DashScope）
# ============================================================

# 阿里云 DashScope API Key (sk- 开头)
DASHSCOPE_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# TTS 配置 - 使用新模型音色 (cosyvoice-v1)
TTS_ENABLED=true
TTS_VOICE=longxiaochun
TTS_SPEED=1.0
TTS_PITCH=1.0

# ============================================================
# Web 服务配置
# ============================================================

WEB_HOST=0.0.0.0
WEB_PORT=8000
```

---

## ✅ 验证配置

### 测试 TTS（语音合成）

```bash
python test_dashscope_tts.py
```

**期望输出：**
```
✅ API 密钥已配置: sk-xxxxxxx... (DashScope)
🎤 使用音色: longxiaochun
✅ 所有测试通过! (3/3)
```

**如果看到警告：**
```
⚠️  警告: 检测到 ModelScope token
```

说明你需要添加 `DASHSCOPE_API_KEY` 到 `.env` 文件。

### 测试完整流程

```bash
# 启动后端
python main.py --mode web

# 新终端启动前端
cd frontend
npm run dev
```

---

## 🎤 TTS 音色选择

### 新模型音色 (cosyvoice-v1) ⭐ 推荐

更快、音质更好、延迟更低

| 音色代码 | 描述 | 性别 |
|---------|------|------|
| `longxiaochun` | 龙小春 | 女（温柔清晰）⭐ |
| `longxiaoqing` | 龙小青 | 女（亲切自然）|
| `longjing` | 龙晶晶 | 女（甜美活泼）|
| `longxiaohao` | 龙小浩 | 男（沉稳大气）|
| `longxiaojian` | 龙小健 | 男（清朗有力）|
| `longxiaobei` | 龙小贝 | 儿童（可爱）|

### 旧模型音色 (sambert-zhichu-v1)

如需使用，在 `.env` 中设置：`TTS_VOICE=zhixiaobai`

---

## 🔍 常见问题

### Q1: 为什么我的 TTS 测试失败？

**原因：** 你可能只配置了 `OPENAI_API_KEY`（ModelScope token），但没有配置 `DASHSCOPE_API_KEY`。

**解决：** 在 `.env` 文件中添加：
```ini
DASHSCOPE_API_KEY=sk-your-dashscope-key
```

### Q2: 如果我只有一个 DashScope API Key，能同时用于 LLM 和 TTS 吗？

**可以！** 如果你不使用 ModelScope，可以只配置一个：

```ini
# 同时用于 LLM 和 TTS
OPENAI_API_KEY=sk-your-dashscope-key
OPENAI_API_BASE=https://dashscope.aliyuncs.com/compatible-mode/v1
OPENAI_MODEL=qwen-plus
```

### Q3: ModelScope 和 DashScope 有什么区别？

| | ModelScope | DashScope |
|---|-----------|-----------|
| **提供商** | ModelScope | 阿里云 |
| **主要功能** | 模型推理（免费） | TTS、LLM（付费/有免费额度）|
| **API Key 格式** | `ms-` 开头 | `sk-` 开头 |
| **TTS 支持** | ❌ 不支持 | ✅ 支持 |

### Q4: 音色代码不对，语音生成失败怎么办？

**原因：** 新旧模型的音色代码不同。

**解决：**
- 如果使用 `cosyvoice-v1`（默认），音色应为：`longxiaochun`, `longxiaohao` 等
- 如果使用 `sambert-zhichu-v1`（旧模型），音色应为：`zhixiaobai`, `zhitian` 等

在 `.env` 中设置正确的音色：
```ini
TTS_VOICE=longxiaochun
```

---

## 🚀 推荐配置

```ini
# LLM - 使用 ModelScope（免费）
OPENAI_API_KEY=ms-your-token
OPENAI_API_BASE=https://api-inference.modelscope.cn/v1/
OPENAI_MODEL=Qwen/Qwen2.5-32B-Instruct

# TTS - 使用 DashScope（音质更好）
DASHSCOPE_API_KEY=sk-your-key
TTS_VOICE=longxiaochun
```

这样配置可以：
- ✅ LLM 免费使用 ModelScope
- ✅ TTS 使用高质量的 DashScope 服务
- ✅ 两个服务互不影响

---

## 📚 相关文档

- **ModelScope Token**: https://www.modelscope.cn/my/myaccesstoken
- **DashScope API Key**: https://dashscope.console.aliyun.com/apiKey
- **DashScope TTS 文档**: https://help.aliyun.com/zh/dashscope/developer-reference/api-text-to-speech
- **Qwen3-TTS 配置**: 查看 `QWEN3_TTS_配置说明.md`

---

**配置完成后，运行 `python test_dashscope_tts.py` 验证！** 🎉


