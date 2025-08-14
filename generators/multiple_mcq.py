"""
Generator for multiple-answer multiple choice exercises.
"""

from .base import ExerciseGenerator
from ..models.exercises import MultipleAnswerMCQExercise
from ..models.examples import EXERCISE_EXAMPLES
from ..formatters.multiple_mcq import MultipleAnswerMCQFormatter


class MultipleAnswerMCQGenerator(ExerciseGenerator):
    def get_exercise_type(self) -> str:
        return "multiple-answer multiple choice"
    
    def get_examples_section(self) -> str:
        """Format multiple-answer MCQ examples for inclusion in prompts."""
        examples = EXERCISE_EXAMPLES["multiple_mcq"]
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
IMPORTANT: Include 3-5 answer options total. At least 2 should be correct, and at least 1 should be incorrect:

{
  "exercises": [
    {
      "title": "Exercise title here",
      "context": "Rich, engaging context or scenario here", 
      "question": "Question text here (should ask 'which of the following' to indicate multiple selections)",
      "hints": ["Hint 1", "Hint 2"],
      "answers": [
        {
          "answer": "Answer option 1",
          "correct": true,
          "feedback": "Feedback for this answer option"
        },
        {
          "answer": "Answer option 2", 
          "correct": false,
          "feedback": "Feedback for this answer option"
        },
        {
          "answer": "Answer option 3",
          "correct": true, 
          "feedback": "Feedback for this answer option"
        }
      ],
      "success_message": "Success message when all correct answers are selected"
    }
  ]
}"""
    
    def parse_exercises(self, parsed_json: dict) -> list[MultipleAnswerMCQExercise]:
        """Parse JSON response into MultipleAnswerMCQExercise objects."""
        exercises = []
        for exercise_data in parsed_json["exercises"]:
            exercises.append(MultipleAnswerMCQExercise(**exercise_data))
        return exercises
    
    def generate_markdown_exercises(self, video_content: str, learning_objectives: list[str] = None) -> list[str]:
        """Generate exercises and format them as markdown strings."""
        exercises = self.generate_exercises(video_content, learning_objectives)
        formatter = MultipleAnswerMCQFormatter()
        return [formatter.format_to_markdown(exercise) for exercise in exercises]
