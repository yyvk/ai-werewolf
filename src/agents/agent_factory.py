"""
Agent工厂
用于创建不同类型的Agent，支持多种LLM提供商

支持的LLM提供商：
- OpenAI (gpt-4, gpt-3.5-turbo等)
- DashScope (通义千问)
- ModelScope (免费推理服务)
- Anthropic (Claude系列)
"""

from typing import Optional, List
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_openai import ChatOpenAI

from .base_agent import BaseAgent
from .langchain_agent import LangChainAgent
from src.core.models import Player
from src.utils.config import get_config


class LLMFactory:
    """LLM工厂类 - 用于创建不同提供商的LLM实例"""
    
    @staticmethod
    def create_llm(provider: Optional[str] = None, **kwargs) -> BaseChatModel:
        """
        创建LLM实例
        
        Args:
            provider: LLM提供商（openai, dashscope, modelscope, anthropic）
                     如果为None，使用配置文件中的默认提供商
            **kwargs: 额外的LLM参数（会覆盖配置文件中的参数）
        
        Returns:
            LangChain BaseChatModel 实例
        
        Raises:
            ValueError: 如果提供商不支持或配置无效
        """
        config = get_config()
        provider = provider or config.llm_provider
        
        # 获取提供商配置
        llm_config = config.get_llm_config(provider)
        
        # 合并用户提供的参数
        llm_config.update(kwargs)
        
        # 根据提供商创建LLM
        if provider in ["openai", "dashscope", "modelscope"]:
            return LLMFactory._create_openai_compatible_llm(llm_config)
        
        elif provider == "anthropic":
            return LLMFactory._create_anthropic_llm(llm_config)
        
        else:
            raise ValueError(f"不支持的LLM提供商: {provider}")
    
    @staticmethod
    def _create_openai_compatible_llm(config: dict) -> ChatOpenAI:
        """
        创建OpenAI兼容的LLM实例
        支持: OpenAI, DashScope, ModelScope
        
        Args:
            config: LLM配置
        
        Returns:
            ChatOpenAI 实例
        """
        # 验证必需参数
        if not config.get("api_key"):
            raise ValueError(f"缺少API Key: {config.get('provider')}")
        
        if not config.get("model"):
            raise ValueError(f"缺少模型名称: {config.get('provider')}")
        
        # 创建 ChatOpenAI 实例
        llm_params = {
            "model": config["model"],
            "api_key": config["api_key"],
            "temperature": config.get("temperature", 0.8),
            "max_tokens": config.get("max_tokens", 500),
            "timeout": config.get("timeout", 60),
        }
        
        # 添加 base_url（如果提供）
        if config.get("base_url"):
            llm_params["base_url"] = config["base_url"]
        
        # 流式输出
        if config.get("streaming"):
            llm_params["streaming"] = True
        
        print(f"✅ 创建LLM实例: {config.get('provider')} - {config['model']}")
        
        return ChatOpenAI(**llm_params)
    
    @staticmethod
    def _create_anthropic_llm(config: dict) -> BaseChatModel:
        """
        创建Anthropic (Claude) LLM实例
        
        Args:
            config: LLM配置
        
        Returns:
            ChatAnthropic 实例
        """
        try:
            from langchain_anthropic import ChatAnthropic
        except ImportError:
            raise ImportError(
                "请安装 langchain-anthropic: pip install langchain-anthropic"
            )
        
        # 验证必需参数
        if not config.get("api_key"):
            raise ValueError("缺少Anthropic API Key")
        
        if not config.get("model"):
            raise ValueError("缺少Anthropic模型名称")
        
        llm_params = {
            "model": config["model"],
            "anthropic_api_key": config["api_key"],
            "temperature": config.get("temperature", 0.8),
            "max_tokens": config.get("max_tokens", 500),
            "timeout": config.get("timeout", 60),
        }
        
        print(f"✅ 创建LLM实例: Anthropic - {config['model']}")
        
        return ChatAnthropic(**llm_params)


class AgentFactory:
    """Agent工厂类 - 用于创建不同类型的Agent"""
    
    @staticmethod
    def create_agent(
        player: Player, 
        llm: Optional[BaseChatModel] = None,
        provider: Optional[str] = None,
        enable_memory: bool = True,
        **kwargs
    ) -> BaseAgent:
        """
        创建Agent
        
        Args:
            player: 玩家对象
            llm: LLM实例（如果为None，会自动创建）
            provider: LLM提供商（如果llm为None时使用）
            enable_memory: 是否启用对话记忆
            **kwargs: 额外的Agent参数
        
        Returns:
            BaseAgent 实例
        """
        # 如果没有提供LLM，创建一个
        if llm is None:
            llm = LLMFactory.create_llm(provider)
        
        # 创建 LangChain Agent
        return LangChainAgent(
            player=player, 
            llm=llm,
            enable_memory=enable_memory,
            **kwargs
        )
    
    @staticmethod
    def create_langchain_agent(
        player: Player, 
        llm: BaseChatModel,
        enable_memory: bool = True
    ) -> LangChainAgent:
        """
        创建LangChain Agent（兼容旧接口）
        
        Args:
            player: 玩家对象
            llm: LLM实例
            enable_memory: 是否启用对话记忆
        
        Returns:
            LangChainAgent 实例
        """
        return LangChainAgent(player, llm, enable_memory)
    
    @staticmethod
    def create_batch_agents(
        players: List[Player], 
        llm: Optional[BaseChatModel] = None,
        provider: Optional[str] = None,
        enable_memory: bool = True,
        **kwargs
    ) -> List[BaseAgent]:
        """
        批量创建Agent
        
        Args:
            players: 玩家列表
            llm: LLM实例（如果为None，会自动创建并复用）
            provider: LLM提供商（如果llm为None时使用）
            enable_memory: 是否启用对话记忆
            **kwargs: 额外的Agent参数
        
        Returns:
            Agent列表
        """
        # 如果没有提供LLM，创建一个并复用
        if llm is None:
            llm = LLMFactory.create_llm(provider)
        
        # 为每个玩家创建Agent
        agents = []
        for player in players:
            agent = AgentFactory.create_agent(
                player=player,
                llm=llm,
                enable_memory=enable_memory,
                **kwargs
            )
            agents.append(agent)
        
        print(f"✅ 批量创建了 {len(agents)} 个Agent")
        
        return agents


def create_llm_from_config(config_name: Optional[str] = None) -> BaseChatModel:
    """
    从配置创建LLM实例（便捷函数）
    
    Args:
        config_name: 配置名称（如果为None，使用默认配置）
    
    Returns:
        BaseChatModel 实例
    """
    return LLMFactory.create_llm(config_name)


def create_agent_from_config(
    player: Player,
    config_name: Optional[str] = None,
    **kwargs
) -> BaseAgent:
    """
    从配置创建Agent实例（便捷函数）
    
    Args:
        player: 玩家对象
        config_name: 配置名称（如果为None，使用默认配置）
        **kwargs: 额外的Agent参数
    
    Returns:
        BaseAgent 实例
    """
    return AgentFactory.create_agent(player, provider=config_name, **kwargs)
