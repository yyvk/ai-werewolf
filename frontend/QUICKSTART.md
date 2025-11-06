# 🚀 AI狼人杀前端 - 快速启动指南

## 第一次使用？按照以下步骤：

### 步骤1: 安装Node.js

确保已安装Node.js 16+

检查版本：
```bash
node --version
npm --version
```

### 步骤2: 安装依赖

```bash
cd frontend
npm install
```

这将安装所有需要的包：
- Vue 3
- Vue Router
- Pinia
- Axios
- Vite

### 步骤3: 启动后端服务

在项目根目录打开新的终端：

```bash
# 确保werewolf环境已激活
python main.py
```

后端服务将运行在：http://localhost:8000

### 步骤4: 启动前端开发服务器

在frontend目录：

```bash
npm run dev
```

前端将运行在：http://localhost:3000

### 步骤5: 打开浏览器

访问：http://localhost:3000

你应该看到AI狼人杀的主页！

## 🎮 使用流程

1. **查看统计** - 主页显示总游戏数和活跃游戏数
2. **创建游戏** - 点击"创建新游戏"按钮
3. **配置参数**：
   - 玩家数量：4-12人
   - LLM提供商：OpenAI (ModelScope)
   - 模型名称：可选，留空使用默认
4. **进入游戏房间** - 创建后自动跳转
5. **开始游戏** - 点击"开始游戏"按钮
6. **观看对局** - 游戏会自动刷新显示最新状态

## 🔧 常见问题

### Q: 前端无法连接后端？
**A**: 确保：
1. 后端服务已启动在8000端口
2. 检查终端是否有错误
3. 访问 http://127.0.0.1:8000/health 测试后端

### Q: npm install 失败？
**A**: 尝试：
```bash
# 清除缓存
npm cache clean --force
# 重新安装
npm install
```

### Q: 端口被占用？
**A**: 修改 `vite.config.js` 中的端口：
```js
server: {
  port: 3001,  // 改成其他端口
}
```

### Q: 页面空白？
**A**: 
1. 打开浏览器控制台查看错误
2. 确认后端API正常
3. 检查网络请求是否成功

## 📱 浏览器要求

推荐使用现代浏览器：
- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Edge 90+
- ✅ Safari 14+

## 🎨 功能预览

### 主页功能
- 📊 实时统计
- ➕ 创建游戏
- 📋 游戏列表
- 🗑️ 删除游戏

### 游戏房间
- 📝 游戏信息面板
- 👥 玩家列表
- 📢 游戏事件流
- 🔄 自动刷新

## 💡 开发技巧

### 修改API地址
编辑 `vite.config.js`:
```js
server: {
  proxy: {
    '/api': {
      target: 'http://your-backend-url:8000',
      changeOrigin: true,
    },
  },
}
```

### 禁用自动刷新
编辑 `src/views/GameRoom.vue`，注释掉：
```js
// startAutoRefresh()
```

### 修改主题颜色
编辑 `src/assets/main.css` 或组件内的样式

## 🚀 生产部署

### 构建项目
```bash
npm run build
```

### 预览构建
```bash
npm run preview
```

### 部署到服务器
将 `dist/` 目录上传到Web服务器（Nginx、Apache等）

## 📞 需要帮助？

- 查看 `README.md` 了解详细文档
- 检查浏览器控制台的错误信息
- 查看后端API文档：http://127.0.0.1:8000/docs

---

**祝你玩得开心！** 🎮🐺



