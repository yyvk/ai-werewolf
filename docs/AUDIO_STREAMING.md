# 音频流式播放配置指南

本文档说明 AI 狼人杀游戏中音频流式播放的实现和配置。

## 架构概述

### 后端流式生成

后端使用 DashScope TTS API 进行真正的流式音频生成：

- **模型**: `qwen3-tts-flash` (默认，支持流式)
- **备用模型**: `sambert-zhichu-v1` (旧模型，不支持流式)
- **音频格式**: API 自动决定（通常为 MP3 或 WAV）
- **传输方式**: Server-Sent Events (SSE)，逐块发送 base64 编码的音频数据

### 前端流式播放

前端使用 **Web Audio API** 实现高质量音频播放：

- ✅ **自动格式检测**: 支持 MP3, WAV, OGG 等格式
- ✅ **智能解码**: 使用 Web Audio API 解码音频数据
- ✅ **兼容回退**: 如果 Web Audio API 失败，自动回退到标准 Audio 元素
- ✅ **详细日志**: 输出音频格式、时长、采样率等信息

## 音频格式说明

### 支持的格式

| 格式 | 优势 | 劣势 | 推荐场景 |
|------|------|------|----------|
| **MP3** | 文件小，广泛支持，流式友好 | 有损压缩 | ✅ 推荐（默认） |
| **WAV** | 无损，高质量 | 文件大，不适合流式 | 高质量要求 |
| **OGG** | 开源，高质量 | 浏览器支持有限 | 特定需求 |

### 格式检测

前端通过检测音频文件的魔术字节自动识别格式：

```javascript
// WAV: 以 "RIFF" 开头 (52 49 46 46)
// MP3: 以 "ID3" 或 sync word 开头 (49 44 33 / FF Ex)
// OGG: 以 "OggS" 开头 (4F 67 67 53)
```

## 配置参数

### 后端配置 (`config/default.json`)

```json
{
  "tts": {
    "enabled": true,
    "provider": "dashscope",
    "providers": {
      "dashscope": {
        "model": "qwen3-tts-flash",
        "voice": "Cherry",
        "speed": 1.0,
        "pitch": 1.0,
        "volume": 50,
        "sample_rate": 16000,
        "format": "wav"
      }
    }
  }
}
```

**参数说明**:

- `model`: TTS 模型
  - `qwen3-tts-flash`: 新模型，支持流式（推荐）
  - `sambert-zhichu-v1`: 旧模型，不支持流式
  
- `voice`: 音色选择（女声）
  - `Cherry`: 甜美清晰 ⭐ 推荐
  - `Bella`: 温柔优雅
  - `Amy`: 亲切自然
  - `Emma`: 活泼可爱
  - `Cora`: 成熟稳重
  
- `speed`: 语速 (0.5-2.0)，默认 1.0
- `pitch`: 音高 (0.5-2.0)，默认 1.0
- `sample_rate`: 采样率（16000 或 24000 Hz）
- `format`: 音频格式（仅用于旧模型）

### 环境变量配置 (`.env`)

```bash
# TTS 配置
TTS_ENABLED=true
TTS_PROVIDER=dashscope
TTS_VOICE=Cherry
TTS_SPEED=1.0
TTS_PITCH=1.0
```

## 流式播放流程

### 完整流程图

```
1. 后端生成音频
   ├─ DashScope API 流式生成
   ├─ 逐块接收音频数据
   └─ 通过 SSE 逐块发送

2. 前端接收数据
   ├─ 监听 SSE 事件
   ├─ 接收 base64 编码的音频块
   └─ 添加到缓冲队列

3. 前端播放音频
   ├─ 合并所有音频块
   ├─ 检测音频格式
   ├─ 使用 Web Audio API 解码
   ├─ 创建音频源并播放
   └─ 如果失败，回退到 Audio 元素
```

### 后端实现

```python
# src/utils/tts_service_dashscope.py
async def text_to_speech_stream(self, text, player_id):
    response = dashscope.MultiModalConversation.call(
        model=self.model,
        text=text,
        stream=True
    )
    
    # 逐块返回音频数据
    for chunk in response:
        if chunk.output.audio.data is not None:
            yield chunk.output.audio.data  # base64 编码
```

### 前端实现

```javascript
// frontend/src/views/GameRoom.vue
async function playStreamingAudio(playerId, playerName) {
  // 1. 合并音频块
  const mergedAudio = mergeAudioChunks(audioBufferQueue.value)
  
  // 2. 检测格式
  const { mimeType, format } = detectAudioFormat(mergedAudio)
  
  // 3. 使用 Web Audio API 播放
  try {
    const audioContext = new AudioContext()
    const audioBuffer = await audioContext.decodeAudioData(mergedAudio.buffer)
    const source = audioContext.createBufferSource()
    source.buffer = audioBuffer
    source.connect(audioContext.destination)
    source.start(0)
  } catch (error) {
    // 回退到标准 Audio 元素
    fallbackToAudioElement(mergedAudio, mimeType)
  }
}
```

## 调试和监控

### 控制台日志

启用详细日志输出，帮助调试：

**后端日志示例**:
```
🎵 开始TTS生成: 玩家1, 文本长度=50, 音色=Cherry
🔍 音频格式检测 (玩家1): 前8字节=49 44 33 04 00 00 00 00
✅ 检测到 MP3 格式
📦 发送音频块 #1 (玩家1): 4096 bytes
📦 发送音频块 #2 (玩家1): 4096 bytes
✅ TTS生成完成 (qwen3-tts-flash): 玩家1, 共5块, 总大小=20480 bytes
```

**前端日志示例**:
```
🔊 准备播放: 玩家1 的流式语音, 音频块数: 5
🔍 音频数据大小: 20480 bytes
🔍 音频数据前8字节: 49 44 33 04 00 00 00 00
✅ 检测到 MP3 格式
🎵 使用 Web Audio API 解码 MP3 格式...
✅ 解码成功: 时长=2.50秒, 采样率=16000Hz, 声道=1
▶️ 正在播放: 玩家1
✅ 播放完成: 玩家1
```

### 常见错误和解决方案

#### 错误 1: `NotSupportedError: Failed to load`

**原因**: 音频格式不匹配或浏览器不支持

**解决方案**:
1. 检查后端返回的音频格式（查看控制台日志）
2. 确认浏览器支持该格式
3. Web Audio API 会自动处理并回退

#### 错误 2: `MEDIA_ERR_DECODE - 解码错误`

**原因**: 音频数据损坏或格式不完整

**解决方案**:
1. 检查网络连接是否稳定
2. 查看后端日志，确认音频生成完整
3. 尝试刷新页面重新播放

#### 错误 3: Web Audio API 解码失败

**原因**: 音频格式特殊或浏览器限制

**解决方案**:
- 代码会自动回退到标准 Audio 元素
- 查看控制台日志确认回退是否成功

## 性能优化建议

### 1. 音频格式选择

- ✅ **推荐 MP3**: 文件小，延迟低，兼容性好
- ⚠️ **谨慎 WAV**: 文件大，传输慢，但质量高
- ⚠️ **避免 OGG**: 浏览器支持有限

### 2. 采样率配置

- **16000 Hz**: 适合语音，文件更小 ✅ 推荐
- **24000 Hz**: 更高质量，但文件更大
- **48000 Hz**: 音乐级质量，不推荐语音使用

### 3. 网络优化

- 使用流式传输减少首次播放延迟
- base64 编码会增加约 33% 数据量
- 考虑使用二进制传输（未来优化）

## 浏览器兼容性

| 浏览器 | Web Audio API | MP3 | WAV | OGG |
|--------|---------------|-----|-----|-----|
| Chrome | ✅ | ✅ | ✅ | ✅ |
| Firefox | ✅ | ✅ | ✅ | ✅ |
| Safari | ✅ | ✅ | ✅ | ❌ |
| Edge | ✅ | ✅ | ✅ | ✅ |

## 未来优化方向

1. **真正的边收边播**: 使用 MediaSource Extensions (MSE)
2. **二进制传输**: 减少 base64 编码开销
3. **音频队列管理**: 支持多个音频排队播放
4. **音量控制**: 添加音量调节功能
5. **播放进度**: 显示播放进度条

## 相关文档

- [DashScope TTS 文档](https://help.aliyun.com/zh/dashscope/developer-reference/cosyvoice-speech-synthesis)
- [Web Audio API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Audio_API)
- [音频格式比较](https://en.wikipedia.org/wiki/Comparison_of_audio_coding_formats)

---

**最后更新**: 2025-11-06


