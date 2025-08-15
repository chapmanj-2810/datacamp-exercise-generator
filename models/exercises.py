# Add this to your existing models/exercises.py file

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
    xp: int = Field(
        description="Experience points awarded for completing the exercise",
        default=100
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
                "language": "python",
                "xp": 100
            }
        }
