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


# Drag and Drop Classification Exercise Components
class DraggableItem(BaseModel):
    content: str = Field(description="The text content of the draggable item")
    id: str = Field(description="Unique identifier for the draggable item")
    incorrect_message: str = Field(description="Feedback message when item is placed in wrong category")


class DropZone(BaseModel):
    id: str = Field(description="Unique identifier for the drop zone")
    title: str = Field(description="Display title for the drop zone category")
    draggable_items: list[DraggableItem] = Field(description="Items that belong in this drop zone")


# Drag and Drop Classification Exercise
class DragDropClassifyExercise(Exercise):
    instructions: str = Field(description="Instructions for the learner on how to complete the exercise")
    hints: list[str] = Field(description="A list of 1-2 single-sentence statements to help learners")
    drop_zones: list[DropZone] = Field(description="Categories/zones where items can be dropped")
    success_message: str = Field(description="Success message when exercise is completed correctly")


# Drag and Drop Order Exercise Components
class OrderableItem(BaseModel):
    content: str = Field(description="The text content of the orderable item")
    id: str = Field(description="Unique identifier for the orderable item")
    incorrect_message: str = Field(description="Feedback message when item is placed in wrong position")


# Drag and Drop Order Exercise
class DragDropOrderExercise(Exercise):
    instructions: str = Field(description="Instructions for the learner on how to complete the exercise")
    hints: list[str] = Field(description="A list of 1-2 single-sentence statements to help learners")
    ordered_items: list[OrderableItem] = Field(description="Items that need to be placed in correct order")
    sequence_title: str = Field(description="Title for the sequence/process being ordered")
    success_message: str = Field(description="Success message when all items are correctly ordered")
    failure_message: str = Field(description="Message shown when ordering is incorrect", default="Try again!")


# Coding Exercise
class CodingExercise(Exercise):
    """Model for coding exercises with scaffolded code completion."""
    
    instructions: list[str] = Field(
        description="List of clear, actionable instructions for the learner"
    )
    hints: list[str] = Field(
        description="List of 1-2 syntax-focused hints about functions, methods, or techniques to use"
    )
    pre_exercise_code: str = Field(
        description="Python code that runs in background when exercise opens - imports, data setup, helper functions"
    )
    sample_code: str = Field(
        description="Solution code with scaffolding (____) replacing key parts learners need to complete"
    )
    solution_code: str = Field(
        description="Complete solution code that matches sample_code exactly except for scaffolding"
    )
    success_message: str = Field(
        description="Success message shown when learner completes the exercise correctly"
    )
    language: str = Field(
        description="Programming language for the exercise",
        default="python"
    )

    class Config:
        schema_extra = {
            "example": {
                "title": "Embedding more detailed descriptions",
                "context": "One of the last predicted labels didn't seem representative of the review; this was probably down to the lack of information being captured when we're only embedding the class labels...",
                "instructions": ["Extract a list containing the sentiment descriptions and embed them."],
                "hints": ["Use a list comprehension to extract the 'description' key from each dictionary in sentiments."],
                "pre_exercise_code": "from openai import OpenAI\nfrom scipy.spatial import distance\n\nsentiments = [...]\nreviews = [...]\n\ndef create_embeddings(texts):\n  # implementation\n  pass",
                "sample_code": "# Extract and embed the descriptions from sentiments\nclass_descriptions = ____\nclass_embeddings = ____",
                "solution_code": "# Extract and embed the descriptions from sentiments\nclass_descriptions = [sentiment['description'] for sentiment in sentiments]\nclass_embeddings = create_embeddings(class_descriptions)",
                "success_message": "There you have it! This time, you were able to correctly classify the second review!",
                "language": "python"
            }
        }
