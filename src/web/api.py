"""
FastAPI Web服务
提供REST API接口
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict
import uuid

games_cache = {}


def create_app() -> FastAPI:
    """创建FastAPI应用"""
    app = FastAPI(
        title="AI狼人杀API",
        description="AI Werewolf Game API",
        version="1.0.0"
    )
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    class GameCreateRequest(BaseModel):
        """创建游戏请求"""
        num_players: int = 6
        llm_provider: str = "modelscope"
        model_name: Optional[str] = None
    
    class GameResponse(BaseModel):
        """游戏响应"""
        game_id: str
        status: str
        round: int
        phase: str
        players: List[Dict]
        events: List[str]
    
    @app.get("/")
    async def root():
        """根路径"""
        return {
            "message": "AI狼人杀API",
            "version": "1.0.0",
            "docs": "/docs"
        }
    
    @app.get("/health")
    async def health_check():
        """健康检查"""
        return {"status": "healthy"}
    
    @app.post("/api/games", response_model=Dict)
    async def create_game(request: GameCreateRequest):
        """创建新游戏"""
        try:
            game_id = str(uuid.uuid4())
            
            game_data = {
                "game_id": game_id,
                "status": "created",
                "round": 0,
                "phase": "waiting",
                "num_players": request.num_players,
                "llm_provider": request.llm_provider
            }
            
            games_cache[game_id] = game_data
            
            return {
                "success": True,
                "game_id": game_id,
                "message": "游戏创建成功"
            }
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    @app.get("/api/games/{game_id}")
    async def get_game(game_id: str):
        """获取游戏状态"""
        if game_id not in games_cache:
            raise HTTPException(status_code=404, detail="游戏不存在")
        
        return games_cache[game_id]
    
    @app.post("/api/games/{game_id}/start")
    async def start_game(game_id: str):
        """开始游戏"""
        if game_id not in games_cache:
            raise HTTPException(status_code=404, detail="游戏不存在")
        
        game = games_cache[game_id]
        game["status"] = "running"
        game["phase"] = "discussion"
        
        return {
            "success": True,
            "message": "游戏已开始"
        }
    
    @app.post("/api/games/{game_id}/action")
    async def game_action(game_id: str, action: Dict):
        """执行游戏操作"""
        if game_id not in games_cache:
            raise HTTPException(status_code=404, detail="游戏不存在")
        
        return {
            "success": True,
            "message": f"操作 {action.get('type')} 已执行"
        }
    
    @app.get("/api/games")
    async def list_games():
        """列出所有游戏"""
        return {
            "games": list(games_cache.values()),
            "total": len(games_cache)
        }
    
    @app.delete("/api/games/{game_id}")
    async def delete_game(game_id: str):
        """删除游戏"""
        if game_id in games_cache:
            del games_cache[game_id]
        
        return {
            "success": True,
            "message": "游戏已删除"
        }
    
    @app.get("/api/stats")
    async def get_stats():
        """获取统计信息"""
        return {
            "total_games": len(games_cache),
            "active_games": sum(1 for g in games_cache.values() if g.get("status") == "running")
        }
    
    return app


if __name__ == "__main__":
    import uvicorn
    app = create_app()
    uvicorn.run(app, host="0.0.0.0", port=8000)

