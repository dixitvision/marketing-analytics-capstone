"""Agent implementations for the AI Agent Company."""

from ai_agent_company.agents.base import AgentRole, AgentStatus, BaseAgent, Task, TaskResult
from ai_agent_company.agents.marketing import MarketingAgent
from ai_agent_company.agents.sales import SalesAgent
from ai_agent_company.agents.support import CustomerSupportAgent

__all__ = [
    "BaseAgent",
    "AgentRole",
    "AgentStatus",
    "Task",
    "TaskResult",
    "SalesAgent",
    "MarketingAgent",
    "CustomerSupportAgent",
]
