# 🔊 AI狼人杀 语音合成（TTS）配置指南

## 功能介绍

本项目已集成 **ModelScope 语音合成服务**，可以在玩家发言时实时生成语音，让游戏体验更加生动！

## 🎯 快速开始

### 1. 启用 TTS 功能

TTS 功能默认已启用。如需配置，可在 `.env` 文件中添加以下配置：

```ini
# TTS 语音合成配置
TTS_ENABLED=true
TTS_MODEL=iic/speech_sambert-hifigan_tts_zh-cn_16k
TTS_VOICE=zhitian_emo
TTS_SPEED=1.0
TTS_PITCH=1.0
```

### 2. API 密钥配置

TTS 服务使用与对话模型相同的 ModelScope API 密钥。

**如果你使用 ModelScope 的 OpenAI 兼容接口**（推荐）：

```ini
# ModelScope 配置（已兼容 OpenAI 格式）
OPENAI_API_KEY=你的-ModelScope-Token
OPENAI_API_BASE=https://api-inference.modelscope.cn/v1/
OPENAI_MODEL=Qwen/Qwen2.5-32B-Instruct
LLM_PROVIDER=openai
```

**或者使用独立的 ModelScope Token**：

```ini
MODELSCOPE_ACCESS_TOKEN=你的-ModelScope-Token
```

> 💡 **提示**：TTS 会自动使用 `OPENAI_API_KEY` 或 `MODELSCOPE_ACCESS_TOKEN`（优先使用前者）。如果你已经配置了对话模型的密钥，无需额外配置。

### 3. 获取 ModelScope Access Token

1. 访问：https://modelscope.cn/my/myaccesstoken
2. 登录你的账号
3. 复制 Access Token
4. 将 Token 添加到 `.env` 文件中

---

## 🎨 语音模型和音色选择

### 推荐的 TTS 模型

根据 [ModelScope 官网](https://www.modelscope.cn/models) 的语音合成模型：

| 模型名称 | 描述 | 质量 | 速度 | 推荐场景 |
|---------|------|------|------|----------|
| **iic/speech_sambert-hifigan_tts_zh-cn_16k** | 中文语音合成（高质量） | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | **推荐使用** |
| iic/speech_sambert-hifigan_tts_zh-cn_24k | 中文语音合成（更高质量） | ⭐⭐⭐⭐⭐ | ⭐⭐ | 高质量输出 |
| iic/speech_paraformer-large_asr_zh-cn-16k | 语音识别（如需ASR功能） | - | - | 语音识别 |

### 可选的音色（voice）

不同的 TTS 模型支持不同的音色参数。以下是一些常用的音色：

#### ModelScope SambertHiFiGAN 支持的音色：

- `zhitian_emo` - 智天（默认，带情感）
- `aida` - 艾达
- `aiya` - 艾雅
- `aibao` - 艾宝
- `xiaoyun` - 小云
- `xiaoxue` - 小雪
- `xiaogang` - 小刚（男声）
- `jiajia` - 佳佳（女声）

### 配置示例

#### 方案 1：默认配置（推荐）

```ini
TTS_ENABLED=true
TTS_MODEL=iic/speech_sambert-hifigan_tts_zh-cn_16k
TTS_VOICE=zhitian_emo
TTS_SPEED=1.0
TTS_PITCH=1.0
```

**特点**：平衡质量与速度，自然流畅

#### 方案 2：高质量语音

```ini
TTS_ENABLED=true
TTS_MODEL=iic/speech_sambert-hifigan_tts_zh-cn_24k
TTS_VOICE=zhitian_emo
TTS_SPEED=0.9
TTS_PITCH=1.0
```

**特点**：最高音质，适合展示和录制

#### 方案 3：快速语音（男声）

```ini
TTS_ENABLED=true
TTS_MODEL=iic/speech_sambert-hifigan_tts_zh-cn_16k
TTS_VOICE=xiaogang
TTS_SPEED=1.2
TTS_PITCH=1.0
```

**特点**：男声角色，语速稍快

#### 方案 4：温柔女声

```ini
TTS_ENABLED=true
TTS_MODEL=iic/speech_sambert-hifigan_tts_zh-cn_16k
TTS_VOICE=jiajia
TTS_SPEED=0.9
TTS_PITCH=1.1
```

**特点**：女声角色，语速稍慢，音调略高

---

## 🎮 使用方法

### 启动游戏

1. **启动后端服务**：

```bash
cd E:\workspace\study\ai-werewolf
python main.py --mode web
```

2. **启动前端服务**：

```bash
cd frontend
npm run dev
```

3. **访问游戏**：

打开浏览器访问：http://localhost:5173

### 游戏中的语音效果

- ✅ 玩家发言时会自动生成语音
- ✅ 语音会在文本显示完成后自动播放
- ✅ 支持流式文本显示 + 语音生成
- ✅ 每个玩家的语音会依次播放，不会重叠

### 控制台查看日志

启动游戏后，控制台会显示 TTS 相关日志：

```
🔊 TTS服务初始化: 模型=iic/speech_sambert-hifigan_tts_zh-cn_16k, 音色=zhitian_emo
✅ 语音生成成功: speech_1_12345.wav
🔊 音频加载完成，开始播放: assets/audio/speech_1_12345.wav
```

---

## 🔧 高级配置

### 参数说明

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `TTS_ENABLED` | boolean | true | 是否启用 TTS |
| `TTS_MODEL` | string | iic/speech_sambert-hifigan_tts_zh-cn_16k | TTS 模型名称 |
| `TTS_VOICE` | string | zhitian_emo | 音色名称 |
| `TTS_SPEED` | float | 1.0 | 语速（0.5 - 2.0） |
| `TTS_PITCH` | float | 1.0 | 音调（0.5 - 2.0） |

### 语速调整

- `0.5` - 慢速（适合理解困难的内容）
- `0.8` - 稍慢
- `1.0` - 正常速度 ⭐
- `1.2` - 稍快
- `1.5` - 快速

### 音调调整

- `0.8` - 低沉
- `1.0` - 正常 ⭐
- `1.2` - 清脆
- `1.5` - 尖锐

---

## 🚨 故障排查

### 问题 1：语音无法生成

**可能原因**：
1. ModelScope API Token 未配置或无效
2. TTS 模型名称错误
3. 网络连接问题

**解决方法**：
1. 检查 `.env` 文件中的 `MODELSCOPE_ACCESS_TOKEN`
2. 确保 Token 有效（访问 https://modelscope.cn/my/myaccesstoken 验证）
3. 查看后端控制台的错误日志

### 问题 2：语音无法播放

**可能原因**：
1. 浏览器阻止自动播放
2. 音频文件路径错误
3. 音频文件生成失败

**解决方法**：
1. 在浏览器中允许自动播放媒体
2. 打开浏览器开发者工具（F12），查看 Console 错误信息
3. 检查 `assets/audio/` 目录下是否有音频文件生成

### 问题 3：语音质量差

**解决方法**：
1. 尝试使用更高质量的模型（24k 版本）
2. 调整语速和音调参数
3. 更换不同的音色

### 问题 4：语音生成太慢

**解决方法**：
1. 使用 16k 版本的模型（更快）
2. 检查网络连接
3. 考虑关闭 TTS 功能（设置 `TTS_ENABLED=false`）

---

## 📁 文件说明

### 后端文件

- `src/utils/tts_service.py` - TTS 服务实现
- `src/utils/config.py` - TTS 配置管理
- `src/web/api.py` - API 接口，集成 TTS
- `assets/audio/` - 生成的音频文件存储目录

### 前端文件

- `frontend/src/views/GameRoom.vue` - 游戏房间组件，包含音频播放逻辑

### 配置文件

- `.env` - 环境变量配置
- `config/default.json` - 默认配置

---

## 🎯 最佳实践

### 1. 推荐配置组合

**日常游戏**：
```ini
TTS_ENABLED=true
TTS_MODEL=iic/speech_sambert-hifigan_tts_zh-cn_16k
TTS_VOICE=zhitian_emo
TTS_SPEED=1.0
TTS_PITCH=1.0
```

**展示演示**：
```ini
TTS_ENABLED=true
TTS_MODEL=iic/speech_sambert-hifigan_tts_zh-cn_24k
TTS_VOICE=aiya
TTS_SPEED=0.9
TTS_PITCH=1.1
```

**快速开发测试**：
```ini
TTS_ENABLED=false
```

### 2. 性能优化建议

- ✅ 使用 16k 模型可获得更快的响应速度
- ✅ 生成的音频文件会缓存在 `assets/audio/` 目录
- ✅ 定期清理旧的音频文件以节省空间

### 3. 多音色组合

可以考虑为不同角色分配不同的音色（需要修改代码）：
- 狼人 → `xiaogang` (男声，低沉)
- 村民 → `aiya` (女声，温和)
- 预言家 → `zhitian_emo` (智慧，带情感)
- 女巫 → `jiajia` (神秘)

---

## 📚 参考资源

- ModelScope 模型列表：https://www.modelscope.cn/models
- ModelScope API 文档：https://www.modelscope.cn/docs/model-service/API-Inference/intro
- 获取 Access Token：https://modelscope.cn/my/myaccesstoken

---

## 🎉 体验效果

配置完成后，你会看到：

1. 🎮 游戏开始后，每个玩家发言时会显示打字机效果
2. 💬 文本显示完成后，自动播放该玩家的语音
3. 🔊 语音播放时，玩家卡片会有特殊的发光效果
4. 📜 所有发言都会记录在游戏日志中

**配置时间**: 2025-11-06  
**推荐模型**: iic/speech_sambert-hifigan_tts_zh-cn_16k ⭐  
**推荐音色**: zhitian_emo ⭐

