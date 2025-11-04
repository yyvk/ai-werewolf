"""
视频生成模块
用于自动生成游戏视频
"""

from .video_generator import VideoGenerator
from .effects import EffectRenderer, EffectType
from .timeline import Timeline, TimelineEvent

__all__ = [
    'VideoGenerator',
    'EffectRenderer',
    'EffectType',
    'Timeline',
    'TimelineEvent',
]

