"""
配置管理
统一管理项目配置
"""

import os
from pathlib import Path
from typing import Optional, Dict, Any
from dotenv import load_dotenv
import json


class Config:
    """配置管理类"""
    
    def __init__(self, config_file: Optional[str] = None):
        """初始化配置"""
        load_dotenv()
        
        self.project_root = Path(__file__).parent.parent.parent
        self.config_dir = self.project_root / "config"
        
        if config_file:
            self.load_from_file(config_file)
        else:
            self._init_default_config()
    
    def _init_default_config(self):
        """初始化默认配置"""
        
        # LLM配置
        self.llm_provider = os.getenv("LLM_PROVIDER", "modelscope")
        
        # ModelScope 对话模型配置
        self.modelscope_token = os.getenv("MODELSCOPE_API_KEY") or os.getenv("OPENAI_API_KEY", "")
        self.modelscope_model = os.getenv("MODELSCOPE_MODEL") or os.getenv("OPENAI_MODEL", "Qwen/Qwen2.5-7B-Instruct")
        self.modelscope_base_url = os.getenv("OPENAI_API_BASE", "https://api-inference.modelscope.cn/v1/")
        
        # OpenAI配置（如果使用 OpenAI）
        self.openai_api_key = os.getenv("OPENAI_API_KEY", "")
        self.openai_model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        
        # DashScope TTS 配置（独立配置）
        self.dashscope_api_key = os.getenv("DASHSCOPE_API_KEY", "")
        
        # LLM通用参数
        self.llm_temperature = float(os.getenv("LLM_TEMPERATURE", "0.8"))
        self.llm_max_tokens = int(os.getenv("LLM_MAX_TOKENS", "500"))
        
        # 游戏配置
        self.game_max_rounds = 10
        self.game_num_players = 6
        self.game_enable_special_roles = True
        
        # 数据库配置
        self.db_vector_path = str(self.project_root / "data" / "vector_db")
        self.db_cache_path = str(self.project_root / "data" / "cache")
        self.db_cache_ttl = 3600
        
        # Web服务配置
        self.web_host = os.getenv("WEB_HOST", "0.0.0.0")
        self.web_port = int(os.getenv("WEB_PORT", "8000"))
        self.web_cors_origins = ["*"]
        
        # 视频生成配置
        self.video_output_dir = str(self.project_root / "output" / "videos")
        self.video_fps = 30
        self.video_resolution = (1920, 1080)
        self.video_quality = "high"
        
        # 日志配置
        self.log_level = os.getenv("LOG_LEVEL", "INFO")
        self.log_dir = str(self.project_root / "data" / "logs")
        self.log_file = "werewolf.log"
        
        # TTS 语音合成配置
        self.tts_enabled = os.getenv("TTS_ENABLED", "true").lower() == "true"
        self.tts_model = os.getenv("TTS_MODEL", "iic/speech_sambert-hifigan_tts_zh-cn_16k")
        self.tts_voice = os.getenv("TTS_VOICE", "zhitian_emo")
        self.tts_speed = float(os.getenv("TTS_SPEED", "1.0"))
        self.tts_pitch = float(os.getenv("TTS_PITCH", "1.0"))
    
    def load_from_file(self, config_file: str):
        """从文件加载配置"""
        config_path = self.config_dir / config_file
        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
                self._update_from_dict(config_data)
    
    def _update_from_dict(self, config_dict: Dict[str, Any]):
        """从字典更新配置"""
        for key, value in config_dict.items():
            # 处理嵌套的 TTS 配置
            if key == 'tts' and isinstance(value, dict):
                if 'enabled' in value:
                    self.tts_enabled = value['enabled']
                if 'model' in value:
                    self.tts_model = value['model']
                if 'voice' in value:
                    self.tts_voice = value['voice']
                if 'speed' in value:
                    self.tts_speed = value['speed']
                if 'pitch' in value:
                    self.tts_pitch = value['pitch']
            elif hasattr(self, key):
                setattr(self, key, value)
    
    def save_to_file(self, config_file: str):
        """保存配置到文件"""
        self.config_dir.mkdir(parents=True, exist_ok=True)
        config_path = self.config_dir / config_file
        
        config_data = {
            key: value for key, value in self.__dict__.items()
            if not key.startswith('_') and key not in ['project_root', 'config_dir']
        }
        
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config_data, f, ensure_ascii=False, indent=2)
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            key: value for key, value in self.__dict__.items()
            if not key.startswith('_')
        }
    
    def get_llm_config(self) -> Dict:
        """获取LLM配置"""
        if self.llm_provider == "modelscope":
            return {
                "provider": "modelscope",
                "api_key": self.modelscope_token,
                "base_url": self.modelscope_base_url,
                "model": self.modelscope_model,
                "temperature": self.llm_temperature,
                "max_tokens": self.llm_max_tokens
            }
        elif self.llm_provider == "openai":
            return {
                "provider": "openai",
                "api_key": self.openai_api_key,
                "model": self.openai_model,
                "temperature": self.llm_temperature,
                "max_tokens": self.llm_max_tokens
            }
        else:
            raise ValueError(f"Unsupported LLM provider: {self.llm_provider}")
    
    def validate(self) -> bool:
        """验证配置"""
        if self.llm_provider == "modelscope" and not self.modelscope_token:
            print("⚠️  Warning: ModelScope token not configured")
            return False
        
        if self.llm_provider == "openai" and not self.openai_api_key:
            print("⚠️  Warning: OpenAI API key not configured")
            return False
        
        return True


# 全局配置实例
_config_instance = None


def get_config() -> Config:
    """获取全局配置实例"""
    global _config_instance
    if _config_instance is None:
        _config_instance = Config()
    return _config_instance


def reload_config():
    """重新加载配置"""
    global _config_instance
    _config_instance = Config()
    return _config_instance

