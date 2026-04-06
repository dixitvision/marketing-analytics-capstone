"""Customer support agent implementation."""

from __future__ import annotations

from typing import Any

from ai_agent_company.agents.base import AgentRole, BaseAgent, Task, TaskResult


class CustomerSupportAgent(BaseAgent):
    """Agent responsible for customer support tasks.

    Capabilities include ticket triage, issue resolution, escalation
    management, and customer satisfaction follow-up.

    Args:
        name: Display name for the agent (default: ``"Customer Support Agent"``).
        llm_client: Optional callable that accepts a prompt and returns a
            string.  When ``None`` the agent operates in mock mode.
    """

    def __init__(
        self,
        name: str = "Customer Support Agent",
        llm_client: Any | None = None,
    ) -> None:
        super().__init__(
            name=name,
            role=AgentRole.CUSTOMER_SUPPORT,
            llm_client=llm_client,
        )

    # ------------------------------------------------------------------
    # BaseAgent contract
    # ------------------------------------------------------------------

    def execute(self, task: Task) -> TaskResult:
        """Handle a customer support task.

        Args:
            task: The support task to execute.

        Returns:
            A :class:`~ai_agent_company.agents.base.TaskResult` with the
            support response.
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
            f"You are a friendly and empathetic customer support specialist.\n"
            f"Task: {task.description}{context_block}\n"
            f"Provide a helpful, clear, and empathetic response that resolves "
            f"the customer's concern."
        )

    def _mock_response(self, prompt: str) -> str:  # noqa: ARG002
        return (
            "[SUPPORT AGENT] Thank you for reaching out. I have reviewed your "
            "request and will work swiftly to resolve this. Our team prioritises "
            "your satisfaction and will provide a full resolution within 24 hours."
        )

    # ------------------------------------------------------------------
    # Convenience methods
    # ------------------------------------------------------------------

    def triage_ticket(
        self,
        customer_name: str,
        issue: str,
        priority: str = "medium",
    ) -> TaskResult:
        """Triage a customer support ticket.

        Args:
            customer_name: Name of the customer submitting the ticket.
            issue: Description of the customer's problem.
            priority: Ticket priority — ``"low"``, ``"medium"``, or
                ``"high"`` (default: ``"medium"``).

        Returns:
            A :class:`~ai_agent_company.agents.base.TaskResult` with the
            triage assessment and next steps.
        """
        task = Task(
            description=f"Triage support ticket for customer: {customer_name}",
            context={
                "customer_name": customer_name,
                "issue": issue,
                "priority": priority,
            },
        )
        return self.handle(task)

    def resolve_issue(
        self,
        ticket_id: str,
        issue_summary: str,
        product: str,
    ) -> TaskResult:
        """Generate a resolution for a known support issue.

        Args:
            ticket_id: Unique identifier of the support ticket.
            issue_summary: Brief summary of the problem.
            product: Product or service the issue relates to.

        Returns:
            A :class:`~ai_agent_company.agents.base.TaskResult` containing
            the resolution steps.
        """
        task = Task(
            description=f"Resolve support issue for ticket {ticket_id}",
            context={
                "ticket_id": ticket_id,
                "issue_summary": issue_summary,
                "product": product,
            },
        )
        return self.handle(task)

    def draft_followup(
        self,
        customer_name: str,
        resolved_issue: str,
        satisfaction_survey_url: str = "",
    ) -> TaskResult:
        """Draft a post-resolution follow-up message for a customer.

        Args:
            customer_name: Name of the customer.
            resolved_issue: Brief description of the issue that was resolved.
            satisfaction_survey_url: Optional URL to a satisfaction survey.

        Returns:
            A :class:`~ai_agent_company.agents.base.TaskResult` containing
            the follow-up message.
        """
        context: dict[str, Any] = {
            "customer_name": customer_name,
            "resolved_issue": resolved_issue,
        }
        if satisfaction_survey_url:
            context["survey_url"] = satisfaction_survey_url

        task = Task(
            description=f"Draft a follow-up message for {customer_name} after issue resolution",
            context=context,
        )
        return self.handle(task)
