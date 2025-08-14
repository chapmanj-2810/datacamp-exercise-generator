"""
Generator for single-answer multiple choice exercises.
"""

from .base import ExerciseGenerator
from ..models.exercises import SingleAnswerMCQExercise
from ..models.examples import EXERCISE_EXAMPLES
from ..formatters.single_mcq import SingleAnswerMCQFormatter


class SingleAnswerMCQGenerator(ExerciseGenerator):
    def get_exercise_type(self) -> str:
        return "single-answer multiple choice"
    
    def get_examples_section(self) -> str:
        """Format single-answer MCQ examples for inclusion in prompts."""
        examples = EXERCISE_EXAMPLES["single_mcq"]
        return f"""EXAMPLES OF GOOD EXERCISE COMPONENTS:

Example Titles:
{chr(10).join(f'- "{title}"' for title in examples["titles"])}

Example Contexts (create rich, scenario-based contexts like these):
{chr(10).join(f'- {context}' for context in examples["contexts"])}

Example Questions:
{chr(10).join(f'- "{question}"' for question in examples["questions"])}

Example Hints:
{chr(10).join(f'- "{hint}"' for hint in examples["hints"])}"""
    
    def get_json_schema(self) -> str:
        return """Respond with ONLY valid JSON in this exact format (no markdown, no extra text). 
IMPORTANT: Vary the number of incorrect answers - some exercises should have 2 incorrect answers (3 total options), others should have 3 incorrect answers (4 total options):

{
  "exercises": [
    {
      "title": "Exercise title here",
      "context": "Rich, engaging context or scenario here", 
      "question": "Question text here",
      "hints": ["Hint 1", "Hint 2"],
      "incorrect_answers": {
        "Wrong answer 1": "Feedback for wrong answer 1",
        "Wrong answer 2": "Feedback for wrong answer 2",
        "Wrong answer 3": "Feedback for wrong answer 3"
      },
      "correct_answer": "The correct answer text",
      "correct_feedback": "Success message for correct answer"
    }
  ]
}"""
    
    def parse_exercises(self, parsed_json: dict) -> list[SingleAnswerMCQExercise]:
        """Parse JSON response into SingleAnswerMCQExercise objects."""
        exercises = []
        for exercise_data in parsed_json["exercises"]:
            exercises.append(SingleAnswerMCQExercise(**exercise_data))
        return exercises
    
    def generate_markdown_exercises(self, video_content: str, learning_objectives: list[str] = None) -> list[str]:
        """Generate exercises and format them as markdown strings."""
        exercises = self.generate_exercises(video_content, learning_objectives)
        formatter = SingleAnswerMCQFormatter()
        return [formatter.format_to_markdown(exercise) for exercise in exercises]
