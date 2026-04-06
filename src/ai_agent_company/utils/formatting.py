"""Formatting helpers for task results and agent output."""

from __future__ import annotations

from ai_agent_company.agents.base import TaskResult


def format_task_result(result: TaskResult) -> str:
    """Render a :class:`~ai_agent_company.agents.base.TaskResult` as a
    human-readable string.

    Args:
        result: The task result to format.

    Returns:
        A formatted multi-line string suitable for display.
    """
    status = "✓ SUCCESS" if result.success else "✗ FAILURE"
    lines = [
        f"Task ID : {result.task_id}",
        f"Agent   : {result.agent_id}",
        f"Status  : {status}",
    ]
    if result.output:
        lines.append(f"Output  : {result.output}")
    if result.error:
        lines.append(f"Error   : {result.error}")
    return "\n".join(lines)
