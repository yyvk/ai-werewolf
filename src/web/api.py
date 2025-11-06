"""
FastAPI Web服务
提供REST API接口
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict
import uuid
import asyncio

# 导入游戏引擎
from src.core.game_engine import WerewolfGame
from src.core.event_system import EventSystem
from src.agents import AgentFactory
from src.utils.config import get_config
from langchain_openai import ChatOpenAI

games_cache = {}
game_engines = {}  # 存储实际的游戏引擎实例


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
                "llm_provider": request.llm_provider,
                "players": [],
                "events": []
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
        
        game = games_cache[game_id]
        
        # 确保返回包含所需字段
        if 'players' not in game:
            game['players'] = []
        if 'events' not in game:
            game['events'] = []
        
        return game
    
    def create_llm():
        """创建LLM实例"""
        config = get_config()
        llm_config = config.get_llm_config()
        return ChatOpenAI(
            model=llm_config["model"],
            api_key=llm_config["api_key"],
            base_url=llm_config.get("base_url"),
            temperature=llm_config["temperature"],
            max_tokens=llm_config["max_tokens"]
        )
    
    async def run_game_round(game_id: str):
        """在后台运行游戏回合"""
        try:
            if game_id not in games_cache or game_id not in game_engines:
                return
            
            game_data = games_cache[game_id]
            game_engine = game_engines[game_id]
            agents = game_engine['agents']
            game = game_engine['game']
            
            # 增加轮次
            game.start_round()
            game_data['round'] = game.state.round
            
            # 讨论阶段
            game_data['phase'] = 'discussion'
            speeches = []
            
            for agent in agents:
                if agent.player.is_alive:
                    speech = agent.speak(game.state)
                    speeches.append({
                        'player_id': agent.player.id,
                        'player_name': agent.player.name,
                        'speech': speech,
                        'role': agent.player.role_name_cn
                    })
                    game.record_speech(agent.player.id, speech)
                    
                    # 添加到事件
                    event_text = f"[{agent.player.name}] {speech}"
                    game_data['events'].append(event_text)
            
            # 等待一小段时间（模拟讨论）
            await asyncio.sleep(1)
            
            # 投票阶段
            game_data['phase'] = 'voting'
            votes = {}
            
            for agent in agents:
                if agent.player.is_alive:
                    vote_to = agent.vote(game.state)
                    votes[agent.player.id] = vote_to
                    game.record_vote(agent.player.id, vote_to)
                    
                    event_text = f"[{agent.player.name}] 投票给 玩家{vote_to}"
                    game_data['events'].append(event_text)
            
            # 统计投票并淘汰
            if votes:
                vote_count = {}
                for vote_to in votes.values():
                    vote_count[vote_to] = vote_count.get(vote_to, 0) + 1
                
                eliminated_id = max(vote_count, key=vote_count.get)
                eliminated_player = next(p for p in game.state.players if p.id == eliminated_id)
                game.eliminate_player(eliminated_id, "投票")
                
                event_text = f"玩家{eliminated_id}({eliminated_player.name}-{eliminated_player.role_name_cn}) 被投票淘汰"
                game_data['events'].append(event_text)
            
            # 检查游戏是否结束
            winner = game.check_game_over()
            if winner:
                game_data['status'] = 'finished'
                game_data['phase'] = 'ended'
                game_data['winner'] = winner
                event_text = f"游戏结束！{winner}胜利！"
                game_data['events'].append(event_text)
            
            # 更新玩家状态
            game_data['players'] = [
                {
                    'id': p.id,
                    'name': p.name,
                    'role': p.role_name_cn,
                    'is_alive': p.is_alive
                }
                for p in game.state.players
            ]
            
        except Exception as e:
            print(f"Game round error: {e}")
            import traceback
            traceback.print_exc()
    
    @app.post("/api/games/{game_id}/start")
    async def start_game(game_id: str, background_tasks: BackgroundTasks):
        """开始游戏"""
        if game_id not in games_cache:
            raise HTTPException(status_code=404, detail="游戏不存在")
        
        game_data = games_cache[game_id]
        
        # 创建游戏引擎
        try:
            event_system = EventSystem()
            game = WerewolfGame(event_system)
            game.setup_game(num_players=game_data['num_players'])
            
            # 创建LLM和Agents
            llm = create_llm()
            agents = AgentFactory.create_batch_agents(game.state.players, llm)
            
            # 保存游戏引擎
            game_engines[game_id] = {
                'game': game,
                'agents': agents,
                'event_system': event_system
            }
            
            # 更新游戏状态
            game_data["status"] = "running"
            game_data["phase"] = "discussion"
            game_data["round"] = 0
            game_data["events"] = ["游戏开始！"]
            
            # 初始化玩家列表
            game_data['players'] = [
                {
                    'id': p.id,
                    'name': p.name,
                    'role': p.role_name_cn,
                    'is_alive': p.is_alive
                }
                for p in game.state.players
            ]
            
            # 在后台运行第一轮
            background_tasks.add_task(run_game_round, game_id)
            
            return {
                "success": True,
                "message": "游戏已开始，AI正在思考中..."
            }
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            raise HTTPException(status_code=500, detail=f"启动游戏失败: {str(e)}")
    
    @app.post("/api/games/{game_id}/next-round")
    async def next_round(game_id: str, background_tasks: BackgroundTasks):
        """进行下一轮"""
        if game_id not in games_cache:
            raise HTTPException(status_code=404, detail="游戏不存在")
        
        game_data = games_cache[game_id]
        
        if game_data['status'] != 'running':
            raise HTTPException(status_code=400, detail="游戏未在运行中")
        
        # 在后台运行下一轮
        background_tasks.add_task(run_game_round, game_id)
        
        return {
            "success": True,
            "message": "下一轮开始"
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

