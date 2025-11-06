"""
基于LangChain的Agent实现
采用LangChain标准模式和最佳实践
"""

import re
from typing import Dict, Optional, AsyncGenerator, List
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.runnables import RunnablePassthrough, RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory

from .base_agent import BaseAgent
from src.core.models import Player, GameState, Role


class LangChainAgent(BaseAgent):
    """
    LangChain AI Agent
    
    采用LangChain标准模式：
    - 使用 ChatPromptTemplate 管理提示词
    - 使用 MessageHistory 管理对话历史
    - 使用 LCEL (LangChain Expression Language) 构建链
    - 支持流式输出
    """
    
    def __init__(self, player: Player, llm: BaseChatModel, enable_memory: bool = True):
        """
        初始化 LangChain Agent
        
        Args:
            player: 玩家对象
            llm: LangChain LLM 实例
            enable_memory: 是否启用对话记忆
        """
        super().__init__(player)
        self.llm = llm
        self.enable_memory = enable_memory
        
        # 初始化消息历史
        self.message_history = ChatMessageHistory()
        
        # 设置提示词模板
        self._setup_prompts()
        
        # 设置链
        self._setup_chains()
    
    def _setup_prompts(self):
        """设置提示词模板"""
        
        # 系统提示词
        self.system_message = f"""你是一名狼人杀游戏玩家。

【你的信息】
玩家编号：{self.player.id}
玩家名称：{self.player.name}
你的角色：{self.player.role_name_cn}
角色说明：{self.player.role_description}

【游戏规则】
1. 狼人的目标是消灭所有好人
2. 好人的目标是找出并投票淘汰所有狼人
3. 白天所有人发言和投票
4. 你需要根据角色特点进行策略性发言
5. 不要直接透露你的真实身份（除非策略需要）

【你的策略】
- 如果你是狼人：隐藏身份，误导好人，保护队友
- 如果你是预言家：谨慎透露身份，引导投票方向
- 如果你是女巫：合理使用解药和毒药
- 如果你是猎人：威慑狼人，关键时刻发挥作用
- 如果你是村民：通过逻辑推理，找出可疑玩家

请保持角色扮演，根据当前局势做出合理的推理和决策。"""
        
        # 思考提示模板
        self.think_prompt = ChatPromptTemplate.from_messages([
            ("system", self.system_message),
            MessagesPlaceholder(variable_name="history", optional=True),
            ("human", """当前游戏状态：
{game_state}

最近发生的事件：
{recent_events}

你的记忆：
{memory_summary}

请分析当前局势，思考你的策略。""")
        ])
        
        # 发言提示模板
        self.speak_prompt = ChatPromptTemplate.from_messages([
            ("system", self.system_message),
            MessagesPlaceholder(variable_name="history", optional=True),
            ("human", """当前游戏状态：
{game_state}

最近发生的事件：
{recent_events}

你的记忆：
{memory_summary}

请基于当前局势，发表一段简短的发言（2-3句话）。
注意：
1. 要符合你的角色身份，进行策略性发言
2. 语言要简洁、自然、口语化
3. 不要透露过多信息，保持神秘感""")
        ])
        
        # 投票提示模板
        self.vote_prompt = ChatPromptTemplate.from_messages([
            ("system", self.system_message),
            MessagesPlaceholder(variable_name="history", optional=True),
            ("human", """当前游戏状态：
{game_state}

最近发生的事件：
{recent_events}

你的记忆：
{memory_summary}

存活的玩家ID：{alive_players}

现在需要投票淘汰一名玩家。
请分析局势并选择你要投票的玩家编号。

要求：
1. 只回复一个数字（玩家编号）
2. 不要有其他内容
3. 必须是存活玩家的编号""")
        ])
    
    def _setup_chains(self):
        """设置 LangChain 链"""
        
        # 思考链
        self.think_chain = (
            self.think_prompt 
            | self.llm 
            | StrOutputParser()
        )
        
        # 发言链
        self.speak_chain = (
            self.speak_prompt 
            | self.llm 
            | StrOutputParser()
        )
        
        # 投票链
        self.vote_chain = (
            self.vote_prompt 
            | self.llm 
            | StrOutputParser()
        )
    
    def _get_chain_inputs(self, game_state: GameState) -> Dict:
        """
        获取链的输入参数
        
        Args:
            game_state: 游戏状态
        
        Returns:
            输入参数字典
        """
        inputs = {
            "game_state": self._format_game_state(game_state),
            "recent_events": self._format_events(game_state.events),
            "memory_summary": self.get_memory_summary(),
        }
        
        # 如果启用记忆，添加历史消息
        if self.enable_memory:
            inputs["history"] = self.message_history.messages
        
        return inputs
    
    def think(self, game_state: GameState) -> str:
        """
        思考当前局势
        
        Args:
            game_state: 游戏状态
        
        Returns:
            思考内容
        """
        try:
            inputs = self._get_chain_inputs(game_state)
            response = self.think_chain.invoke(inputs)
            
            # 记录到消息历史
            if self.enable_memory:
                self.message_history.add_user_message(f"分析局势：{inputs['game_state']}")
                self.message_history.add_ai_message(response)
            
            return response.strip()
        
        except Exception as e:
            print(f"  ⚠️ 思考失败: {e}")
            return "我需要更多时间观察局势。"
    
    def speak(self, game_state: GameState) -> str:
        """
        发言
        
        Args:
            game_state: 游戏状态
        
        Returns:
            发言内容
        """
        try:
            inputs = self._get_chain_inputs(game_state)
            response = self.speak_chain.invoke(inputs)
            
            # 记录观察
            self.observe(f"我在第{game_state.round}轮发言了")
            
            # 记录到消息历史
            if self.enable_memory:
                self.message_history.add_user_message(f"第{game_state.round}轮发言")
                self.message_history.add_ai_message(response)
            
            return response.strip()
        
        except Exception as e:
            print(f"  ⚠️ LLM调用失败: {e}")
            return self._fallback_speak()
    
    async def speak_stream(self, game_state: GameState) -> AsyncGenerator[str, None]:
        """
        流式发言
        
        Args:
            game_state: 游戏状态
        
        Yields:
            发言内容的文本块
        """
        try:
            inputs = self._get_chain_inputs(game_state)
            
            # 使用 LangChain 的流式 API
            full_response = ""
            
            async for chunk in self.speak_chain.astream(inputs):
                full_response += chunk
                yield chunk
            
            # 记录观察
            self.observe(f"我在第{game_state.round}轮发言了")
            
            # 记录到消息历史
            if self.enable_memory:
                self.message_history.add_user_message(f"第{game_state.round}轮发言")
                self.message_history.add_ai_message(full_response)
        
        except Exception as e:
            print(f"  ⚠️ LLM流式调用失败: {e}")
            # 降级处理：直接返回完整文本
            fallback_text = self._fallback_speak()
            for char in fallback_text:
                yield char
    
    def vote(self, game_state: GameState) -> int:
        """
        投票
        
        Args:
            game_state: 游戏状态
        
        Returns:
            投票的玩家ID
        """
        try:
            alive_players = [
                p.id for p in game_state.get_alive_players() 
                if p.id != self.player.id
            ]
            
            if not alive_players:
                return self.player.id
            
            inputs = self._get_chain_inputs(game_state)
            inputs["alive_players"] = ", ".join(map(str, alive_players))
            
            response = self.vote_chain.invoke(inputs)
            
            # 解析投票结果
            numbers = re.findall(r'\d+', response)
            if numbers:
                vote_id = int(numbers[0])
                if vote_id in alive_players:
                    self.observe(f"我在第{game_state.round}轮投票给{vote_id}号")
                    
                    # 记录到消息历史
                    if self.enable_memory:
                        self.message_history.add_user_message(f"第{game_state.round}轮投票")
                        self.message_history.add_ai_message(f"投票给{vote_id}号")
                    
                    return vote_id
            
            # 如果解析失败，返回第一个存活玩家
            fallback_vote = alive_players[0]
            print(f"  ⚠️ 投票解析失败，默认投给{fallback_vote}号")
            return fallback_vote
        
        except Exception as e:
            print(f"  ⚠️ 投票失败: {e}")
            # 降级：随机选择
            alive_players = [
                p.id for p in game_state.get_alive_players() 
                if p.id != self.player.id
            ]
            return alive_players[0] if alive_players else self.player.id
    
    def _format_game_state(self, game_state: GameState) -> str:
        """
        格式化游戏状态
        
        Args:
            game_state: 游戏状态
        
        Returns:
            格式化的游戏状态文本
        """
        lines = [
            f"回合数：{game_state.round}",
            f"阶段：{game_state.phase.value}",
            "",
            "存活玩家："
        ]
        
        for p in game_state.get_alive_players():
            lines.append(f"  - {p.id}号 {p.name}")
        
        # 添加已淘汰玩家信息
        eliminated = [p for p in game_state.players if not p.is_alive]
        if eliminated:
            lines.append("")
            lines.append("已淘汰玩家：")
            for p in eliminated:
                lines.append(f"  - {p.id}号 {p.name}")
        
        return "\n".join(lines)
    
    def _format_events(self, events: List[str]) -> str:
        """
        格式化事件
        
        Args:
            events: 事件列表
        
        Returns:
            格式化的事件文本
        """
        if not events:
            return "暂无事件"
        
        # 只显示最近5个事件
        recent_events = events[-5:]
        return "\n".join(f"  - {event}" for event in recent_events)
    
    def _fallback_speak(self) -> str:
        """
        降级发言（LLM失败时使用）
        
        Returns:
            后备发言内容
        """
        fallback_speeches = {
            Role.WEREWOLF: "根据目前的信息，我觉得需要仔细观察每个人的发言。",
            Role.VILLAGER: "我是好人，希望大家能理性分析，找出真正的狼人。",
            Role.SEER: "我观察了一些线索，但现在还不能确定。",
            Role.WITCH: "我会谨慎使用我的能力，现在先观察局势。",
            Role.HUNTER: "作为一名玩家，我会认真分析每个人的行为。"
        }
        return fallback_speeches.get(self.player.role, "我需要更多时间思考。")
    
    def clear_history(self):
        """清除对话历史"""
        self.message_history.clear()
    
    def get_message_count(self) -> int:
        """获取消息数量"""
        return len(self.message_history.messages)
    
    def to_dict(self) -> Dict:
        """
        转换为字典
        
        Returns:
            字典表示
        """
        base_dict = super().to_dict()
        
        # 添加消息历史
        if self.enable_memory:
            base_dict["message_history"] = [
                {
                    "type": msg.type,
                    "content": msg.content
                }
                for msg in self.message_history.messages
            ]
        
        return base_dict
