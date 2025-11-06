"""
检测可用的 TTS 服务选项
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# 设置 Windows 控制台编码为 UTF-8
if sys.platform == 'win32':
    import locale
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass

load_dotenv()

print("=" * 60)
print("🔍 检测可用的 TTS 服务")
print("=" * 60)
print()

# 检查 API 密钥
print("1️⃣ 检查 API 密钥配置")
modelscope_key = os.getenv("OPENAI_API_KEY")
dashscope_key = os.getenv("DASHSCOPE_API_KEY")

if modelscope_key and dashscope_key:
    print(f"   ✅ ModelScope Token (LLM): {modelscope_key[:20]}...")
    print(f"   ✅ DashScope API Key (TTS): {dashscope_key[:20]}...")
    print("   💡 推荐配置：LLM用ModelScope，TTS用DashScope")
elif dashscope_key:
    print(f"   ✅ DashScope API Key: {dashscope_key[:20]}...")
    if dashscope_key.startswith("sk-"):
        print("   ✅ 正确的 DashScope Key 格式 (sk- 开头)")
elif modelscope_key:
    print(f"   ⚠️  ModelScope Token: {modelscope_key[:20]}...")
    if modelscope_key.startswith("ms-"):
        print("   ⚠️  ModelScope Token 不支持 DashScope TTS")
        print("   💡 请添加 DASHSCOPE_API_KEY 到 .env 文件")
        print("   获取地址: https://dashscope.console.aliyun.com/apiKey")
else:
    print("   ❌ 未找到 API 密钥")
    print("   请在 .env 文件中配置:")
    print("   - OPENAI_API_KEY (ModelScope, 用于LLM)")
    print("   - DASHSCOPE_API_KEY (DashScope, 用于TTS)")
print()

# 检查 dashscope 库
print("2️⃣ 检查 DashScope SDK")
try:
    import dashscope
    print("   ✅ dashscope 已安装")
    dashscope_available = True
except ImportError:
    print("   ❌ dashscope 未安装")
    print("   安装命令: pip install dashscope")
    dashscope_available = False
print()

# 检查 httpx 库
print("3️⃣ 检查 HTTP 客户端")
try:
    import httpx
    print("   ✅ httpx 已安装")
    httpx_available = True
except ImportError:
    print("   ❌ httpx 未安装")
    print("   安装命令: pip install httpx")
    httpx_available = False
print()

# 推荐方案
print("=" * 60)
print("📋 推荐方案")
print("=" * 60)
print()

if dashscope_available and dashscope_key:
    print("✨ 推荐使用: DashScope TTS")
    print()
    print("   优势:")
    print("   - ✅ 阿里云官方服务，稳定可靠")
    print("   - ✅ SDK 封装完善，易于使用")
    print("   - ✅ 支持多种音色")
    print("   - ✅ 响应速度快")
    print("   - ✅ 新模型 cosyvoice-v1 音质更好")
    print()
    print("   使用步骤:")
    print("   1. 确保 .env 中配置了 DASHSCOPE_API_KEY")
    print("   2. 运行: python test_dashscope_tts.py")
    print()
elif dashscope_available and modelscope_key and modelscope_key.startswith("ms-"):
    print("⚠️  需要配置 DashScope API Key")
    print()
    print("   当前状态:")
    print("   - ✅ 已安装 dashscope SDK")
    print("   - ⚠️  仅有 ModelScope Token (ms- 开头)")
    print("   - ❌ 缺少 DashScope API Key (sk- 开头)")
    print()
    print("   配置步骤:")
    print("   1. 访问: https://dashscope.console.aliyun.com/apiKey")
    print("   2. 获取 DashScope API Key (sk- 开头)")
    print("   3. 在 .env 中添加: DASHSCOPE_API_KEY=sk-xxxxx")
    print("   4. 运行: python test_dashscope_tts.py")
    print()
elif httpx_available and (modelscope_key or dashscope_key):
    print("⚠️ 可以尝试: ModelScope 推理 API")
    print()
    print("   说明:")
    print("   - 使用 ModelScope 的通用推理 API")
    print("   - 可能存在 API 端点兼容性问题")
    print("   - 建议安装 dashscope 使用官方服务")
    print()
    print("   使用步骤:")
    print("   1. 运行: python test_tts.py")
    print("   2. 如果失败，请安装 dashscope")
    print()
else:
    print("❌ 缺少必要的依赖")
    print()
    print("   请按以下步骤配置:")
    print()
    print("   1. 安装依赖:")
    print("      pip install dashscope httpx")
    print()
    print("   2. 配置 API 密钥:")
    print("      在 .env 文件中添加:")
    print("      OPENAI_API_KEY=你的密钥")
    print()

print("=" * 60)
print("💡 提示")
print("=" * 60)
print()
print("DashScope 音色选项:")
print()
print("新模型 (cosyvoice-v1) ⭐ 推荐:")
print("  女声: longxiaochun(温柔), longxiaoqing(亲切), longjing(甜美)")
print("  男声: longxiaohao(沉稳), longxiaojian(清朗)")
print("  儿童: longxiaobei(可爱)")
print()
print("旧模型 (sambert-zhichu-v1):")
print("  - zhixiaobai (智小白 - 女声)")
print("  - zhixiaoxia (智小夏 - 女声)")  
print("  - zhiyan (智妍 - 女声)")
print("  - zhibei (智贝 - 儿童)")
print("  - zhitian (智天 - 男声)")
print("  - zhigang (智刚 - 男声)")
print()
print("配置示例 (.env):")
print("  TTS_VOICE=longxiaochun  # 新模型音色")
print("  # 或")
print("  TTS_VOICE=zhixiaobai  # 旧模型音色")
print()

