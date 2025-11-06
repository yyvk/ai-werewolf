# 🔊 阿里云 TTS 配置说明

## 🎯 配置步骤

### 第一步：获取阿里云 API Key

1. 访问阿里云 DashScope 控制台：
   https://dashscope.console.aliyun.com/apiKey

2. 登录你的阿里云账号

3. 创建或复制你的 API-KEY

### 第二步：配置 .env 文件

在项目根目录的 `.env` 文件中，修改配置：

```ini
# 使用阿里云 DashScope 的 API Key
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
OPENAI_API_BASE=https://dashscope.aliyuncs.com/compatible-mode/v1
OPENAI_MODEL=qwen-plus
LLM_PROVIDER=openai

# TTS 配置
TTS_ENABLED=true
TTS_VOICE=zhixiaobai
```

**重要**：
- `OPENAI_API_KEY` 这里填写你的**阿里云 DashScope API Key**
- 不是 ModelScope 的 Token
- TTS 会自动使用这个 Key

### 第三步：测试

```bash
python test_tts.py
```

---

## 🎨 支持的音色

### 新模型音色 (cosyvoice-v1) ⭐ 推荐

| 音色代码 | 描述 | 性别 | 特点 |
|---------|------|------|------|
| `longxiaochun` | 龙小春 | 女 | 温柔、清晰 ⭐ |
| `longxiaoqing` | 龙小青 | 女 | 亲切、自然 |
| `longjing` | 龙晶晶 | 女 | 甜美、活泼 |
| `longxiaohao` | 龙小浩 | 男 | 沉稳、大气 ⭐ |
| `longxiaojian` | 龙小健 | 男 | 清朗、有力 |
| `longxiaobei` | 龙小贝 | 儿童 | 可爱、童声 |

### 旧模型音色 (sambert-zhichu-v1)

| 音色代码 | 描述 | 性别 | 推荐 |
|---------|------|------|------|
| `zhixiaobai` | 智小白（活泼） | 女 | ⭐ |
| `zhixiaoxia` | 智小夏（温柔） | 女 | ⭐ |
| `zhiyan` | 智妍（甜美） | 女 | |
| `zhitian` | 智天（亲切） | 男 | ⭐ |
| `zhigang` | 智刚（沉稳） | 男 | |
| `zhibei` | 智贝（可爱） | 儿童 | |

### 修改音色

在 `.env` 文件中添加或修改：

```ini
# 使用新模型音色（推荐）
TTS_VOICE=longxiaochun  # 女声
# 或
TTS_VOICE=longxiaohao   # 男声

# 使用旧模型音色（如果使用 sambert-zhichu-v1）
TTS_VOICE=zhitian  # 改为男声
```

### 选择模型

项目默认已配置使用 **`cosyvoice-v1`**（新模型）。

如果需要切换回旧模型，修改 `config/default.json`：

```json
"tts": {
  "model": "sambert-zhichu-v1",  // 旧模型
  "voice": "zhixiaobai"           // 使用旧模型音色
}
```

---

## 📋 完整的 .env 配置示例

```ini
# ============================================================
# 阿里云 DashScope 配置
# ============================================================

# API Key（从 https://dashscope.console.aliyun.com/apiKey 获取）
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# API 端点（使用阿里云兼容 OpenAI 的接口）
OPENAI_API_BASE=https://dashscope.aliyuncs.com/compatible-mode/v1

# 对话模型
OPENAI_MODEL=qwen-plus
LLM_PROVIDER=openai

# LLM 参数
LLM_TEMPERATURE=0.8
LLM_MAX_TOKENS=500

# ============================================================
# TTS 语音合成配置
# ============================================================

TTS_ENABLED=true

# 使用新模型音色（推荐 - cosyvoice-v1）
TTS_VOICE=longxiaochun

# 或使用旧模型音色（sambert-zhichu-v1）
# TTS_VOICE=zhixiaobai

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

运行测试脚本：

```bash
python test_tts.py
```

如果看到：
```
✅ API 密钥已配置
✅ 语音生成成功
```

说明配置成功！

---

## 🚀 启动游戏

### 启动后端
```bash
python main.py --mode web
```

### 启动前端（新终端）
```bash
cd frontend
npm run dev
```

### 访问游戏
http://localhost:5173

---

## ❓ 常见问题

### Q: 在哪里获取阿里云 API Key？
**A**: https://dashscope.console.aliyun.com/apiKey

### Q: API Key 是免费的吗？
**A**: 阿里云提供免费额度，个人使用足够。

### Q: 对话模型也要改成阿里云的吗？
**A**: 建议统一使用阿里云，更稳定。模型可以选择 `qwen-plus` 或 `qwen-max`。

### Q: 原来的 ModelScope Token 还能用吗？
**A**: 不能。需要使用阿里云 DashScope 的 API Key。

---

## 🔗 有用的链接

- **获取 API Key**: https://dashscope.console.aliyun.com/apiKey
- **DashScope 文档**: https://help.aliyun.com/zh/dashscope/
- **TTS 文档**: https://help.aliyun.com/zh/dashscope/developer-reference/api-text-to-speech

---

**更新日期**: 2025-11-06  
**推荐方案**: 阿里云 DashScope ⭐  
**推荐模型**: `cosyvoice-v1` (Qwen3-TTS-Flash-Realtime) 🚀  
**默认音色**: `longxiaochun` (龙小春 - 温柔女声)

