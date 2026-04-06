"""AI Agent Company — a multi-agent framework for business automation."""

from ai_agent_company.agents.marketing import MarketingAgent
from ai_agent_company.agents.sales import SalesAgent
from ai_agent_company.agents.support import CustomerSupportAgent
from ai_agent_company.company import Company

__all__ = ["Company", "SalesAgent", "MarketingAgent", "CustomerSupportAgent"]
__version__ = "0.1.0"
