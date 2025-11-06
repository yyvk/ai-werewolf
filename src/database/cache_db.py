"""
缓存数据库接口
用于缓存LLM响应、游戏状态等
支持集成：Redis, Memcached等
"""

import json
import time
from typing import Optional, Any, Dict
from pathlib import Path

from .base_db import BaseDatabase


class CacheDatabase(BaseDatabase):
    """缓存数据库"""
    
    def __init__(self, cache_dir: str = "data/cache", ttl: int = 3600):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.ttl = ttl  # 默认1小时过期
        self.memory_cache: Dict[str, tuple[Any, float]] = {}
        self.connected = False
        self.cache_type = "memory"
    
    def connect(self):
        """连接缓存"""
        self.connected = True
        print(f"[OK] Cache DB connected: {self.cache_type}")
    
    def disconnect(self):
        """断开连接"""
        self.connected = False
        self.memory_cache.clear()
    
    def save(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """保存到缓存"""
        try:
            expire_time = time.time() + (ttl or self.ttl)
            self.memory_cache[key] = (value, expire_time)
            return True
        except Exception as e:
            print(f"[ERROR] Cache save error: {e}")
            return False
    
    def get(self, key: str) -> Optional[Any]:
        """从缓存获取"""
        try:
            if key in self.memory_cache:
                value, expire_time = self.memory_cache[key]
                if time.time() < expire_time:
                    return value
                else:
                    del self.memory_cache[key]
            return None
        except Exception as e:
            print(f"[ERROR] Cache get error: {e}")
            return None
    
    def delete(self, key: str) -> bool:
        """从缓存删除"""
        try:
            if key in self.memory_cache:
                del self.memory_cache[key]
            return True
        except Exception as e:
            print(f"[ERROR] Cache delete error: {e}")
            return False
    
    def exists(self, key: str) -> bool:
        """检查缓存是否存在且未过期"""
        if key in self.memory_cache:
            _, expire_time = self.memory_cache[key]
            if time.time() < expire_time:
                return True
            else:
                del self.memory_cache[key]
        return False
    
    def clear_all(self):
        """清空所有缓存"""
        self.memory_cache.clear()
    
    def clear_expired(self):
        """清理过期缓存"""
        current_time = time.time()
        expired_keys = [
            key for key, (_, expire_time) in self.memory_cache.items()
            if current_time >= expire_time
        ]
        for key in expired_keys:
            del self.memory_cache[key]
    
    def cache_llm_response(self, prompt: str, response: str, ttl: int = 7200):
        """缓存LLM响应"""
        key = f"llm_response_{hash(prompt)}"
        return self.save(key, response, ttl)
    
    def get_cached_llm_response(self, prompt: str) -> Optional[str]:
        """获取缓存的LLM响应"""
        key = f"llm_response_{hash(prompt)}"
        return self.get(key)
    
    def cache_game_state(self, game_id: str, state: Dict):
        """缓存游戏状态"""
        key = f"game_state_{game_id}"
        return self.save(key, state, 1800)
    
    def get_cached_game_state(self, game_id: str) -> Optional[Dict]:
        """获取缓存的游戏状态"""
        key = f"game_state_{game_id}"
        return self.get(key)

