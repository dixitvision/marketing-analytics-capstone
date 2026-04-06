"""Tests for utility modules."""

from __future__ import annotations

from ai_agent_company.agents.base import TaskResult
from ai_agent_company.utils.formatting import format_task_result
from ai_agent_company.utils.logging import get_logger


class TestGetLogger:
    def test_returns_logger_with_correct_name(self):
        logger = get_logger("test.module")
        assert logger.name == "test.module"

    def test_logger_has_handler(self):
        logger = get_logger("test.handler_check")
        assert len(logger.handlers) >= 1

    def test_calling_twice_does_not_duplicate_handlers(self):
        get_logger("test.double")
        logger = get_logger("test.double")
        assert len(logger.handlers) == 1


class TestFormatTaskResult:
    def test_success_result_contains_success_marker(self):
        result = TaskResult(task_id="t1", agent_id="a1", output="done")
        text = format_task_result(result)
        assert "SUCCESS" in text
        assert "t1" in text
        assert "a1" in text
        assert "done" in text

    def test_failure_result_contains_failure_marker(self):
        result = TaskResult(
            task_id="t2", agent_id="a2", output="", success=False, error="bad thing"
        )
        text = format_task_result(result)
        assert "FAILURE" in text
        assert "bad thing" in text

    def test_result_without_error_has_no_error_line(self):
        result = TaskResult(task_id="t3", agent_id="a3", output="ok")
        text = format_task_result(result)
        assert "Error" not in text
