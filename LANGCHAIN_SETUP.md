# 🦜 LangChain版本配置指南

## 📝 新版本特点

使用LangChain重构后的版本具有以下优势：

✅ **专业的Agent架构** - 基于LangChain的Agent框架  
✅ **更好的提示词管理** - 使用ChatPromptTemplate  
✅ **记忆功能** - 集成ConversationBufferMemory  
✅ **多LLM支持** - 轻松切换不同的LLM提供商  
✅ **兼容OpenAI接口** - ModelScope使用OpenAI兼容接口  
✅ **更好的错误处理** - 自动降级到fallback模式  

---

## 🔑 重要：获取ModelScope Access Token

### ⚠️ 注意区别

- **旧版API Key** (不再使用): `ms-xxx` 格式
- **新版Access Token** (推荐): 更长的字符串格式

### 获取Access Token的步骤

1. **访问ModelScope个人中心**
   ```
   https://modelscope.cn/my/myaccesstoken
   ```

2. **创建或查看Access Token**
   - 点击"创建令牌"或查看现有令牌
   - 复制完整的Access Token
   - ⚠️ 保密保存！不要分享或提交到Git

3. **Token示例格式**
   ```
   你的token应该类似这样的长字符串
   （不是 ms-xxx 格式）
   ```

---

## 🛠️ 配置方法

### 方法1：使用环境变量（推荐）

1. **创建.env文件**
   ```powershell
   cd E:\workspace\study\werewolf
   New-Item -ItemType File -Path .env -Force
   notepad .env
   ```

2. **在.env文件中添加**
   ```env
   # ModelScope配置（推荐）
   MODELSCOPE_ACCESS_TOKEN=your-access-token-here
   
   # 或使用OpenAI
   OPENAI_API_KEY=sk-your-openai-key-here
   ```

3. **运行游戏**
   ```powershell
   python werewolf_langchain.py
   ```

### 方法2：直接在代码中配置（快速测试）

编辑 `werewolf_langchain.py` 文件，找到第59-62行：

```python
@dataclass
class LLMConfig:
    """LLM配置"""
    provider: LLMProvider = LLMProvider.MODELSCOPE
    
    # ModelScope配置
    modelscope_token: str = "your-actual-token-here"  # 👈 填入你的token
```

---

## 🚀 快速开始

### 步骤1：激活Conda环境

```powershell
conda activate werewolf
cd E:\workspace\study\werewolf
```

### 步骤2：测试LLM连接

```powershell
python -c "from werewolf_langchain import LLMConfig, test_llm_connection; config = LLMConfig(); test_llm_connection(config)"
```

### 步骤3：运行游戏

```powershell
python werewolf_langchain.py
```

---

## 🎮 使用不同的LLM提供商

### 使用ModelScope（免费，推荐）

```python
from werewolf_langchain import WerewolfGame, LLMConfig, LLMProvider

config = LLMConfig(
    provider=LLMProvider.MODELSCOPE,
    modelscope_token="your-access-token",
    modelscope_model="Qwen/Qwen2.5-7B-Instruct"  # 可选其他模型
)

game = WerewolfGame(config)
game.play(max_rounds=3)
```

### 使用OpenAI

```python
config = LLMConfig(
    provider=LLMProvider.OPENAI,
    openai_api_key="sk-your-key",
    openai_model="gpt-4o-mini"  # 或 gpt-4
)

game = WerewolfGame(config)
game.play(max_rounds=3)
```

---

## 📦 可用的ModelScope模型

推荐使用以下模型（均兼容OpenAI接口）：

| 模型ID | 参数量 | 特点 | 推荐场景 |
|--------|--------|------|---------|
| `Qwen/Qwen2.5-7B-Instruct` | 7B | 平衡性能速度 | 游戏AI（推荐） |
| `Qwen/Qwen2.5-14B-Instruct` | 14B | 更强推理能力 | 复杂对话 |
| `Qwen/Qwen2.5-32B-Instruct` | 32B | 高级推理 | 专业应用 |
| `Qwen/Qwen2.5-Coder-32B-Instruct` | 32B | 编程特化 | 代码相关 |

更多模型：https://modelscope.cn/models

---

## 🔧 高级配置

### 自定义Agent行为

编辑 `werewolf_langchain.py` 中的Agent类：

```python
class WerewolfAgent:
    def _setup_prompts(self):
        # 修改系统提示词
        system_template = """你是一名经验丰富的狼人杀玩家。
        
【你的风格】
- 性格：冷静、善于分析
- 策略：逻辑推理为主
- 特点：{custom_trait}

{role_description}
"""
```

### 调整LLM参数

```python
config = LLMConfig(
    provider=LLMProvider.MODELSCOPE,
    temperature=0.9,      # 提高创造性 (0.0-1.0)
    max_tokens=800,       # 增加回复长度
)
```

### 添加更多轮次

```python
game.play(max_rounds=5)  # 运行5轮
```

---

## 🐛 问题排查

### 问题1：401 Unauthorized

**原因**: Access Token无效或过期

**解决**:
1. 访问 https://modelscope.cn/my/myaccesstoken
2. 创建新的Access Token
3. 更新.env文件或代码中的token
4. 确保使用的是Access Token，不是旧版API Key

### 问题2：Import Error

**原因**: LangChain未安装

**解决**:
```powershell
pip install langchain langchain-openai langchain-community
```

### 问题3：网络连接失败

**原因**: 无法访问ModelScope API

**解决**:
1. 检查网络连接
2. 如需代理，设置环境变量：
   ```powershell
   $env:HTTP_PROXY="http://proxy:port"
   $env:HTTPS_PROXY="http://proxy:port"
   ```
3. 或切换到OpenAI：
   ```python
   config = LLMConfig(provider=LLMProvider.OPENAI)
   ```

### 问题4：LLM响应慢

**原因**: 模型太大或网络慢

**解决**:
1. 使用更小的模型：
   ```python
   modelscope_model="Qwen/Qwen2.5-7B-Instruct"
   ```
2. 减少max_tokens：
   ```python
   max_tokens=200
   ```

---

## 💡 最佳实践

### 1. 环境变量管理

创建 `.env` 文件（推荐）：
```env
MODELSCOPE_ACCESS_TOKEN=your-token
OPENAI_API_KEY=your-key

# 可选配置
MODELSCOPE_MODEL=Qwen/Qwen2.5-7B-Instruct
LLM_TEMPERATURE=0.8
LLM_MAX_TOKENS=500
```

### 2. Git忽略敏感信息

确保 `.gitignore` 包含：
```gitignore
.env
*.env
*token*
*secret*
```

### 3. 错误处理

代码已包含自动降级：
- LLM调用失败 → 使用fallback回复
- 投票解析失败 → 随机选择
- 网络错误 → 显示友好提示

### 4. 成本控制

ModelScope免费额度有限，建议：
- 开发时使用较小模型
- 控制max_tokens数量
- 监控API使用量

---

## 📊 与旧版对比

| 特性 | 旧版 | LangChain版本 |
|------|------|--------------|
| Agent框架 | 自定义 | LangChain Agent |
| 提示词管理 | 字符串拼接 | ChatPromptTemplate |
| 记忆功能 | 简单列表 | ConversationBufferMemory |
| LLM切换 | 硬编码 | 配置化切换 |
| 错误处理 | 基础 | 完善的降级机制 |
| 代码组织 | 单文件 | 模块化设计 |
| 可扩展性 | 中等 | 高 |

---

## 🔗 相关资源

### 官方文档
- **ModelScope**: https://modelscope.cn/docs
- **ModelScope API**: https://www.modelscope.cn/docs/api-inference/intro
- **LangChain**: https://python.langchain.com/
- **LangChain ChatOpenAI**: https://python.langchain.com/docs/integrations/chat/openai

### 获取Token
- **ModelScope Access Token**: https://modelscope.cn/my/myaccesstoken
- **OpenAI API Key**: https://platform.openai.com/api-keys

### 社区
- **ModelScope社区**: https://modelscope.cn/community
- **LangChain GitHub**: https://github.com/langchain-ai/langchain

---

## 📝 快速命令参考

```powershell
# 激活环境
conda activate werewolf

# 进入项目目录
cd E:\workspace\study\werewolf

# 测试LLM连接
python -c "from werewolf_langchain import test_llm_connection, LLMConfig; test_llm_connection(LLMConfig())"

# 运行游戏
python werewolf_langchain.py

# 查看已安装包
pip list | Select-String "langchain|openai"

# 更新LangChain
pip install --upgrade langchain langchain-openai
```

---

**配置完成时间**: 2025-11-03  
**推荐配置**: ModelScope + Qwen2.5-7B-Instruct  
**需要帮助**: 查看 [MODELSCOPE_GUIDE.md](./MODELSCOPE_GUIDE.md)



