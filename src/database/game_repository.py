"""
游戏数据仓库
统一管理游戏数据的存储和检索
"""

import json
from typing import Optional, List, Dict
from pathlib import Path
from datetime import datetime

from src.core.models import GameState


class GameRepository:
    """游戏数据仓库"""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.games_dir = self.data_dir / "games"
        self.games_dir.mkdir(parents=True, exist_ok=True)
    
    def save_game(self, game_state: GameState) -> bool:
        """保存游戏状态"""
        try:
            game_file = self.games_dir / f"{game_state.game_id}.json"
            with open(game_file, 'w', encoding='utf-8') as f:
                json.dump(game_state.to_dict(), f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"❌ Save game error: {e}")
            return False
    
    def load_game(self, game_id: str) -> Optional[Dict]:
        """加载游戏状态"""
        try:
            game_file = self.games_dir / f"{game_id}.json"
            if game_file.exists():
                with open(game_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return None
        except Exception as e:
            print(f"❌ Load game error: {e}")
            return None
    
    def list_games(self, limit: int = 100) -> List[Dict]:
        """列出所有游戏"""
        games = []
        for game_file in self.games_dir.glob("*.json"):
            try:
                with open(game_file, 'r', encoding='utf-8') as f:
                    game_data = json.load(f)
                    games.append({
                        "game_id": game_data["game_id"],
                        "round": game_data["round"],
                        "created_at": game_data["created_at"],
                        "players_count": len(game_data["players"])
                    })
            except Exception:
                continue
        
        games.sort(key=lambda x: x["created_at"], reverse=True)
        return games[:limit]
    
    def delete_game(self, game_id: str) -> bool:
        """删除游戏记录"""
        try:
            game_file = self.games_dir / f"{game_id}.json"
            if game_file.exists():
                game_file.unlink()
            return True
        except Exception as e:
            print(f"❌ Delete game error: {e}")
            return False
    
    def save_game_replay(self, game_id: str, events: List[Dict]):
        """保存游戏回放"""
        try:
            replay_file = self.data_dir / "replays" / f"{game_id}.json"
            replay_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(replay_file, 'w', encoding='utf-8') as f:
                json.dump({
                    "game_id": game_id,
                    "events": events,
                    "saved_at": datetime.now().isoformat()
                }, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"❌ Save replay error: {e}")
            return False
    
    def load_game_replay(self, game_id: str) -> Optional[List[Dict]]:
        """加载游戏回放"""
        try:
            replay_file = self.data_dir / "replays" / f"{game_id}.json"
            if replay_file.exists():
                with open(replay_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return data.get("events", [])
            return None
        except Exception as e:
            print(f"❌ Load replay error: {e}")
            return None

