# ⚡ 快速配置 Qwen3-TTS-Flash（5分钟搞定）

## 🎯 问题诊断

如果你看到这个错误：
```
❌ 语音生成失败
✅ API 密钥已配置: ms-593358a7...
```

**原因：** 你使用的是 **ModelScope token**（`ms-` 开头），但 Qwen3-TTS需要 **DashScope API Key**（`sk-` 开头）

---

## ✅ 解决方案

### 步骤 1：获取 DashScope API Key

1. 访问：https://dashscope.console.aliyun.com/apiKey
2. 登录阿里云账号
3. 点击「创建新的 API-KEY」
4. 复制 API Key（格式：`sk-xxxxxxxxxxxxxxxx`）

### 步骤 2：修改 .env 文件

在 `.env` 文件中添加：

```ini
# 阿里云 DashScope API Key（用于TTS，sk- 开头）
DASHSCOPE_API_KEY=sk-你的DashScope密钥

# TTS 音色配置（使用新模型）
TTS_VOICE=longxiaochun
```

**完整配置示例：**

```ini
# ============================================================
# LLM 推理（使用 ModelScope）
# ============================================================
OPENAI_API_KEY=ms-593358a7-2adf-xxxx-xxxx-xxxxxxxxxxxx
OPENAI_API_BASE=https://api-inference.modelscope.cn/v1/
OPENAI_MODEL=Qwen/Qwen2.5-32B-Instruct

# ============================================================
# TTS 语音（使用 DashScope）
# ============================================================
DASHSCOPE_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TTS_ENABLED=true
TTS_VOICE=Cherry
```

### 步骤 3：测试

运行测试脚本：

```bash
python test_qwen3_tts.py
```

**期望输出：**
```
✅ API 密钥已配置: sk-xxxxxxx... (DashScope)
🎤 使用音色: Cherry
🎯 模型: qwen3-tts-flash
✅ 所有测试通过! (3/3)
🎉 Qwen3-TTS-Flash 配置成功!
```

---

## 🎤 音色选择（可选）

在 `.env` 中修改 `TTS_VOICE` 来更换音色：

### Qwen3-TTS-Flash 音色
```ini
TTS_VOICE=Cherry  # 甜美清晰 ⭐ 默认
TTS_VOICE=Bella   # 温柔优雅
TTS_VOICE=Amy     # 亲切自然
TTS_VOICE=Emma    # 活泼可爱
TTS_VOICE=Cora    # 成熟稳重
TTS_VOICE=Eva     # 知性优雅
TTS_VOICE=Kate    # 清新甜美
TTS_VOICE=Luna    # 温柔轻柔
TTS_VOICE=Sara    # 干练明快
```

---

## 🔧 检查配置

**方法1：运行配置检查工具**
```bash
python check_tts_options.py
```

**方法2：直接测试**
```bash
python test_qwen3_tts.py
```

---

## ❓ 常见问题

### Q: 我需要两个不同的 API Key 吗？

**A: 推荐但不是必须。**

**推荐配置（免费）：**
- LLM 用 ModelScope（`ms-` 开头，免费）
- TTS 用 DashScope（`sk-` 开头，有免费额度）

**简化配置（付费/有免费额度）：**
- 都用 DashScope（只需一个 `sk-` 开头的 Key）

### Q: DashScope API Key 免费吗？

**A: 有免费额度。** 个人测试和小规模使用足够。

查看定价：https://help.aliyun.com/zh/dashscope/developer-reference/tongyi-qianwen-metering-and-billing

### Q: 为什么音色改成了 Cherry？

**A: 新模型更好。**

项目已升级到 `qwen3-tts-flash`：
- ⚡ 延迟更低（~97ms vs ~200ms）
- 🎵 音质更好（24kHz vs 16kHz）
- 🚀 支持流式输出
- 🌍 支持多语言

旧模型的音色如 `zhixiaobai` 在新模型中不可用。

### Q: 可以切换回旧模型吗？

**A: 可以，但不推荐。** 

新模型 `qwen3-tts-flash` 音质更好、延迟更低。如果确实需要，修改 `config/default.json`：

```json
"tts": {
  "model": "sambert-zhichu-v1",
  "voice": "zhixiaobai"
}
```

然后在 `.env` 中：
```ini
TTS_VOICE=zhixiaobai
```

注意：代码会自动降级，如果新模型失败会尝试旧模型。

---

## 📚 详细文档

- **双API配置指南**: `双API配置指南.md`
- **Qwen3-TTS配置**: `QWEN3_TTS_配置说明.md`
- **阿里云TTS配置**: `阿里云TTS配置说明.md`

---

## 🚀 启动游戏

配置完成后：

```bash
# 后端
python main.py --mode web

# 前端（新终端）
cd frontend
npm run dev
```

访问：http://localhost:5173

---

**5分钟搞定！现在试试 `python test_qwen3_tts.py` 吧！** 🎉

