from typing import Dict, Any, Tuple
import json
import logging
from abc import ABC, abstractmethod
from typing import Optional

from .exceptions import ModelExecutionError

logger = logging.getLogger(__name__)

class BaseExecutor(ABC):
    """
    大模型执行层基类。负责接收 Prompt 并调用 LLM 服务，必须返回纯文本。
    """
    
    @abstractmethod
    def execute(self, system_prompt: str, user_prompt: str, temperature: float = 0.2, max_tokens: int = 4096) -> str:
        """
        核心调用方法，需被具体模型提供商（OpenAI, Gemini 等）实现
        """
        pass

class MockExecutor(BaseExecutor):
    """
    一个简单的桩类，用来在不连外网时测试主流程
    """
    def __init__(self, mock_response: str = ""):
        self.mock_response = mock_response or """
{
  "artifact_type": "PRD_Brief",
  "project_name": "Mock Project",
  "background": ["Mock Background"],
  "goals": ["Mock Goal"],
  "constraints": ["Mock Constraint"]
}
{
  "task_goal": "Goal",
  "key_findings": ["Finding"],
  "unresolved_items": [],
  "artifact_ids": ["mock_id"],
  "next_recommended_action": "Mock Action"
}
"""
    
    def execute(self, system_prompt: str, user_prompt: str, temperature: float = 0.2, max_tokens: int = 4096) -> str:
        logger.info(f"MockExecutor received prompt. System length: {len(system_prompt)}, User length: {len(user_prompt)}")
        return self.mock_response
