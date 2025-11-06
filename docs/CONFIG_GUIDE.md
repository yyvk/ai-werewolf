# 配置系统指南

## 目录
- [概述](#概述)
- [配置优先级](#配置优先级)
- [配置文件说明](#配置文件说明)
- [环境变量配置](#环境变量配置)
- [LLM提供商配置](#llm提供商配置)
- [TTS提供商配置](#tts提供商配置)
- [快速开始](#快速开始)
- [常见问题](#常见问题)

---

## 概述

AI狼人杀项目采用**多层配置系统**，支持灵活的配置管理：

```
环境变量 (.env) → 配置文件 (default.json) → 代码默认值
    ↑ 最高优先级                                  ↓ 最低优先级
```

### 主要特性

✅ **环境变量优先** - `.env` 文件中的配置会覆盖配置文件  
✅ **多提供商支持** - 支持 OpenAI, DashScope, ModelScope, Anthropic  
✅ **热重载** - 修改配置后无需重启（部分配置）  
✅ **类型安全** - 使用 Pydantic 进行配置验证  
✅ **LangChain规范** - 采用 LangChain 标准模式

---

## 配置优先级

配置加载顺序（后者覆盖前者）：

1. **代码默认值** - 硬编码的后备配置
2. **配置文件** (`config/default.json`) - 项目默认配置
3. **环境变量** (`.env`) - 用户自定义配置 ⭐ **优先级最高**

### 示例

如果你在 `default.json` 中设置：
```json
{
  "llm": {
    "provider": "modelscope",
    "temperature": 0.7
  }
}
```

但在 `.env` 中设置：
```bash
LLM_PROVIDER=openai
LLM_TEMPERATURE=0.9
```

**最终结果**：`provider=openai`, `temperature=0.9`（环境变量优先）

---

## 配置文件说明

### `config/default.json`

包含所有配置的默认值，结构清晰：

```json
{
  "game": {
    "num_players": 9,
    "roles": {...},
    "language": "zh",
    "max_rounds": 10
  },
  "llm": {
    "provider": "modelscope",
    "temperature": 0.8,
    "max_tokens": 500,
    "providers": {
      "openai": {...},
      "dashscope": {...},
      "modelscope": {...}
    }
  },
  "tts": {
    "enabled": true,
    "provider": "dashscope",
    "providers": {
      "dashscope": {...}
    }
  },
  "web": {...},
  "database": {...},
  "logging": {...}
}
```

### 修改配置文件

1. 直接编辑 `config/default.json`
2. 或创建新的配置文件（如 `config/production.json`）

---

## 环境变量配置

### 创建 `.env` 文件

```bash
# 复制示例文件
cp env.example.txt .env

# 编辑配置
vim .env  # 或使用你喜欢的编辑器
```

### `.env` 文件结构

```bash
# ============== LLM配置 ==============
LLM_PROVIDER=modelscope              # LLM提供商
LLM_TEMPERATURE=0.8                  # 温度参数
LLM_MAX_TOKENS=500                   # 最大tokens

# OpenAI
OPENAI_API_KEY=sk-xxx
OPENAI_MODEL=gpt-4o-mini

# DashScope
DASHSCOPE_API_KEY=sk-xxx
DASHSCOPE_MODEL=qwen-plus

# ModelScope
MODELSCOPE_API_KEY=ms-xxx
MODELSCOPE_MODEL=Qwen/Qwen2.5-32B-Instruct

# ============== TTS配置 ==============
TTS_ENABLED=true
TTS_PROVIDER=dashscope
TTS_MODEL=qwen3-tts-flash
TTS_VOICE=Cherry
TTS_SPEED=1.0
TTS_PITCH=1.0

# ============== Web配置 ==============
WEB_HOST=0.0.0.0
WEB_PORT=8000

# ============== 游戏配置 ==============
GAME_LANGUAGE=zh
GAME_NUM_PLAYERS=9
DEBUG_MODE=false
```

---

## LLM提供商配置

### 支持的提供商

| 提供商 | 优势 | 成本 | 推荐场景 |
|--------|------|------|----------|
| **ModelScope** | 免费、国内访问快 | 免费 | 开发测试 ⭐ |
| **DashScope** | 高质量、稳定 | 付费 | 生产环境 |
| **OpenAI** | 最高质量 | 付费 | 高质量需求 |
| **Anthropic** | Claude系列 | 付费 | 特定需求 |

### 配置方案

#### 方案A：ModelScope + DashScope（推荐 🌟）

**特点**：LLM免费，TTS付费但有免费额度

```bash
# .env
LLM_PROVIDER=modelscope
OPENAI_API_KEY=ms-your-modelscope-token
OPENAI_API_BASE=https://api-inference.modelscope.cn/v1/
OPENAI_MODEL=Qwen/Qwen2.5-32B-Instruct

DASHSCOPE_API_KEY=sk-your-dashscope-key
TTS_ENABLED=true
```

#### 方案B：全部使用DashScope

**特点**：配置简单，一个Key搞定

```bash
# .env
LLM_PROVIDER=dashscope
OPENAI_API_KEY=sk-your-dashscope-key
OPENAI_API_BASE=https://dashscope.aliyuncs.com/compatible-mode/v1
OPENAI_MODEL=qwen-plus

DASHSCOPE_API_KEY=sk-your-dashscope-key
```

#### 方案C：使用OpenAI

**特点**：最高质量，但成本较高

```bash
# .env
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-your-openai-key
OPENAI_MODEL=gpt-4o-mini

# TTS仍使用DashScope
DASHSCOPE_API_KEY=sk-your-dashscope-key
```

### 获取API Key

- **ModelScope**: https://www.modelscope.cn/my/myaccesstoken
- **DashScope**: https://dashscope.console.aliyun.com/apiKey
- **OpenAI**: https://platform.openai.com/api-keys
- **Anthropic**: https://console.anthropic.com/

---

## TTS提供商配置

### DashScope TTS（推荐）

```bash
TTS_PROVIDER=dashscope
DASHSCOPE_API_KEY=sk-your-key
TTS_MODEL=qwen3-tts-flash
TTS_VOICE=Cherry         # 音色选择
TTS_SPEED=1.0            # 语速 (0.5-2.0)
TTS_PITCH=1.0            # 音高 (0.5-2.0)
```

### 可用音色

**女声**：
- `Cherry` - 甜美清晰 ⭐ 推荐
- `Bella` - 温柔优雅
- `Amy` - 亲切自然
- `Emma` - 活泼可爱
- `Cora` - 成熟稳重
- `Eva` - 知性优雅

**男声**：
- `William` - 磁性低沉
- `James` - 沉稳可靠
- `Thomas` - 年轻活力

---

## 快速开始

### 1. 最小配置（仅3项）

```bash
# .env
LLM_PROVIDER=modelscope
OPENAI_API_KEY=ms-your-token
DASHSCOPE_API_KEY=sk-your-key
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 测试配置

```bash
python test_config.py
```

### 4. 启动服务

```bash
# 后端
python main.py

# 前端（另一个终端）
cd frontend
npm run dev
```

### 5. 访问应用

打开浏览器访问：http://localhost:5173

---

## 常见问题

### Q1: 如何切换LLM提供商？

修改 `.env` 文件中的 `LLM_PROVIDER`：

```bash
# 使用 ModelScope
LLM_PROVIDER=modelscope

# 使用 OpenAI
LLM_PROVIDER=openai

# 使用 DashScope
LLM_PROVIDER=dashscope
```

### Q2: 如何修改LLM温度参数？

```bash
# .env
LLM_TEMPERATURE=0.9  # 更随机 (0.0-2.0)
```

或在代码中：

```python
from src.agents.agent_factory import LLMFactory

llm = LLMFactory.create_llm(temperature=0.9)
```

### Q3: 如何禁用TTS？

```bash
# .env
TTS_ENABLED=false
```

### Q4: 配置修改后需要重启吗？

- **环境变量**：需要重启
- **代码参数**：立即生效

### Q5: 如何查看当前配置？

```python
from src.utils.config import get_config

config = get_config()
print(config.to_dict())
```

或运行测试：

```bash
python test_config.py
```

### Q6: ModelScope Token在哪里获取？

1. 访问 https://www.modelscope.cn
2. 登录账号
3. 进入「个人中心」→「访问令牌」
4. 复制 `ms-` 开头的token

### Q7: 如何验证配置是否正确？

```bash
python test_config.py
```

看到 `✅ 所有测试通过` 表示配置正确。

### Q8: 支持多个LLM同时使用吗？

可以！在代码中指定：

```python
from src.agents.agent_factory import AgentFactory

# 使用 OpenAI
agent1 = AgentFactory.create_agent(player1, provider="openai")

# 使用 ModelScope
agent2 = AgentFactory.create_agent(player2, provider="modelscope")
```

---

## 高级用法

### 自定义配置文件

```python
from src.utils.config import Config

# 加载自定义配置
config = Config(config_file="production.json")
```

### 程序化配置

```python
from src.agents.agent_factory import LLMFactory

# 直接传参，覆盖配置
llm = LLMFactory.create_llm(
    provider="openai",
    temperature=0.9,
    max_tokens=1000
)
```

### 配置验证

```python
from src.utils.config import get_config

config = get_config()

if config.validate():
    print("配置有效！")
else:
    print("配置无效，请检查API Key")
```

---

## 最佳实践

1. ✅ **使用 `.env` 文件** - 不要把API Key硬编码到代码中
2. ✅ **不要提交 `.env`** - 确保 `.env` 在 `.gitignore` 中
3. ✅ **使用 `env.example.txt`** - 提供配置示例，方便团队使用
4. ✅ **定期测试配置** - 运行 `test_config.py` 确保配置正确
5. ✅ **开发用ModelScope** - 免费且快速
6. ✅ **生产用DashScope/OpenAI** - 质量更稳定

---

## 配置参考

### 完整的环境变量列表

查看 `env.example.txt` 文件，包含所有可配置项的详细说明。

### 完整的配置文件结构

查看 `config/default.json` 文件，了解默认配置。

---

## 技术支持

遇到问题？

1. 查看 [README.md](../README.md)
2. 运行 `python test_config.py` 诊断配置
3. 查看日志文件 `data/logs/werewolf.log`
4. 提交 Issue 到 GitHub

---

**祝你使用愉快！** 🎉

