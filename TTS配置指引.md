# 🎙️ TTS 配置指引

> **一句话配置：** 复制 `env.example.txt` 到 `.env`，填入 API Key，运行 `python test_qwen3_tts.py` 测试。

---

## 📋 配置文件说明

本项目提供了以下配置相关文件：

| 文件 | 用途 | 查看时机 |
|------|------|---------|
| **env.example.txt** | 完整配置模板 ⭐ | 首次配置必看 |
| **快速配置TTS.md** | 5分钟快速上手 | 想快速开始 |
| **QWEN3_TTS_配置说明.md** | 详细配置文档 | 需要详细了解 |
| **双API配置指南.md** | 双API配置方案 | 使用 ModelScope + DashScope |
| **配置完成总结.md** | 配置状态总结 | 确认配置结果 |

---

## ⚡ 3分钟快速配置

### 第1步：复制配置文件

```bash
cp env.example.txt .env
```

### 第2步：填写 API Key

编辑 `.env` 文件，填入你的密钥：

```ini
# LLM 推理（ModelScope - 免费）
OPENAI_API_KEY=ms-your-token-here

# TTS 语音（DashScope - 有免费额度）
DASHSCOPE_API_KEY=sk-your-key-here

# 音色设置
TTS_VOICE=Cherry
```

**获取密钥：**
- ModelScope: https://www.modelscope.cn/my/myaccesstoken
- DashScope: https://dashscope.console.aliyun.com/apiKey

### 第3步：测试

```bash
python test_qwen3_tts.py
```

看到 `✅ 所有测试通过!` 即为成功！

---

## 🎯 核心配置项

### 必填项（3个）

```ini
OPENAI_API_KEY=ms-xxx          # ModelScope token（或使用 DashScope key）
DASHSCOPE_API_KEY=sk-xxx       # DashScope API Key（用于TTS）
TTS_VOICE=Cherry               # 音色
```

### 可选项

```ini
TTS_SPEED=1.0                  # 语速（0.5-2.0）
TTS_PITCH=1.0                  # 音高（0.5-2.0）
LLM_TEMPERATURE=0.8            # LLM 温度
LLM_MAX_TOKENS=500             # LLM 最大 token
```

---

## 🎤 音色选择

### Qwen3-TTS-Flash（推荐）

```ini
TTS_VOICE=Cherry   # ⭐ 甜美清晰（默认）
TTS_VOICE=Bella    # 温柔优雅
TTS_VOICE=Amy      # 亲切自然
TTS_VOICE=Emma     # 活泼可爱
TTS_VOICE=Cora     # 成熟稳重
TTS_VOICE=Eva      # 知性优雅
TTS_VOICE=Kate     # 清新甜美
TTS_VOICE=Luna     # 温柔轻柔
TTS_VOICE=Sara     # 干练明快
```

---

## 🔧 配置方案

### 方案A：双API（推荐 - 免费）

```ini
# LLM 用 ModelScope（免费）
OPENAI_API_KEY=ms-your-token
OPENAI_API_BASE=https://api-inference.modelscope.cn/v1/
OPENAI_MODEL=Qwen/Qwen2.5-32B-Instruct

# TTS 用 DashScope（有免费额度）
DASHSCOPE_API_KEY=sk-your-key
TTS_VOICE=Cherry
```

### 方案B：单API（简化）

```ini
# 全部用 DashScope
OPENAI_API_KEY=sk-your-key
OPENAI_API_BASE=https://dashscope.aliyuncs.com/compatible-mode/v1
OPENAI_MODEL=qwen-plus

TTS_VOICE=Cherry
```

---

## ✅ 测试工具

```bash
# 测试 TTS
python test_qwen3_tts.py

# 检查配置
python check_tts_options.py

# 完整测试
python main.py --mode web       # 后端
cd frontend && npm run dev      # 前端
```

---

## 📚 详细文档

- **完整配置**: 查看 `env.example.txt` 的注释
- **快速上手**: 阅读 `快速配置TTS.md`
- **详细说明**: 参考 `QWEN3_TTS_配置说明.md`
- **配置总结**: 查看 `配置完成总结.md`

---

## ❓ 常见问题

**Q: 需要几个 API Key？**
- 最少1个（DashScope）
- 推荐2个（ModelScope + DashScope，可省钱）

**Q: 如何测试是否配置成功？**
```bash
python test_qwen3_tts.py
```

**Q: 音色不生效怎么办？**
- 检查 `.env` 中的 `TTS_VOICE` 配置
- 确保使用 Qwen3-TTS 音色（Cherry、Bella等）
- 不要使用旧音色（zhixiaobai等）

---

## 🚀 快速启动

```bash
# 1. 配置
cp env.example.txt .env
# 编辑 .env 填入 API Key

# 2. 测试
python test_qwen3_tts.py

# 3. 启动
python main.py --mode web        # 后端
cd frontend && npm run dev       # 前端

# 4. 访问
# http://localhost:5173
```

---

**配置很简单！遇到问题查看详细文档即可。** 🎉


