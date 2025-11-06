# 🚀 AI狼人杀 - 快速启动

## 一键启动指南

### 步骤1: 启动后端服务器

在项目根目录打开终端：

```bash
python main.py
```

**后端服务地址：**
- API服务: http://localhost:8000
- API文档: http://localhost:8000/docs
- 健康检查: http://localhost:8000/health

### 步骤2: 启动前端服务器

在新终端中运行：

```bash
cd frontend
npm run dev
```

**前端服务地址：**
- Web界面: http://localhost:3000

## 🎮 开始游戏

1. 打开浏览器访问：http://localhost:3000
2. 点击 **"创建新游戏"** 按钮
3. 配置游戏参数：
   - 玩家数量：6（默认）
   - LLM提供商：OpenAI (ModelScope)
4. 点击 **"创建游戏"** 并进入游戏房间
5. 点击 **"开始游戏"** 让AI开始对局
6. 点击 **"下一轮"** 继续游戏进程

## 📋 功能列表

### Web界面功能
- ✅ 创建新游戏
- ✅ 查看游戏列表
- ✅ 进入游戏房间
- ✅ 查看玩家状态和角色
- ✅ 查看游戏事件流
- ✅ 控制游戏进程
- ✅ 实时刷新状态
- ✅ 删除游戏

### API功能
- ✅ REST API接口
- ✅ 游戏状态管理
- ✅ AI Agent对局
- ✅ 自动游戏流程
- ✅ 完整的API文档

## 🔧 配置说明

### 环境变量设置

复制 `env.example.txt` 到 `.env` 并配置：

```bash
# ModelScope/OpenAI配置
OPENAI_API_KEY=your-api-key
OPENAI_API_BASE=https://api-inference.modelscope.cn/v1
OPENAI_MODEL=Qwen/Qwen2.5-7B-Instruct
```

### 修改配置

编辑 `config/default.json`：

```json
{
  "game": {
    "num_players": 6,
    "roles": { "werewolf": 2, "villager": 3, "seer": 1 }
  },
  "web": {
    "host": "0.0.0.0",
    "port": 8000
  }
}
```

## 🐛 故障排除

### 后端启动失败
- 检查Python环境是否正确
- 确认依赖已安装：`pip install -r requirements.txt`
- 检查端口8000是否被占用

### 前端启动失败
- 确认Node.js已安装（16+）
- 安装依赖：`npm install`
- 检查端口3000是否被占用

### API连接失败
- 确认后端服务已启动
- 访问 http://localhost:8000/health 检查后端状态
- 检查防火墙设置

## 📚 更多文档

- [快速启动指南](frontend/QUICKSTART.md)
- [项目README](README.md)
- [架构设计](ARCHITECTURE.md)
- [项目结构](PROJECT_STRUCTURE.md)

## 🎯 测试脚本

### 测试Web API（PowerShell）

```powershell
.\test_web_api.ps1
```

### 测试完整流程（PowerShell）

```powershell
.\test_complete_flow.ps1
```

---

**开始享受AI狼人杀的精彩对局吧！** 🐺🤖

