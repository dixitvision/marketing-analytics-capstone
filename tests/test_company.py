"""Tests for the Company orchestrator."""

from __future__ import annotations

import pytest

from ai_agent_company.agents.base import AgentRole, AgentStatus, BaseAgent, Task, TaskResult
from ai_agent_company.company import Company

# ---------------------------------------------------------------------------
# Helper stub
# ---------------------------------------------------------------------------


class CustomAgent(BaseAgent):
    """Custom agent registered during tests to validate registration logic."""

    def __init__(self):
        super().__init__(name="Custom Agent", role=AgentRole.GENERAL)

    def execute(self, task: Task) -> TaskResult:
        return TaskResult(
            task_id=task.task_id,
            agent_id=self.agent_id,
            output="Custom output",
        )


# ---------------------------------------------------------------------------
# Company initialisation tests
# ---------------------------------------------------------------------------


class TestCompanyInit:
    def test_default_name(self):
        company = Company()
        assert company.name == "AI Agent Company"

    def test_custom_name(self):
        company = Company(name="Acme AI")
        assert company.name == "Acme AI"

    def test_default_agents_registered(self):
        company = Company()
        roles = {a.role for a in company.agents}
        assert AgentRole.SALES in roles
        assert AgentRole.MARKETING in roles
        assert AgentRole.CUSTOMER_SUPPORT in roles

    def test_initial_task_results_empty(self):
        company = Company()
        assert company.task_results == []


# ---------------------------------------------------------------------------
# Agent registration & lookup
# ---------------------------------------------------------------------------


class TestAgentManagement:
    def test_register_agent_increases_count(self):
        company = Company()
        initial_count = len(company.agents)
        company.register_agent(CustomAgent())
        assert len(company.agents) == initial_count + 1

    def test_get_agent_by_role_returns_correct_role(self):
        company = Company()
        agent = company.get_agent_by_role(AgentRole.SALES)
        assert agent is not None
        assert agent.role == AgentRole.SALES

    def test_get_agent_by_unknown_role_returns_none(self):
        company = Company()
        agent = company.get_agent_by_role(AgentRole.GENERAL)
        assert agent is None

    def test_get_agent_by_role_returns_idle_first(self):
        company = Company()
        # After a run_task call the agent should be IDLE again.
        company.run_task("quick task", AgentRole.SALES)
        agent = company.get_agent_by_role(AgentRole.SALES)
        assert agent is not None
        assert agent.status == AgentStatus.IDLE


# ---------------------------------------------------------------------------
# Task assignment
# ---------------------------------------------------------------------------


class TestTaskAssignment:
    def test_assign_task_returns_task_result(self):
        company = Company()
        task = Task(description="Qualify a lead")
        result = company.assign_task(task, AgentRole.SALES)
        assert isinstance(result, TaskResult)
        assert result.success is True

    def test_assign_task_unknown_role_raises(self):
        company = Company()
        task = Task(description="Do something unknown")
        with pytest.raises(ValueError, match="No agent registered for role"):
            company.assign_task(task, AgentRole.GENERAL)

    def test_run_task_creates_and_routes_task(self):
        company = Company()
        result = company.run_task(
            "Create a marketing campaign",
            AgentRole.MARKETING,
            context={"product": "Widget X"},
        )
        assert result.success is True

    def test_run_task_adds_to_results(self):
        company = Company()
        assert len(company.task_results) == 0
        company.run_task("Support ticket", AgentRole.CUSTOMER_SUPPORT)
        assert len(company.task_results) == 1

    def test_multiple_tasks_accumulate_results(self):
        company = Company()
        for _ in range(3):
            company.run_task("Task", AgentRole.MARKETING)
        assert len(company.task_results) == 3

    def test_task_results_is_copy(self):
        company = Company()
        company.run_task("task", AgentRole.SALES)
        results = company.task_results
        results.clear()
        assert len(company.task_results) == 1


# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------


class TestCompanySummary:
    def test_summary_structure(self):
        company = Company()
        s = company.summary()
        assert "company" in s
        assert "total_tasks" in s
        assert "successful_tasks" in s
        assert "failed_tasks" in s
        assert "tasks_by_role" in s
        assert "registered_agents" in s

    def test_summary_company_name(self):
        company = Company(name="Test Co")
        assert company.summary()["company"] == "Test Co"

    def test_summary_task_counts(self):
        company = Company()
        company.run_task("task 1", AgentRole.SALES)
        company.run_task("task 2", AgentRole.MARKETING)
        s = company.summary()
        assert s["total_tasks"] == 2
        assert s["successful_tasks"] == 2
        assert s["failed_tasks"] == 0

    def test_repr_contains_name(self):
        company = Company(name="My Company")
        assert "My Company" in repr(company)


# ---------------------------------------------------------------------------
# LLM client pass-through
# ---------------------------------------------------------------------------


class TestLLMClientPassThrough:
    def test_llm_client_forwarded_to_agents(self):
        calls: list[str] = []

        def fake_llm(prompt: str) -> str:
            calls.append(prompt)
            return "LLM answer"

        company = Company(llm_client=fake_llm)
        company.run_task("Qualify lead for Bob", AgentRole.SALES)
        assert len(calls) == 1
