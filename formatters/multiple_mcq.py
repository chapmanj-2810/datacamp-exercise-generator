"""
Formatter for multiple-answer multiple choice exercises.
"""

from .base import ExerciseFormatter
from ..models.exercises import MultipleAnswerMCQExercise


class MultipleAnswerMCQFormatter(ExerciseFormatter):
    def format_to_markdown(self, exercise: MultipleAnswerMCQExercise) -> str:
        """Convert a MultipleAnswerMCQExercise object to the final markdown format."""
        # Format hints (joining multiple hints with newlines if more than one)
        if len(exercise.hints) > 1:
            hints_formatted = "\n    ".join(exercise.hints)
        else:
            hints_formatted = exercise.hints[0] if exercise.hints else ""
        
        # Format solution items from the answers list
        solution_items = []
        for answer_obj in exercise.answers:
            # Handle both dict and object access patterns
            if isinstance(answer_obj, dict):
                answer_text = answer_obj['answer']
                is_correct = answer_obj['correct']
                feedback_text = answer_obj['feedback']
            else:
                answer_text = answer_obj.answer
                is_correct = answer_obj.correct
                feedback_text = answer_obj.feedback
                
            solution_items.append(f"""      - answer: {answer_text}
        correct: {str(is_correct).lower()}
        feedback: >-
          {feedback_text}""")
        
        solution_items_formatted = "\n".join(solution_items)
        
        # Construct the full exercise markdown with complex YAML structure
        return f"""## {exercise.title}

```yaml
type: PureMultipleChoiceExercise
key: 
xp: 50
version: v2
data:
  assignment: >-
    {exercise.context}


    **{exercise.question}**
  hint: >-
    - {hints_formatted}
  language: python
  question:
    flavor: PureMultipleAnswers
    solutionItems:
{solution_items_formatted}
    successMessage: >-
      {exercise.success_message}
  sct: >-
    # Examples of good success messages:
    https://instructor-support.datacamp.com/en/articles/2299773-exercise-success-messages.
```"""
