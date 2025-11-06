# 🐺 AI狼人杀 | AI Werewolf

> 基于AI Agent的智能狼人杀游戏，让AI玩家进行推理、欺骗和对决

[English](README_EN.md) | 简体中文

## ✨ 项目简介

AI狼人杀是一个创新的狼人杀游戏项目，使用AI Agent技术让多个AI玩家进行自主推理、发言和投票。每个AI玩家都拥有独立的思考能力、记忆系统和行为策略，能够进行真实的游戏对局。

### 🎯 核心特点

- **🤖 智能AI玩家** - 基于大语言模型的智能Agent，能够推理和欺骗
- **🎭 性格化角色** - 每个AI都有独特的性格和发言风格（理性派、激进派、幽默派）
- **🎬 观赏性强** - AI之间的对话和推理本身就是精彩内容
- **🏗️ 模块化架构** - 清晰的代码组织，易于扩展和维护
- **🌐 Web界面** - 现代化的Web界面，实时观看AI对局
- **🔊 语音合成** - 支持通义千问TTS，为AI角色配音

## 🚀 快速开始

### 环境要求

- Python 3.8+
- Node.js 16+
- LLM API密钥（OpenAI、通义千问、或其他兼容服务）

### 安装步骤

```bash
# 1. 克隆项目
git clone https://github.com/yyvk/ai-werewolf.git
cd ai-werewolf

# 2. 安装Python依赖
pip install -r requirements.txt

# 3. 配置环境变量
cp env.example.txt .env
# 编辑 .env 文件，填入你的API密钥

# 4. 安装前端依赖
cd frontend
npm install
cd ..
```

### 配置API密钥

在 `.env` 文件中配置LLM API：

```bash
# OpenAI配置
OPENAI_API_KEY=your-api-key-here
OPENAI_MODEL=gpt-4o-mini

# 或使用通义千问（阿里云）
DASHSCOPE_API_KEY=your-api-key-here
DASHSCOPE_MODEL=qwen-turbo

# 或使用ModelScope
OPENAI_API_KEY=your-modelscope-token
OPENAI_API_BASE=https://api-inference.modelscope.cn/v1
OPENAI_MODEL=Qwen/Qwen2.5-7B-Instruct
```

### 启动项目

#### 方式一：使用启动脚本（推荐）

**Windows PowerShell:**
```powershell
# 启动后端
.\start_backend.ps1

# 启动前端（新终端）
cd frontend
.\start.ps1
```

**Linux/Mac:**
```bash
# 启动后端
python main.py

# 启动前端（新终端）
cd frontend
npm run dev
```

#### 方式二：手动启动

**启动后端API服务:**
```bash
python main.py
```

后端服务地址：
- API服务: http://localhost:8000
- API文档: http://localhost:8000/docs
- 健康检查: http://localhost:8000/health

**启动前端Web界面:**
```bash
cd frontend
npm run dev
```

前端服务地址：http://localhost:3000

### 开始游戏

1. 打开浏览器访问 http://localhost:3000
2. 点击 **"创建新游戏"** 按钮
3. 配置游戏参数（玩家数量、角色配置等）
4. 点击 **"创建游戏"** 并进入游戏房间
5. 点击 **"开始游戏"** 让AI开始对局
6. 点击 **"下一轮"** 推进游戏进程

## 📁 项目结构

```
ai-werewolf/
├── src/                    # 源代码
│   ├── core/              # 核心游戏逻辑
│   │   ├── models.py      # 数据模型
│   │   ├── game_engine.py # 游戏引擎
│   │   └── event_system.py# 事件系统
│   ├── agents/            # AI Agent实现
│   │   ├── base_agent.py  # Agent基类
│   │   ├── langchain_agent.py # LangChain实现
│   │   └── agent_factory.py # Agent工厂
│   ├── database/          # 数据库接口层
│   ├── web/              # Web API服务
│   ├── video/            # 视频生成模块
│   └── utils/            # 工具和配置
├── frontend/             # 前端Web界面
│   ├── src/             # 源代码
│   │   ├── components/  # Vue组件
│   │   ├── views/       # 页面视图
│   │   ├── stores/      # 状态管理
│   │   └── api/         # API接口
│   └── public/          # 静态资源
├── data/                # 数据目录
│   ├── games/          # 游戏记录
│   ├── logs/           # 日志文件
│   └── cache/          # 缓存数据
├── assets/             # 资源文件
├── config/             # 配置文件
└── docs/               # 文档
```

## 🏗️ 技术架构

### 架构风格

- **模块化设计** - 6个核心模块，职责清晰
- **事件驱动** - 支持实时响应和状态更新
- **Agent架构** - 每个AI玩家是独立的智能体

### 技术栈

| 层次 | 技术 |
|------|------|
| AI/LLM | LangChain, OpenAI, 通义千问, ModelScope |
| Web框架 | FastAPI, Uvicorn, WebSocket |
| 前端 | Vue 3, Vite, Pinia, Vue Router |
| 数据库 | JSON文件存储, ChromaDB（计划）, Redis（计划） |
| 语音合成 | DashScope TTS (通义千问) |
| 视频处理 | MoviePy（计划）, OpenCV（计划） |

### 架构图

```
┌─────────────────────────────────────────────┐
│           客户端层 (Web Browser)             │
│         Vue 3 + Vite + Axios                │
└───────────────────┬─────────────────────────┘
                    │ HTTP/WebSocket
┌───────────────────┴─────────────────────────┐
│           API层 (FastAPI)                    │
│     REST API + WebSocket                    │
└───────────────────┬─────────────────────────┘
                    │
┌───────────────────┴─────────────────────────┐
│         业务逻辑层 (Business Logic)          │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │游戏引擎   │  │AI Agent  │  │事件系统   │  │
│  │GameEngine│  │LangChain │  │Events    │  │
│  └──────────┘  └──────────┘  └──────────┘  │
└───────────────────┬─────────────────────────┘
                    │
┌───────────────────┴─────────────────────────┐
│         数据访问层 (Data Access)             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │游戏仓库   │  │缓存数据库 │  │向量数据库 │  │
│  │JSON      │  │Memory    │  │(计划)    │  │
│  └──────────┘  └──────────┘  └──────────┘  │
└───────────────────┬─────────────────────────┘
                    │
┌───────────────────┴─────────────────────────┐
│         外部服务层 (External Services)       │
│     OpenAI / 通义千问 / ModelScope          │
└─────────────────────────────────────────────┘
```

## 🎮 功能特色

### 已实现功能 ✅

- ✅ 完整的狼人杀游戏规则引擎（6人/9人局）
- ✅ 基于LangChain的AI Agent系统
- ✅ 支持多种角色：狼人、村民、预言家、女巫、猎人
- ✅ 三种AI性格：理性派、激进派、幽默派
- ✅ RESTful API接口
- ✅ WebSocket实时通信（计划中）
- ✅ Vue 3前端界面
- ✅ 游戏状态持久化（JSON）
- ✅ 事件系统和游戏回放
- ✅ TTS语音合成（通义千问）

### 开发中功能 🚧

- 🚧 WebSocket实时游戏状态推送
- 🚧 多房间支持
- 🚧 游戏视频生成
- 🚧 精彩片段自动剪辑
- 🚧 玩家可参与游戏（1人+N个AI）

### 计划功能 📋

- 📋 向量数据库集成（ChromaDB）
- 📋 Redis缓存层
- 📋 更多游戏模式（白狼王、守卫等）
- 📋 AI学习和进化
- 📋 社交功能（分享、评论）
- 📋 移动端适配

## 🔧 配置说明

### 游戏配置

编辑 `config/default.json` 来自定义游戏参数：

```json
{
  "game": {
    "num_players": 9,
    "roles": {
      "werewolf": 3,
      "villager": 3,
      "seer": 1,
      "witch": 1,
      "hunter": 1
    }
  },
  "llm": {
    "provider": "openai",
    "model": "gpt-4o-mini",
    "temperature": 0.7
  },
  "agent": {
    "personalities": ["rational", "aggressive", "humorous"],
    "memory_limit": 10
  },
  "tts": {
    "enabled": true,
    "model": "qwen3-tts-flash",
    "voice": "Cherry"
  }
}
```

### 支持的LLM提供商

1. **OpenAI**
   ```bash
   OPENAI_API_KEY=sk-...
   OPENAI_MODEL=gpt-4o-mini
   ```

2. **通义千问（阿里云DashScope）**
   ```bash
   DASHSCOPE_API_KEY=sk-...
   DASHSCOPE_MODEL=qwen-turbo
   ```

3. **ModelScope**
   ```bash
   OPENAI_API_KEY=your-token
   OPENAI_API_BASE=https://api-inference.modelscope.cn/v1
   OPENAI_MODEL=Qwen/Qwen2.5-7B-Instruct
   ```

### TTS语音配置

支持通义千问TTS服务，可选的语音角色包括：
- Cherry (女声，温柔甜美)
- ZhiMiao (女声，知性优雅)
- Zhitian (男声，成熟稳重)
- ZhiYan (女声，清脆明亮)

## 🛠️ 开发指南

### 添加新角色

1. 在 `src/core/models.py` 中添加角色枚举
2. 在 `config/default.json` 中配置角色数量
3. 实现角色特殊技能（如需要）

### 自定义AI性格

在 `src/agents/langchain_agent.py` 中修改性格提示词：

```python
PERSONALITIES = {
    "rational": "你是一个理性冷静的玩家...",
    "aggressive": "你是一个激进大胆的玩家...",
    "humorous": "你是一个幽默风趣的玩家..."
}
```

### 添加API端点

在 `src/web/api.py` 中添加新的路由：

```python
@app.post("/api/custom-endpoint")
async def custom_endpoint():
    # 实现逻辑
    return {"status": "ok"}
```

### 运行测试

```bash
# 测试后端API
python -m pytest tests/

# 测试完整流程（Windows）
.\test_complete_flow.ps1

# 测试Web API（Windows）
.\test_web_api.ps1
```

## 🤝 参与贡献

欢迎参与项目开发！

1. Fork 本项目
2. 创建 Feature 分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 提交 Pull Request

### 开发规范

- 遵循 PEP 8 Python代码规范
- 使用类型提示（Type Hints）
- 编写清晰的文档字符串
- 保持函数简短和单一职责
- 添加必要的单元测试

## 📊 产品愿景

### 观赏型产品（当前阶段）
- 用户可以观看AI之间的精彩对局
- AI具有不同性格和发言风格
- 自动生成精彩片段
- 支持暂停、回看、倍速播放

### 互动型产品（计划中）
- 用户可作为玩家参与（1人+8个AI）
- 用户可押注/预测谁是狼人
- 用户可自定义AI性格
- 社交分享和好友对战

### 差异化竞争点
- ✨ AI性格化（不是冰冷的逻辑机器）
- ✨ 名人/IP联动（如"马斯克 vs 诸葛亮"）
- ✨ 短视频优先（适合抖音/B站传播）
- ✨ 观看+参与双模式

## 🐛 故障排除

### 后端启动失败
- 检查Python版本（需要3.8+）
- 确认依赖已安装：`pip install -r requirements.txt`
- 检查端口8000是否被占用
- 验证API密钥配置正确

### 前端启动失败
- 确认Node.js已安装（需要16+）
- 安装依赖：`cd frontend && npm install`
- 检查端口3000是否被占用

### AI不发言或发言异常
- 检查 `.env` 中的API密钥是否正确
- 查看日志文件 `data/logs/werewolf_*.log`
- 尝试降低 `config/default.json` 中的 `temperature` 值
- 确认网络可以访问LLM API服务

### TTS语音不可用
- 确认配置了 `DASHSCOPE_API_KEY`
- 检查 `config/default.json` 中 `tts.enabled` 为 `true`
- 查看日志了解具体错误信息

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 📞 联系方式

- **GitHub Issues**: [提交问题](https://github.com/yyvk/ai-werewolf/issues)
- **项目主页**: [https://github.com/yyvk/ai-werewolf](https://github.com/yyvk/ai-werewolf)

---

**让AI玩狼人杀，看推理与欺骗的精彩对决！** 🎭🤖
