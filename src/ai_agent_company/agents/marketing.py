"""Marketing agent implementation."""

from __future__ import annotations

from typing import Any

from ai_agent_company.agents.base import AgentRole, BaseAgent, Task, TaskResult


class MarketingAgent(BaseAgent):
    """Agent responsible for marketing-related tasks.

    Capabilities include campaign planning, content generation, channel
    strategy, and campaign performance analysis.

    Args:
        name: Display name for the agent (default: ``"Marketing Agent"``).
        llm_client: Optional callable that accepts a prompt and returns a
            string.  When ``None`` the agent operates in mock mode.
    """

    def __init__(
        self,
        name: str = "Marketing Agent",
        llm_client: Any | None = None,
    ) -> None:
        super().__init__(name=name, role=AgentRole.MARKETING, llm_client=llm_client)

    # ------------------------------------------------------------------
    # BaseAgent contract
    # ------------------------------------------------------------------

    def execute(self, task: Task) -> TaskResult:
        """Handle a marketing task.

        Args:
            task: The marketing task to execute.

        Returns:
            A :class:`~ai_agent_company.agents.base.TaskResult` with the
            generated marketing output.
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
            f"You are an expert digital marketing strategist.\n"
            f"Task: {task.description}{context_block}\n"
            f"Provide a data-driven, creative, and actionable response."
        )

    def _mock_response(self, prompt: str) -> str:  # noqa: ARG002
        return (
            "[MARKETING AGENT] I have analysed the marketing request and will "
            "design a targeted multi-channel campaign. Key tactics will include "
            "content marketing, paid social, SEO optimisation, and email nurture sequences."
        )

    # ------------------------------------------------------------------
    # Convenience methods
    # ------------------------------------------------------------------

    def create_campaign(
        self,
        product: str,
        target_audience: str,
        budget: float,
        channels: list[str] | None = None,
    ) -> TaskResult:
        """Create a marketing campaign plan.

        Args:
            product: The product or service to promote.
            target_audience: Description of the intended audience.
            budget: Campaign budget in USD.
            channels: List of marketing channels to use.  Defaults to a
                standard set if not provided.

        Returns:
            A :class:`~ai_agent_company.agents.base.TaskResult` with the
            campaign plan.
        """
        if channels is None:
            channels = ["email", "social media", "SEO", "PPC"]
        task = Task(
            description=f"Create a marketing campaign for {product}",
            context={
                "product": product,
                "target_audience": target_audience,
                "budget": budget,
                "channels": ", ".join(channels),
            },
        )
        return self.handle(task)

    def generate_content(self, topic: str, format: str, tone: str = "professional") -> TaskResult:
        """Generate marketing content.

        Args:
            topic: Subject of the content piece.
            format: Content format (e.g. ``"blog post"``, ``"social media post"``).
            tone: Desired writing tone (default: ``"professional"``).

        Returns:
            A :class:`~ai_agent_company.agents.base.TaskResult` with the
            generated content.
        """
        task = Task(
            description=f"Generate {format} content about: {topic}",
            context={"topic": topic, "format": format, "tone": tone},
        )
        return self.handle(task)

    def analyse_campaign(
        self,
        campaign_name: str,
        impressions: int,
        clicks: int,
        conversions: int,
        spend: float,
    ) -> TaskResult:
        """Analyse campaign performance metrics.

        Args:
            campaign_name: Name of the campaign.
            impressions: Total ad impressions.
            clicks: Total clicks received.
            conversions: Total conversions achieved.
            spend: Total money spent in USD.

        Returns:
            A :class:`~ai_agent_company.agents.base.TaskResult` containing
            the performance analysis and recommendations.
        """
        ctr = (clicks / impressions * 100) if impressions > 0 else 0.0
        cvr = (conversions / clicks * 100) if clicks > 0 else 0.0
        cpa = (spend / conversions) if conversions > 0 else float("inf")
        task = Task(
            description=f"Analyse performance for campaign: {campaign_name}",
            context={
                "campaign_name": campaign_name,
                "impressions": impressions,
                "clicks": clicks,
                "conversions": conversions,
                "spend": spend,
                "ctr_percent": round(ctr, 2),
                "cvr_percent": round(cvr, 2),
                "cost_per_acquisition": round(cpa, 2),
            },
        )
        return self.handle(task)
