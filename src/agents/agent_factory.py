"""
Agent工厂
用于创建不同类型的Agent
"""

from typing import Optional
from langchain_openai import ChatOpenAI

from .base_agent import BaseAgent
from .langchain_agent import LangChainAgent
from src.core.models import Player


class AgentFactory:
    """Agent工厂类"""
    
    @staticmethod
    def create_langchain_agent(player: Player, llm: ChatOpenAI) -> LangChainAgent:
        """创建LangChain Agent"""
        return LangChainAgent(player, llm)
    
    @staticmethod
    def create_batch_agents(players: list, llm: ChatOpenAI) -> list:
        """批量创建Agent"""
        return [AgentFactory.create_langchain_agent(player, llm) for player in players]

