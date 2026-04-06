"""Base agent definition for the AI Agent Company framework."""

from __future__ import annotations

import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any


class AgentRole(StrEnum):
    """Roles that agents can fulfil within the company."""

    SALES = "sales"
    MARKETING = "marketing"
    CUSTOMER_SUPPORT = "customer_support"
    GENERAL = "general"


class AgentStatus(StrEnum):
    """Operational status of an agent."""

    IDLE = "idle"
    BUSY = "busy"
    ERROR = "error"


@dataclass
class Task:
    """A unit of work to be executed by an agent.

    Attributes:
        description: Human-readable description of what needs to be done.
        context: Optional additional data the agent may use.
        task_id: Unique identifier automatically assigned on creation.
    """

    description: str
    context: dict[str, Any] = field(default_factory=dict)
    task_id: str = field(default_factory=lambda: str(uuid.uuid4()))


@dataclass
class TaskResult:
    """The outcome produced by an agent after executing a task.

    Attributes:
        task_id: Identifier of the originating task.
        agent_id: Identifier of the agent that handled the task.
        output: The textual or structured result.
        success: Whether the task completed without error.
        error: Error message when ``success`` is ``False``.
    """

    task_id: str
    agent_id: str
    output: str
    success: bool = True
    error: str | None = None


class BaseAgent(ABC):
    """Abstract base class that every company agent must inherit from.

    Subclasses are required to implement :meth:`execute` with the domain
    logic that turns a :class:`Task` into a :class:`TaskResult`.

    Args:
        name: Display name for the agent.
        role: The :class:`AgentRole` this agent fills.
        llm_client: An optional callable that accepts a prompt string and
            returns a response string.  When ``None`` is supplied the agent
            operates in *mock* mode and delegates entirely to
            :meth:`_mock_response`.
    """

    def __init__(
        self,
        name: str,
        role: AgentRole,
        llm_client: Any | None = None,
    ) -> None:
        self.agent_id: str = str(uuid.uuid4())
        self.name = name
        self.role = role
        self.status = AgentStatus.IDLE
        self._llm_client = llm_client
        self._task_history: list[TaskResult] = []

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    def handle(self, task: Task) -> TaskResult:
        """Execute *task* and return the result, updating agent status.

        This method manages the agent lifecycle around :meth:`execute` so
        that individual subclasses do not need to duplicate status tracking
        or error handling.
        """
        self.status = AgentStatus.BUSY
        try:
            result = self.execute(task)
        except Exception as exc:  # noqa: BLE001
            result = TaskResult(
                task_id=task.task_id,
                agent_id=self.agent_id,
                output="",
                success=False,
                error=str(exc),
            )
            self.status = AgentStatus.ERROR
        else:
            self.status = AgentStatus.IDLE

        self._task_history.append(result)
        return result

    @property
    def task_history(self) -> list[TaskResult]:
        """Read-only view of all tasks handled by this agent."""
        return list(self._task_history)

    # ------------------------------------------------------------------
    # Subclass contract
    # ------------------------------------------------------------------

    @abstractmethod
    def execute(self, task: Task) -> TaskResult:
        """Perform the domain work for *task* and return a :class:`TaskResult`.

        Args:
            task: The task to execute.

        Returns:
            A :class:`TaskResult` describing the outcome.
        """

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _call_llm(self, prompt: str) -> str:
        """Invoke the LLM client or fall back to a mock response.

        Args:
            prompt: The prompt to send to the language model.

        Returns:
            The model's text response.
        """
        if self._llm_client is not None:
            return str(self._llm_client(prompt))
        return self._mock_response(prompt)

    def _mock_response(self, prompt: str) -> str:  # noqa: ARG002
        """Return a placeholder response when no LLM client is configured.

        Override this in subclasses to provide more meaningful stubs.

        Args:
            prompt: The prompt that would have been sent to the LLM.

        Returns:
            A generic placeholder string.
        """
        return f"[{self.role.value.upper()} AGENT — {self.name}] Mock response for prompt."

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"name={self.name!r}, "
            f"role={self.role.value!r}, "
            f"status={self.status.value!r})"
        )
