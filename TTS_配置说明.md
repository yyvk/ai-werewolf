# 🔧 TTS 配置说明 - 兼容你的现有配置

## ✅ 好消息！

TTS 功能现在**完全兼容**你现有的配置方式！

如果你的 `.env` 文件中已经配置了：

```ini
OPENAI_API_KEY=你的-ModelScope-Token
OPENAI_API_BASE=https://api-inference.modelscope.cn/v1/
OPENAI_MODEL=Qwen/Qwen2.5-32B-Instruct
LLM_PROVIDER=openai
```

那么 **TTS 会自动使用这个配置，无需任何额外设置！**

---

## 🎯 你需要做的只有 3 件事

### 1. 确保启用 TTS（可选，默认已启用）

在 `.env` 中添加（或确认已存在）：

```ini
TTS_ENABLED=true
```

### 2. 安装依赖

```bash
pip install httpx
```

### 3. 启动游戏

```bash
# 后端
python main.py --mode web

# 前端（新终端）
cd frontend
npm run dev
```

**就这么简单！** 🎉

---

## 🔍 技术说明

### 配置优先级

TTS 服务会按以下顺序查找 API 密钥：

1. **OPENAI_API_KEY** ⭐ （优先，兼容 ModelScope）
2. MODELSCOPE_ACCESS_TOKEN（备选）

所以你现有的配置会被自动识别和使用。

### 为什么这样设计？

ModelScope 提供了 **OpenAI 兼容接口**，这意味着：
- ✅ 使用 `OPENAI_API_KEY` 和 `OPENAI_API_BASE` 就能访问 ModelScope
- ✅ 对话模型和 TTS 模型可以共用同一个密钥
- ✅ 无需维护多个配置变量

---

## 📝 完整的 .env 配置示例

```ini
# ============================================================
# LLM 配置（你现有的配置方式）
# ============================================================
OPENAI_API_KEY=你的-ModelScope-Token
OPENAI_API_BASE=https://api-inference.modelscope.cn/v1/
OPENAI_MODEL=Qwen/Qwen2.5-32B-Instruct
LLM_PROVIDER=openai

# ============================================================
# TTS 配置（可选）
# ============================================================
TTS_ENABLED=true                                              # 启用 TTS
TTS_MODEL=iic/speech_sambert-hifigan_tts_zh-cn_16k          # TTS 模型
TTS_VOICE=zhitian_emo                                        # 音色
TTS_SPEED=1.0                                                # 语速
TTS_PITCH=1.0                                                # 音调
```

---

## 🎨 自定义音色（可选）

如果想换个音色，只需修改 `TTS_VOICE`：

```ini
# 女声选项
TTS_VOICE=zhitian_emo   # 智天（默认，带情感）⭐
TTS_VOICE=aiya          # 艾雅（温柔）
TTS_VOICE=xiaoyun       # 小云（活泼）

# 男声选项
TTS_VOICE=xiaogang      # 小刚（低沉）
```

---

## 🧪 测试一下

运行测试脚本验证配置：

```bash
python test_tts.py
```

如果看到：

```
✅ API 密钥已配置 (来源: OPENAI_API_KEY): sk-xxx...
✅ 语音生成成功!
```

说明一切正常！

---

## ❓ 常见问题

### Q: 我需要修改现有配置吗？
**A**: 不需要！你的配置已经完美兼容。

### Q: OPENAI_API_KEY 和 MODELSCOPE_ACCESS_TOKEN 有什么区别？
**A**: 没有实质区别。ModelScope 支持 OpenAI 兼容接口，所以 `OPENAI_API_KEY` 既可以用于对话，也可以用于 TTS。

### Q: 如果我两个都配置了会怎样？
**A**: TTS 会优先使用 `OPENAI_API_KEY`。

### Q: 我可以为 TTS 单独配置密钥吗？
**A**: 可以！如果你想用不同的密钥，可以单独配置 `MODELSCOPE_ACCESS_TOKEN`。

---

## 🎉 开始使用

现在你可以直接启动游戏，享受带语音的 AI 狼人杀了！

```bash
# 终端 1
python main.py --mode web

# 终端 2
cd frontend
npm run dev
```

访问 http://localhost:5173，创建游戏，然后听 AI 玩家发言吧！🎮🔊

---

**配置更新日期**: 2025-11-06  
**兼容状态**: ✅ 完全兼容现有配置

