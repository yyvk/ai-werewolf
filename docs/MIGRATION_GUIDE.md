# 迁移指南 - v2.0 配置系统重构

## 概述

本次重构采用了 **LangChain 规范**，并完全重写了配置系统。如果你之前使用的是旧版本，请按照本指南迁移。

---

## 主要变化

### 1. 配置系统重构 ✨

**旧版本**：
```python
# 配置分散在多个地方，难以管理
config.modelscope_token = "xxx"
config.tts_voice = "xxx"
```

**新版本**：
```python
# 统一配置管理，支持多提供商
from src.utils.config import get_config

config = get_config()
llm_config = config.get_llm_config()  # 获取LLM配置
tts_config = config.get_tts_config()  # 获取TTS配置
```

### 2. 环境变量优先级 🔥

**旧版本**：配置文件优先

**新版本**：环境变量 > 配置文件 > 默认值

```bash
# .env 文件中的配置会覆盖 default.json
LLM_PROVIDER=openai
LLM_TEMPERATURE=0.9
```

### 3. LLM工厂模式 🏭

**旧版本**：
```python
llm = ChatOpenAI(
    api_key=config.openai_api_key,
    model=config.openai_model,
    temperature=0.8
)
```

**新版本**：
```python
from src.agents.agent_factory import LLMFactory

# 自动从配置创建，支持多提供商
llm = LLMFactory.create_llm()  # 使用默认提供商
llm = LLMFactory.create_llm("openai")  # 指定提供商
```

### 4. Agent创建简化 🤖

**旧版本**：
```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(...)
agent = LangChainAgent(player, llm)
```

**新版本**：
```python
from src.agents.agent_factory import AgentFactory

# 自动创建LLM和Agent
agent = AgentFactory.create_agent(player)

# 指定提供商
agent = AgentFactory.create_agent(player, provider="openai")
```

### 5. 多提供商支持 🌐

**旧版本**：仅支持 OpenAI 和 ModelScope

**新版本**：支持多种提供商
- ✅ OpenAI (gpt-4, gpt-3.5-turbo)
- ✅ DashScope (qwen-plus, qwen-turbo)
- ✅ ModelScope (免费推理)
- ✅ Anthropic (Claude系列)

---

## 迁移步骤

### 第1步：更新依赖

```bash
pip install --upgrade -r requirements.txt
```

### 第2步：创建 .env 文件

```bash
# 复制示例文件
cp env.example.txt .env

# 编辑配置
vim .env
```

填入你的API Key：

```bash
# 方案A：ModelScope + DashScope（推荐免费）
LLM_PROVIDER=modelscope
OPENAI_API_KEY=ms-your-modelscope-token
OPENAI_API_BASE=https://api-inference.modelscope.cn/v1/
OPENAI_MODEL=Qwen/Qwen2.5-32B-Instruct

DASHSCOPE_API_KEY=sk-your-dashscope-key
TTS_ENABLED=true
TTS_VOICE=Cherry

# 方案B：全部使用DashScope
# LLM_PROVIDER=dashscope
# OPENAI_API_KEY=sk-your-dashscope-key
# OPENAI_API_BASE=https://dashscope.aliyuncs.com/compatible-mode/v1
# OPENAI_MODEL=qwen-plus
# DASHSCOPE_API_KEY=sk-your-dashscope-key
```

### 第3步：更新配置文件（可选）

如果你有自定义的配置文件，请参考新的 `config/default.json` 结构更新：

```json
{
  "llm": {
    "provider": "modelscope",
    "temperature": 0.8,
    "providers": {
      "openai": {...},
      "dashscope": {...},
      "modelscope": {...}
    }
  },
  "tts": {
    "provider": "dashscope",
    "providers": {
      "dashscope": {...}
    }
  }
}
```

### 第4步：更新代码

#### 旧代码：
```python
from src.utils.config import get_config
from langchain_openai import ChatOpenAI
from src.agents import LangChainAgent

config = get_config()

# 手动创建LLM
llm = ChatOpenAI(
    api_key=config.openai_api_key,
    model=config.openai_model,
    temperature=config.llm_temperature
)

# 创建Agent
agent = LangChainAgent(player, llm)
```

#### 新代码：
```python
from src.agents.agent_factory import AgentFactory

# 一行代码搞定！自动从配置创建LLM和Agent
agent = AgentFactory.create_agent(player)
```

### 第5步：测试配置

```bash
python test_config.py
```

看到 `✅ 所有测试通过` 表示迁移成功！

---

## 配置文件映射

### 环境变量映射

| 旧变量 | 新变量 | 说明 |
|--------|--------|------|
| `OPENAI_API_KEY` | `OPENAI_API_KEY` | 保持不变 |
| `OPENAI_MODEL` | `OPENAI_MODEL` | 保持不变 |
| `MODELSCOPE_API_KEY` | `MODELSCOPE_API_KEY` 或 `OPENAI_API_KEY` | 兼容 |
| `MODELSCOPE_MODEL` | `MODELSCOPE_MODEL` 或 `OPENAI_MODEL` | 兼容 |
| `DASHSCOPE_API_KEY` | `DASHSCOPE_API_KEY` | 保持不变 |
| `TTS_VOICE` | `TTS_VOICE` | 保持不变 |
| `TTS_MODEL` | `TTS_MODEL` | 保持不变 |
| `LLM_TEMPERATURE` | `LLM_TEMPERATURE` | 保持不变 |
| `LLM_MAX_TOKENS` | `LLM_MAX_TOKENS` | 保持不变 |
| - | `LLM_PROVIDER` | **新增** 选择LLM提供商 |
| - | `TTS_PROVIDER` | **新增** 选择TTS提供商 |

### 配置文件结构变化

**旧结构** (`default.json`)：
```json
{
  "llm": {
    "provider": "openai",
    "model": "gpt-4o-mini",
    "temperature": 0.7
  }
}
```

**新结构** (`default.json`)：
```json
{
  "llm": {
    "provider": "modelscope",
    "temperature": 0.8,
    "providers": {
      "openai": {
        "api_key": "",
        "model": "gpt-4o-mini",
        "base_url": "https://api.openai.com/v1"
      },
      "modelscope": {
        "api_key": "",
        "model": "Qwen/Qwen2.5-32B-Instruct",
        "base_url": "https://api-inference.modelscope.cn/v1/"
      }
    }
  }
}
```

---

## API变化

### 配置API

#### 获取配置
```python
# 旧API
config = Config()
token = config.modelscope_token

# 新API
config = get_config()
llm_config = config.get_llm_config()
token = llm_config['api_key']
```

#### 配置验证
```python
# 新增
config.validate()  # 返回 True/False
```

### LLM创建API

```python
# 旧API
from langchain_openai import ChatOpenAI
llm = ChatOpenAI(api_key=xxx, model=xxx)

# 新API
from src.agents.agent_factory import LLMFactory
llm = LLMFactory.create_llm()  # 自动从配置创建
llm = LLMFactory.create_llm("openai")  # 指定提供商
```

### Agent创建API

```python
# 旧API
agent = LangChainAgent(player, llm)

# 新API
from src.agents.agent_factory import AgentFactory
agent = AgentFactory.create_agent(player)
agent = AgentFactory.create_agent(player, provider="openai")
```

---

## 兼容性说明

### 向后兼容

为了保持兼容性，旧的环境变量**仍然有效**：

```bash
# 这些仍然可用
OPENAI_API_KEY=xxx
OPENAI_MODEL=xxx
MODELSCOPE_API_KEY=xxx
```

但推荐使用新的配置方式：

```bash
# 推荐
LLM_PROVIDER=modelscope
OPENAI_API_KEY=ms-xxx  # 用于 ModelScope
DASHSCOPE_API_KEY=sk-xxx  # 用于 TTS
```

### 不兼容的变化

以下功能不再支持或已改变：

1. ❌ **直接访问配置属性**
   ```python
   # 旧方式（不推荐）
   config.modelscope_token
   
   # 新方式
   config.get_llm_config("modelscope")["api_key"]
   ```

2. ❌ **手动创建LLM**
   ```python
   # 不推荐（虽然仍可用）
   llm = ChatOpenAI(api_key=xxx, model=xxx)
   
   # 推荐
   llm = LLMFactory.create_llm()
   ```

---

## 常见问题

### Q: 旧的 .env 文件还能用吗？

**A**: 可以！但建议按照新格式更新，添加 `LLM_PROVIDER` 等新变量。

### Q: 必须使用 .env 文件吗？

**A**: 不是必须的，但**强烈推荐**。你也可以直接修改 `config/default.json`。

### Q: 如何从旧的配置文件迁移？

**A**: 
1. 备份旧配置
2. 复制 `env.example.txt` 为 `.env`
3. 将旧配置的值填入新的 `.env`
4. 运行 `python test_config.py` 测试

### Q: 迁移后性能有变化吗？

**A**: 
- ✅ 配置加载速度：无明显差异
- ✅ LLM调用：性能相同（只是创建方式不同）
- ✅ 内存占用：略微优化（单例模式）

### Q: 需要修改现有代码吗？

**A**: 
- 如果使用 `AgentFactory.create_batch_agents()`：**无需修改**
- 如果直接创建 `LangChainAgent`：**建议更新**为新API
- 如果读取配置：**建议更新**为新API

---

## 迁移检查清单

完成以下步骤确保迁移成功：

- [ ] 更新依赖 `pip install --upgrade -r requirements.txt`
- [ ] 创建 `.env` 文件并填写配置
- [ ] 添加 `LLM_PROVIDER` 变量
- [ ] 测试配置 `python test_config.py`
- [ ] 更新代码使用新API（可选但推荐）
- [ ] 启动服务测试 `python main.py`
- [ ] 验证LLM和TTS工作正常

---

## 获取帮助

- 📖 详细配置说明：[CONFIG_GUIDE.md](./CONFIG_GUIDE.md)
- 📝 示例配置：`env.example.txt`
- 🧪 配置测试：`python test_config.py`
- 💬 遇到问题？提交 Issue 到 GitHub

---

**迁移愉快！** 🚀

如果遇到任何问题，请先运行 `python test_config.py` 进行诊断。

