# 🚀 TTS 语音功能 - 快速开始

## 📋 前置条件

1. Python 3.8+
2. Node.js 16+
3. ModelScope API Token

---

## ⚡ 5分钟快速启动

### 步骤 1: 安装依赖

```bash
# 安装 Python 依赖
pip install httpx

# 或安装所有依赖
pip install -r requirements.txt
```

### 步骤 2: 配置 API Token

1. 访问 https://modelscope.cn/my/myaccesstoken
2. 登录并复制你的 Access Token
3. 在项目根目录的 `.env` 文件中配置：

```ini
# 使用 ModelScope 的 OpenAI 兼容接口（推荐）
OPENAI_API_KEY=your-token-here
OPENAI_API_BASE=https://api-inference.modelscope.cn/v1/
LLM_PROVIDER=openai
TTS_ENABLED=true
```

> 💡 如果你已经配置了 `OPENAI_API_KEY`，TTS 会自动使用，无需额外配置！

### 步骤 3: 测试 TTS 功能

```bash
python test_tts.py
```

如果看到 ✅ 标记，说明配置成功！

### 步骤 4: 启动游戏

**终端 1 - 启动后端**：
```bash
python main.py --mode web
```

**终端 2 - 启动前端**：
```bash
cd frontend
npm run dev
```

### 步骤 5: 开始游戏

1. 访问 http://localhost:5173
2. 创建新游戏
3. 点击"开始游戏"
4. 点击"下一轮"
5. 🎉 玩家发言时会自动播放语音！

---

## 🎨 自定义音色

在 `.env` 文件中修改：

```ini
# 女声（温柔）
TTS_VOICE=aiya

# 男声（低沉）
TTS_VOICE=xiaogang

# 默认（带情感）
TTS_VOICE=zhitian_emo
```

---

## 🔧 调整语速

```ini
# 慢速
TTS_SPEED=0.8

# 正常
TTS_SPEED=1.0

# 快速
TTS_SPEED=1.2
```

---

## ❌ 禁用语音

如果不需要语音，可以在 `.env` 中设置：

```ini
TTS_ENABLED=false
```

---

## 🐛 遇到问题？

### 问题 1: 无法生成语音

**检查**：
- API Token 是否正确配置
- 网络连接是否正常
- 查看终端错误日志

**解决**：
```bash
# 测试 API Token
python test_tts.py
```

### 问题 2: 语音无法播放

**检查**：
- 浏览器是否允许自动播放
- 打开浏览器控制台（F12）查看错误
- 检查 `assets/audio/` 目录是否有文件

### 问题 3: 生成速度慢

**解决**：
- 使用 16k 模型（默认）而不是 24k
- 检查网络连接

---

## 📚 更多帮助

- 完整配置指南：[TTS_GUIDE.md](./TTS_GUIDE.md)
- ModelScope 模型列表：https://www.modelscope.cn/models
- 项目文档：[README.md](./README.md)

---

**享受你的 AI 狼人杀语音版游戏！** 🎮🔊

