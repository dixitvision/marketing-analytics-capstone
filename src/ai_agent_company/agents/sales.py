"""Sales agent implementation."""

from __future__ import annotations

from typing import Any

from ai_agent_company.agents.base import AgentRole, BaseAgent, Task, TaskResult


class SalesAgent(BaseAgent):
    """Agent responsible for sales-related tasks.

    Capabilities include lead qualification, proposal drafting, objection
    handling, and follow-up scheduling.

    Args:
        name: Display name for the agent (default: ``"Sales Agent"``).
        llm_client: Optional callable that accepts a prompt and returns a
            string.  When ``None`` the agent operates in mock mode.
    """

    def __init__(
        self,
        name: str = "Sales Agent",
        llm_client: Any | None = None,
    ) -> None:
        super().__init__(name=name, role=AgentRole.SALES, llm_client=llm_client)

    # ------------------------------------------------------------------
    # BaseAgent contract
    # ------------------------------------------------------------------

    def execute(self, task: Task) -> TaskResult:
        """Handle a sales task.

        Builds a prompt from the task description and any context provided
        (e.g. ``lead_name``, ``product``, ``budget``), then returns the
        LLM response wrapped in a :class:`~ai_agent_company.agents.base.TaskResult`.

        Args:
            task: The sales task to execute.

        Returns:
            A :class:`~ai_agent_company.agents.base.TaskResult` with the
            generated response.
        """
        prompt = self._build_prompt(task)
        response = self._call_llm(prompt)
        return TaskResult(
            task_id=task.task_id,
            agent_id=self.agent_id,
            output=response,
        )

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _build_prompt(self, task: Task) -> str:
        context_lines = "\n".join(
            f"  {key}: {value}" for key, value in task.context.items()
        )
        context_block = f"\nContext:\n{context_lines}" if context_lines else ""
        return (
            f"You are a professional sales agent.\n"
            f"Task: {task.description}{context_block}\n"
            f"Provide a helpful, concise, and professional response."
        )

    def _mock_response(self, prompt: str) -> str:  # noqa: ARG002
        return (
            "[SALES AGENT] I have reviewed the sales task and will proceed with "
            "a tailored outreach strategy. I'll qualify the lead, prepare a "
            "compelling proposal, and schedule a follow-up call."
        )

    # ------------------------------------------------------------------
    # Convenience methods
    # ------------------------------------------------------------------

    def qualify_lead(self, lead_name: str, budget: float, needs: str) -> TaskResult:
        """Qualify a sales lead.

        Args:
            lead_name: Name of the prospect.
            budget: Prospect's estimated budget in USD.
            needs: Brief description of what the prospect is looking for.

        Returns:
            A :class:`~ai_agent_company.agents.base.TaskResult` with the
            qualification assessment.
        """
        task = Task(
            description=f"Qualify the sales lead: {lead_name}",
            context={"lead_name": lead_name, "budget": budget, "needs": needs},
        )
        return self.handle(task)

    def draft_proposal(self, client_name: str, product: str, price: float) -> TaskResult:
        """Draft a sales proposal.

        Args:
            client_name: Name of the prospective client.
            product: Product or service being proposed.
            price: Proposed price in USD.

        Returns:
            A :class:`~ai_agent_company.agents.base.TaskResult` containing
            the drafted proposal.
        """
        task = Task(
            description=f"Draft a sales proposal for {client_name}",
            context={"client_name": client_name, "product": product, "price": price},
        )
        return self.handle(task)
