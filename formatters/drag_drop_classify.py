"""
Formatter for drag-and-drop classify exercises.
"""

from .base import ExerciseFormatter
from ..models.exercises import DragDropClassifyExercise


class DragDropClassifyFormatter(ExerciseFormatter):
    def format_to_markdown(self, exercise: DragDropClassifyExercise) -> str:
        """Convert a DragDropClassifyExercise object to the final markdown format."""
        
        # Format hints
        hints_formatted = "\n    ".join(exercise.hints)
        
        # Generate correctness conditions and solution structure
        correctness_checks = []
        solution_dropzones = []
        
        for dropzone in exercise.drop_zones:
            dropzone_items = []
            
            for item in dropzone.draggable_items:
                # Create correctness condition
                correctness_checks.append(f"""        - condition: check_target({item.id}) == {dropzone.id}
          message: >-
            {item.incorrect_message}
          shouldBe: true""")
                
                # Add item to solution dropzone
                dropzone_items.append(f"""          - content: {item.content}
            id: {item.id}
            incorrectMessage: >-
              {item.incorrect_message}""")
            
            # Build solution dropzone
            solution_dropzones.append(f"""      - draggableItems:
{chr(10).join(dropzone_items)}
        id: {dropzone.id}
        title: {dropzone.title}""")
        
        # Combine correctness conditions
        correctness_checks_formatted = "\n".join(correctness_checks)
        
        # Combine solution dropzones
        solution_dropzones_formatted = "\n".join(solution_dropzones)
        
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
      isOrdered: false
      successMessage: >-
        {exercise.success_message}
    flavor: Classify
    solution:
      - id: options
        title: Options
{solution_dropzones_formatted}
```"""
