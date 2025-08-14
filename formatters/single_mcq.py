"""
Formatter for single-answer multiple choice exercises.
"""

import random
from .base import ExerciseFormatter
from models.exercises import SingleAnswerMCQExercise


class SingleAnswerMCQFormatter(ExerciseFormatter):
    def format_to_markdown(self, exercise: SingleAnswerMCQExercise) -> str:
        """Convert a SingleAnswerMCQExercise object to the final markdown format."""
        # Format hints
        hints_formatted = "\n".join(f"- {hint}" for hint in exercise.hints)
        
        # Format answer and feedback blocks
        answer_feedback_block = self._format_answer_feedback_blocks(
            exercise.incorrect_answers, 
            exercise.correct_answer, 
            exercise.correct_feedback
        )
        
        # Construct the full exercise markdown
        return f"""## {exercise.title}

```yaml
type: PureMultipleChoiceExercise
key:
kind: PureMultipleChoice
xp: 50
```

{exercise.context}

**{exercise.question}**

`@hint`
{hints_formatted}

{answer_feedback_block}"""
    
    def _format_answer_feedback_blocks(self, incorrect_answers: dict[str, str], correct_answer: str, correct_feedback: str) -> str:
        """Format the possible answers and feedback blocks for the exercise output."""
        # Convert incorrect answers to list of tuples
        incorrect_items = list(incorrect_answers.items())
        
        # Pick a random index to insert the correct answer
        insert_index = random.randint(0, len(incorrect_items))
        
        # Insert correct answer into the combined list
        all_items = (
            incorrect_items[:insert_index] +
            [(correct_answer, correct_feedback)] +
            incorrect_items[insert_index:]
        )
        
        # Format possible answers (with brackets around correct answer)
        possible_answers = []
        for answer, _ in all_items:
            if answer == correct_answer:
                possible_answers.append(f"- [{answer}]")
            else:
                possible_answers.append(f"- {answer}")
        
        # Format feedback messages
        feedback_messages = [f"- {feedback}" for _, feedback in all_items]
        
        # Combine into final formatted string
        return f"`@possible_answers`\n" + "\n".join(possible_answers) + f"\n\n`@feedback`\n" + "\n".join(feedback_messages)
