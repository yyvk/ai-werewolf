"""
测试 DashScope TTS 语音合成功能
推荐使用这个版本，更稳定可靠
"""

import asyncio
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# 设置 Windows 控制台编码为 UTF-8
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass

# 加载环境变量
load_dotenv()

print()
print("=" * 60)
print("🔊 测试 DashScope TTS 功能")
print("=" * 60)
print()

# 检查依赖
try:
    import dashscope
    from dashscope.audio.tts import SpeechSynthesizer
except ImportError:
    print("❌ 错误: dashscope 未安装")
    print()
    print("请运行以下命令安装:")
    print("  pip install dashscope")
    print()
    exit(1)

# 检查 API 密钥（优先使用 DASHSCOPE_API_KEY）
api_key = os.getenv("DASHSCOPE_API_KEY") or os.getenv("OPENAI_API_KEY")
if not api_key:
    print("❌ 错误: 未找到 API 密钥")
    print()
    print("请在 .env 文件中配置:")
    print("  DASHSCOPE_API_KEY=你的DashScope密钥")
    print("  （或 OPENAI_API_KEY 如果同时用于LLM和TTS）")
    print()
    exit(1)

# 检测密钥类型
key_type = "DashScope" if api_key.startswith("sk-") else "ModelScope"
if key_type == "ModelScope":
    print("⚠️  警告: 检测到 ModelScope token")
    print("   DashScope TTS 需要 DashScope API Key (sk- 开头)")
    print("   获取地址: https://dashscope.console.aliyun.com/apiKey")
    print()
    print("   如果你的 LLM 用 ModelScope，TTS 用 DashScope：")
    print("   请在 .env 中添加: DASHSCOPE_API_KEY=sk-xxxxx")
    print()

print(f"✅ API 密钥已配置: {api_key[:20]}... ({key_type})")
dashscope.api_key = api_key
print()

# 音频输出目录
output_dir = Path(__file__).parent / "assets" / "audio"
output_dir.mkdir(parents=True, exist_ok=True)

# 测试音色
voice = os.getenv("TTS_VOICE", "zhixiaobai")
print(f"🎤 使用音色: {voice}")
print()

# 测试文本
test_texts = [
    "大家好，我是玩家1号。",
    "根据目前的局势，我认为2号玩家的发言比较可疑。",
    "我投票给2号玩家。"
]

print("📝 开始测试语音生成...")
print()

success_count = 0
for i, text in enumerate(test_texts, 1):
    print(f"--- 测试 {i} ---")
    print(f"文本: {text}")
    
    try:
        # 生成文件名
        file_name = f"speech_test_{i}.wav"
        file_path = output_dir / file_name
        
        # 调用 DashScope TTS API
        result = SpeechSynthesizer.call(
            model='qwen3-tts-flash-realtime',
            text=text,
            sample_rate=22050,
            format='wav',
            voice=voice
        )
        
        # 调试：打印result类型和属性
        print(f"调试: result类型 = {type(result)}")
        print(f"调试: 状态码 = {result.get_response().status_code if hasattr(result, 'get_response') else 'N/A'}")
        
        # 检查是否有音频数据
        audio_data = result.get_audio_data()
        if audio_data is not None:
            with open(file_path, 'wb') as f:
                f.write(audio_data)
            
            file_size = file_path.stat().st_size
            print(f"✅ 语音生成成功!")
            print(f"📁 文件路径: {file_path}")
            print(f"📊 文件大小: {file_size} bytes")
            success_count += 1
        else:
            print(f"❌ 语音生成失败")
            # 打印详细的响应信息
            try:
                response = result.get_response()
                print(f"错误信息: {response}")
                if hasattr(response, 'status_code'):
                    print(f"状态码: {response.status_code}")
                if hasattr(response, 'message'):
                    print(f"消息: {response.message}")
            except Exception as err:
                print(f"无法获取错误详情: {err}")
    
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        print(f"详细错误:\n{traceback.format_exc()}")
    
    print()

print("=" * 60)
if success_count == len(test_texts):
    print(f"✅ 所有测试通过! ({success_count}/{len(test_texts)})")
    print()
    print("🎉 DashScope TTS 配置成功!")
    print()
    print("下一步:")
    print("  1. 在游戏中使用 DashScope TTS")
    print("  2. 运行: python main.py --mode web")
    print("  3. 启动前端: cd frontend && npm run dev")
else:
    print(f"⚠️ 部分测试失败 ({success_count}/{len(test_texts)})")
    print()
    print("请检查:")
    print("  - API 密钥是否正确")
    print("  - 网络连接是否正常")
    print("  - DashScope 服务是否可用")
print("=" * 60)
print()

