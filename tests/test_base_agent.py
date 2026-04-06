"""Tests for the base agent module."""

from __future__ import annotations

from ai_agent_company.agents.base import (
    AgentRole,
    AgentStatus,
    BaseAgent,
    Task,
    TaskResult,
)

# ---------------------------------------------------------------------------
# Concrete stub for testing the abstract BaseAgent
# ---------------------------------------------------------------------------


class StubAgent(BaseAgent):
    """Minimal concrete agent used only for testing BaseAgent behaviour."""

    def __init__(self, llm_client=None):
        super().__init__(name="Stub Agent", role=AgentRole.GENERAL, llm_client=llm_client)

    def execute(self, task: Task) -> TaskResult:
        response = self._call_llm(task.description)
        return TaskResult(
            task_id=task.task_id,
            agent_id=self.agent_id,
            output=response,
        )


class ErrorAgent(BaseAgent):
    """Agent that always raises an exception during execution."""

    def __init__(self):
        super().__init__(name="Error Agent", role=AgentRole.GENERAL)

    def execute(self, task: Task) -> TaskResult:  # noqa: ARG002
        raise RuntimeError("Simulated failure")


# ---------------------------------------------------------------------------
# Task tests
# ---------------------------------------------------------------------------


class TestTask:
    def test_task_has_unique_id(self):
        t1 = Task(description="first")
        t2 = Task(description="second")
        assert t1.task_id != t2.task_id

    def test_task_default_context_is_empty(self):
        task = Task(description="do something")
        assert task.context == {}

    def test_task_with_context(self):
        task = Task(description="send email", context={"to": "alice@example.com"})
        assert task.context["to"] == "alice@example.com"


# ---------------------------------------------------------------------------
# TaskResult tests
# ---------------------------------------------------------------------------


class TestTaskResult:
    def test_default_success_is_true(self):
        result = TaskResult(task_id="t1", agent_id="a1", output="done")
        assert result.success is True
        assert result.error is None

    def test_failure_result(self):
        result = TaskResult(task_id="t1", agent_id="a1", output="", success=False, error="oops")
        assert result.success is False
        assert result.error == "oops"


# ---------------------------------------------------------------------------
# BaseAgent / StubAgent tests
# ---------------------------------------------------------------------------


class TestBaseAgent:
    def test_initial_status_is_idle(self):
        agent = StubAgent()
        assert agent.status == AgentStatus.IDLE

    def test_agent_has_unique_id(self):
        a1 = StubAgent()
        a2 = StubAgent()
        assert a1.agent_id != a2.agent_id

    def test_handle_returns_task_result(self):
        agent = StubAgent()
        task = Task(description="test task")
        result = agent.handle(task)
        assert isinstance(result, TaskResult)
        assert result.task_id == task.task_id
        assert result.agent_id == agent.agent_id

    def test_handle_adds_to_task_history(self):
        agent = StubAgent()
        agent.handle(Task(description="first"))
        agent.handle(Task(description="second"))
        assert len(agent.task_history) == 2

    def test_task_history_is_read_only_copy(self):
        agent = StubAgent()
        agent.handle(Task(description="task"))
        history = agent.task_history
        history.clear()
        assert len(agent.task_history) == 1

    def test_status_returns_to_idle_after_success(self):
        agent = StubAgent()
        agent.handle(Task(description="task"))
        assert agent.status == AgentStatus.IDLE

    def test_status_becomes_error_on_exception(self):
        agent = ErrorAgent()
        result = agent.handle(Task(description="failing task"))
        assert agent.status == AgentStatus.ERROR
        assert result.success is False
        assert "Simulated failure" in (result.error or "")

    def test_mock_response_returned_without_llm_client(self):
        agent = StubAgent()
        task = Task(description="anything")
        result = agent.handle(task)
        assert len(result.output) > 0

    def test_custom_llm_client_is_called(self):
        calls: list[str] = []

        def fake_llm(prompt: str) -> str:
            calls.append(prompt)
            return "LLM response"

        agent = StubAgent(llm_client=fake_llm)
        task = Task(description="call the LLM")
        result = agent.handle(task)
        assert len(calls) == 1
        assert result.output == "LLM response"

    def test_repr_contains_name_and_role(self):
        agent = StubAgent()
        r = repr(agent)
        assert "Stub Agent" in r
        assert "general" in r
