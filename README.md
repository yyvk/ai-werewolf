# 🐺 AI狼人杀项目

> 基于AI Agent的智能狼人杀游戏，让AI玩家进行推理、欺骗和对决

## 📋 项目简介

这是一个创新的狼人杀游戏项目，使用AI Agent技术让多个AI玩家进行自主推理、发言和投票。每个AI玩家都拥有独立的思考能力、记忆系统和行为策略，能够进行真实的游戏对局。

### 🎯 核心特点

- **🤖 智能AI玩家** - 基于大语言模型的智能Agent，能够推理和欺骗
- **🎭 性格化角色** - 每个AI都有独特的性格和发言风格
- **🎬 观赏性强** - AI之间的对话和推理本身就是精彩内容
- **🏗️ 模块化架构** - 清晰的代码组织，易于扩展和维护
- **🌐 Web界面** - 现代化的Web界面，实时观看AI对局

## 🚀 快速开始

### 环境要求

- Python 3.8+
- LLM API密钥（OpenAI、通义千问、或其他兼容服务）

### 安装步骤

```bash
# 1. 克隆项目
git clone https://github.com/yyvk/ai-werewolf.git
cd ai-werewolf

# 2. 安装依赖
pip install -r requirements.txt

# 3. 配置环境变量
cp env.example.txt .env
# 编辑 .env 文件，填入你的API密钥
```

### 配置说明

在 `.env` 文件中配置LLM API：

```bash
# OpenAI配置
OPENAI_API_KEY=your-api-key-here
OPENAI_MODEL=gpt-4o-mini

# 或使用通义千问（阿里云）
DASHSCOPE_API_KEY=your-api-key-here
DASHSCOPE_MODEL=qwen-turbo

# 或使用ModelScope
MODELSCOPE_ACCESS_TOKEN=your-token-here
```

### 运行游戏

#### 启动后端API服务

```bash
python main.py
```

后端服务将运行在：http://localhost:8000
API文档：http://localhost:8000/docs

#### 启动前端Web界面

```bash
cd frontend
npm install  # 首次运行需要安装依赖
npm run dev
```

前端将运行在：http://localhost:3000

更多详细信息请查看 [frontend/QUICKSTART.md](frontend/QUICKSTART.md)

## 📁 项目结构

```
ai-werewolf/
├── src/                    # 源代码
│   ├── core/               # 核心游戏逻辑
│   ├── agents/             # AI Agent实现
│   ├── database/           # 数据库接口层
│   ├── web/                # Web API服务
│   ├── video/              # 视频生成模块
│   └── utils/              # 工具和配置
├── data/                   # 数据目录
│   ├── games/              # 游戏记录
│   ├── logs/               # 日志文件
│   ├── cache/              # 缓存数据
│   └── vector_db/          # 向量数据库
├── assets/                 # 资源文件
│   ├── images/             # 图片
│   ├── audio/              # 音频
│   └── effects/            # 特效
├── output/                 # 输出目录
│   ├── videos/             # 生成的视频
│   └── screenshots/        # 截图
├── config/                 # 配置文件
├── docs/                   # 文档
└── tests/                  # 测试代码
```

## 📚 文档

### 核心文档
- **[ARCHITECTURE.md](./ARCHITECTURE.md)** - 技术架构设计
- **[PROJECT_STRUCTURE.md](./PROJECT_STRUCTURE.md)** - 项目结构说明
- **[AI狼人杀产品设计方案.md](./AI狼人杀产品设计方案.md)** - 完整产品设计
- **[狼人杀经典玩法调研.md](./狼人杀经典玩法调研.md)** - 游戏规则调研

### 配置指南
- **[CONDA_SETUP.md](./CONDA_SETUP.md)** - Conda环境配置
- **[LANGCHAIN_SETUP.md](./LANGCHAIN_SETUP.md)** - LangChain配置
- **[MODELSCOPE_GUIDE.md](./MODELSCOPE_GUIDE.md)** - ModelScope API指南

## 🏗️ 技术架构

### 架构风格
- **模块化设计** - 6个核心模块，职责清晰
- **事件驱动** - 支持实时响应和状态更新
- **Agent架构** - 每个AI玩家是独立的智能体

### 技术栈

| 层次 | 技术 |
|------|------|
| AI/LLM | LangChain, OpenAI, ModelScope |
| Web框架 | FastAPI, Uvicorn, WebSocket |
| 数据库 | ChromaDB（计划）, Redis（计划）, JSON |
| 视频处理 | MoviePy（计划）, OpenCV（计划） |
| 前端 | React（计划）, WebSocket |

## 🎮 游戏特色

### 观赏型产品
- 用户可以观看AI之间的精彩对局
- AI具有不同性格（理性派、激进派、幽默派）
- 自动生成精彩片段
- 支持暂停、回看、倍速播放

### 互动型产品（计划中）
- 用户可作为玩家参与（1人+8个AI）
- 用户可押注/预测谁是狼人
- 用户可自定义AI性格

## 🎯 产品愿景

### 核心目标
**快速吸引用户观看 + 提升用户留存**

### 差异化竞争点
- ✨ AI性格化（不是冰冷的逻辑机器）
- ✨ 名人/IP联动（如"马斯克 vs 诸葛亮"）
- ✨ 短视频优先（适合抖音/B站传播）
- ✨ 观看+参与双模式

### 内容营销
- 短视频传播："AI版狼人杀！9个AI互相欺骗"
- 特色玩法：名人AI对局、历史人物竞技
- 社交分享：精彩对局卡片、好友对战

## 🛠️ 开发进度

### 当前阶段：架构设计 ✅
- ✅ 项目结构设计
- ✅ 技术方案确定
- ✅ 文档体系建立
- ✅ 依赖配置完成

### 下一阶段：核心实现 🚧
- ⏳ 游戏引擎实现
- ⏳ AI Agent开发
- ⏳ LLM API集成
- ⏳ 基础游戏流程

### 后续阶段
- 📋 Web API服务
- 📋 前端界面开发
- 📋 视频生成功能
- 📋 性能优化

## 💡 使用场景

### 娱乐观看
- 观看AI对局，享受推理过程
- 学习狼人杀策略和技巧
- 作为背景娱乐内容

### 内容创作
- 生成短视频素材
- 制作游戏解说内容
- AI对话有趣片段

### 游戏参与
- 与AI一起游戏
- 测试自己的推理能力
- 体验不同角色玩法

## 🤝 参与贡献

欢迎参与项目开发！

1. Fork 本项目
2. 创建 Feature 分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 提交 Pull Request

## 📝 开发规范

- 遵循 PEP 8 Python代码规范
- 使用类型提示（Type Hints）
- 编写清晰的文档字符串
- 保持函数简短和单一职责
- 添加必要的单元测试

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 📞 联系方式

- **GitHub Issues**: [提交问题](https://github.com/yyvk/ai-werewolf/issues)
- **项目主页**: [https://github.com/yyvk/ai-werewolf](https://github.com/yyvk/ai-werewolf)

---

**让AI玩狼人杀，看推理与欺骗的精彩对决！** 🎭🤖
