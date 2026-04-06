"""Company orchestrator — routes tasks to the appropriate agents."""

from __future__ import annotations

from typing import Any

from ai_agent_company.agents.base import AgentRole, AgentStatus, BaseAgent, Task, TaskResult
from ai_agent_company.agents.marketing import MarketingAgent
from ai_agent_company.agents.sales import SalesAgent
from ai_agent_company.agents.support import CustomerSupportAgent
from ai_agent_company.utils.logging import get_logger

logger = get_logger(__name__)


class Company:
    """Orchestrates a team of specialised AI agents.

    The :class:`Company` creates and manages a roster of agents — one per
    supported role by default — and routes incoming tasks to the agent best
    suited to handle them.

    Args:
        name: Name of the company (used in logging and reports).
        llm_client: Optional callable passed through to every agent.  When
            ``None``, all agents operate in mock mode.
    """

    def __init__(
        self,
        name: str = "AI Agent Company",
        llm_client: Any | None = None,
    ) -> None:
        self.name = name
        self._agents: dict[str, BaseAgent] = {}
        self._llm_client = llm_client
        self._results: list[TaskResult] = []

        self._register_default_agents()

    # ------------------------------------------------------------------
    # Agent management
    # ------------------------------------------------------------------

    def _register_default_agents(self) -> None:
        for agent in [
            SalesAgent(llm_client=self._llm_client),
            MarketingAgent(llm_client=self._llm_client),
            CustomerSupportAgent(llm_client=self._llm_client),
        ]:
            self.register_agent(agent)

    def register_agent(self, agent: BaseAgent) -> None:
        """Register an agent with the company.

        Args:
            agent: The agent instance to register.
        """
        self._agents[agent.agent_id] = agent
        logger.info("Registered agent %r (%s)", agent.name, agent.role.value)

    def get_agent_by_role(self, role: AgentRole) -> BaseAgent | None:
        """Return the first idle agent with the given *role*, or any agent of
        that role if none are idle.

        Args:
            role: The role to look for.

        Returns:
            A matching :class:`~ai_agent_company.agents.base.BaseAgent`, or
            ``None`` if no agent with that role is registered.
        """
        candidates = [a for a in self._agents.values() if a.role == role]
        if not candidates:
            return None
        idle = [a for a in candidates if a.status == AgentStatus.IDLE]
        return idle[0] if idle else candidates[0]

    @property
    def agents(self) -> list[BaseAgent]:
        """All registered agents."""
        return list(self._agents.values())

    # ------------------------------------------------------------------
    # Task routing
    # ------------------------------------------------------------------

    def assign_task(self, task: Task, role: AgentRole) -> TaskResult:
        """Route *task* to an agent with the specified *role*.

        Args:
            task: The task to assign.
            role: The agent role that should handle the task.

        Returns:
            The :class:`~ai_agent_company.agents.base.TaskResult` produced
            by the agent.

        Raises:
            ValueError: If no agent with *role* is registered.
        """
        agent = self.get_agent_by_role(role)
        if agent is None:
            raise ValueError(f"No agent registered for role: {role.value}")

        logger.info(
            "Assigning task %r to %r (%s)",
            task.description[:60],
            agent.name,
            role.value,
        )
        result = agent.handle(task)
        self._results.append(result)

        if result.success:
            logger.info("Task %s completed successfully.", task.task_id)
        else:
            logger.error("Task %s failed: %s", task.task_id, result.error)

        return result

    def run_task(
        self,
        description: str,
        role: AgentRole,
        context: dict[str, Any] | None = None,
    ) -> TaskResult:
        """Convenience method to create and assign a task in one call.

        Args:
            description: Human-readable description of the task.
            role: The agent role that should handle the task.
            context: Optional key-value data passed to the agent.

        Returns:
            The :class:`~ai_agent_company.agents.base.TaskResult` produced
            by the agent.
        """
        task = Task(description=description, context=context or {})
        return self.assign_task(task, role)

    # ------------------------------------------------------------------
    # Reporting
    # ------------------------------------------------------------------

    @property
    def task_results(self) -> list[TaskResult]:
        """All task results accumulated since the company was created."""
        return list(self._results)

    def summary(self) -> dict[str, Any]:
        """Return a high-level summary of company activity.

        Returns:
            A dictionary with total tasks, success count, failure count,
            and a per-role breakdown.
        """
        total = len(self._results)
        successes = sum(1 for r in self._results if r.success)
        failures = total - successes

        role_counts: dict[str, int] = {}
        for agent in self._agents.values():
            role_counts[agent.role.value] = role_counts.get(agent.role.value, 0) + len(
                agent.task_history
            )

        return {
            "company": self.name,
            "total_tasks": total,
            "successful_tasks": successes,
            "failed_tasks": failures,
            "tasks_by_role": role_counts,
            "registered_agents": len(self._agents),
        }

    def __repr__(self) -> str:
        return (
            f"Company(name={self.name!r}, agents={len(self._agents)}, "
            f"tasks_completed={len(self._results)})"
        )
