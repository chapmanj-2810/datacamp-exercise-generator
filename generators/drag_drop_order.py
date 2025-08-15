"""
Generator for drag-and-drop order exercises.
"""

from .base import ExerciseGenerator
from ..models.exercises import DragDropOrderExercise, OrderableItem
from ..models.examples import EXERCISE_EXAMPLES
from ..formatters.drag_drop_order import DragDropOrderFormatter
from uuid import uuid4


class DragDropOrderGenerator(ExerciseGenerator):
    def get_exercise_type(self) -> str:
        return "drag-and-drop order"
    
    def get_examples_section(self) -> str:
        """Format drag-drop order examples for inclusion in prompts."""
        examples = EXERCISE_EXAMPLES["drag_drop_order"]
        return f"""EXAMPLES OF GOOD EXERCISE COMPONENTS:

Example Titles:
{chr(10).join(f'- "{title}"' for title in examples["titles"])}

Example Contexts (create rich, scenario-based contexts like these):
{chr(10).join(f'- {context}' for context in examples["contexts"])}

Example Instructions:
{chr(10).join(f'- "{instruction}"' for instruction in examples["instructions"])}

Example Hints:
{chr(10).join(f'- "{hint}"' for hint in examples["hints"])}"""
    
    def get_json_schema(self) -> str:
        return """Respond with ONLY valid JSON in this exact format (no markdown, no extra text).
Create exactly 4-6 orderable items that represent a sequential process or workflow:

{
  "exercises": [
    {
      "title": "Exercise title here",
      "context": "Rich, engaging context or scenario here",
      "instructions": "Clear instructions telling learners to order/sequence the items", 
      "hints": ["Hint 1", "Hint 2"],
      "ordered_items": [
        {
          "content": "First step in the process",
          "id": "step_1",
          "incorrect_message": "Feedback explaining why this step comes first"
        },
        {
          "content": "Second step in the process",
          "id": "step_2", 
          "incorrect_message": "Feedback explaining why this step comes second"
        },
        {
          "content": "Third step in the process",
          "id": "step_3",
          "incorrect_message": "Feedback explaining why this step comes third"
        }
      ],
      "sequence_title": "Name of the process/workflow being ordered",
      "success_message": "Success message when items are correctly ordered",
      "failure_message": "Try again!"
    }
  ]
}"""
    
    def parse_exercises(self, parsed_json: dict) -> list[DragDropOrderExercise]:
        """Parse JSON response into DragDropOrderExercise objects."""
        exercises = []
        for exercise_data in parsed_json["exercises"]:
            # Parse ordered items
            ordered_items = []
            for item_data in exercise_data["ordered_items"]:
                # Generate unique ID if not provided
                if "id" not in item_data or not item_data["id"]:
                    item_data["id"] = f"step_{uuid4().hex[:8]}"
                ordered_items.append(OrderableItem(**item_data))
            
            exercise_data["ordered_items"] = ordered_items
            exercises.append(DragDropOrderExercise(**exercise_data))
        return exercises
    
    def generate_markdown_exercises(self, video_content: str, learning_objectives: list[str] = None) -> list[str]:
        """Generate exercises and format them as markdown strings."""
        exercises = self.generate_exercises(video_content, learning_objectives)
        formatter = DragDropOrderFormatter()
        return [formatter.format_to_markdown(exercise) for exercise in exercises]
