"""
语音合成服务 - 使用 DashScope API
阿里云的语音合成服务
"""

import os
import asyncio
import base64
from typing import Optional
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
    
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None, voice: Optional[str] = None):
        """
        初始化 TTS 服务
        
        Args:
            api_key: DashScope API密钥
            model: TTS模型名称
            voice: 音色名称
        """
        if not DASHSCOPE_AVAILABLE:
            raise ImportError("dashscope 库未安装")
        
        # 优先使用 DASHSCOPE_API_KEY（用于TTS），其次使用 OPENAI_API_KEY
        # 这样可以让 LLM 用 ModelScope，TTS 用 DashScope
        self.api_key = api_key or os.getenv("DASHSCOPE_API_KEY") or os.getenv("OPENAI_API_KEY", "")
        dashscope.api_key = self.api_key
        
        # 从配置文件读取模型名称
        self.model = model or os.getenv("TTS_MODEL", "qwen3-tts-flash")
        
        # DashScope 支持的音色
        # Qwen3-TTS-Flash 默认音色：Cherry
        # 旧模型默认音色：zhixiaobai
        self.voice = voice or os.getenv("TTS_VOICE", "Cherry")
        
        # 设置 DashScope API 地址（北京地域）
        dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'
        
        # 音频输出目录
        self.output_dir = Path(__file__).parent.parent.parent / "assets" / "audio"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"🔊 DashScope TTS服务初始化: 模型={self.model}, 音色={self.voice}")
    
    async def text_to_speech(self, text: str, player_id: Optional[int] = None) -> Optional[str]:
        """
        将文本转换为语音
        
        Args:
            text: 要转换的文本
            player_id: 玩家ID（用于生成文件名）
            
        Returns:
            音频文件的路径，如果失败则返回None
        """
        if not text or not self.api_key:
            return None
        
        try:
            # 生成文件名
            file_name = f"speech_{player_id}_{hash(text) % 100000}.wav"
            file_path = self.output_dir / file_name
            
            # 使用配置的 TTS 模型
            try:
                response = dashscope.MultiModalConversation.call(
                    api_key=self.api_key,
                    model=self.model,
                    text=text,
                    voice=self.voice,
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
                    
                    print(f"✅ 语音生成成功 (Qwen3-TTS): {file_name}")
                    return str(file_path)
                else:
                    print(f"⚠️ Qwen3-TTS 生成失败，尝试旧模型")
                    raise Exception("No audio data")
                    
            except Exception as e:
                # 如果新 API 失败，回退到旧模型 (SpeechSynthesizer)
                print(f"⚠️ Qwen3-TTS 失败 ({e})，使用旧模型")
                
                result = SpeechSynthesizer.call(
                    model='sambert-zhichu-v1',
                    text=text,
                    sample_rate=16000,
                    format='wav',
                    voice='zhixiaobai' if self.voice == 'Cherry' else self.voice
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
    
    async def text_to_speech_stream(self, text: str, player_id: Optional[int] = None):
        """
        流式生成语音（生成完整音频后返回）
        
        Args:
            text: 要转换的文本
            player_id: 玩家ID
            
        Yields:
            音频数据块（base64编码的字符串）
        """
        if not text or not self.api_key:
            return
        
        try:
            print(f"🎵 开始TTS生成: 玩家{player_id}, 文本长度={len(text)}")
            
            # 使用配置的 TTS 模型
            try:
                response = dashscope.MultiModalConversation.call(
                    api_key=self.api_key,
                    model=self.model,
                    text=text,
                    voice=self.voice,
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
                    # 合并所有音频块
                    complete_audio = b''.join(audio_chunks)
                    # 返回完整的base64编码音频
                    audio_base64 = base64.b64encode(complete_audio).decode('utf-8')
                    yield audio_base64
                    print(f"✅ TTS生成成功 (Qwen3-TTS): 玩家{player_id}, 大小={len(complete_audio)} bytes")
                else:
                    print(f"⚠️ Qwen3-TTS 生成失败，尝试旧模型")
                    raise Exception("No audio data")
                    
            except Exception as e:
                # 如果新 API 失败，回退到旧模型（非流式）
                print(f"⚠️ Qwen3-TTS失败 ({e})，使用旧模型")
                
                result = SpeechSynthesizer.call(
                    model='sambert-zhichu-v1',
                    text=text,
                    sample_rate=16000,
                    format='wav',
                    voice='zhixiaobai' if self.voice == 'Cherry' else self.voice
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


# 全局实例
_dashscope_tts_instance = None


def get_dashscope_tts_service() -> DashScopeTTSService:
    """获取全局 DashScope TTS 服务实例"""
    global _dashscope_tts_instance
    if _dashscope_tts_instance is None:
        # 从配置文件读取 TTS 配置
        from src.utils.config import get_config
        config = get_config()
        _dashscope_tts_instance = DashScopeTTSService(
            model=config.tts_model if hasattr(config, 'tts_model') else None,
            voice=config.tts_voice if hasattr(config, 'tts_voice') else None
        )
    return _dashscope_tts_instance

