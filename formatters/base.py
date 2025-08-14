"""
Base formatter abstract class.
"""

from abc import ABC, abstractmethod
from ..models.exercises import Exercise


class ExerciseFormatter(ABC):
    @abstractmethod
    def format_to_markdown(self, exercise: Exercise) -> str:
        """Convert an exercise object to markdown/YAML format."""
        pass
