"""
Generator for coding exercises.
"""

from .base import ExerciseGenerator
from ..models.exercises import CodingExercise
from ..models.examples import EXERCISE_EXAMPLES
from ..formatters.coding import CodingFormatter


class CodingGenerator(ExerciseGenerator):
    def get_exercise_type(self) -> str:
        return "coding"
    
    def get_examples_section(self) -> str:
        """Format coding exercise examples for inclusion in prompts."""
        examples = EXERCISE_EXAMPLES["coding"]
        return f"""EXAMPLES OF GOOD EXERCISE COMPONENTS:

Example Titles:
{chr(10).join(f'- "{title}"' for title in examples["titles"])}

Example Contexts (create rich, scenario-based contexts like these):
{chr(10).join(f'- {context}' for context in examples["contexts"])}

Example Instructions:
{chr(10).join(f'- "{instruction}"' for instruction in examples["instructions"])}

Example Hints (focus on syntax, functions, methods):
{chr(10).join(f'- "{hint}"' for hint in examples["hints"])}

Example Code Patterns:
{chr(10).join(f'- {pattern}' for pattern in examples["code_patterns"])}"""
    
    def get_json_schema(self) -> str:
        return """Respond with ONLY valid JSON in this exact format (no markdown, no extra text).

CRITICAL CODING CONSISTENCY RULES:
- Use the SAME libraries, functions, and syntax patterns shown in the video content
- Match the video's coding style and technology stack (e.g., if video uses OpenAI client, use that)
- Use exactly four underscores (____) for Python scaffolding
- Place scaffolding on the most educationally relevant parts 
- Sample and solution code must match EXACTLY except for the ____ parts
- Scale scaffolding amount based on difficulty (more scaffolding = easier)
- Create scenarios that apply the same concepts but don't give away the exact solution

{
  "exercises": [
    {
      "title": "Exercise title here",
      "context": "Rich context explaining the problem and motivation",
      "instructions": ["Clear actionable instruction 1", "Clear actionable instruction 2"],
      "hints": ["Syntax-focused hint about functions/methods to use"],
      "pre_exercise_code": "# Imports, data setup, helper functions\\nimport pandas as pd\\ndata = pd.read_csv('file.csv')\\n\\ndef helper_function():\\n    return 'something'",
      "sample_code": "# Comment describing what this section does\\nresult = ____\\nprocessed_data = some_function(____)",
      "solution_code": "# Comment describing what this section does\\nresult = data.groupby('column').mean()\\nprocessed_data = some_function(result)",
      "success_message": "Engaging success message with learning reinforcement!",
      "language": "python"
    }
  ]
}"""
    
    def parse_exercises(self, parsed_json: dict) -> list[CodingExercise]:
        """Parse JSON response into CodingExercise objects."""
        exercises = []
        for exercise_data in parsed_json["exercises"]:
            exercises.append(CodingExercise(**exercise_data))
        return exercises
    
    def generate_markdown_exercises(self, video_content: str, learning_objectives: list[str] = None) -> list[str]:
        """Generate exercises and format them as markdown strings."""
        exercises = self.generate_exercises(video_content, learning_objectives)
        formatter = CodingFormatter()
        return [formatter.format_to_markdown(exercise) for exercise in exercises]
