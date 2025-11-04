"""
数据库基类
定义统一的数据库接口
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class BaseDatabase(ABC):
    """数据库基类"""
    
    @abstractmethod
    def connect(self):
        """连接数据库"""
        pass
    
    @abstractmethod
    def disconnect(self):
        """断开连接"""
        pass
    
    @abstractmethod
    def save(self, key: str, value: Any) -> bool:
        """保存数据"""
        pass
    
    @abstractmethod
    def get(self, key: str) -> Optional[Any]:
        """获取数据"""
        pass
    
    @abstractmethod
    def delete(self, key: str) -> bool:
        """删除数据"""
        pass
    
    @abstractmethod
    def exists(self, key: str) -> bool:
        """检查是否存在"""
        pass

