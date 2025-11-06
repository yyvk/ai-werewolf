# 🤖 ModelScope模型配置指南

## 📊 模型对比（2025最新）

### AI狼人杀推荐模型

| 模型 | 参数量 | 推理能力 | 响应速度 | 推荐场景 | 评分 |
|------|--------|----------|----------|----------|------|
| **Qwen3-Max** | 超大 | ⭐⭐⭐⭐⭐ | ⭐⭐ | 正式运行 | 🏆 |
| **Qwen2.5-32B-Instruct** | 32B | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 平衡首选 | ⭐推荐 |
| **Qwen2.5-14B-Instruct** | 14B | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 快速测试 | ✅ |
| **Qwen2.5-7B-Instruct** | 7B | ⭐⭐ | ⭐⭐⭐⭐⭐ | 开发调试 | 💡 |

---

## 🎯 推荐配置

### 方案1：旗舰性能（最佳游戏体验）

```ini
# .env 文件配置
OPENAI_API_KEY=你的-ModelScope-Access-Token
OPENAI_API_BASE=https://api-inference.modelscope.cn/v1/
OPENAI_MODEL=Qwen/Qwen3-Max
LLM_PROVIDER=openai
GAME_LANGUAGE=zh
DEBUG_MODE=false
```

**优势**：
- ✅ 最强推理能力，AI表现最智能
- ✅ 复杂策略和欺骗能力强
- ✅ 对话质量最高

**劣势**：
- ⚠️ 响应较慢（可能5-10秒/回合）
- ⚠️ 可能有调用限制

---

### 方案2：平衡推荐（⭐推荐）

```ini
# .env 文件配置
OPENAI_API_KEY=你的-ModelScope-Access-Token
OPENAI_API_BASE=https://api-inference.modelscope.cn/v1/
OPENAI_MODEL=Qwen/Qwen2.5-32B-Instruct
LLM_PROVIDER=openai
GAME_LANGUAGE=zh
DEBUG_MODE=false
```

**优势**：
- ✅ 推理能力强，适合狼人杀
- ✅ 响应速度适中（2-5秒/回合）
- ✅ 性价比最高

**最佳选择**：适合大多数用户

---

### 方案3：快速开发（快速测试）

```ini
# .env 文件配置
OPENAI_API_KEY=你的-ModelScope-Access-Token
OPENAI_API_BASE=https://api-inference.modelscope.cn/v1/
OPENAI_MODEL=Qwen/Qwen2.5-14B-Instruct
LLM_PROVIDER=openai
GAME_LANGUAGE=zh
DEBUG_MODE=true
```

**优势**：
- ✅ 响应速度快（1-3秒/回合）
- ✅ 适合快速迭代开发
- ✅ 基本推理能力够用

---

## 🚀 配置步骤

### 1. 获取ModelScope Access Token

访问：https://modelscope.cn/my/myaccesstoken

登录并复制你的Token

### 2. 编辑 .env 文件

```bash
notepad .env
```

或在Cursor中直接编辑

### 3. 粘贴配置

选择上面任一方案，复制配置到 `.env` 文件

**记得替换 `你的-ModelScope-Access-Token`**

### 4. 测试连接

```bash
python test_modelscope.py
```

### 5. 运行游戏

```bash
python main.py --mode console --rounds 2
```

---

## 🎮 不同模型的AI表现差异

### Qwen3-Max / Qwen2.5-32B
```
AI发言示例：
"根据1号和3号的发言矛盾，以及2号玩家一直在避重就轻，
我推测2号可能是狼人。1号的逻辑链条清晰，倾向于好人。
综合考虑，我这轮投2号。"
```
✅ 逻辑严密，推理深入

### Qwen2.5-14B
```
AI发言示例：
"我觉得2号说话有点可疑，1号的理由比较合理。
这一轮我投2号。"
```
✅ 基本推理，简洁明了

### Qwen2.5-7B
```
AI发言示例：
"2号可疑，投2号。"
```
⚠️ 推理简单，缺乏深度

---

## 💡 选择建议

### 你应该选择哪个？

1. **首次运行测试** → `Qwen2.5-14B-Instruct`
   - 快速验证项目是否正常工作
   
2. **正式玩游戏** → `Qwen2.5-32B-Instruct` ⭐
   - 最佳平衡，游戏体验好
   
3. **追求最强AI** → `Qwen3-Max`
   - 最智能的AI狼人杀体验
   
4. **开发调试代码** → `Qwen2.5-7B-Instruct`
   - 最快响应，节省开发时间

---

## 🔄 随时切换模型

只需修改 `.env` 文件中的 `OPENAI_MODEL` 行：

```ini
# 从这个
OPENAI_MODEL=Qwen/Qwen2.5-7B-Instruct

# 改成这个
OPENAI_MODEL=Qwen/Qwen2.5-32B-Instruct
```

保存后重新运行即可。

---

## 📚 更多资源

- ModelScope模型列表：https://www.modelscope.cn/models
- API文档：https://www.modelscope.cn/docs/model-service/API-Inference/intro
- 获取Token：https://modelscope.cn/my/myaccesstoken

---

**配置时间**: 2025-11-04  
**推荐模型**: Qwen/Qwen2.5-32B-Instruct ⭐





