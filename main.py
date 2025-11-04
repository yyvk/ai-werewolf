"""
AI狼人杀 - 主程序入口
"""

import sys
import argparse
from pathlib import Path

# 添加src到路径
sys.path.insert(0, str(Path(__file__).parent))

from src.core.models import Player, Role, GameState
from src.core.game_engine import WerewolfGame
from src.core.event_system import EventSystem, EventType
from src.agents import LangChainAgent, AgentFactory
from src.database import VectorDatabase, CacheDatabase, GameRepository
from src.utils.config import get_config
from src.utils.logger import setup_logger, GameLogger

from langchain_openai import ChatOpenAI


def create_llm(config):
    """创建LLM实例"""
    llm_config = config.get_llm_config()
    
    return ChatOpenAI(
        model=llm_config["model"],
        api_key=llm_config["api_key"],
        base_url=llm_config.get("base_url"),
        temperature=llm_config["temperature"],
        max_tokens=llm_config["max_tokens"]
    )


def run_console_game(num_rounds: int = 2):
    """运行控制台版游戏"""
    # 加载配置
    config = get_config()
    
    # 设置日志
    logger = setup_logger()
    logger.info("启动AI狼人杀游戏...")
    
    # 初始化数据库
    vector_db = VectorDatabase(config.db_vector_path)
    cache_db = CacheDatabase(config.db_cache_path)
    game_repo = GameRepository()
    
    vector_db.connect()
    cache_db.connect()
    
    # 创建事件系统
    event_system = EventSystem()
    
    # 创建游戏引擎
    game = WerewolfGame(event_system)
    game.setup_game(num_players=6)
    
    # 创建游戏日志
    game_logger = GameLogger(game.game_id)
    
    # 创建LLM
    try:
        llm = create_llm(config)
        logger.info(f"✅ LLM初始化成功: {config.llm_provider}")
    except Exception as e:
        logger.error(f"❌ LLM初始化失败: {e}")
        return
    
    # 创建Agent
    agents = AgentFactory.create_batch_agents(game.state.players, llm)
    logger.info(f"✅ 创建了 {len(agents)} 个AI Agent")
    
    print("\n" + "="*60)
    print("  AI狼人杀游戏")
    print("="*60)
    print(f"  游戏ID: {game.game_id}")
    print(f"  LLM: {config.llm_provider} - {config.get_llm_config()['model']}")
    print("="*60)
    
    # 显示玩家
    for player in game.state.players:
        print(f"  [{player.id}] {player.name} - {player.role_name_cn}")
    print()
    
    # 游戏主循环
    for round_num in range(1, num_rounds + 1):
        game.start_round()
        game_logger.log_event("round_start", {"round": round_num})
        
        print(f"\n{'='*60}")
        print(f"  第{round_num}轮 - 讨论阶段")
        print(f"{'='*60}\n")
        
        # 讨论阶段
        for agent in agents:
            if agent.player.is_alive:
                print(f"[{agent.player.id}] {agent.player.name} 发言：")
                speech = agent.speak(game.state)
                print(f"  {speech}\n")
                
                game.record_speech(agent.player.id, speech)
                game_logger.log_event("player_speak", {
                    "player_id": agent.player.id,
                    "player_name": agent.player.name,
                    "speech": speech
                })
        
        # 投票阶段
        game.change_phase(game.state.phase.__class__.VOTING)
        print(f"{'='*60}")
        print(f"  投票阶段")
        print(f"{'='*60}\n")
        
        votes = {}
        for agent in agents:
            if agent.player.is_alive:
                vote_to = agent.vote(game.state)
                votes[agent.player.id] = vote_to
                print(f"[{agent.player.id}] {agent.player.name} 投票给 {vote_to} 号")
                
                game.record_vote(agent.player.id, vote_to)
                game_logger.log_event("player_vote", {
                    "voter_id": agent.player.id,
                    "target_id": vote_to
                })
        
        # 统计投票
        vote_count = {}
        for vote_to in votes.values():
            vote_count[vote_to] = vote_count.get(vote_to, 0) + 1
        
        # 淘汰得票最多的玩家
        if vote_count:
            eliminated_id = max(vote_count, key=vote_count.get)
            game.eliminate_player(eliminated_id, "投票")
            game_logger.log_event("player_eliminated", {"player_id": eliminated_id})
        
        # 检查游戏是否结束
        winner = game.check_game_over()
        if winner:
            break
    
    # 游戏总结
    print("\n" + "="*60)
    print("  游戏总结")
    print("="*60)
    
    for agent in agents:
        status = "存活" if agent.player.is_alive else "淘汰"
        print(f"[{agent.player.id}] {agent.player.name} - {agent.player.role_name_cn} ({status})")
    
    print("="*60)
    
    # 保存游戏数据
    game_repo.save_game(game.state)
    game_logger.save_events()
    logger.info(f"游戏结束，数据已保存: {game.game_id}")
    
    # 保存游戏回放
    events = [e.to_dict() for e in event_system.get_history()]
    game_repo.save_game_replay(game.game_id, events)
    logger.info(f"游戏回放已保存: {game.game_id}")
    
    # 断开数据库连接
    vector_db.disconnect()
    cache_db.disconnect()


def run_web_server():
    """运行Web服务"""
    import uvicorn
    from src.web.api import create_app
    
    config = get_config()
    app = create_app()
    
    print(f"\n🌐 启动Web服务器...")
    print(f"   地址: http://{config.web_host}:{config.web_port}")
    print(f"   文档: http://{config.web_host}:{config.web_port}/docs")
    
    uvicorn.run(
        app,
        host=config.web_host,
        port=config.web_port
    )


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="AI狼人杀游戏")
    parser.add_argument(
        "--mode",
        choices=["console", "web"],
        default="console",
        help="运行模式：console（控制台）或 web（Web服务）"
    )
    parser.add_argument(
        "--rounds",
        type=int,
        default=2,
        help="游戏轮数（控制台模式）"
    )
    
    args = parser.parse_args()
    
    if args.mode == "console":
        run_console_game(args.rounds)
    elif args.mode == "web":
        run_web_server()


if __name__ == "__main__":
    main()

