"""
FastAPI Web服务
提供REST API接口
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional, Dict, AsyncGenerator
import uuid
import asyncio
import json
from pathlib import Path

# 导入游戏引擎
from src.core.game_engine import WerewolfGame
from src.core.event_system import EventSystem
from src.agents import AgentFactory
from src.utils.config import get_config
from src.utils.tts_service_dashscope import get_dashscope_tts_service
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
    
    # 添加静态文件服务（用于提供音频文件）
    audio_dir = Path(__file__).parent.parent.parent / "assets" / "audio"
    audio_dir.mkdir(parents=True, exist_ok=True)
    app.mount("/audio", StaticFiles(directory=str(audio_dir)), name="audio")
    
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
    
    async def stream_game_round(game_id: str) -> AsyncGenerator[str, None]:
        """流式运行游戏回合"""
        try:
            if game_id not in games_cache or game_id not in game_engines:
                yield f"data: {json.dumps({'type': 'error', 'message': '游戏不存在'})}\n\n"
                return
            
            game_data = games_cache[game_id]
            game_engine = game_engines[game_id]
            agents = game_engine['agents']
            game = game_engine['game']
            
            # 增加轮次
            game.start_round()
            game_data['round'] = game.state.round
            
            yield f"data: {json.dumps({'type': 'round_start', 'round': game.state.round})}\n\n"
            await asyncio.sleep(0.1)
            
            # 讨论阶段
            game_data['phase'] = 'discussion'
            yield f"data: {json.dumps({'type': 'phase_change', 'phase': 'discussion'})}\n\n"
            await asyncio.sleep(0.3)
            
            # 每个玩家发言
            for agent in agents:
                if agent.player.is_alive:
                    # 发送玩家开始发言的通知
                    yield f"data: {json.dumps({'type': 'speech_start', 'player_id': agent.player.id, 'player_name': agent.player.name, 'role': agent.player.role_name_cn})}\n\n"
                    await asyncio.sleep(0.3)
                    
                    # 获取发言（流式）
                    full_speech = ""
                    
                    # 流式输出文字
                    async for chunk in agent.speak_stream(game.state):
                        full_speech += chunk
                        yield f"data: {json.dumps({'type': 'speech_chunk', 'player_id': agent.player.id, 'chunk': chunk})}\n\n"
                        await asyncio.sleep(0.05)  # 控制打字速度
                    
                    # 文字输出完成后，生成并发送音频
                    config = get_config()
                    if config.tts_enabled and full_speech:
                        try:
                            print(f"[TTS] Starting audio generation for player {agent.player.id}, text length: {len(full_speech)}")
                            tts_service = get_dashscope_tts_service()
                            
                            # 生成音频并发送
                            audio_chunks_sent = 0
                            async for audio_chunk in tts_service.text_to_speech_stream(full_speech, agent.player.id):
                                if audio_chunk:
                                    audio_chunks_sent += 1
                                    yield f"data: {json.dumps({'type': 'audio_chunk', 'player_id': agent.player.id, 'audio_data': audio_chunk})}\n\n"
                                    print(f"[TTS] Sent audio chunk {audio_chunks_sent} for player {agent.player.id}, size: {len(audio_chunk)} bytes")
                                    await asyncio.sleep(0)
                                else:
                                    print(f"[TTS] Warning: Empty audio chunk for player {agent.player.id}")
                            
                            yield f"data: {json.dumps({'type': 'audio_end', 'player_id': agent.player.id})}\n\n"
                            print(f"[TTS] Audio generation completed for player {agent.player.id}, total chunks: {audio_chunks_sent}")
                        except Exception as e:
                            print(f"[TTS] Failed to generate audio for player {agent.player.id}: {e}")
                            import traceback
                            traceback.print_exc()
                            # 发送错误事件
                            yield f"data: {json.dumps({'type': 'error', 'message': f'TTS generation failed: {str(e)}'})}\n\n"
                    
                    # 发言结束，记录事件
                    game.record_speech(agent.player.id, full_speech)
                    event_text = f"[{agent.player.name}] {full_speech}"
                    game_data['events'].append(event_text)
                    
                    # 发送发言结束事件
                    yield f"data: {json.dumps({'type': 'speech_end', 'player_id': agent.player.id, 'speech': full_speech})}\n\n"
                    await asyncio.sleep(0.3)
            
            # 投票阶段
            game_data['phase'] = 'voting'
            yield f"data: {json.dumps({'type': 'phase_change', 'phase': 'voting'})}\n\n"
            await asyncio.sleep(0.5)
            
            votes = {}
            for agent in agents:
                if agent.player.is_alive:
                    vote_to = agent.vote(game.state)
                    votes[agent.player.id] = vote_to
                    game.record_vote(agent.player.id, vote_to)
                    
                    event_text = f"[{agent.player.name}] 投票给 玩家{vote_to}"
                    game_data['events'].append(event_text)
                    
                    yield f"data: {json.dumps({'type': 'vote', 'player_id': agent.player.id, 'vote_to': vote_to, 'player_name': agent.player.name})}\n\n"
                    await asyncio.sleep(0.3)
            
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
                
                yield f"data: {json.dumps({'type': 'elimination', 'player_id': eliminated_id, 'player_name': eliminated_player.name, 'role': eliminated_player.role_name_cn})}\n\n"
                await asyncio.sleep(0.5)
            
            # 检查游戏是否结束
            winner = game.check_game_over()
            if winner:
                game_data['status'] = 'finished'
                game_data['phase'] = 'ended'
                game_data['winner'] = winner
                event_text = f"游戏结束！{winner}胜利！"
                game_data['events'].append(event_text)
                
                yield f"data: {json.dumps({'type': 'game_end', 'winner': winner})}\n\n"
            
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
            
            # 发送完成事件（使用自定义事件类型）
            yield f"event: complete\ndata: {json.dumps({'type': 'complete', 'game_data': game_data})}\n\n"
            
        except Exception as e:
            print(f"Game round error: {e}")
            import traceback
            traceback.print_exc()
            yield f"data: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"
    
    @app.post("/api/games/{game_id}/start")
    async def start_game(game_id: str):
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
            
            # 不再在后台运行，让前端通过流式API来获取
            return {
                "success": True,
                "message": "游戏已开始，准备进入第一轮..."
            }
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            raise HTTPException(status_code=500, detail=f"启动游戏失败: {str(e)}")
    
    @app.get("/api/games/{game_id}/stream-round")
    async def stream_round(game_id: str):
        """流式进行下一轮游戏"""
        if game_id not in games_cache:
            raise HTTPException(status_code=404, detail="游戏不存在")
        
        game_data = games_cache[game_id]
        
        if game_data['status'] != 'running':
            raise HTTPException(status_code=400, detail="游戏未在运行中")
        
        return StreamingResponse(
            stream_game_round(game_id),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "X-Accel-Buffering": "no"
            }
        )
    
    @app.post("/api/games/{game_id}/next-round")
    async def next_round(game_id: str):
        """触发下一轮游戏（非流式，用于兼容）"""
        if game_id not in games_cache:
            raise HTTPException(status_code=404, detail="游戏不存在")
        
        game_data = games_cache[game_id]
        
        if game_data['status'] != 'running':
            raise HTTPException(status_code=400, detail="游戏未在运行中")
        
        return {
            "success": True,
            "message": "请使用 /api/games/{game_id}/stream-round 接口获取流式更新"
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

