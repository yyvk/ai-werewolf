"""
基于LangChain的Agent实现
"""

import re
from typing import Dict, Optional, AsyncGenerator
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from .base_agent import BaseAgent
from src.core.models import Player, GameState, Role


class LangChainAgent(BaseAgent):
    """LangChain AI Agent"""
    
    def __init__(self, player: Player, llm: ChatOpenAI):
        super().__init__(player)
        self.llm = llm
        self._setup_prompts()
    
    def _setup_prompts(self):
        """设置提示词模板"""
        # 系统提示词
        system_template = """你是一名狼人杀游戏玩家。

【你的信息】
玩家编号：{player_id}
玩家名称：{player_name}
你的角色：{role_name}
角色说明：{role_description}

【游戏规则】
1. 狼人的目标是消灭所有好人
2. 好人的目标是找出并投票淘汰所有狼人
3. 白天所有人发言和投票
4. 你需要根据角色特点进行策略性发言
5. 不要直接透露你的真实身份（除非策略需要）

【你的记忆】
{memory_summary}

请保持角色扮演，根据当前局势做出合理的推理和决策。"""

        self.system_prompt = system_template.format(
            player_id=self.player.id,
            player_name=self.player.name,
            role_name=self.player.role_name_cn,
            role_description=self.player.role_description,
            memory_summary="{memory_summary}"
        )
        
        # 发言提示模板
        self.speak_prompt = ChatPromptTemplate.from_messages([
            ("system", self.system_prompt),
            ("human", """当前游戏状态：
{game_state}

最近发生的事件：
{recent_events}

请基于当前局势，发表一段简短的发言（2-3句话）。
注意：要符合你的角色身份，进行策略性发言。""")
        ])
        
        # 投票提示模板
        self.vote_prompt = ChatPromptTemplate.from_messages([
            ("system", self.system_prompt),
            ("human", """当前游戏状态：
{game_state}

最近发生的事件：
{recent_events}

存活的玩家ID：{alive_players}

现在需要投票淘汰一名玩家。
请分析局势并选择你要投票的玩家编号。
只需回复一个数字，不要有其他内容。""")
        ])
    
    def think(self, game_state: GameState) -> str:
        """思考当前局势"""
        try:
            think_prompt = ChatPromptTemplate.from_messages([
                ("system", self.system_prompt),
                ("human", """当前游戏状态：
{game_state}

最近发生的事件：
{recent_events}

请分析当前局势，思考你的策略。""")
            ])
            
            chain = think_prompt | self.llm | StrOutputParser()
            
            response = chain.invoke({
                "memory_summary": self.get_memory_summary(),
                "game_state": self._format_game_state(game_state),
                "recent_events": self._format_events(game_state.events)
            })
            
            return response.strip()
        except Exception as e:
            print(f"  ⚠️ 思考失败: {e}")
            return "我需要更多时间观察局势。"
    
    def speak(self, game_state: GameState) -> str:
        """发言"""
        try:
            chain = self.speak_prompt | self.llm | StrOutputParser()
            
            response = chain.invoke({
                "memory_summary": self.get_memory_summary(),
                "game_state": self._format_game_state(game_state),
                "recent_events": self._format_events(game_state.events)
            })
            
            # 记录观察
            self.observe(f"我在第{game_state.round}轮发言了")
            
            return response.strip()
        except Exception as e:
            print(f"  ⚠️ LLM调用失败: {e}")
            return self._fallback_speak()
    
    async def speak_stream(self, game_state: GameState) -> AsyncGenerator[str, None]:
        """流式发言"""
        try:
            chain = self.speak_prompt | self.llm | StrOutputParser()
            
            # 使用 LangChain 的流式 API
            full_response = ""
            async for chunk in chain.astream({
                "memory_summary": self.get_memory_summary(),
                "game_state": self._format_game_state(game_state),
                "recent_events": self._format_events(game_state.events)
            }):
                full_response += chunk
                yield chunk
            
            # 记录观察
            self.observe(f"我在第{game_state.round}轮发言了")
            
        except Exception as e:
            print(f"  ⚠️ LLM流式调用失败: {e}")
            # 降级处理：直接返回完整文本
            fallback_text = self._fallback_speak()
            for char in fallback_text:
                yield char
    
    def vote(self, game_state: GameState) -> int:
        """投票"""
        try:
            alive_players = [p.id for p in game_state.get_alive_players() 
                           if p.id != self.player.id]
            
            if not alive_players:
                return self.player.id
            
            chain = self.vote_prompt | self.llm | StrOutputParser()
            
            response = chain.invoke({
                "memory_summary": self.get_memory_summary(),
                "game_state": self._format_game_state(game_state),
                "recent_events": self._format_events(game_state.events),
                "alive_players": ", ".join(map(str, alive_players))
            })
            
            # 解析投票结果
            numbers = re.findall(r'\d+', response)
            if numbers:
                vote_id = int(numbers[0])
                if vote_id in alive_players:
                    self.observe(f"我在第{game_state.round}轮投票给{vote_id}号")
                    return vote_id
            
            # 如果解析失败，返回第一个存活玩家
            return alive_players[0]
            
        except Exception as e:
            print(f"  ⚠️ 投票失败: {e}")
            # 降级：随机选择
            alive_players = [p.id for p in game_state.get_alive_players() 
                           if p.id != self.player.id]
            return alive_players[0] if alive_players else self.player.id
    
    def _format_game_state(self, game_state: GameState) -> str:
        """格式化游戏状态"""
        lines = [
            f"回合数：{game_state.round}",
            f"阶段：{game_state.phase.value}",
            "",
            "存活玩家："
        ]
        
        for p in game_state.get_alive_players():
            lines.append(f"  - {p.id}号 {p.name}")
        
        return "\n".join(lines)
    
    def _format_events(self, events: list) -> str:
        """格式化事件"""
        if not events:
            return "暂无事件"
        return "\n".join(f"  - {event}" for event in events[-5:])
    
    def _fallback_speak(self) -> str:
        """降级发言（LLM失败时使用）"""
        fallback_speeches = {
            Role.WEREWOLF: "根据目前的信息，我觉得需要仔细观察每个人的发言。",
            Role.VILLAGER: "我是好人，希望大家能理性分析，找出真正的狼人。",
            Role.SEER: "我观察了一些线索，但现在还不能确定。",
            Role.WITCH: "我会谨慎使用我的能力，现在先观察局势。",
            Role.HUNTER: "作为一名玩家，我会认真分析每个人的行为。"
        }
        return fallback_speeches.get(self.player.role, "我需要更多时间思考。")

