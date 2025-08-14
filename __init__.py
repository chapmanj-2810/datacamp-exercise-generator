"""
DataCamp Exercise Generator

An intelligent system for automatically generating DataCamp exercises from video content.
"""

from .core import LearningDesigner, load_video_content
from .generators import get_exercise_generator
from .models import ExerciseType

__version__ = "0.1.0"

__all__ = [
    "LearningDesigner",
    "get_exercise_generator", 
    "load_video_content",
    "ExerciseType"
]
