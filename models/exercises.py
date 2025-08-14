"""
Exercise Pydantic models for different exercise types.
"""

from abc import ABC
from pydantic import BaseModel, Field


# Base exercise class for extensibility
class Exercise(BaseModel, ABC):
    title: str = Field(description="The title of the exercise.")
    context: str = Field(description="Additional exercise context to introduce and motivate the exercise.")


# Multiple Choice Question Exercise - Single Answer
class SingleAnswerMCQExercise(Exercise):
    question: str = Field(description="A question related to the learning objectives of the video testing learners on their understanding of the video content only.")
    hints: list[str] = Field(description="A list of 1-2 single-sentence statements to help learners reach the solution. Do not tell learners what the solution is, just information to help them realise it.")
    incorrect_answers: dict[str, str] = Field(description="Dictionary mapping incorrect answers to their feedback messages. These messages should nudge learners in the correct direction while not providing the answer clearly.")
    correct_answer: str = Field(description="The correct answer to the question.")
    correct_feedback: str = Field(description="Success message shown when the learner selects the correct answer.")


# Multiple Choice Question Exercise - Multiple Answers
class MultipleAnswerMCQExercise(Exercise):
    question: str = Field(description="A question that requires selecting multiple correct answers.")
    hints: list[str] = Field(description="A list of 1-2 single-sentence statements to help learners reach the solution.")
    answers: list[dict] = Field(description="List of answer objects with 'answer', 'correct' (boolean), and 'feedback' fields.")
    success_message: str = Field(description="Success message shown when all correct answers are selected.")

    class Config:
        schema_extra = {
            "example": {
                "title": "Making the leap from single to multi-agents",
                "context": "You're an experienced Staff Engineer that's been brought in to mentor a Junior AI Engineer...",
                "question": "Which of the following are benefits of a multi-agent design over single agents?",
                "hints": ["Single agents can struggle to manage a large number of tools, especially if the tools are different but similar."],
                "answers": [
                    {
                        "answer": "A single agent is struggling to decide which tools to select",
                        "correct": True,
                        "feedback": "An agent is aware of the tools at its disposal, but like a human presented with a long list of choices, it may select sub-optimal options when lots of tools are available."
                    },
                    {
                        "answer": "Two agents are always better than one", 
                        "correct": False,
                        "feedback": "Multi-agent systems are definitely cool, but the use case may not always require the additional complexity of coding and managing more than one agent."
                    }
                ],
                "success_message": "Wow, you sure are smashing this! Let's dive a little deeper into some of these multi-agent design patterns."
            }
        }
