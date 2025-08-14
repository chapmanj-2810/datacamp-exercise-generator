"""
Generator for drag-and-drop classify exercises.
"""

from .base import ExerciseGenerator
from ..models.exercises import DragDropClassifyExercise, DraggableItem, DropZone
from ..models.examples import EXERCISE_EXAMPLES
from ..formatters.drag_drop_classify import DragDropClassifyFormatter
from uuid import uuid4


class DragDropClassifyGenerator(ExerciseGenerator):
    def get_exercise_type(self) -> str:
        return "drag-and-drop classify"
    
    def get_examples_section(self) -> str:
        """Format drag-drop classify examples for inclusion in prompts."""
        examples = EXERCISE_EXAMPLES["drag_drop_classify"]
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
Create exactly 2 drop zones (categories) with 2-4 draggable items total (distributed across the zones):

{
  "exercises": [
    {
      "title": "Exercise title here",
      "context": "Rich, engaging context or scenario here",
      "instructions": "Clear instructions telling learners what to classify/sort", 
      "hints": ["Hint 1", "Hint 2"],
      "drop_zones": [
        {
          "id": "category_1", 
          "title": "First Category Name",
          "draggable_items": [
            {
              "content": "Item that belongs in this category",
              "id": "item_1",
              "incorrect_message": "Feedback explaining why this belongs in category 1"
            }
          ]
        },
        {
          "id": "category_2",
          "title": "Second Category Name", 
          "draggable_items": [
            {
              "content": "Item that belongs in this category",
              "id": "item_2", 
              "incorrect_message": "Feedback explaining why this belongs in category 2"
            }
          ]
        }
      ],
      "success_message": "Success message when all items are correctly classified"
    }
  ]
}"""
    
    def parse_exercises(self, parsed_json: dict) -> list[DragDropClassifyExercise]:
        """Parse JSON response into DragDropClassifyExercise objects."""
        exercises = []
        for exercise_data in parsed_json["exercises"]:
            # Parse drop zones with their draggable items
            drop_zones = []
            for zone_data in exercise_data["drop_zones"]:
                draggable_items = []
                for item_data in zone_data["draggable_items"]:
                    # Generate unique ID if not provided
                    if "id" not in item_data or not item_data["id"]:
                        item_data["id"] = f"item_{uuid4().hex[:8]}"
                    draggable_items.append(DraggableItem(**item_data))
                
                # Generate unique ID for drop zone if not provided
                if "id" not in zone_data or not zone_data["id"]:
                    zone_data["id"] = f"dropzone_{uuid4().hex[:8]}"
                    
                drop_zones.append(DropZone(
                    id=zone_data["id"],
                    title=zone_data["title"], 
                    draggable_items=draggable_items
                ))
            
            exercise_data["drop_zones"] = drop_zones
            exercises.append(DragDropClassifyExercise(**exercise_data))
        return exercises
    
    def generate_markdown_exercises(self, video_content: str, learning_objectives: list[str] = None) -> list[str]:
        """Generate exercises and format them as markdown strings."""
        exercises = self.generate_exercises(video_content, learning_objectives)
        formatter = DragDropClassifyFormatter()
        return [formatter.format_to_markdown(exercise) for exercise in exercises]
