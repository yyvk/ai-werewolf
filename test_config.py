"""
测试新的配置系统
验证配置加载和LLM/TTS创建
"""

import sys
import os
from pathlib import Path

# 设置标准输出编码为 UTF-8（解决 Windows GBK 编码问题）
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
    os.environ['PYTHONIOENCODING'] = 'utf-8'

# 添加src到路径
sys.path.insert(0, str(Path(__file__).parent))


def test_config_loading():
    """测试配置加载"""
    print("\n" + "="*60)
    print("测试1: 配置加载")
    print("="*60)
    
    from src.utils.config import get_config
    
    config = get_config()
    
    print(f"\n✅ 配置加载成功")
    print(f"  LLM提供商: {config.llm_provider}")
    print(f"  LLM温度: {config.llm_temperature}")
    print(f"  LLM最大tokens: {config.llm_max_tokens}")
    print(f"  TTS启用: {config.tts_enabled}")
    print(f"  TTS提供商: {config.tts_provider}")
    print(f"  Web主机: {config.web_host}")
    print(f"  Web端口: {config.web_port}")
    
    return config


def test_llm_config():
    """测试LLM配置获取"""
    print("\n" + "="*60)
    print("测试2: LLM配置")
    print("="*60)
    
    from src.utils.config import get_config
    
    config = get_config()
    
    # 测试不同提供商的配置
    for provider in ["openai", "dashscope", "modelscope"]:
        try:
            llm_config = config.get_llm_config(provider)
            print(f"\n✅ {provider} 配置:")
            print(f"  模型: {llm_config.get('model', 'N/A')}")
            print(f"  API Key: {'已配置' if llm_config.get('api_key') else '未配置'}")
            print(f"  Base URL: {llm_config.get('base_url', 'N/A')}")
        except Exception as e:
            print(f"\n⚠️ {provider} 配置获取失败: {e}")


def test_tts_config():
    """测试TTS配置获取"""
    print("\n" + "="*60)
    print("测试3: TTS配置")
    print("="*60)
    
    from src.utils.config import get_config
    
    config = get_config()
    
    tts_config = config.get_tts_config()
    print(f"\n✅ TTS配置:")
    print(f"  提供商: {tts_config.get('provider', 'N/A')}")
    print(f"  模型: {tts_config.get('model', 'N/A')}")
    print(f"  音色: {tts_config.get('voice', 'N/A')}")
    print(f"  语速: {tts_config.get('speed', 'N/A')}")
    print(f"  音高: {tts_config.get('pitch', 'N/A')}")
    print(f"  API Key: {'已配置' if tts_config.get('api_key') else '未配置'}")


def test_llm_creation():
    """测试LLM创建"""
    print("\n" + "="*60)
    print("测试4: LLM实例创建")
    print("="*60)
    
    try:
        from src.agents.agent_factory import LLMFactory
        from src.utils.config import get_config
        
        config = get_config()
        provider = config.llm_provider
        
        print(f"\n尝试创建 {provider} LLM实例...")
        llm = LLMFactory.create_llm(provider)
        
        print(f"✅ LLM实例创建成功")
        print(f"  类型: {type(llm).__name__}")
        
        return llm
    
    except Exception as e:
        print(f"❌ LLM实例创建失败: {e}")
        import traceback
        traceback.print_exc()
        return None


def test_tts_creation():
    """测试TTS创建"""
    print("\n" + "="*60)
    print("测试5: TTS实例创建")
    print("="*60)
    
    try:
        from src.utils.tts_service_dashscope import get_dashscope_tts_service
        
        print(f"\n尝试创建 DashScope TTS实例...")
        tts = get_dashscope_tts_service()
        
        print(f"✅ TTS实例创建成功")
        print(f"  配置: {tts.get_config()}")
        
        return tts
    
    except Exception as e:
        print(f"❌ TTS实例创建失败: {e}")
        import traceback
        traceback.print_exc()
        return None


def test_config_validation():
    """测试配置验证"""
    print("\n" + "="*60)
    print("测试6: 配置验证")
    print("="*60)
    
    from src.utils.config import get_config
    
    config = get_config()
    is_valid = config.validate()
    
    if is_valid:
        print("\n✅ 配置验证通过 - 所有必需的API Key都已配置")
    else:
        print("\n⚠️ 配置验证失败 - 请检查API Key配置")


def test_agent_creation():
    """测试Agent创建"""
    print("\n" + "="*60)
    print("测试7: Agent实例创建")
    print("="*60)
    
    try:
        from src.agents.agent_factory import AgentFactory
        from src.core.models import Player, Role
        
        # 创建一个测试玩家
        player = Player(
            id=1,
            name="测试玩家",
            role=Role.VILLAGER
        )
        
        print(f"\n尝试创建Agent...")
        agent = AgentFactory.create_agent(player)
        
        print(f"✅ Agent实例创建成功")
        print(f"  玩家: {agent.player.name}")
        print(f"  角色: {agent.player.role_name_cn}")
        print(f"  启用记忆: {agent.enable_memory}")
        
        return agent
    
    except Exception as e:
        print(f"❌ Agent实例创建失败: {e}")
        import traceback
        traceback.print_exc()
        return None


def main():
    """运行所有测试"""
    print("\n" + "="*60)
    print("🚀 AI狼人杀 - 配置系统测试")
    print("="*60)
    
    try:
        # 测试1: 配置加载
        config = test_config_loading()
        
        # 测试2: LLM配置
        test_llm_config()
        
        # 测试3: TTS配置
        test_tts_config()
        
        # 测试4: LLM创建
        llm = test_llm_creation()
        
        # 测试5: TTS创建
        tts = test_tts_creation()
        
        # 测试6: 配置验证
        test_config_validation()
        
        # 测试7: Agent创建
        agent = test_agent_creation()
        
        # 总结
        print("\n" + "="*60)
        print("📊 测试总结")
        print("="*60)
        
        results = {
            "配置加载": config is not None,
            "LLM创建": llm is not None,
            "TTS创建": tts is not None,
            "Agent创建": agent is not None
        }
        
        for test_name, success in results.items():
            status = "✅ 通过" if success else "❌ 失败"
            print(f"  {test_name}: {status}")
        
        all_passed = all(results.values())
        
        if all_passed:
            print("\n🎉 所有测试通过！配置系统工作正常。")
        else:
            print("\n⚠️ 部分测试失败，请检查配置和API Key。")
        
        print("\n提示：")
        print("  1. 确保 .env 文件存在并配置了正确的API Key")
        print("  2. 检查 config/default.json 中的默认配置")
        print("  3. 运行 'python main.py' 启动游戏服务")
        print("="*60 + "\n")
    
    except Exception as e:
        print(f"\n❌ 测试过程出错: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

