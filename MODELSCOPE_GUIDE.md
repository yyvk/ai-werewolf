# 🚀 ModelScope API使用指南

## 📝 ModelScope配置说明

**如何获取API Key**:
1. 访问 https://modelscope.cn/my/myaccesstoken
2. 登录ModelScope账号
3. 创建访问令牌
4. 复制生成的Access Token

**API Key格式**: `your-modelscope-access-token`

## 🔧 配置方法

### 方法1：直接在代码中使用

在代码中直接指定API Key：

```python
from werewolf_with_modelscope import ModelScopeLLM

llm = ModelScopeLLM(
    api_key="your-modelscope-access-token",
    model="qwen-turbo"
)
```

### 方法2：使用环境变量（推荐生产环境）

1. **创建.env文件**（如果还没有）：
   ```powershell
   cd E:\workspace\study\werewolf
   Copy-Item modelscope_config.txt .env
   ```

2. **.env文件内容**：
   ```
   MODELSCOPE_API_KEY=your-modelscope-access-token
   MODELSCOPE_MODEL=qwen-turbo
   ```

3. **代码中加载**：
   ```python
   from dotenv import load_dotenv
   load_dotenv()  # 加载.env文件
   
   from werewolf_with_modelscope import ModelScopeLLM
   llm = ModelScopeLLM()  # 自动从环境变量读取
   ```

## 🎯 可用的模型

ModelScope平台支持多个通义千问模型：

| 模型名称 | 特点 | 推荐场景 |
|---------|------|---------|
| `qwen-turbo` | 快速响应，成本低 | 日常对话、游戏AI |
| `qwen-plus` | 平衡性能和速度 | 复杂推理任务 |
| `qwen-max` | 最强性能 | 需要最佳效果时 |
| `qwen2.5-72b-instruct` | 大模型 | 专业级应用 |

## 📖 基础使用示例

### 示例1：简单对话

```python
from werewolf_with_modelscope import ModelScopeLLM

# 初始化（使用你自己的API Key）
llm = ModelScopeLLM(
    api_key="your-modelscope-access-token",
    model="qwen-turbo"
)

# 生成回复
response = llm.generate("你好，请介绍一下狼人杀游戏的规则。")
print(response)
```

### 示例2：运行完整游戏

```python
from werewolf_with_modelscope import WerewolfGame, ModelScopeLLM

# 初始化LLM
llm = ModelScopeLLM()

# 创建游戏
game = WerewolfGame(llm)

# 运行游戏（3轮演示）
game.play(max_rounds=3)
```

## 🐛 问题排查

### 问题1：网络连接失败

**症状**: ConnectionError, ConnectionResetError

**可能原因**:
1. 网络防火墙阻止连接
2. 需要代理访问
3. API服务暂时不可用

**解决方法**:

#### A. 检查网络连接
```powershell
ping dashscope.aliyuncs.com
```

#### B. 配置代理（如果需要）
```python
import os
os.environ['HTTP_PROXY'] = 'http://your-proxy:port'
os.environ['HTTPS_PROXY'] = 'http://your-proxy:port'
```

或在命令行设置：
```powershell
$env:HTTP_PROXY="http://your-proxy:port"
$env:HTTPS_PROXY="http://your-proxy:port"
```

#### C. 使用模拟模式
如果API暂时无法连接，代码会自动切换到模拟模式继续运行。

### 问题2：API Key无效

**症状**: 401 Unauthorized

**解决方法**:
1. 确认API Key正确
2. 检查API Key是否已激活
3. 访问 https://www.modelscope.cn/my/myapikey 确认状态

### 问题3：模型不支持

**症状**: Model not found

**解决方法**:
更换为支持的模型：
```python
llm = ModelScopeLLM(model="qwen-turbo")  # 或 qwen-plus, qwen-max
```

## 🎮 运行狼人杀游戏

### 完整流程

1. **确保环境已激活**：
   ```powershell
   conda activate werewolf
   ```

2. **运行游戏**：
   ```powershell
   cd E:\workspace\study\werewolf
   python werewolf_with_modelscope.py
   ```

3. **游戏流程**：
   - ✅ 自动分配6名AI玩家角色
   - ✅ 每轮进行讨论和投票
   - ✅ AI根据角色进行策略性发言
   - ✅ 自动判断胜负

### 自定义游戏

编辑 `werewolf_with_modelscope.py` 文件：

```python
# 修改游戏轮数
game.play(max_rounds=5)  # 运行5轮

# 修改玩家数量（需要同时修改角色配置）
game.setup_game(num_players=8)

# 修改模型参数
llm.generate(prompt, temperature=0.9, max_tokens=500)
```

## 💡 高级技巧

### 1. 调整AI创造性

```python
# 更保守的AI（temperature更低）
response = llm.generate(prompt, temperature=0.5)

# 更有创意的AI（temperature更高）
response = llm.generate(prompt, temperature=1.0)
```

### 2. 控制回复长度

```python
# 简短回复
response = llm.generate(prompt, max_tokens=100)

# 详细回复
response = llm.generate(prompt, max_tokens=800)
```

### 3. 添加系统提示词

修改代码中的prompt，加入更详细的角色设定：

```python
prompt = f"""
你是一位经验丰富的狼人杀玩家。

【角色设定】
- 性格：谨慎、善于分析
- 风格：逻辑推理为主，情感为辅
- 策略：{role_strategy}

{game_context}

请基于以上信息进行发言。
"""
```

## 📊 API使用限制

ModelScope免费API的限制（请以官方为准）：
- **QPM**: 每分钟请求次数限制
- **QPS**: 每秒请求次数限制
- **Token限制**: 单次请求的最大token数

建议：
- 游戏中添加适当延迟，避免触发限流
- 监控API调用频率
- 准备降级方案（模拟模式）

## 🔗 相关链接

- ModelScope官网：https://www.modelscope.cn/
- API文档：https://www.modelscope.cn/docs
- 我的API Keys：https://www.modelscope.cn/my/myapikey
- DashScope文档：https://help.aliyun.com/zh/dashscope/

## ⚠️ 注意事项

1. **不要将API Key提交到Git仓库**
   - 使用 `.env` 文件存储
   - 确保 `.env` 在 `.gitignore` 中

2. **监控API使用量**
   - 定期检查用量
   - 避免超出限额

3. **错误处理**
   - 代码已包含自动降级到模拟模式
   - 生产环境建议增加重试机制

## 🚀 快速测试命令

测试API连接（简单版）：
```powershell
cd E:\workspace\study\werewolf
& "$env:USERPROFILE\Miniconda3\envs\werewolf\python.exe" -c "from werewolf_with_modelscope import test_modelscope_api; test_modelscope_api()"
```

运行完整游戏：
```powershell
& "$env:USERPROFILE\Miniconda3\envs\werewolf\python.exe" werewolf_with_modelscope.py
```

---

**配置完成时间**: 2025-11-03
**推荐模型**: qwen-turbo

**安全提醒**：请使用你自己的ModelScope Access Token，不要使用示例中的占位符

