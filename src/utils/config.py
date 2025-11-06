"""
配置管理模块
采用 LangChain 规范，支持多种配置源

配置加载优先级：
1. 环境变量 (.env)  - 最高优先级
2. 配置文件 (config/default.json)  - 默认配置
"""

import os
from pathlib import Path
from typing import Optional, Dict, Any, List
from dotenv import load_dotenv
import json


class Config:
    """配置管理类"""
    
    def __init__(self, config_file: str = "default.json", load_env: bool = True):
        """
        初始化配置
        
        Args:
            config_file: 配置文件名（默认: default.json）
            load_env: 是否加载环境变量（默认: True）
        """
        self.project_root = Path(__file__).parent.parent.parent
        self.config_dir = self.project_root / "config"
        
        # 1. 加载环境变量（如果启用）
        if load_env:
            env_path = self.project_root / ".env"
            if env_path.exists():
                load_dotenv(env_path)
                print(f"✅ 已加载环境变量: {env_path}")
        
        # 2. 加载默认配置文件
        self._config = self._load_config_file(config_file)
        
        # 3. 使用环境变量覆盖配置
        self._override_from_env()
        
        print(f"✅ 配置初始化完成: LLM提供商={self.llm_provider}, TTS={self.tts_enabled}")
    
    def _load_config_file(self, config_file: str) -> Dict[str, Any]:
        """加载配置文件"""
        config_path = self.config_dir / config_file
        
        if not config_path.exists():
            print(f"⚠️ 配置文件不存在: {config_path}，使用默认配置")
            return self._get_default_config()
        
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                print(f"✅ 已加载配置文件: {config_path}")
                return config
        except Exception as e:
            print(f"❌ 加载配置文件失败: {e}，使用默认配置")
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """获取默认配置（作为后备）"""
        return {
            "game": {
                "num_players": 6,
                "language": "zh",
                "debug_mode": False,
                "max_rounds": 10
            },
            "llm": {
                "provider": "modelscope",
                "temperature": 0.8,
                "max_tokens": 500,
                "streaming": True,
                "providers": {}
            },
            "tts": {
                "enabled": True,
                "provider": "dashscope"
            },
            "web": {
                "host": "0.0.0.0",
                "port": 8000
            }
        }
    
    def _override_from_env(self):
        """使用环境变量覆盖配置"""
        
        # ============== 游戏配置 ==============
        if "GAME_NUM_PLAYERS" in os.environ:
            self._config.setdefault("game", {})["num_players"] = int(os.getenv("GAME_NUM_PLAYERS"))
        
        if "GAME_LANGUAGE" in os.environ:
            self._config.setdefault("game", {})["language"] = os.getenv("GAME_LANGUAGE")
        
        if "DEBUG_MODE" in os.environ:
            self._config.setdefault("game", {})["debug_mode"] = os.getenv("DEBUG_MODE", "false").lower() == "true"
        
        # ============== LLM配置 ==============
        if "LLM_PROVIDER" in os.environ:
            self._config.setdefault("llm", {})["provider"] = os.getenv("LLM_PROVIDER")
        
        if "LLM_TEMPERATURE" in os.environ:
            self._config.setdefault("llm", {})["temperature"] = float(os.getenv("LLM_TEMPERATURE"))
        
        if "LLM_MAX_TOKENS" in os.environ:
            self._config.setdefault("llm", {})["max_tokens"] = int(os.getenv("LLM_MAX_TOKENS"))
        
        # LLM提供商特定配置
        llm_providers = self._config.setdefault("llm", {}).setdefault("providers", {})
        
        # OpenAI
        if "OPENAI_API_KEY" in os.environ:
            openai_config = llm_providers.setdefault("openai", {})
            openai_config["api_key"] = os.getenv("OPENAI_API_KEY")
        
        if "OPENAI_API_BASE" in os.environ:
            llm_providers.setdefault("openai", {})["base_url"] = os.getenv("OPENAI_API_BASE")
        
        if "OPENAI_MODEL" in os.environ:
            llm_providers.setdefault("openai", {})["model"] = os.getenv("OPENAI_MODEL")
        
        # DashScope
        if "DASHSCOPE_API_KEY" in os.environ:
            dashscope_config = llm_providers.setdefault("dashscope", {})
            dashscope_config["api_key"] = os.getenv("DASHSCOPE_API_KEY")
        
        if "DASHSCOPE_MODEL" in os.environ:
            llm_providers.setdefault("dashscope", {})["model"] = os.getenv("DASHSCOPE_MODEL")
        
        # ModelScope
        if "MODELSCOPE_API_KEY" in os.environ:
            modelscope_config = llm_providers.setdefault("modelscope", {})
            modelscope_config["api_key"] = os.getenv("MODELSCOPE_API_KEY")
        
        if "MODELSCOPE_MODEL" in os.environ:
            llm_providers.setdefault("modelscope", {})["model"] = os.getenv("MODELSCOPE_MODEL")
        
        # 如果没有专门的 MODELSCOPE_API_KEY，尝试使用 OPENAI_API_KEY（兼容性）
        if "OPENAI_API_KEY" in os.environ and "modelscope" in llm_providers:
            if not llm_providers["modelscope"].get("api_key"):
                llm_providers["modelscope"]["api_key"] = os.getenv("OPENAI_API_KEY")
        
        # Anthropic
        if "ANTHROPIC_API_KEY" in os.environ:
            anthropic_config = llm_providers.setdefault("anthropic", {})
            anthropic_config["api_key"] = os.getenv("ANTHROPIC_API_KEY")
        
        # ============== TTS配置 ==============
        if "TTS_ENABLED" in os.environ:
            self._config.setdefault("tts", {})["enabled"] = os.getenv("TTS_ENABLED", "true").lower() == "true"
        
        if "TTS_PROVIDER" in os.environ:
            self._config.setdefault("tts", {})["provider"] = os.getenv("TTS_PROVIDER")
        
        tts_providers = self._config.setdefault("tts", {}).setdefault("providers", {})
        
        # DashScope TTS
        dashscope_tts = tts_providers.setdefault("dashscope", {})
        
        if "DASHSCOPE_API_KEY" in os.environ:
            dashscope_tts["api_key"] = os.getenv("DASHSCOPE_API_KEY")
        
        # 如果没有 DASHSCOPE_API_KEY，尝试使用 OPENAI_API_KEY（兼容性）
        if "OPENAI_API_KEY" in os.environ and not dashscope_tts.get("api_key"):
            dashscope_tts["api_key"] = os.getenv("OPENAI_API_KEY")
        
        if "TTS_MODEL" in os.environ:
            dashscope_tts["model"] = os.getenv("TTS_MODEL")
        
        if "TTS_VOICE" in os.environ:
            dashscope_tts["voice"] = os.getenv("TTS_VOICE")
        
        if "TTS_SPEED" in os.environ:
            dashscope_tts["speed"] = float(os.getenv("TTS_SPEED"))
        
        if "TTS_PITCH" in os.environ:
            dashscope_tts["pitch"] = float(os.getenv("TTS_PITCH"))
        
        # ============== Web配置 ==============
        if "WEB_HOST" in os.environ:
            self._config.setdefault("web", {})["host"] = os.getenv("WEB_HOST")
        
        if "WEB_PORT" in os.environ:
            self._config.setdefault("web", {})["port"] = int(os.getenv("WEB_PORT"))
        
        if "CORS_ORIGINS" in os.environ:
            origins = os.getenv("CORS_ORIGINS", "*").split(",")
            self._config.setdefault("web", {})["cors_origins"] = origins
        
        # ============== 数据库配置 ==============
        if "CACHE_ENABLED" in os.environ:
            self._config.setdefault("database", {})["cache_enabled"] = os.getenv("CACHE_ENABLED", "true").lower() == "true"
        
        if "CACHE_TTL" in os.environ:
            self._config.setdefault("database", {})["cache_ttl"] = int(os.getenv("CACHE_TTL"))
        
        # ============== 日志配置 ==============
        if "LOG_LEVEL" in os.environ:
            self._config.setdefault("logging", {})["level"] = os.getenv("LOG_LEVEL")
    
    # ==================== 属性访问方法 ====================
    
    @property
    def llm_provider(self) -> str:
        """获取LLM提供商"""
        return self._config.get("llm", {}).get("provider", "modelscope")
    
    @property
    def llm_temperature(self) -> float:
        """获取LLM温度"""
        return self._config.get("llm", {}).get("temperature", 0.8)
    
    @property
    def llm_max_tokens(self) -> int:
        """获取LLM最大tokens"""
        return self._config.get("llm", {}).get("max_tokens", 500)
    
    @property
    def llm_streaming(self) -> bool:
        """是否启用流式输出"""
        return self._config.get("llm", {}).get("streaming", True)
    
    @property
    def tts_enabled(self) -> bool:
        """是否启用TTS"""
        return self._config.get("tts", {}).get("enabled", True)
    
    @property
    def tts_provider(self) -> str:
        """获取TTS提供商"""
        return self._config.get("tts", {}).get("provider", "dashscope")
    
    @property
    def web_host(self) -> str:
        """获取Web服务器主机"""
        return self._config.get("web", {}).get("host", "0.0.0.0")
    
    @property
    def web_port(self) -> int:
        """获取Web服务器端口"""
        return self._config.get("web", {}).get("port", 8000)
    
    @property
    def web_cors_origins(self) -> List[str]:
        """获取CORS允许的源"""
        return self._config.get("web", {}).get("cors_origins", ["*"])
    
    @property
    def game_num_players(self) -> int:
        """获取游戏玩家数"""
        return self._config.get("game", {}).get("num_players", 6)
    
    @property
    def game_language(self) -> str:
        """获取游戏语言"""
        return self._config.get("game", {}).get("language", "zh")
    
    @property
    def debug_mode(self) -> bool:
        """是否为调试模式"""
        return self._config.get("game", {}).get("debug_mode", False)
    
    # ==================== 配置获取方法 ====================
    
    def get_llm_config(self, provider: Optional[str] = None) -> Dict[str, Any]:
        """
        获取LLM配置
        
        Args:
            provider: LLM提供商，如果为None则使用默认提供商
        
        Returns:
            LLM配置字典
        """
        provider = provider or self.llm_provider
        
        llm_config = self._config.get("llm", {})
        providers_config = llm_config.get("providers", {})
        provider_config = providers_config.get(provider, {})
        
        # 合并通用配置和提供商特定配置
        config = {
            "provider": provider,
            "temperature": llm_config.get("temperature", 0.8),
            "max_tokens": llm_config.get("max_tokens", 500),
            "streaming": llm_config.get("streaming", True),
        }
        
        # 添加提供商特定配置
        config.update(provider_config)
        
        return config
    
    def get_tts_config(self, provider: Optional[str] = None) -> Dict[str, Any]:
        """
        获取TTS配置
        
        Args:
            provider: TTS提供商，如果为None则使用默认提供商
        
        Returns:
            TTS配置字典
        """
        provider = provider or self.tts_provider
        
        tts_config = self._config.get("tts", {})
        providers_config = tts_config.get("providers", {})
        provider_config = providers_config.get(provider, {})
        
        config = {
            "provider": provider,
            "enabled": tts_config.get("enabled", True),
        }
        
        # 添加提供商特定配置
        config.update(provider_config)
        
        return config
    
    def get_game_config(self) -> Dict[str, Any]:
        """获取游戏配置"""
        return self._config.get("game", {})
    
    def get_web_config(self) -> Dict[str, Any]:
        """获取Web配置"""
        return self._config.get("web", {})
    
    def get_database_config(self) -> Dict[str, Any]:
        """获取数据库配置"""
        return self._config.get("database", {})
    
    def get_logging_config(self) -> Dict[str, Any]:
        """获取日志配置"""
        return self._config.get("logging", {})
    
    # ==================== 工具方法 ====================
    
    def validate(self) -> bool:
        """
        验证配置
        
        Returns:
            配置是否有效
        """
        errors = []
        
        # 验证LLM配置
        llm_config = self.get_llm_config()
        if not llm_config.get("api_key"):
            errors.append(f"LLM提供商 {self.llm_provider} 缺少 API Key")
        
        # 验证TTS配置（如果启用）
        if self.tts_enabled:
            tts_config = self.get_tts_config()
            if not tts_config.get("api_key"):
                errors.append(f"TTS提供商 {self.tts_provider} 缺少 API Key")
        
        if errors:
            print("\n⚠️ 配置验证失败：")
            for error in errors:
                print(f"  - {error}")
            return False
        
        print("✅ 配置验证通过")
        return True
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return self._config.copy()
    
    def save_to_file(self, config_file: str):
        """
        保存配置到文件
        
        Args:
            config_file: 配置文件名
        """
        self.config_dir.mkdir(parents=True, exist_ok=True)
        config_path = self.config_dir / config_file
        
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(self._config, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 配置已保存到: {config_path}")
    
    def __repr__(self) -> str:
        """字符串表示"""
        return f"Config(provider={self.llm_provider}, tts_enabled={self.tts_enabled})"


# ==================== 全局配置实例 ====================

_config_instance: Optional[Config] = None


def get_config(reload: bool = False) -> Config:
    """
    获取全局配置实例（单例模式）
    
    Args:
        reload: 是否重新加载配置
    
    Returns:
        Config实例
    """
    global _config_instance
    
    if _config_instance is None or reload:
        _config_instance = Config()
    
    return _config_instance


def reload_config() -> Config:
    """重新加载配置"""
    return get_config(reload=True)


# ==================== 兼容性属性（用于旧代码） ====================

def _get_legacy_attr(attr_name: str) -> Any:
    """获取旧版本的属性（用于向后兼容）"""
    config = get_config()
    
    # 映射旧属性名到新属性
    attr_map = {
        "modelscope_token": lambda: config.get_llm_config("modelscope").get("api_key", ""),
        "modelscope_model": lambda: config.get_llm_config("modelscope").get("model", ""),
        "modelscope_base_url": lambda: config.get_llm_config("modelscope").get("base_url", ""),
        "openai_api_key": lambda: config.get_llm_config("openai").get("api_key", ""),
        "openai_model": lambda: config.get_llm_config("openai").get("model", ""),
        "dashscope_api_key": lambda: config.get_tts_config("dashscope").get("api_key", ""),
        "tts_model": lambda: config.get_tts_config().get("model", ""),
        "tts_voice": lambda: config.get_tts_config().get("voice", ""),
        "tts_speed": lambda: config.get_tts_config().get("speed", 1.0),
        "tts_pitch": lambda: config.get_tts_config().get("pitch", 1.0),
    }
    
    if attr_name in attr_map:
        return attr_map[attr_name]()
    
    return getattr(config, attr_name, None)
