"""
视频时间轴
管理视频事件的时间序列
"""

from typing import List, Dict
from dataclasses import dataclass, field
from datetime import datetime, timedelta


@dataclass
class TimelineEvent:
    """时间轴事件"""
    start_time: float  # 秒
    duration: float    # 秒
    event_type: str
    content: Dict
    effect_name: str = ""
    priority: int = 0


class Timeline:
    """视频时间轴"""
    
    def __init__(self, fps: int = 30):
        self.fps = fps
        self.events: List[TimelineEvent] = []
        self.total_duration = 0.0
    
    def add_event(self, event: TimelineEvent):
        """添加事件到时间轴"""
        self.events.append(event)
        self.events.sort(key=lambda x: x.start_time)
        
        event_end = event.start_time + event.duration
        if event_end > self.total_duration:
            self.total_duration = event_end
    
    def get_events_at_time(self, time: float) -> List[TimelineEvent]:
        """获取指定时间的所有事件"""
        return [
            e for e in self.events
            if e.start_time <= time < e.start_time + e.duration
        ]
    
    def get_frame_events(self, frame_number: int) -> List[TimelineEvent]:
        """获取指定帧的所有事件"""
        time = frame_number / self.fps
        return self.get_events_at_time(time)
    
    def optimize(self):
        """优化时间轴"""
        pass
    
    def export(self) -> Dict:
        """导出时间轴数据"""
        return {
            "fps": self.fps,
            "total_duration": self.total_duration,
            "total_frames": int(self.total_duration * self.fps),
            "events": [
                {
                    "start_time": e.start_time,
                    "duration": e.duration,
                    "type": e.event_type,
                    "effect": e.effect_name,
                    "priority": e.priority
                }
                for e in self.events
            ]
        }
    
    def get_chapters(self) -> List[Dict]:
        """获取视频章节"""
        chapters = []
        current_round = 0
        chapter_start = 0.0
        
        for event in self.events:
            if event.event_type == "round_start":
                if current_round > 0:
                    chapters.append({
                        "round": current_round,
                        "start": chapter_start,
                        "end": event.start_time
                    })
                current_round += 1
                chapter_start = event.start_time
        
        if current_round > 0:
            chapters.append({
                "round": current_round,
                "start": chapter_start,
                "end": self.total_duration
            })
        
        return chapters

