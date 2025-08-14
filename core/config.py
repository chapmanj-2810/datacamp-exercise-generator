"""
Configuration settings for the exercise generator.
"""

import os
from typing import Optional


class Config:
    """Configuration settings for the DataCamp Exercise Generator."""
    
    # OpenAI Settings
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    DEFAULT_MODEL: str = "gpt-4o"
    DEFAULT_TEMPERATURE: float = 0.0
    PLANNING_TEMPERATURE: float = 0.3
    
    # Exercise Generation Settings
    MIN_EXERCISES: int = 2
    MAX_EXERCISES: int = 4
    
    @classmethod
    def validate(cls) -> None:
        """Validate configuration settings."""
        if not cls.OPENAI_API_KEY:
            raise ValueError(
                "OPENAI_API_KEY environment variable is required. "
                "Please set it with: export OPENAI_API_KEY='your-api-key'"
            )
