"""
Formatter for drag-and-drop order exercises.
"""

from uuid import uuid4
from .base import ExerciseFormatter
from ..models.exercises import DragDropOrderExercise


class DragDropOrderFormatter(ExerciseFormatter):
    def format_to_markdown(self, exercise: DragDropOrderExercise) -> str:
        """Convert a DragDropOrderExercise object to the final markdown format."""
        
        # Format hints
        hints_formatted = "\n    ".join(exercise.hints)
        
        # Generate correctness conditions for each item in order
        correctness_checks: list[str] = []
        draggable_items: list[str] = []
        
        for item in exercise.ordered_items:
            # Create correctness condition - each item must be in correct index position
            correctness_checks.append(f"""        - condition: check_index({item.id}) == solution
          message: {item.incorrect_message}
          shouldBe: true""")
            
            # Add item to draggable items list
            draggable_items.append(f"""          - content: {item.content}
            id: {item.id}
            incorrectMessage: {item.incorrect_message}""")
        
        # Combine correctness conditions
        correctness_checks_formatted = "\n".join(correctness_checks)
        
        # Combine draggable items
        draggable_items_formatted = "\n".join(draggable_items)
        
        # Generate unique ID for the solution container
        solution_id = f"solution_{uuid4().hex[:8]}"
        
        # Construct the full exercise markdown
        return f"""## {exercise.title}

```yaml
type: DragAndDropExercise
key: 
xp: 100
version: v2
data:
  assignment: >-
    {exercise.context}
  hint: >-
    - {hints_formatted}
  instructions: >-
    - {exercise.instructions}
  question:
    correctnessConditions:
      checks:
{correctness_checks_formatted}
      failureMessage: {exercise.failure_message}
      isOrdered: true
      successMessage: >-
        {exercise.success_message}
    flavor: Order
    solution:
      - draggableItems:
{draggable_items_formatted}
        id: {solution_id}
        title: {exercise.sequence_title}
```"""
