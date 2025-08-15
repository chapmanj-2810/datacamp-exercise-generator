"""
DataCamp Exercise Generator - Models Package

This package contains all Pydantic models and data structures used throughout the system.
"""

from .exercises import (
    Exercise, SingleAnswerMCQExercise, MultipleAnswerMCQExercise,
    DragDropClassifyExercise, DragDropOrderExercise, CodingExercise,
    DraggableItem, DropZone, OrderableItem
)
from .planning import ExerciseType, ExercisePlan, LearningPlan
from .examples import EXERCISE_EXAMPLES

__all__ = [
    "Exercise",
    "SingleAnswerMCQExercise", 
    "MultipleAnswerMCQExercise",
    "DragDropClassifyExercise",
    "DragDropOrderExercise",
    "CodingExercise",
    "DraggableItem",
    "DropZone", 
    "OrderableItem",
    "ExerciseType",
    "ExercisePlan",
    "LearningPlan",
    "EXERCISE_EXAMPLES"
]
