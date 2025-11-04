# 🏗️ AI狼人杀 - 架构文档

## 📋 目录

- [项目概述](#项目概述)
- [架构设计](#架构设计)
- [目录结构](#目录结构)
- [核心模块](#核心模块)
- [数据流](#数据流)
- [扩展指南](#扩展指南)

---

## 项目概述

### 核心特性
✅ **模块化设计** - 清晰的模块划分，易于维护和扩展  
✅ **事件驱动架构** - 支持实时响应和视频生成  
✅ **数据库抽象层** - 支持向量数据库和缓存  
✅ **Web API** - 提供REST API和WebSocket支持  
✅ **视频生成** - 自动化游戏视频制作  
✅ **可扩展Agent** - 基于LangChain的AI Agent架构  

---

## 架构设计

### 整体架构图

```
┌─────────────────────────────────────────────────────────────┐
│                     客户端层 (Client Layer)                  │
│  ┌─────────────┐  ┌─────────────┐  ┌──────────────┐        │
│  │ Web浏览器    │  │ 移动应用     │  │  CLI客户端   │        │
│  └─────────────┘  └─────────────┘  └──────────────┘        │
└───────────────────────────┬─────────────────────────────────┘
                            │ HTTP/WebSocket
┌───────────────────────────┴─────────────────────────────────┐
│                    API层 (API Layer)                         │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  FastAPI Web Service                                 │    │
│  │  - REST API Endpoints                                │    │
│  │  - WebSocket Support                                 │    │
│  │  - CORS & Authentication                             │    │
│  └─────────────────────────────────────────────────────┘    │
└───────────────────────────┬─────────────────────────────────┘
                            │
┌───────────────────────────┴─────────────────────────────────┐
│                  业务逻辑层 (Business Logic Layer)            │
│                                                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  游戏引擎    │  │  Agent管理器 │  │   事件系统   │      │
│  │ GameEngine   │  │ AgentFactory │  │ EventSystem  │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│                                                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  视频生成器  │  │   AI Agent   │  │  配置管理器  │      │
│  │VideoGenerator│  │ LangChain    │  │    Config    │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└───────────────────────────┬─────────────────────────────────┘
                            │
┌───────────────────────────┴─────────────────────────────────┐
│                  数据访问层 (Data Access Layer)              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  向量数据库  │  │   缓存数据库 │  │  游戏仓库    │      │
│  │  VectorDB    │  │   CacheDB    │  │ GameRepo     │      │
│  │(ChromaDB/    │  │  (Redis/     │  │(JSON/SQLite) │      │
│  │ FAISS)       │  │  Memory)     │  │              │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└───────────────────────────┬─────────────────────────────────┘
                            │
┌───────────────────────────┴─────────────────────────────────┐
│                外部服务层 (External Services)                │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ ModelScope   │  │   OpenAI     │  │   本地LLM    │      │
│  │     API      │  │     API      │  │  (Ollama)    │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
```

---

## 目录结构

```
ai-werewolf/
├── src/                         # 源代码
│   ├── core/                    # 核心游戏逻辑
│   │   ├── models.py            # 数据模型（Player, GameState等）
│   │   ├── game_engine.py       # 游戏引擎
│   │   └── event_system.py      # 事件系统
│   │
│   ├── agents/                  # AI Agent模块
│   │   ├── base_agent.py        # Agent基类
│   │   ├── langchain_agent.py   # LangChain实现
│   │   └── agent_factory.py     # Agent工厂
│   │
│   ├── database/                # 数据库模块
│   │   ├── base_db.py           # 数据库基类
│   │   ├── vector_db.py         # 向量数据库
│   │   ├── cache_db.py          # 缓存数据库
│   │   └── game_repository.py   # 游戏数据仓库
│   │
│   ├── web/                     # Web服务
│   │   ├── api.py               # FastAPI应用
│   │   └── websocket.py         # WebSocket管理
│   │
│   ├── video/                   # 视频生成
│   │   ├── video_generator.py   # 视频生成器
│   │   ├── effects.py           # 特效渲染
│   │   └── timeline.py          # 时间轴管理
│   │
│   └── utils/                   # 工具模块
│       ├── config.py            # 配置管理
│       └── logger.py            # 日志模块
│
├── config/                      # 配置文件
│   └── default.json             # 默认配置
│
├── data/                        # 数据目录
│   ├── vector_db/               # 向量数据库数据
│   ├── cache/                   # 缓存数据
│   ├── games/                   # 游戏记录
│   ├── replays/                 # 游戏回放
│   └── logs/                    # 日志文件
│
├── assets/                      # 资源文件
│   ├── images/                  # 图片资源
│   ├── audio/                   # 音频资源
│   └── effects/                 # 特效资源
│
├── output/                      # 输出目录
│   ├── videos/                  # 生成的视频
│   └── screenshots/             # 截图
│
├── tests/                       # 测试代码
│   ├── test_core/               # 核心模块测试
│   ├── test_agents/             # Agent测试
│   └── test_api/                # API测试
│
├── docs/                        # 文档
│
├── main.py                      # 主程序入口（待实现）
├── requirements.txt             # Python依赖
├── .env                         # 环境变量（不提交）
├── .gitignore                   # Git忽略文件
├── ARCHITECTURE.md              # 架构文档（本文件）
└── README.md                    # 项目说明
```

---

## 核心模块

### 1. Core模块（src/core/）

#### 数据模型（models.py）

核心数据结构（待实现）：
- `Player`: 玩家数据
- `Role`: 角色枚举
- `GameState`: 游戏状态
- `GamePhase`: 游戏阶段
- `AgentMemory`: Agent记忆

**设计要点**:
- 使用dataclass简化数据类定义
- 提供to_dict()方法支持序列化
- 包含业务逻辑方法（如check_game_over）

#### 游戏引擎（game_engine.py）

主要功能（待实现）：
- `setup_game()`: 初始化游戏
- `start_round()`: 开始新轮次
- `change_phase()`: 改变游戏阶段
- `eliminate_player()`: 淘汰玩家
- `check_game_over()`: 检查胜负

**设计要点**:
- 负责游戏规则和流程控制
- 与EventSystem集成，发布游戏事件
- 无状态设计，所有状态存储在GameState中

#### 事件系统（event_system.py）

主要功能（待实现）：
- `subscribe()`: 订阅事件
- `emit()`: 发布事件
- `get_history()`: 获取事件历史
- `get_key_moments()`: 获取关键时刻

**设计要点**:
- 发布-订阅模式
- 支持事件历史记录
- 为视频生成提供关键时刻标记

### 2. Agents模块（src/agents/）

#### Agent基类（base_agent.py）

抽象接口（待实现）：
- `think()`: 思考（抽象方法）
- `speak()`: 发言（抽象方法）
- `vote()`: 投票（抽象方法）
- `observe()`: 观察
- `update_belief()`: 更新判断

**设计要点**:
- 使用ABC定义接口
- 包含记忆管理功能
- 支持不同的Agent实现

#### LangChain Agent（langchain_agent.py）

功能（待实现）：
- 使用ChatOpenAI作为LLM后端
- ChatPromptTemplate管理提示词
- 自动降级到fallback模式

**设计要点**:
- 集成LangChain框架
- 模板化提示词管理
- 完善的错误处理

### 3. Database模块（src/database/）

#### 数据库架构

```
BaseDatabase (抽象基类)
    ├── VectorDatabase（向量数据库）
    │   - 支持语义搜索
    │   - 存储游戏记忆和策略
    │   - 可集成ChromaDB/FAISS
    │
    ├── CacheDatabase（缓存数据库）
    │   - 缓存LLM响应
    │   - 缓存游戏状态
    │   - 可集成Redis
    │
    └── GameRepository（游戏仓库）
        - 保存/加载游戏
        - 游戏回放功能
        - JSON文件存储
```

**设计要点**:
- 统一的数据库接口
- 易于切换实现（文件→Redis→数据库）
- 支持不同的存储需求

### 4. Web模块（src/web/）

#### FastAPI服务（api.py）

主要端点（待实现）：
```
POST /api/games          # 创建游戏
GET  /api/games/:id      # 获取游戏状态
POST /api/games/:id/start # 开始游戏
POST /api/games/:id/action # 执行操作
GET  /api/stats          # 获取统计
```

**设计要点**:
- RESTful API设计
- 支持CORS
- 完整的错误处理
- OpenAPI文档（/docs）

#### WebSocket（websocket.py）

功能（待实现）：
- `connect()`: 建立连接
- `broadcast()`: 广播消息
- `send_to_player()`: 发送给特定玩家

**设计要点**:
- 实时游戏状态推送
- 多房间支持
- 连接管理

### 5. Video模块（src/video/）

#### 视频生成流程

```
游戏事件 → Timeline → 渲染帧 → 添加特效 → 合成视频
```

**组件**（待实现）:
- **VideoGenerator**: 主生成器
- **EffectRenderer**: 特效渲染
- **Timeline**: 时间轴管理

**支持的功能**:
- 完整游戏视频
- 精彩集锦
- 玩家视角
- GIF动图导出

---

## 数据流

### 游戏流程数据流

```
1. 初始化
   User → main.py → Config → GameEngine → GameState

2. 创建Agent
   GameState.players → AgentFactory → LangChainAgent

3. 游戏回合
   GameEngine → Agent.speak() → LLM API → Response
                ↓
             EventSystem → Subscribers
                ↓
           (WebSocket, Logger, VideoGenerator)

4. 投票淘汰
   Agent.vote() → GameEngine.eliminate_player() → GameState.update()
                                ↓
                          EventSystem.emit(PLAYER_DIED)

5. 保存数据
   GameState → GameRepository → JSON文件
   Events → VideoGenerator → MP4视频
```

### LLM调用流程

```
Agent.speak() →  Cache.get(prompt)  →  [Cache Hit] → Return cached
        ↓
    [Cache Miss]
        ↓
   LangChain → ChatOpenAI → ModelScope/OpenAI API
        ↓
   Response → Cache.set() → Return response
```

---

## 扩展指南

### 添加新角色

1. **在core/models.py中添加角色枚举**
```python
class Role(str, Enum):
    NEW_ROLE = "new_role"
```

2. **添加角色描述**
```python
@property
def role_description(self) -> str:
    descriptions = {
        Role.NEW_ROLE: "新角色的描述..."
    }
```

3. **实现特殊技能（如需要）**
```python
class NewRoleAgent(LangChainAgent):
    def use_skill(self, game_state: GameState):
        # 实现技能逻辑
        pass
```

### 集成新的数据库

1. **继承BaseDatabase**
```python
class RedisDatabase(BaseDatabase):
    def connect(self):
        self.client = redis.Redis(...)
    
    def save(self, key, value):
        self.client.set(key, json.dumps(value))
```

2. **在Config中配置**
```python
self.cache_type = "redis"
self.redis_host = "localhost"
self.redis_port = 6379
```

### 添加新的特效

1. **在video/effects.py中添加**
```python
self.effects_library["new_effect"] = {
    "type": EffectType.CUSTOM,
    "duration": 1.0,
    "params": {...}
}
```

2. **实现渲染逻辑**
```python
def _render_new_effect(self, frame, progress):
    # 特效实现
    return frame
```

### 开发Web前端

1. **创建frontend目录**
```
frontend/
├── public/
├── src/
│   ├── components/
│   ├── pages/
│   └── api/
└── package.json
```

2. **使用API**
```javascript
// 创建游戏
fetch('/api/games', {
    method: 'POST',
    body: JSON.stringify({num_players: 6})
})

// WebSocket连接
const ws = new WebSocket('ws://localhost:8000/ws/game123')
```

---

## 最佳实践

### 1. 代码组织
- ✅ 单一职责原则
- ✅ 模块间低耦合
- ✅ 使用依赖注入
- ✅ 避免循环依赖

### 2. 错误处理
- ✅ 使用try-except捕获异常
- ✅ 提供降级方案
- ✅ 记录详细日志
- ✅ 友好的错误提示

### 3. 性能优化
- ✅ 缓存LLM响应
- ✅ 异步处理I/O操作
- ✅ 批量处理数据
- ✅ 使用连接池

### 4. 测试
- ✅ 单元测试（pytest）
- ✅ 集成测试
- ✅ Mock外部API
- ✅ 覆盖率 > 80%

---

## 技术栈

| 层次 | 技术 |
|------|------|
| AI/LLM | LangChain, OpenAI, ModelScope |
| Web框架 | FastAPI, Uvicorn |
| 数据库 | ChromaDB（计划）, Redis（计划）, SQLite |
| 视频处理 | MoviePy（计划）, OpenCV（计划）, PIL |
| 前端 | React（计划）, WebSocket |
| 部署 | Docker, K8s |

---

## 贡献指南

1. Fork项目
2. 创建feature分支
3. 提交代码（遵循代码规范）
4. 创建Pull Request

---

**项目**: AI Werewolf  
**文档**: 架构设计
