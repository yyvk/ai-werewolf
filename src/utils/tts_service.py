"""
语音合成服务 (Text-to-Speech)
使用 ModelScope 语音合成模型
"""

import os
import base64
import asyncio
from typing import Optional
import httpx
from pathlib import Path


class TTSService:
    """语音合成服务类"""
    
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None, voice: Optional[str] = None):
        """
        初始化 TTS 服务
        
        Args:
            api_key: ModelScope API密钥
            model: 语音合成模型名称
            voice: 音色名称
        """
        # TTS 专用的 API Key（优先使用 DASHSCOPE_API_KEY）
        self.api_key = api_key or os.getenv("DASHSCOPE_API_KEY") or os.getenv("OPENAI_API_KEY", "")
        self.model = model or os.getenv("TTS_MODEL", "iic/speech_sambert-hifigan_tts_zh-cn_16k")
        # 阿里云支持的音色：zhixiaobai, zhixiaoxia, zhiyan, zhitian, zhigang 等
        self.voice = voice or os.getenv("TTS_VOICE", "zhixiaobai")
        
        # 阿里云 DashScope TTS API 端点
        self.api_base = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text2speech/synthesis"
        
        # 音频输出目录
        self.output_dir = Path(__file__).parent.parent.parent / "assets" / "audio"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"🔊 TTS服务初始化: 模型={self.model}, 音色={self.voice}")
        print(f"   API 端点: {self.api_base}")
    
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
            # 准备请求
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            # 阿里云 DashScope TTS API 请求格式
            payload = {
                "model": "sambert-zhichu-v1",
                "input": {
                    "text": text
                },
                "parameters": {
                    "voice": self.voice,
                    "format": "wav",
                    "sample_rate": 16000,
                    "volume": 50
                }
            }
            
            # 发送请求
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    self.api_base,
                    json=payload,
                    headers=headers
                )
                
                if response.status_code != 200:
                    print(f"⚠️ TTS API 错误: {response.status_code}")
                    print(f"   请求 URL: {self.api_base}")
                    print(f"   响应内容: {response.text[:200]}")
                    return None
                
                result = response.json()
                print(f"   响应结构: {list(result.keys())}")
                
                # 从响应中提取音频数据
                # 阿里云 DashScope 返回格式: {"output": {"audio_url": "..."}}
                if "output" in result:
                    output = result["output"]
                    
                    # 方式1: 返回 URL
                    if "audio_url" in output:
                        audio_url = output["audio_url"]
                        print(f"   下载音频: {audio_url}")
                        audio_response = await client.get(audio_url)
                        
                        if audio_response.status_code == 200:
                            file_name = f"speech_{player_id}_{hash(text) % 100000}.wav"
                            file_path = self.output_dir / file_name
                            
                            with open(file_path, "wb") as f:
                                f.write(audio_response.content)
                            
                            print(f"✅ 语音生成成功: {file_name}")
                            return str(file_path)
                    
                    # 方式2: 返回 base64 编码的音频
                    elif "audio" in output:
                        audio_data = output["audio"]
                        if isinstance(audio_data, str):
                            audio_bytes = base64.b64decode(audio_data)
                        else:
                            audio_bytes = audio_data
                        
                        file_name = f"speech_{player_id}_{hash(text) % 100000}.wav"
                        file_path = self.output_dir / file_name
                        
                        with open(file_path, "wb") as f:
                            f.write(audio_bytes)
                        
                        print(f"✅ 语音生成成功: {file_name}")
                        return str(file_path)
                
                print(f"⚠️ TTS 响应中没有音频数据")
                print(f"   完整响应: {result}")
                return None
                
        except Exception as e:
            print(f"❌ TTS 生成失败: {e}")
            return None
    
    async def text_to_speech_stream(self, text: str, player_id: Optional[int] = None):
        """
        流式文本转语音（当文本较长时分段处理）
        
        Args:
            text: 要转换的文本
            player_id: 玩家ID
            
        Yields:
            音频文件路径
        """
        # 将长文本分段（按句子分）
        import re
        sentences = re.split(r'([。！？.!?])', text)
        
        # 重新组合句子和标点
        segments = []
        for i in range(0, len(sentences) - 1, 2):
            if i + 1 < len(sentences):
                segments.append(sentences[i] + sentences[i + 1])
            else:
                segments.append(sentences[i])
        
        # 如果没有分段，直接处理整个文本
        if not segments:
            segments = [text]
        
        # 为每个分段生成语音
        for i, segment in enumerate(segments):
            if segment.strip():
                audio_path = await self.text_to_speech(segment, player_id)
                if audio_path:
                    yield audio_path
                    await asyncio.sleep(0.1)  # 短暂延迟


# 全局 TTS 服务实例
_tts_instance = None


def get_tts_service() -> TTSService:
    """获取全局 TTS 服务实例"""
    global _tts_instance
    if _tts_instance is None:
        _tts_instance = TTSService()
    return _tts_instance

