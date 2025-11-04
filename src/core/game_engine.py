"""
游戏引擎核心逻辑
"""

import uuid
from typing import List, Optional
from datetime import datetime

from .models import Player, Role, GameState, GamePhase, Camp
from .event_system import EventSystem, GameEvent, EventType


class WerewolfGame:
    """狼人杀游戏引擎"""
    
    def __init__(self, event_system: Optional[EventSystem] = None):
        self.game_id = str(uuid.uuid4())
        self.state: Optional[GameState] = None
        self.event_system = event_system or EventSystem()
        
    def setup_game(self, num_players: int = 6, roles: Optional[List[Role]] = None):
        """初始化游戏"""
        if roles is None:
            # 默认6人局配置
            roles = [
                Role.WEREWOLF, Role.WEREWOLF,
                Role.VILLAGER, Role.VILLAGER,
                Role.SEER, Role.WITCH
            ]
        
        # 创建玩家
        players = []
        for i in range(min(num_players, len(roles))):
            player = Player(
                id=i + 1,
                name=f"玩家{i + 1}",
                role=roles[i]
            )
            players.append(player)
        
        # 初始化游戏状态
        self.state = GameState(
            game_id=self.game_id,
            players=players,
            round=0,
            phase=GamePhase.DISCUSSION
        )
        
        # 发布游戏开始事件
        self.event_system.emit(GameEvent(
            type=EventType.GAME_START,
            timestamp=datetime.now(),
            data={
                "game_id": self.game_id,
                "num_players": num_players,
                "roles": [r.value for r in roles]
            },
            need_effect=True,
            effect_type="game_start_animation",
            priority=10
        ))
        
        return self.state
    
    def start_round(self):
        """开始新一轮"""
        if not self.state:
            raise ValueError("Game not initialized")
        
        self.state.round += 1
        self.state.phase = GamePhase.DISCUSSION
        
        self.event_system.emit(GameEvent(
            type=EventType.ROUND_START,
            timestamp=datetime.now(),
            data={"round": self.state.round},
            need_effect=True,
            effect_type="round_start_transition",
            priority=7
        ))
    
    def change_phase(self, new_phase: GamePhase):
        """改变游戏阶段"""
        if not self.state:
            raise ValueError("Game not initialized")
        
        old_phase = self.state.phase
        self.state.phase = new_phase
        
        self.event_system.emit(GameEvent(
            type=EventType.PHASE_CHANGE,
            timestamp=datetime.now(),
            data={
                "old_phase": old_phase.value,
                "new_phase": new_phase.value,
                "round": self.state.round
            },
            need_effect=True,
            effect_type="phase_transition",
            priority=5
        ))
    
    def eliminate_player(self, player_id: int, reason: str = "投票"):
        """淘汰玩家"""
        if not self.state:
            raise ValueError("Game not initialized")
        
        player = self.state.get_player_by_id(player_id)
        if not player or not player.is_alive:
            return
        
        player.is_alive = False
        self.state.add_event(f"{player.name}（{player.role_name_cn}）被{reason}淘汰")
        
        self.event_system.emit(GameEvent(
            type=EventType.PLAYER_DIED,
            timestamp=datetime.now(),
            data={
                "player_id": player_id,
                "player_name": player.name,
                "role": player.role.value,
                "reason": reason,
                "round": self.state.round
            },
            need_effect=True,
            effect_type="death_animation",
            priority=9
        ))
    
    def record_speech(self, player_id: int, speech: str):
        """记录玩家发言"""
        if not self.state:
            raise ValueError("Game not initialized")
        
        player = self.state.get_player_by_id(player_id)
        if not player:
            return
        
        self.state.add_event(f"{player.name} 发言")
        
        self.event_system.emit(GameEvent(
            type=EventType.PLAYER_SPEAK,
            timestamp=datetime.now(),
            data={
                "player_id": player_id,
                "player_name": player.name,
                "speech": speech,
                "round": self.state.round
            },
            need_effect=False,
            priority=3
        ))
    
    def record_vote(self, voter_id: int, target_id: int):
        """记录投票"""
        if not self.state:
            raise ValueError("Game not initialized")
        
        self.event_system.emit(GameEvent(
            type=EventType.PLAYER_VOTE,
            timestamp=datetime.now(),
            data={
                "voter_id": voter_id,
                "target_id": target_id,
                "round": self.state.round
            },
            need_effect=True,
            effect_type="vote_effect",
            priority=4
        ))
    
    def use_skill(self, player_id: int, skill_name: str, target_id: Optional[int] = None):
        """使用技能"""
        if not self.state:
            raise ValueError("Game not initialized")
        
        player = self.state.get_player_by_id(player_id)
        if not player:
            return
        
        self.event_system.emit(GameEvent(
            type=EventType.PLAYER_SKILL,
            timestamp=datetime.now(),
            data={
                "player_id": player_id,
                "player_name": player.name,
                "role": player.role.value,
                "skill_name": skill_name,
                "target_id": target_id,
                "round": self.state.round
            },
            need_effect=True,
            effect_type=f"skill_{skill_name}",
            priority=8
        ))
    
    def check_game_over(self) -> Optional[Camp]:
        """检查游戏是否结束"""
        if not self.state:
            return None
        
        winner = self.state.check_game_over()
        
        if winner:
            self.state.phase = GamePhase.ENDED
            
            self.event_system.emit(GameEvent(
                type=EventType.GAME_END,
                timestamp=datetime.now(),
                data={
                    "winner": winner.value,
                    "total_rounds": self.state.round,
                    "survivors": [p.to_dict() for p in self.state.get_alive_players()]
                },
                need_effect=True,
                effect_type="game_end_celebration",
                priority=10
            ))
        
        return winner
    
    def get_state_snapshot(self) -> dict:
        """获取游戏状态快照"""
        if not self.state:
            return {}
        return self.state.to_dict()

