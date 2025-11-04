"""
Agent基类
定义Agent的接口和基础功能
"""

from abc import ABC, abstractmethod
from typing import Dict, Optional

from src.core.models import Player, AgentMemory, GameState


class BaseAgent(ABC):
    """Agent基类"""
    
    def __init__(self, player: Player):
        self.player = player
        self.memory = AgentMemory(player_id=player.id)
    
    @abstractmethod
    def think(self, game_state: GameState) -> str:
        """思考当前局势"""
        pass
    
    @abstractmethod
    def speak(self, game_state: GameState) -> str:
        """发言"""
        pass
    
    @abstractmethod
    def vote(self, game_state: GameState) -> int:
        """投票"""
        pass
    
    def use_skill(self, game_state: GameState) -> Optional[Dict]:
        """使用技能（特殊角色）"""
        return None
    
    def observe(self, observation: str):
        """观察并记录"""
        self.memory.add_observation(observation)
    
    def update_belief(self, target_id: int, belief: str):
        """更新对其他玩家的判断"""
        self.memory.update_belief(target_id, belief)
    
    def get_memory_summary(self) -> str:
        """获取记忆摘要"""
        recent_observations = self.memory.observations[-5:]
        return "\n".join(f"- {obs}" for obs in recent_observations)
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "player": self.player.to_dict(),
            "memory": self.memory.to_dict()
        }

