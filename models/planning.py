"""
Learning design and planning models.
"""

from enum import Enum
from pydantic import BaseModel, Field


# Exercise type enumeration for type safety
class ExerciseType(str, Enum):
    SINGLE_MCQ = "single_mcq"
    MULTIPLE_MCQ = "multiple_mcq"
    DRAG_DROP_CLASSIFY = "drag_drop_classify"
    DRAG_DROP_ORDER = "drag_drop_order"


class ExercisePlan(BaseModel):
    exercise_type: ExerciseType = Field(description="The type of exercise to create")
    learning_objective: str = Field(description="The specific learning objective this exercise should target")
    rationale: str = Field(description="Why this exercise type is appropriate for this learning objective")
    difficulty_level: str = Field(description="Beginner, Intermediate, or Advanced", examples=["Beginner", "Intermediate", "Advanced"])


class LearningPlan(BaseModel):
    video_title: str = Field(description="A descriptive title for the video content")
    video_summary: str = Field(description="A brief summary of what the video covers")
    exercise_plans: list[ExercisePlan] = Field(description="List of exercises planned for this video, in the order they should appear")
