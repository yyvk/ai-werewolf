# 🎙️ Qwen3-TTS-Flash 配置说明

## ✨ 新模型特性

**`qwen3-tts-flash`** 是阿里云推出的新一代实时语音合成模型，相比旧的 `sambert-zhichu-v1` 具有以下优势：

- ⚡ **更低延迟**：实时流式合成，响应更快
- 🎵 **音质更好**：更自然的语音表现
- 🗣️ **音色更丰富**：支持更多音色选项
- 🚀 **更高效率**：优化的推理性能

---

## 📋 配置完成情况

✅ 已完成以下配置：

1. **配置文件** (`config/default.json`)
   - 模型改为：`qwen3-tts-flash`
   - API：使用 `MultiModalConversation.call()`
   - 采样率：`24000 Hz`
   - 默认音色：`Cherry`

2. **TTS 服务** (`src/utils/tts_service_dashscope.py`)
   - 更新为使用新 API
   - 支持流式音频生成
   - 自动降级到旧模型

3. **测试脚本** (`test_qwen3_tts.py`)
   - 新的测试脚本，使用正确的 API

---

## 🎤 支持的音色

Qwen3-TTS-Flash 支持以下音色：

### 女声 ⭐
| 音色代码 | 描述 |
|---------|------|
| `Cherry` | 甜美清晰 ⭐ 默认 |
| `Bella` | 温柔优雅 |
| `Amy` | 亲切自然 |
| `Emma` | 活泼可爱 |
| `Cora` | 成熟稳重 |
| `Eva` | 知性优雅 |
| `Kate` | 清新甜美 |
| `Luna` | 温柔轻柔 |
| `Sara` | 干练明快 |

---

## 🔧 修改音色

### 方式 1：通过环境变量（推荐）

在 `.env` 文件中配置：

```ini
# TTS 配置
TTS_ENABLED=true
TTS_VOICE=Cherry  # 改成你想要的音色
```

### 方式 2：修改配置文件

编辑 `config/default.json`：

```json
"tts": {
  "enabled": true,
  "model": "qwen3-tts-flash",
  "voice": "Bella",  // 改成其他音色
  "speed": 1.0,
  "pitch": 1.0
}
```

---

## ✅ 测试配置

运行测试脚本验证配置：

```bash
# 方法1：使用环境变量设置音色
$env:TTS_VOICE='Cherry'; python test_qwen3_tts.py

# 方法2：直接运行（使用配置文件中的音色）
python test_qwen3_tts.py
```

如果看到以下输出，说明配置成功：

```
✅ 所有测试通过! (3/3)
🎉 Qwen3-TTS-Flash 配置成功!
```

测试音频文件会保存在：`assets/audio/qwen3_test_*.wav`

---

## 🎮 在游戏中使用

### 启动后端服务

```bash
python main.py --mode web
```

### 启动前端（新终端窗口）

```bash
cd frontend
npm run dev
```

### 访问游戏

打开浏览器访问：http://localhost:5173

---

## 🔑 API 密钥配置

确保 `.env` 文件中配置了阿里云 DashScope API Key：

```ini
# 阿里云 DashScope API Key
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
OPENAI_API_BASE=https://dashscope.aliyuncs.com/compatible-mode/v1
```

**获取 API Key**: https://dashscope.console.aliyun.com/apiKey

---

## ⚙️ 高级配置

### 调整语速

在配置文件中修改 `speed` 参数：

```json
"tts": {
  "speed": 1.2  // 1.0 = 正常速度，1.2 = 加快 20%
}
```

### 调整音高

```json
"tts": {
  "pitch": 1.0  // 1.0 = 正常音高，0.8 = 降低音高
}
```

---

## 📊 模型对比

| 特性 | sambert-zhichu-v1 (旧) | qwen3-tts-flash (新) |
|-----|----------------------|---------------------|
| API | SpeechSynthesizer | MultiModalConversation ⭐ |
| 延迟 | ~200ms | ~97ms ⚡ |
| 音质 | 标准 | 更自然 🎵 |
| 采样率 | 16kHz | 24kHz |
| 音色数量 | 6 个 | 17 个 |
| 流式支持 | 否 | 是 ✅ |
| 多语言 | 中文 | 10+ 语言 🌍 |

---

## ❓ 常见问题

### Q: 为什么音色名称变了？

**A**: 新模型 `qwen3-tts-flash` 使用完全不同的 API 和音色系统。旧模型的音色如 `zhixiaobai` 在新模型中不可用。请使用新的音色代码，如 `Cherry`、`Bella` 等。

### Q: 可以同时使用多个音色吗？

**A**: 可以。在游戏中可以为不同玩家配置不同音色。目前默认所有玩家使用同一音色，如需区分可以修改代码。

### Q: 新模型会增加费用吗？

**A**: 阿里云提供免费额度，个人测试和小规模使用足够。具体计费请查看：https://help.aliyun.com/zh/dashscope/developer-reference/tongyi-qianwen-metering-and-billing

### Q: 如果想切回旧模型怎么办？

**A**: 将配置文件中的 `model` 改回 `sambert-zhichu-v1`，`sample_rate` 改为 `16000`，音色改为 `zhixiaobai` 等旧音色即可。

---

## 🔗 相关链接

- **DashScope 控制台**: https://dashscope.console.aliyun.com/
- **API 文档**: https://help.aliyun.com/zh/dashscope/developer-reference/api-text-to-speech
- **音色试听**: https://help.aliyun.com/zh/dashscope/developer-reference/model-square

---

## 📝 更新记录

- **2025-11-06**: 升级到 `qwen3-tts-flash` 模型
- 模型：`sambert-zhichu-v1` → `qwen3-tts-flash`
- API：`SpeechSynthesizer` → `MultiModalConversation`
- 采样率：`16000 Hz` → `24000 Hz`
- 默认音色：`zhixiaobai` → `Cherry`
- 支持流式输出和多语言

---

**配置完成！** 🎉

现在你可以运行 `python test_qwen3_tts.py` 来测试新的语音模型了。

