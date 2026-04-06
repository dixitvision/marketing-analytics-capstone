"""Configuration for the AI Agent Company."""

from __future__ import annotations

import os
from dataclasses import dataclass, field


@dataclass
class Config:
    """Runtime configuration for the AI Agent Company.

    All values can be overridden with environment variables:

    - ``AIAGENT_COMPANY_NAME`` — company name
    - ``AIAGENT_LLM_MODEL`` — model identifier string
    - ``AIAGENT_LLM_TEMPERATURE`` — sampling temperature (float)
    - ``AIAGENT_LOG_LEVEL`` — logging level (e.g. ``"INFO"``, ``"DEBUG"``)

    Attributes:
        company_name: Display name used in reports and logs.
        llm_model: Language model identifier.
        llm_temperature: Sampling temperature for the LLM (0.0–2.0).
        log_level: Logging verbosity.
        extra: Any additional key-value pairs for custom deployments.
    """

    company_name: str = field(
        default_factory=lambda: os.getenv("AIAGENT_COMPANY_NAME", "AI Agent Company")
    )
    llm_model: str = field(
        default_factory=lambda: os.getenv("AIAGENT_LLM_MODEL", "gpt-4o")
    )
    llm_temperature: float = field(
        default_factory=lambda: float(os.getenv("AIAGENT_LLM_TEMPERATURE", "0.7"))
    )
    log_level: str = field(
        default_factory=lambda: os.getenv("AIAGENT_LOG_LEVEL", "INFO")
    )
    extra: dict[str, str] = field(default_factory=dict)

    @classmethod
    def from_env(cls) -> Config:
        """Create a :class:`Config` fully populated from environment variables.

        Returns:
            A :class:`Config` instance with all values sourced from the
            process environment (or defaults when absent).
        """
        return cls()
