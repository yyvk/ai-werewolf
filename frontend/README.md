# 🎮 AI Werewolf Frontend | AI狼人杀前端

> Modern web interface built with Vue 3 + Vite for the AI Werewolf game

[English](#english) | [简体中文](#中文)

---

## English

### 🚀 Quick Start

#### Prerequisites
- Node.js 16+
- npm or yarn

#### Installation

```bash
cd frontend
npm install
```

#### Development Mode

```bash
npm run dev
```

Visit: http://localhost:3000

#### Production Build

```bash
npm run build
```

Build output in `dist/` directory

### 📁 Project Structure

```
frontend/
├── public/              # Static assets
├── src/
│   ├── api/            # API interface
│   │   └── game.js     # Game API
│   ├── assets/         # Assets
│   │   └── main.css    # Global styles
│   ├── components/     # Reusable components
│   ├── router/         # Router configuration
│   │   └── index.js    # Route definitions
│   ├── stores/         # Pinia state management
│   │   └── gameStore.js # Game state
│   ├── views/          # Page components
│   │   ├── Home.vue    # Home page
│   │   └── GameRoom.vue # Game room
│   ├── App.vue         # Root component
│   └── main.js         # Entry file
├── index.html          # HTML template
├── package.json        # Project config
├── vite.config.js      # Vite config
└── README.md
```

### 🎨 Features

#### Home Page
- ✅ Real-time game statistics
- ✅ Create new games
- ✅ View game list
- ✅ Delete games
- ✅ Enter game rooms

#### Game Room
- ✅ View game details
- ✅ Start game
- ✅ Real-time state refresh
- ✅ Display player list
- ✅ View game event stream
- ✅ Auto-refresh (every 5 seconds)
- ✅ Dynamic day/night background
- ✅ Circular player layout (village view)
- ✅ Role-based player icons
- ✅ Speaking player animations
- ✅ Immersive game atmosphere

### 🔧 Tech Stack

- **Framework**: Vue 3 (Composition API)
- **Build Tool**: Vite
- **Router**: Vue Router 4
- **State Management**: Pinia
- **HTTP Client**: Axios
- **Styling**: CSS3 (gradients, animations, Grid, Flexbox)

### 🌐 API Integration

Frontend communicates with backend API via Axios:

```js
import { gameAPI } from '@/api/game'

// Create game
const result = await gameAPI.createGame({
  num_players: 6,
  llm_provider: 'openai'
})

// Get game list
const games = await gameAPI.getGames()
```

### 🎮 Usage Flow

1. **View Statistics** - Home page shows total games and active games
2. **Create Game** - Click "Create New Game" button
3. **Configure Parameters**:
   - Number of players: 4-12
   - LLM Provider: OpenAI (ModelScope)
   - Model name: Optional, leave empty for default
4. **Enter Game Room** - Auto-redirect after creation
5. **Start Game** - Click "Start Game" button
6. **Watch Match** - Game auto-refreshes with latest state

### 🎨 UI Highlights

#### Dynamic Background
- **Day**: Blue sky and green field gradient with sun ☀️
- **Night**: Deep blue starry sky with moon 🌙
- Smooth transitions between phases

#### Circular Player Layout
- Players arranged in a circle (village view)
- Each player card features:
  - **Circular Avatar**: Role icon (🐺 Werewolf, 👨 Villager, 🔮 Seer, etc.)
  - **Number Badge**: Player number in top-right
  - **Name Plate**: Player name and role
  - **Animations**: 
    - Pulse animation for alive players
    - Scale animation and glow for speaking players
    - Hover to enlarge and show detailed info card

#### Role Icons
- 🐺 Werewolf
- 👨 Villager
- 🔮 Seer
- 🧙 Witch
- 🏹 Hunter
- 🛡️ Guard
- 💀 Eliminated
- 🤖 Unassigned

### 🛠️ Development

#### Start Backend Service
```bash
python main.py
```

Backend runs at: http://localhost:8000

#### Start Frontend Dev Server
```bash
cd frontend
npm run dev
```

Frontend runs at: http://localhost:3000

### 🐛 Troubleshooting

#### Frontend can't connect to backend?
Ensure:
1. Backend service is running on port 8000
2. Check terminal for errors
3. Visit http://127.0.0.1:8000/health to test backend

#### npm install fails?
Try:
```bash
npm cache clean --force
npm install
```

#### Port already in use?
Modify port in `vite.config.js`:
```js
server: {
  port: 3001,  // Change to another port
}
```

### 📱 Browser Requirements

Recommended modern browsers:
- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Edge 90+
- ✅ Safari 14+

### 📄 License

MIT License

---

## 中文

### 🚀 快速开始

#### 环境要求
- Node.js 16+
- npm 或 yarn

#### 安装依赖

```bash
cd frontend
npm install
```

#### 开发模式

```bash
npm run dev
```

访问：http://localhost:3000

#### 生产构建

```bash
npm run build
```

构建产物在 `dist/` 目录

### 📁 项目结构

```
frontend/
├── public/              # 静态资源
├── src/
│   ├── api/            # API接口
│   │   └── game.js     # 游戏相关API
│   ├── assets/         # 静态资源
│   │   └── main.css    # 全局样式
│   ├── components/     # 可复用组件
│   ├── router/         # 路由配置
│   │   └── index.js    # 路由定义
│   ├── stores/         # Pinia状态管理
│   │   └── gameStore.js # 游戏状态
│   ├── views/          # 页面组件
│   │   ├── Home.vue    # 首页
│   │   └── GameRoom.vue # 游戏房间
│   ├── App.vue         # 根组件
│   └── main.js         # 入口文件
├── index.html          # HTML模板
├── package.json        # 项目配置
├── vite.config.js      # Vite配置
└── README.md
```

### 🎨 功能特性

#### 首页
- ✅ 实时游戏统计
- ✅ 创建新游戏
- ✅ 查看游戏列表
- ✅ 删除游戏
- ✅ 进入游戏房间

#### 游戏房间
- ✅ 查看游戏详情
- ✅ 开始游戏
- ✅ 实时刷新游戏状态
- ✅ 显示玩家列表
- ✅ 查看游戏事件流
- ✅ 自动轮询更新（每5秒）
- ✅ 动态昼夜背景切换
- ✅ 玩家圆形布局（村庄视图）
- ✅ 基于角色的玩家图标
- ✅ 发言玩家动画效果
- ✅ 沉浸式游戏氛围

### 🔧 技术栈

- **框架**: Vue 3 (Composition API)
- **构建工具**: Vite
- **路由**: Vue Router 4
- **状态管理**: Pinia
- **HTTP客户端**: Axios
- **样式**: CSS3 (渐变、动画、Grid、Flexbox)

### 🌐 API集成

前端通过Axios与后端API通信：

```js
import { gameAPI } from '@/api/game'

// 创建游戏
const result = await gameAPI.createGame({
  num_players: 6,
  llm_provider: 'openai'
})

// 获取游戏列表
const games = await gameAPI.getGames()
```

### 🎮 使用流程

1. **查看统计** - 主页显示总游戏数和活跃游戏数
2. **创建游戏** - 点击"创建新游戏"按钮
3. **配置参数**：
   - 玩家数量：4-12人
   - LLM提供商：OpenAI (ModelScope)
   - 模型名称：可选，留空使用默认
4. **进入游戏房间** - 创建后自动跳转
5. **开始游戏** - 点击"开始游戏"按钮
6. **观看对局** - 游戏会自动刷新显示最新状态

### 🎨 界面亮点

#### 动态背景切换
- **白天**: 蓝天绿地渐变，配合太阳☀️图标
- **黑夜**: 深蓝色星空，配合月亮🌙图标
- 阶段之间平滑过渡

#### 玩家圆形布局
- 玩家围成圆形排列（村庄视图）
- 每个玩家卡片包含：
  - **圆形头像**: 角色图标（🐺狼人、👨村民、🔮预言家等）
  - **编号徽章**: 右上角显示玩家编号
  - **名牌**: 显示玩家名称和角色
  - **动画效果**: 
    - 存活玩家有脉冲动画
    - 发言玩家有缩放动画和光晕效果
    - 悬浮时放大并显示详细信息卡片

#### 角色图标
- 🐺 狼人
- 👨 村民
- 🔮 预言家
- 🧙 女巫
- 🏹 猎人
- 🛡️ 守卫
- 💀 已淘汰
- 🤖 未分配

### 🛠️ 开发指南

#### 启动后端服务
```bash
python main.py
```

后端运行在：http://localhost:8000

#### 启动前端开发服务器
```bash
cd frontend
npm run dev
```

前端运行在：http://localhost:3000

### 🐛 故障排除

#### 前端无法连接后端？
确保：
1. 后端服务已启动在8000端口
2. 检查终端是否有错误
3. 访问 http://127.0.0.1:8000/health 测试后端

#### npm install 失败？
尝试：
```bash
npm cache clean --force
npm install
```

#### 端口被占用？
修改 `vite.config.js` 中的端口：
```js
server: {
  port: 3001,  // 改成其他端口
}
```

### 📱 浏览器要求

推荐使用现代浏览器：
- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Edge 90+
- ✅ Safari 14+

### 📄 许可证

MIT License

---

**Powered by Vue 3 + Vite** ⚡️
