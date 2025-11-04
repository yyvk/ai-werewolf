"""
WebSocket管理
实时推送游戏状态更新
"""

from typing import Dict, List
from fastapi import WebSocket


class WebSocketManager:
    """WebSocket连接管理器"""
    
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}
    
    async def connect(self, websocket: WebSocket, game_id: str):
        """接受新连接"""
        await websocket.accept()
        if game_id not in self.active_connections:
            self.active_connections[game_id] = []
        self.active_connections[game_id].append(websocket)
    
    def disconnect(self, websocket: WebSocket, game_id: str):
        """断开连接"""
        if game_id in self.active_connections:
            self.active_connections[game_id].remove(websocket)
    
    async def broadcast(self, game_id: str, message: dict):
        """广播消息到所有连接"""
        if game_id in self.active_connections:
            for connection in self.active_connections[game_id]:
                try:
                    await connection.send_json(message)
                except Exception as e:
                    print(f"WebSocket send error: {e}")
    
    async def send_to_player(self, websocket: WebSocket, message: dict):
        """发送消息给特定玩家"""
        try:
            await websocket.send_json(message)
        except Exception as e:
            print(f"WebSocket send error: {e}")

