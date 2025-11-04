# 🐍 Conda环境配置指南

## ✅ 已完成的安装

- ✅ Miniconda 已安装 (conda 25.9.1)
- ✅ 创建了 `werewolf` 虚拟环境 (Python 3.11.14)
- ✅ 已安装核心依赖：
  - `openai` (2.6.1) - OpenAI API客户端
  - `dashscope` (1.24.9) - 阿里云通义千问API
  - `python-dotenv` (1.2.1) - 环境变量管理
  - `pydantic` (2.12.3) - 数据验证

## 📍 安装路径

- **Miniconda安装目录**: `C:\Users\30677\Miniconda3`
- **werewolf环境目录**: `C:\Users\30677\Miniconda3\envs\werewolf`
- **Python解释器**: `C:\Users\30677\Miniconda3\envs\werewolf\python.exe`

## 🚀 如何使用Conda环境

### 方法1：在PowerShell中使用（推荐）

1. **初始化PowerShell（首次使用）**
   ```powershell
   & "$env:USERPROFILE\Miniconda3\Scripts\conda.exe" init powershell
   ```
   然后重启PowerShell。

2. **激活werewolf环境**
   ```powershell
   conda activate werewolf
   ```

3. **验证环境**
   ```powershell
   python --version  # 应该显示 Python 3.11.14
   ```

4. **运行狼人杀项目**
   ```powershell
   cd E:\workspace\study\werewolf
   python werewolf_agent_demo.py  # 纯Python演示
   python werewolf_with_llm.py    # LLM版本（需要配置API key）
   ```

5. **退出环境**
   ```powershell
   conda deactivate
   ```

### 方法2：直接使用Python解释器

不需要激活环境，直接使用完整路径：

```powershell
cd E:\workspace\study\werewolf
& "$env:USERPROFILE\Miniconda3\envs\werewolf\python.exe" werewolf_agent_demo.py
```

## 🔑 配置API密钥

1. **创建.env文件**
   
   在项目根目录创建`.env`文件（基于`env.example.txt`）：
   ```powershell
   cd E:\workspace\study\werewolf
   Copy-Item env.example.txt .env
   notepad .env  # 或使用你喜欢的编辑器
   ```

2. **填入你的API密钥**
   
   编辑`.env`文件，填入实际的API密钥：
   ```
   # 使用OpenAI
   OPENAI_API_KEY=sk-your-actual-key-here
   LLM_PROVIDER=openai
   
   # 或使用通义千问
   DASHSCOPE_API_KEY=your-dashscope-key-here
   LLM_PROVIDER=dashscope
   ```

## 📦 安装额外依赖

如果需要安装其他依赖（如langchain、fastapi等）：

```powershell
# 激活环境
conda activate werewolf

# 安装完整依赖
pip install -r requirements.txt

# 或只安装特定包
pip install langchain langgraph fastapi
```

## 🔧 常用Conda命令

```powershell
# 查看所有环境
conda env list

# 查看当前环境已安装的包
conda list
# 或
pip list

# 更新包
pip install --upgrade openai

# 删除环境（如需重建）
conda env remove -n werewolf

# 导出环境配置
conda env export > environment.yml
```

## 💡 在VS Code中使用

1. 打开VS Code
2. 按 `Ctrl+Shift+P`，输入 "Python: Select Interpreter"
3. 选择：`C:\Users\30677\Miniconda3\envs\werewolf\python.exe`
4. 现在你可以直接运行和调试项目了

## 🐛 常见问题

### 问题1：conda命令不可用
**解决**：运行conda init后需要重启终端
```powershell
& "$env:USERPROFILE\Miniconda3\Scripts\conda.exe" init powershell
# 然后关闭并重新打开PowerShell
```

### 问题2：脚本执行策略错误
**解决**：允许PowerShell执行脚本
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 问题3：找不到模块
**解决**：确保环境已激活或使用完整路径
```powershell
# 方式1：激活环境
conda activate werewolf
python your_script.py

# 方式2：使用完整路径
& "$env:USERPROFILE\Miniconda3\envs\werewolf\python.exe" your_script.py
```

## 📚 下一步

1. ✅ 配置`.env`文件
2. ✅ 运行基础Demo测试环境
3. ✅ 开始开发AI狼人杀游戏！

查看 `README.md` 获取更多项目信息。
查看 `QUICK_START.md` 获取快速开始指南。

---

**环境配置时间**: 2025-11-03
**Conda版本**: 25.9.1
**Python版本**: 3.11.14

