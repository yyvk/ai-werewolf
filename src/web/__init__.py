"""
Web服务模块
提供HTTP API和WebSocket支持
"""

from .api import create_app
from .websocket import WebSocketManager

__all__ = [
    'create_app',
    'WebSocketManager',
]

