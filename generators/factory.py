"""
Factory function for creating exercise generators.
"""

from .base import ExerciseGenerator
from .single_mcq import SingleAnswerMCQGenerator
from .multiple_mcq import MultipleAnswerMCQGenerator
from .drag_drop_classify import DragDropClassifyGenerator
from .drag_drop_order import DragDropOrderGenerator
from .coding import CodingGenerator  # New import


def get_exercise_generator(exercise_type: str = "single_mcq", **kwargs) -> ExerciseGenerator:
    """Factory function to get the appropriate exercise generator."""
    generators: dict[str, type[ExerciseGenerator]] = {
        "single_mcq": SingleAnswerMCQGenerator,
        "multiple_mcq": MultipleAnswerMCQGenerator,
        "drag_drop_classify": DragDropClassifyGenerator,
        "drag_drop_order": DragDropOrderGenerator,
        "coding": CodingGenerator,  # New generator
    }
    
    if exercise_type not in generators:
        raise ValueError(f"Unknown exercise type: {exercise_type}. Available types: {list(generators.keys())}")
    
    return generators[exercise_type](**kwargs)
