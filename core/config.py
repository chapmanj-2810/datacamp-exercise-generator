import os
from typing import Optional

class Config:
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    DEFAULT_MODEL: str = "gpt-4o"
    DEFAULT_TEMPERATURE: float = 0.0
    PLANNING_TEMPERATURE: float = 0.3
