"""
游戏事件系统
用于游戏状态变化的发布-订阅模式
为视频生成、UI更新等提供钩子
"""

from enum import Enum
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional
from datetime import datetime


class EventType(str, Enum):
    """事件类型"""
    # 游戏流程事件
    GAME_START = "game_start"
    GAME_END = "game_end"
    ROUND_START = "round_start"
    ROUND_END = "round_end"
    PHASE_CHANGE = "phase_change"
    
    # 玩家行为事件
    PLAYER_SPEAK = "player_speak"
    PLAYER_VOTE = "player_vote"
    PLAYER_DIED = "player_died"
    PLAYER_SKILL = "player_skill"
    
    # 特效触发事件
    SKILL_EFFECT = "skill_effect"
    ROLE_REVEAL = "role_reveal"
    DRAMATIC_MOMENT = "dramatic_moment"


@dataclass
class GameEvent:
    """游戏事件"""
    type: EventType
    timestamp: datetime
    data: Dict[str, Any]
    
    # 视频制作相关
    need_effect: bool = False  # 是否需要特效
    effect_type: str = ""      # 特效类型
    priority: int = 0          # 优先级（用于视频剪辑）
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "type": self.type.value,
            "timestamp": self.timestamp.isoformat(),
            "data": self.data,
            "need_effect": self.need_effect,
            "effect_type": self.effect_type,
            "priority": self.priority,
        }


class EventSystem:
    """事件系统"""
    
    def __init__(self):
        self._listeners: Dict[EventType, List[Callable]] = {}
        self._event_history: List[GameEvent] = []
    
    def subscribe(self, event_type: EventType, callback: Callable):
        """订阅事件"""
        if event_type not in self._listeners:
            self._listeners[event_type] = []
        self._listeners[event_type].append(callback)
    
    def unsubscribe(self, event_type: EventType, callback: Callable):
        """取消订阅"""
        if event_type in self._listeners:
            self._listeners[event_type].remove(callback)
    
    def emit(self, event: GameEvent):
        """发布事件"""
        # 保存到历史
        self._event_history.append(event)
        
        # 通知所有订阅者
        if event.type in self._listeners:
            for callback in self._listeners[event.type]:
                try:
                    callback(event)
                except Exception as e:
                    print(f"Event callback error: {e}")
    
    def get_history(self, event_type: Optional[EventType] = None, limit: int = 100) -> List[GameEvent]:
        """获取事件历史"""
        events = self._event_history
        
        if event_type:
            events = [e for e in events if e.type == event_type]
        
        return events[-limit:]
    
    def clear_history(self):
        """清空历史"""
        self._event_history.clear()
    
    def get_key_moments(self, min_priority: int = 5) -> List[GameEvent]:
        """获取关键时刻（用于视频剪辑）"""
        return [e for e in self._event_history if e.priority >= min_priority]

