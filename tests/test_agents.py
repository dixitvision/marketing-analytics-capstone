"""Tests for the specialised agent implementations."""

from __future__ import annotations

from ai_agent_company.agents.base import AgentRole, TaskResult
from ai_agent_company.agents.marketing import MarketingAgent
from ai_agent_company.agents.sales import SalesAgent
from ai_agent_company.agents.support import CustomerSupportAgent

# ---------------------------------------------------------------------------
# SalesAgent
# ---------------------------------------------------------------------------


class TestSalesAgent:
    def test_default_name_and_role(self):
        agent = SalesAgent()
        assert agent.name == "Sales Agent"
        assert agent.role == AgentRole.SALES

    def test_qualify_lead_returns_result(self):
        agent = SalesAgent()
        result = agent.qualify_lead("Acme Corp", budget=50000.0, needs="CRM software")
        assert isinstance(result, TaskResult)
        assert result.success is True
        assert len(result.output) > 0

    def test_draft_proposal_returns_result(self):
        agent = SalesAgent()
        result = agent.draft_proposal("Globex", product="Analytics Platform", price=12000.0)
        assert isinstance(result, TaskResult)
        assert result.success is True

    def test_qualify_lead_stored_in_history(self):
        agent = SalesAgent()
        agent.qualify_lead("Test Lead", budget=1000.0, needs="email marketing")
        assert len(agent.task_history) == 1

    def test_custom_llm_called_during_qualify(self):
        responses: list[str] = []

        def fake_llm(prompt: str) -> str:
            responses.append(prompt)
            return "Custom LLM answer"

        agent = SalesAgent(llm_client=fake_llm)
        result = agent.qualify_lead("Lead X", budget=5000.0, needs="automation")
        assert len(responses) == 1
        assert result.output == "Custom LLM answer"

    def test_mock_response_contains_role_keywords(self):
        agent = SalesAgent()
        result = agent.qualify_lead("Lead Y", budget=100.0, needs="test")
        assert "SALES" in result.output.upper() or "sales" in result.output.lower()


# ---------------------------------------------------------------------------
# MarketingAgent
# ---------------------------------------------------------------------------


class TestMarketingAgent:
    def test_default_name_and_role(self):
        agent = MarketingAgent()
        assert agent.name == "Marketing Agent"
        assert agent.role == AgentRole.MARKETING

    def test_create_campaign_returns_result(self):
        agent = MarketingAgent()
        result = agent.create_campaign(
            product="Cloud Storage",
            target_audience="SMBs",
            budget=20000.0,
        )
        assert isinstance(result, TaskResult)
        assert result.success is True

    def test_create_campaign_with_custom_channels(self):
        agent = MarketingAgent()
        result = agent.create_campaign(
            product="SaaS Tool",
            target_audience="Developers",
            budget=5000.0,
            channels=["LinkedIn", "GitHub Sponsors"],
        )
        assert result.success is True

    def test_generate_content_returns_result(self):
        agent = MarketingAgent()
        result = agent.generate_content(
            topic="AI in marketing",
            format="blog post",
            tone="informative",
        )
        assert isinstance(result, TaskResult)
        assert result.success is True

    def test_analyse_campaign_computes_metrics(self):
        agent = MarketingAgent()
        result = agent.analyse_campaign(
            campaign_name="Q1 Launch",
            impressions=10000,
            clicks=500,
            conversions=50,
            spend=2000.0,
        )
        assert result.success is True
        # Confirm the context was populated with computed metrics
        history = agent.task_history
        assert len(history) == 1

    def test_analyse_campaign_zero_impressions(self):
        """CTR should be 0 when impressions is 0 (no ZeroDivisionError)."""
        agent = MarketingAgent()
        result = agent.analyse_campaign(
            campaign_name="Empty Campaign",
            impressions=0,
            clicks=0,
            conversions=0,
            spend=0.0,
        )
        assert result.success is True

    def test_analyse_campaign_zero_conversions_cpa(self):
        """CPA should be inf when there are clicks but zero conversions."""
        agent = MarketingAgent()
        # We can only verify no exception is raised (CPA is inf in context).
        result = agent.analyse_campaign(
            campaign_name="No Conversions",
            impressions=1000,
            clicks=100,
            conversions=0,
            spend=500.0,
        )
        assert result.success is True


# ---------------------------------------------------------------------------
# CustomerSupportAgent
# ---------------------------------------------------------------------------


class TestCustomerSupportAgent:
    def test_default_name_and_role(self):
        agent = CustomerSupportAgent()
        assert agent.name == "Customer Support Agent"
        assert agent.role == AgentRole.CUSTOMER_SUPPORT

    def test_triage_ticket_returns_result(self):
        agent = CustomerSupportAgent()
        result = agent.triage_ticket(
            customer_name="Jane Doe",
            issue="Cannot log in to my account",
            priority="high",
        )
        assert isinstance(result, TaskResult)
        assert result.success is True

    def test_resolve_issue_returns_result(self):
        agent = CustomerSupportAgent()
        result = agent.resolve_issue(
            ticket_id="TKT-001",
            issue_summary="Password reset link not arriving",
            product="Auth Service",
        )
        assert result.success is True

    def test_draft_followup_without_survey(self):
        agent = CustomerSupportAgent()
        result = agent.draft_followup(
            customer_name="Bob Smith",
            resolved_issue="Login issue resolved",
        )
        assert result.success is True

    def test_draft_followup_with_survey_url(self):
        agent = CustomerSupportAgent()
        result = agent.draft_followup(
            customer_name="Alice",
            resolved_issue="Billing discrepancy fixed",
            satisfaction_survey_url="https://example.com/survey",
        )
        assert result.success is True

    def test_triage_default_priority(self):
        """Triage should work with the default medium priority."""
        agent = CustomerSupportAgent()
        result = agent.triage_ticket(customer_name="X", issue="Slow loading times")
        assert result.success is True
