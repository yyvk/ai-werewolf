# 🔊 TTS 语音功能 - 解决 404 错误

## 🎯 问题诊断

你遇到的 `404 page not found` 错误说明 ModelScope 推理 API 的端点格式不正确。

## ✅ 推荐解决方案：使用 DashScope

**DashScope 是阿里云官方的语音服务**，比通用的 ModelScope 推理 API 更稳定可靠。

### 为什么选择 DashScope？

- ✅ **官方 SDK**：阿里云官方支持
- ✅ **稳定可靠**：专用语音服务，不是通用推理 API
- ✅ **使用简单**：SDK 封装完善
- ✅ **响应快速**：国内服务器
- ✅ **免费额度**：足够个人使用

---

## 🚀 快速切换到 DashScope（3 步）

### 步骤 1: 安装 DashScope SDK

```bash
pip install dashscope
```

### 步骤 2: 运行检测脚本

```bash
python check_tts_options.py
```

这会告诉你当前配置状态。

### 步骤 3: 测试 DashScope TTS

```bash
python test_dashscope_tts.py
```

如果看到 ✅ 标记，说明成功！

---

## 📝 配置说明

### 你的 .env 文件

你current的配置已经可以用了：

```ini
OPENAI_API_KEY=你的密钥
OPENAI_API_BASE=https://api-inference.modelscope.cn/v1/
OPENAI_MODEL=Qwen/Qwen2.5-32B-Instruct
LLM_PROVIDER=openai
TTS_ENABLED=true
```

DashScope TTS 会自动使用 `OPENAI_API_KEY`。

### 可选：自定义音色

```ini
# DashScope 支持的音色
TTS_VOICE=zhixiaobai   # 女声（默认）⭐
TTS_VOICE=zhitian      # 男声
TTS_VOICE=zhiyan       # 温柔女声
```

---

## 🔧 集成到项目

修改 `src/web/api.py`，使用 DashScope TTS：

```python
# 在文件顶部导入
from src.utils.tts_service_dashscope import get_dashscope_tts_service

# 在 speech_end 事件中
try:
    tts_service = get_dashscope_tts_service()
    audio_path = await tts_service.text_to_speech(full_speech, agent.player.id)
    ...
except Exception as e:
    print(f"⚠️ TTS生成失败: {e}")
```

---

## 📊 两种方案对比

| 特性 | DashScope ⭐ | ModelScope 推理 API |
|------|--------------|---------------------|
| 稳定性 | ✅ 高 | ⚠️ 中 |
| 安装 | pip install dashscope | pip install httpx |
| API 端点 | 官方封装，无需关心 | 需要手动配置 |
| 音色选项 | 6+ 种 | 取决于模型 |
| 响应速度 | 快 | 中等 |
| 文档 | 完善 | 有限 |
| 推荐 | ✅ 强烈推荐 | 备选 |

---

## 🎮 完整使用流程

### 1. 检查环境

```bash
python check_tts_options.py
```

### 2. 测试 TTS

```bash
python test_dashscope_tts.py
```

### 3. 集成到项目

修改 `src/web/api.py`（我会帮你完成）

### 4. 启动游戏

```bash
# 终端 1
python main.py --mode web

# 终端 2
cd frontend
npm run dev
```

### 5. 开始游戏

访问 http://localhost:5173，享受语音版 AI 狼人杀！

---

## ❓ 常见问题

### Q: 我需要修改很多代码吗？
**A**: 不需要！只需修改 API 文件中的一行导入即可。

### Q: DashScope 要额外付费吗？
**A**: 不需要！免费额度足够个人使用。

### Q: 音色可以自定义吗？
**A**: 可以！在 .env 中设置 TTS_VOICE。

### Q: 会影响现有的对话模型吗？
**A**: 不会！TTS 和对话模型独立运行。

---

## 🎉 下一步

请运行：

```bash
python check_tts_options.py
```

然后告诉我结果，我会帮你完成集成！

---

**更新日期**: 2025-11-06  
**推荐方案**: DashScope TTS ⭐

