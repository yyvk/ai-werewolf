"""
语音合成服务 - 使用 DashScope API
阿里云的语音合成服务

采用新的配置系统，支持从配置文件和环境变量加载配置
"""

import os
import asyncio
import base64
from typing import Optional, Dict, Any
from pathlib import Path

try:
    import dashscope
    from dashscope.audio.tts import SpeechSynthesizer
    DASHSCOPE_AVAILABLE = True
except ImportError:
    DASHSCOPE_AVAILABLE = False
    print("⚠️ dashscope 未安装，请运行: pip install dashscope")


class DashScopeTTSService:
    """DashScope 语音合成服务类"""
    
    def __init__(
        self, 
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        voice: Optional[str] = None,
        speed: Optional[float] = None,
        pitch: Optional[float] = None,
        use_config: bool = True
    ):
        """
        初始化 TTS 服务
        
        Args:
            api_key: DashScope API密钥
            model: TTS模型名称
            voice: 音色名称
            speed: 语速（0.5-2.0）
            pitch: 音高（0.5-2.0）
            use_config: 是否使用配置文件（默认: True）
        """
        if not DASHSCOPE_AVAILABLE:
            raise ImportError("dashscope 库未安装，请运行: pip install dashscope")
        
        # 加载配置
        if use_config:
            from src.utils.config import get_config
            config = get_config()
            tts_config = config.get_tts_config("dashscope")
        else:
            tts_config = {}
        
        # 参数优先级：传入参数 > 配置文件 > 默认值
        self.api_key = api_key or tts_config.get("api_key", "")
        self.model = model or tts_config.get("model", "qwen3-tts-flash")
        self.voice = voice or tts_config.get("voice", "Cherry")
        self.speed = speed if speed is not None else tts_config.get("speed", 1.0)
        self.pitch = pitch if pitch is not None else tts_config.get("pitch", 1.0)
        self.volume = tts_config.get("volume", 50)
        self.sample_rate = tts_config.get("sample_rate", 16000)
        self.format = tts_config.get("format", "wav")
        
        # 设置 DashScope API Key
        if self.api_key:
            dashscope.api_key = self.api_key
        else:
            print("⚠️ 未配置 DashScope API Key")
        
        # 设置 DashScope API 地址（北京地域）
        dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'
        
        # 音频输出目录
        self.output_dir = Path(__file__).parent.parent.parent / "assets" / "audio"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"🔊 DashScope TTS服务初始化:")
        print(f"   模型: {self.model}")
        print(f"   音色: {self.voice}")
        print(f"   语速: {self.speed}")
        print(f"   音高: {self.pitch}")
    
    async def text_to_speech(
        self, 
        text: str, 
        player_id: Optional[int] = None,
        voice: Optional[str] = None,
        speed: Optional[float] = None,
        pitch: Optional[float] = None
    ) -> Optional[str]:
        """
        将文本转换为语音
        
        Args:
            text: 要转换的文本
            player_id: 玩家ID（用于生成文件名）
            voice: 音色（可选，覆盖默认音色）
            speed: 语速（可选，覆盖默认语速）
            pitch: 音高（可选，覆盖默认音高）
        
        Returns:
            音频文件的路径，如果失败则返回None
        """
        if not text or not self.api_key:
            return None
        
        # 使用传入的参数或默认参数
        voice = voice or self.voice
        speed = speed if speed is not None else self.speed
        pitch = pitch if pitch is not None else self.pitch
        
        try:
            # 生成文件名
            file_name = f"speech_{player_id}_{hash(text) % 100000}.{self.format}"
            file_path = self.output_dir / file_name
            
            # 使用配置的 TTS 模型
            try:
                response = dashscope.MultiModalConversation.call(
                    api_key=self.api_key,
                    model=self.model,
                    text=text,
                    voice=voice,
                    language_type="Chinese",
                    stream=True
                )
                
                # 收集所有音频数据
                audio_chunks = []
                for chunk in response:
                    if hasattr(chunk.output, 'audio') and chunk.output.audio.data is not None:
                        wav_bytes = base64.b64decode(chunk.output.audio.data)
                        audio_chunks.append(wav_bytes)
                
                if audio_chunks:
                    # 合并并保存音频
                    complete_audio = b''.join(audio_chunks)
                    with open(file_path, 'wb') as f:
                        f.write(complete_audio)
                    
                    print(f"✅ 语音生成成功 ({self.model}): {file_name}")
                    return str(file_path)
                else:
                    print(f"⚠️ {self.model} 生成失败，尝试旧模型")
                    raise Exception("No audio data")
            
            except Exception as e:
                # 如果新 API 失败，回退到旧模型 (SpeechSynthesizer)
                print(f"⚠️ {self.model} 失败 ({e})，使用旧模型")
                
                # 音色映射（新模型音色 -> 旧模型音色）
                voice_mapping = {
                    "Cherry": "zhixiaobai",
                    "Bella": "zhixiaoxia",
                    "Amy": "zhiyan",
                }
                old_voice = voice_mapping.get(voice, "zhixiaobai")
                
                result = SpeechSynthesizer.call(
                    model='sambert-zhichu-v1',
                    text=text,
                    sample_rate=self.sample_rate,
                    format=self.format,
                    voice=old_voice
                )
                
                if result.get_audio_data() is not None:
                    with open(file_path, 'wb') as f:
                        f.write(result.get_audio_data())
                    
                    print(f"✅ 语音生成成功 (旧模型): {file_name}")
                    return str(file_path)
                else:
                    print(f"⚠️ TTS 生成失败: {result}")
                    return None
        
        except Exception as e:
            print(f"❌ TTS 生成失败: {e}")
            return None
    
    async def text_to_speech_stream(
        self, 
        text: str, 
        player_id: Optional[int] = None,
        voice: Optional[str] = None,
        speed: Optional[float] = None,
        pitch: Optional[float] = None
    ):
        """
        流式生成语音（生成完整音频后返回）
        
        Args:
            text: 要转换的文本
            player_id: 玩家ID
            voice: 音色（可选，覆盖默认音色）
            speed: 语速（可选，覆盖默认语速）
            pitch: 音高（可选，覆盖默认音高）
        
        Yields:
            音频数据块（base64编码的字符串）
        """
        if not text or not self.api_key:
            return
        
        # 使用传入的参数或默认参数
        voice = voice or self.voice
        speed = speed if speed is not None else self.speed
        pitch = pitch if pitch is not None else self.pitch
        
        try:
            print(f"🎵 开始TTS生成: 玩家{player_id}, 文本长度={len(text)}, 音色={voice}")
            
            # 使用配置的 TTS 模型
            try:
                response = dashscope.MultiModalConversation.call(
                    api_key=self.api_key,
                    model=self.model,
                    text=text,
                    voice=voice,
                    language_type="Chinese",
                    stream=True
                )
                
                # 真正的流式：逐块返回音频数据（不等待全部完成）
                chunk_count = 0
                total_bytes = 0
                first_chunk = True
                
                for chunk in response:
                    if hasattr(chunk.output, 'audio') and chunk.output.audio.data is not None:
                        # 直接返回每个音频块（已经是 base64 编码）
                        audio_chunk_base64 = chunk.output.audio.data
                        audio_bytes = base64.b64decode(audio_chunk_base64)
                        
                        # 检测第一个块的音频格式
                        if first_chunk and len(audio_bytes) >= 8:
                            magic_bytes = ' '.join([f'{b:02x}' for b in audio_bytes[:8]])
                            print(f"🔍 音频格式检测 (玩家{player_id}): 前8字节={magic_bytes}")
                            
                            # 检测格式
                            if audio_bytes[:4] == b'RIFF':
                                print(f"✅ 检测到 WAV 格式")
                            elif audio_bytes[:3] == b'ID3' or (audio_bytes[0] == 0xFF and (audio_bytes[1] & 0xE0) == 0xE0):
                                print(f"✅ 检测到 MP3 格式")
                            elif audio_bytes[:4] == b'OggS':
                                print(f"✅ 检测到 OGG 格式")
                            else:
                                print(f"⚠️ 未知音频格式")
                            
                            first_chunk = False
                        
                        chunk_count += 1
                        total_bytes += len(audio_bytes)
                        yield audio_chunk_base64
                        print(f"📦 发送音频块 #{chunk_count} (玩家{player_id}): {len(audio_bytes)} bytes")
                        await asyncio.sleep(0)  # 让出控制权
                
                if chunk_count > 0:
                    print(f"✅ TTS生成完成 ({self.model}): 玩家{player_id}, 共{chunk_count}块, 总大小={total_bytes} bytes")
                else:
                    print(f"⚠️ {self.model} 生成失败，尝试旧模型")
                    raise Exception("No audio data")
            
            except Exception as e:
                # 如果新 API 失败，回退到旧模型（非流式）
                print(f"⚠️ {self.model}失败 ({e})，使用旧模型")
                
                # 音色映射
                voice_mapping = {
                    "Cherry": "zhixiaobai",
                    "Bella": "zhixiaoxia",
                    "Amy": "zhiyan",
                }
                old_voice = voice_mapping.get(voice, "zhixiaobai")
                
                result = SpeechSynthesizer.call(
                    model='sambert-zhichu-v1',
                    text=text,
                    sample_rate=self.sample_rate,
                    format=self.format,
                    voice=old_voice
                )
                
                if result.get_audio_data() is not None:
                    # 旧模型不支持流式，直接返回完整音频的base64
                    audio_data = result.get_audio_data()
                    audio_base64 = base64.b64encode(audio_data).decode('utf-8')
                    yield audio_base64
                    print(f"✅ 语音生成成功 (旧模型): 玩家{player_id}")
                else:
                    print(f"⚠️ TTS 生成失败: {result}")
        
        except Exception as e:
            print(f"❌ TTS生成失败: {e}")
            import traceback
            traceback.print_exc()
    
    def get_config(self) -> Dict[str, Any]:
        """
        获取当前配置
        
        Returns:
            配置字典
        """
        return {
            "model": self.model,
            "voice": self.voice,
            "speed": self.speed,
            "pitch": self.pitch,
            "volume": self.volume,
            "sample_rate": self.sample_rate,
            "format": self.format
        }


# ==================== 全局实例 ====================

_dashscope_tts_instance: Optional[DashScopeTTSService] = None


def get_dashscope_tts_service(reload: bool = False) -> DashScopeTTSService:
    """
    获取全局 DashScope TTS 服务实例（单例模式）
    
    Args:
        reload: 是否重新加载实例
    
    Returns:
        DashScopeTTSService 实例
    """
    global _dashscope_tts_instance
    
    if _dashscope_tts_instance is None or reload:
        _dashscope_tts_instance = DashScopeTTSService(use_config=True)
    
    return _dashscope_tts_instance


def reload_tts_service() -> DashScopeTTSService:
    """重新加载TTS服务"""
    return get_dashscope_tts_service(reload=True)


# ==================== TTS工厂（支持多种提供商） ====================

class TTSFactory:
    """TTS工厂类 - 用于创建不同提供商的TTS服务"""
    
    @staticmethod
    def create_tts(provider: Optional[str] = None, **kwargs):
        """
        创建TTS服务实例
        
        Args:
            provider: TTS提供商（dashscope, azure, elevenlabs）
                     如果为None，使用配置文件中的默认提供商
            **kwargs: 额外的TTS参数
        
        Returns:
            TTS服务实例
        
        Raises:
            ValueError: 如果提供商不支持
        """
        if provider is None:
            from src.utils.config import get_config
            config = get_config()
            provider = config.tts_provider
        
        if provider == "dashscope":
            return DashScopeTTSService(**kwargs)
        
        elif provider == "azure":
            raise NotImplementedError("Azure TTS 暂未实现")
        
        elif provider == "elevenlabs":
            raise NotImplementedError("ElevenLabs TTS 暂未实现")
        
        else:
            raise ValueError(f"不支持的TTS提供商: {provider}")


def create_tts_from_config(provider: Optional[str] = None):
    """
    从配置创建TTS服务实例（便捷函数）
    
    Args:
        provider: TTS提供商（如果为None，使用配置文件中的默认提供商）
    
    Returns:
        TTS服务实例
    """
    return TTSFactory.create_tts(provider)
