"""
向量数据库接口
用于存储和检索游戏记忆、策略等
支持集成：ChromaDB, FAISS, Pinecone等
"""

import json
from typing import List, Dict, Optional, Any
from pathlib import Path

from .base_db import BaseDatabase


class VectorDatabase(BaseDatabase):
    """向量数据库"""
    
    def __init__(self, db_path: str = "data/vector_db"):
        self.db_path = Path(db_path)
        self.db_path.mkdir(parents=True, exist_ok=True)
        self.connected = False
        self.db_type = "file"
        
    def connect(self):
        """连接数据库"""
        self.connected = True
        print(f"[OK] Vector DB connected: {self.db_path}")
        
    def disconnect(self):
        """断开连接"""
        self.connected = False
    
    def save(self, key: str, value: Any) -> bool:
        """保存数据"""
        try:
            file_path = self.db_path / f"{key}.json"
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(value, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"[ERROR] Save error: {e}")
            return False
    
    def get(self, key: str) -> Optional[Any]:
        """获取数据"""
        try:
            file_path = self.db_path / f"{key}.json"
            if file_path.exists():
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return None
        except Exception as e:
            print(f"[ERROR] Get error: {e}")
            return None
    
    def delete(self, key: str) -> bool:
        """删除数据"""
        try:
            file_path = self.db_path / f"{key}.json"
            if file_path.exists():
                file_path.unlink()
            return True
        except Exception as e:
            print(f"[ERROR] Delete error: {e}")
            return False
    
    def exists(self, key: str) -> bool:
        """检查是否存在"""
        file_path = self.db_path / f"{key}.json"
        return file_path.exists()
    
    def search_similar(self, query: str, top_k: int = 5) -> List[Dict]:
        """相似度搜索"""
        print("[WARN] Vector similarity search not implemented yet")
        return []
    
    def add_embedding(self, key: str, text: str, metadata: Optional[Dict] = None):
        """添加嵌入向量"""
        pass
    
    def save_game_memory(self, game_id: str, player_id: int, memories: List[str]):
        """保存玩家游戏记忆"""
        key = f"game_{game_id}_player_{player_id}_memory"
        return self.save(key, {"memories": memories})
    
    def get_game_memory(self, game_id: str, player_id: int) -> List[str]:
        """获取玩家游戏记忆"""
        key = f"game_{game_id}_player_{player_id}_memory"
        data = self.get(key)
        return data.get("memories", []) if data else []
    
    def save_game_strategy(self, role: str, strategy: Dict):
        """保存角色策略"""
        key = f"strategy_{role}"
        return self.save(key, strategy)
    
    def get_game_strategy(self, role: str) -> Optional[Dict]:
        """获取角色策略"""
        key = f"strategy_{role}"
        return self.get(key)

