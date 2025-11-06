"""
测试 TTS 语音合成功能
"""

import asyncio
import os
from pathlib import Path
from dotenv import load_dotenv
from src.utils.tts_service import TTSService

# 加载环境变量
load_dotenv()


async def test_tts_basic():
    """测试基本的 TTS 功能"""
    print("=" * 60)
    print("🔊 测试 TTS 基本功能")
    print("=" * 60)
    
    # 检查 DashScope API 密钥
    api_key = os.getenv("DASHSCOPE_API_KEY") or os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ 错误: 未找到 DashScope API 密钥")
        print()
        print("💡 请在 .env 文件中配置:")
        print("   DASHSCOPE_API_KEY=sk-your-api-key-here")
        print()
        print("获取地址: https://dashscope.console.aliyun.com/apiKey")
        return False
    
    key_source = "DASHSCOPE_API_KEY" if os.getenv("DASHSCOPE_API_KEY") else "OPENAI_API_KEY"
    print(f"✅ API 密钥已配置 (来源: {key_source}): {api_key[:20]}...")
    
    # 创建 TTS 服务
    tts_service = TTSService()
    
    # 测试文本
    test_texts = [
        "大家好，我是玩家1号。",
        "根据目前的局势，我认为2号玩家的发言比较可疑。",
        "我投票给2号玩家。"
    ]
    
    print("\n📝 开始测试语音生成...")
    
    for i, text in enumerate(test_texts, 1):
        print(f"\n--- 测试 {i} ---")
        print(f"文本: {text}")
        
        try:
            audio_path = await tts_service.text_to_speech(text, player_id=i)
            
            if audio_path:
                print(f"✅ 语音生成成功!")
                print(f"📁 文件路径: {audio_path}")
                
                # 检查文件是否存在
                if Path(audio_path).exists():
                    file_size = Path(audio_path).stat().st_size
                    print(f"📊 文件大小: {file_size} bytes")
                else:
                    print(f"⚠️ 警告: 文件不存在: {audio_path}")
            else:
                print(f"❌ 语音生成失败")
                return False
                
        except Exception as e:
            print(f"❌ 测试失败: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    print("\n" + "=" * 60)
    print("✅ 所有测试通过！")
    print("=" * 60)
    return True


async def test_tts_with_different_voices():
    """测试不同音色"""
    print("\n" + "=" * 60)
    print("🎨 测试不同音色")
    print("=" * 60)
    
    voices = ["zhitian_emo", "aiya", "xiaogang"]
    test_text = "我是狼人杀游戏中的一名玩家。"
    
    for voice in voices:
        print(f"\n🎤 测试音色: {voice}")
        tts_service = TTSService(voice=voice)
        
        try:
            audio_path = await tts_service.text_to_speech(test_text, player_id=99)
            if audio_path:
                print(f"✅ 音色 {voice} 测试成功")
            else:
                print(f"⚠️ 音色 {voice} 生成失败（可能该模型不支持此音色）")
        except Exception as e:
            print(f"❌ 音色 {voice} 测试失败: {e}")


async def test_tts_long_text():
    """测试长文本语音生成"""
    print("\n" + "=" * 60)
    print("📄 测试长文本语音生成")
    print("=" * 60)
    
    long_text = """
    大家好，我是玩家3号。
    根据目前的局势分析，我观察到以下几点：
    第一，玩家1号的发言非常可疑，他一直在试图转移话题。
    第二，玩家2号虽然看起来很积极，但逻辑链条不够严密。
    第三，玩家4号一直保持沉默，这也是一个值得注意的点。
    综合以上分析，我这一轮投票给玩家1号。
    """.strip()
    
    print(f"文本长度: {len(long_text)} 字符")
    print(f"文本内容:\n{long_text}\n")
    
    tts_service = TTSService()
    
    try:
        audio_path = await tts_service.text_to_speech(long_text, player_id=3)
        if audio_path:
            print(f"✅ 长文本语音生成成功!")
            print(f"📁 文件路径: {audio_path}")
            file_size = Path(audio_path).stat().st_size
            print(f"📊 文件大小: {file_size} bytes")
        else:
            print(f"❌ 长文本语音生成失败")
    except Exception as e:
        print(f"❌ 测试失败: {e}")


async def main():
    """主测试函数"""
    # 设置 UTF-8 编码以支持 emoji
    import sys
    if sys.platform == 'win32':
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    print("\n")
    print("🎮 " + "=" * 56 + " 🎮")
    print("     AI 狼人杀 - TTS 语音合成功能测试")
    print("🎮 " + "=" * 56 + " 🎮")
    print()
    
    # 测试基本功能
    success = await test_tts_basic()
    
    if not success:
        print("\n❌ 基本功能测试失败，跳过后续测试")
        return
    
    # 测试不同音色（可选）
    try:
        await test_tts_with_different_voices()
    except Exception as e:
        print(f"⚠️ 音色测试跳过: {e}")
    
    # 测试长文本（可选）
    try:
        await test_tts_long_text()
    except Exception as e:
        print(f"⚠️ 长文本测试跳过: {e}")
    
    # 显示生成的音频文件
    print("\n" + "=" * 60)
    print("📁 生成的音频文件:")
    print("=" * 60)
    
    audio_dir = Path(__file__).parent / "assets" / "audio"
    if audio_dir.exists():
        audio_files = list(audio_dir.glob("*.wav"))
        if audio_files:
            print(f"\n找到 {len(audio_files)} 个音频文件:")
            for i, file in enumerate(audio_files[-10:], 1):  # 只显示最后10个
                size = file.stat().st_size
                print(f"{i}. {file.name} ({size} bytes)")
        else:
            print("⚠️ 音频目录为空")
    else:
        print(f"⚠️ 音频目录不存在: {audio_dir}")
    
    print("\n" + "=" * 60)
    print("✨ 测试完成!")
    print("=" * 60)
    print("\n💡 提示:")
    print("   1. 如果测试成功，可以启动 Web 游戏体验完整功能")
    print("   2. 生成的音频文件保存在 assets/audio/ 目录")
    print("   3. 可以在浏览器中播放这些音频文件进行验证")
    print()


if __name__ == "__main__":
    asyncio.run(main())

