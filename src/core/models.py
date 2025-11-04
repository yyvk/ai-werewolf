"""
游戏核心数据模型
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from datetime import datetime


class Role(str, Enum):
    """角色类型"""
    WEREWOLF = "werewolf"      # 狼人
    VILLAGER = "villager"      # 村民
    SEER = "seer"              # 预言家
    WITCH = "witch"            # 女巫
    HUNTER = "hunter"          # 猎人
    GUARD = "guard"            # 守卫
    IDIOT = "idiot"            # 白痴


class GamePhase(str, Enum):
    """游戏阶段"""
    NIGHT = "night"            # 夜晚
    DISCUSSION = "discussion"  # 讨论
    VOTING = "voting"          # 投票
    ENDED = "ended"            # 结束


class Camp(str, Enum):
    """阵营"""
    WEREWOLF = "werewolf"      # 狼人阵营
    VILLAGER = "villager"      # 好人阵营


@dataclass
class Player:
    """玩家数据类"""
    id: int
    name: str
    role: Role
    is_alive: bool = True
    is_protected: bool = False  # 是否被守卫保护
    votes_received: int = 0
    
    # 技能相关
    has_used_skill: bool = False
    skill_data: Dict[str, Any] = field(default_factory=dict)
    
    @property
    def camp(self) -> Camp:
        """所属阵营"""
        return Camp.WEREWOLF if self.role == Role.WEREWOLF else Camp.VILLAGER
    
    @property
    def role_name_cn(self) -> str:
        """角色中文名"""
        role_names = {
            Role.WEREWOLF: "狼人",
            Role.VILLAGER: "村民",
            Role.SEER: "预言家",
            Role.WITCH: "女巫",
            Role.HUNTER: "猎人",
            Role.GUARD: "守卫",
            Role.IDIOT: "白痴",
        }
        return role_names.get(self.role, "未知")
    
    @property
    def role_description(self) -> str:
        """角色描述"""
        descriptions = {
            Role.WEREWOLF: "你是狼人，目标是消灭所有好人。夜晚可以和其他狼人一起杀人。白天要隐藏身份，伪装成好人。",
            Role.VILLAGER: "你是村民，目标是找出并投票淘汰所有狼人。你没有特殊能力，但要通过推理找出狼人。",
            Role.SEER: "你是预言家，每晚可以查验一名玩家的身份。你要引导好人找出狼人，但也要注意自己的安全。",
            Role.WITCH: "你是女巫，拥有一瓶解药和一瓶毒药。解药可以救人，毒药可以杀人，每瓶只能使用一次。",
            Role.HUNTER: "你是猎人，如果被淘汰可以开枪带走一名玩家。你要选择合适的时机使用这个能力。",
            Role.GUARD: "你是守卫，每晚可以守护一名玩家（不能连续两晚守护同一人）。被守护的玩家当晚免疫死亡。",
            Role.IDIOT: "你是白痴，被投票时可以翻牌免疫一次。但之后失去投票权，且不能被狼人刀杀。",
        }
        return descriptions.get(self.role, "普通角色")
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "id": self.id,
            "name": self.name,
            "role": self.role.value,
            "role_name": self.role_name_cn,
            "is_alive": self.is_alive,
            "is_protected": self.is_protected,
            "votes_received": self.votes_received,
            "camp": self.camp.value,
        }


@dataclass
class GameState:
    """游戏状态"""
    game_id: str
    round: int = 0
    phase: GamePhase = GamePhase.DISCUSSION
    players: List[Player] = field(default_factory=list)
    events: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    # 游戏配置
    max_rounds: int = 10
    enable_special_roles: bool = True
    
    def get_alive_players(self, camp: Optional[Camp] = None) -> List[Player]:
        """获取存活玩家"""
        players = [p for p in self.players if p.is_alive]
        if camp:
            players = [p for p in players if p.camp == camp]
        return players
    
    def get_player_by_id(self, player_id: int) -> Optional[Player]:
        """根据ID获取玩家"""
        for player in self.players:
            if player.id == player_id:
                return player
        return None
    
    def add_event(self, event: str):
        """添加事件"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.events.append(f"[{timestamp}] {event}")
        self.updated_at = datetime.now()
    
    def check_game_over(self) -> Optional[Camp]:
        """检查游戏是否结束，返回获胜阵营"""
        alive_werewolves = len(self.get_alive_players(Camp.WEREWOLF))
        alive_villagers = len(self.get_alive_players(Camp.VILLAGER))
        
        if alive_werewolves == 0:
            return Camp.VILLAGER
        
        if alive_villagers <= alive_werewolves:
            return Camp.WEREWOLF
        
        return None
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "game_id": self.game_id,
            "round": self.round,
            "phase": self.phase.value,
            "players": [p.to_dict() for p in self.players],
            "alive_werewolves": len(self.get_alive_players(Camp.WEREWOLF)),
            "alive_villagers": len(self.get_alive_players(Camp.VILLAGER)),
            "recent_events": self.events[-10:],
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }


@dataclass
class AgentMemory:
    """Agent记忆数据"""
    player_id: int
    observations: List[str] = field(default_factory=list)
    beliefs: Dict[int, str] = field(default_factory=dict)  # 对其他玩家的判断
    strategies: List[str] = field(default_factory=list)
    
    def add_observation(self, observation: str):
        """添加观察"""
        self.observations.append(observation)
        if len(self.observations) > 50:  # 保留最近50条
            self.observations = self.observations[-50:]
    
    def update_belief(self, target_id: int, belief: str):
        """更新对某玩家的判断"""
        self.beliefs[target_id] = belief
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "player_id": self.player_id,
            "observations": self.observations[-10:],
            "beliefs": self.beliefs,
            "strategies": self.strategies,
        }

