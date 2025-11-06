# 🚀 启动前端指南

## 方法1：自动安装和启动（推荐）

### 首次使用 - 安装依赖

```powershell
cd frontend
powershell -ExecutionPolicy Bypass -File setup.ps1
```

### 启动完整服务（后端+前端）

```powershell
cd frontend
powershell -ExecutionPolicy Bypass -File start.ps1
```

这会自动启动：
- 后端服务（8000端口）
- 前端服务（3000端口）

---

## 方法2：手动启动

### 步骤1：启动后端

打开终端1：
```bash
# 项目根目录
python main.py --mode web
```

### 步骤2：启动前端

打开终端2：
```bash
cd frontend
npm run dev
```

### 步骤3：访问应用

浏览器打开：**http://localhost:3000**

---

## 快速测试

只测试前端（不需要后端）：

```bash
cd frontend
npm run dev
```

注意：没有后端时，API调用会失败。

---

## 🎯 访问地址

| 服务 | 地址 | 说明 |
|------|------|------|
| **前端界面** | http://localhost:3000 | Vue主页 |
| **后端API** | http://localhost:8000 | FastAPI服务 |
| **API文档** | http://localhost:8000/docs | Swagger UI |

---

## 🐛 遇到问题？

### 端口被占用
修改 `frontend/vite.config.js` 的端口号

### npm install失败
```bash
npm cache clean --force
npm install
```

### 后端连接失败
1. 确保后端在8000端口运行
2. 访问 http://localhost:8000/health 测试

---

## 📚 更多文档

- **详细文档**: `frontend/README.md`
- **快速指南**: `frontend/QUICKSTART.md`

---

**准备好了吗？开始你的AI狼人杀之旅！** 🎮🐺










