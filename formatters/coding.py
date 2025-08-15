"""
Formatter for coding exercises.
"""

from .base import ExerciseFormatter
from ..models.exercises import CodingExercise
import uuid


class CodingFormatter(ExerciseFormatter):
    def format_to_markdown(self, exercise: CodingExercise) -> str:
        """Convert a CodingExercise object to the final markdown format."""
        
        # Generate a unique key for the exercise
        exercise_key = uuid.uuid4().hex[:10]
        
        # Format instructions
        instructions_formatted = "\n".join(f"- {instruction}" for instruction in exercise.instructions)
        
        # Format hints  
        hints_formatted = "\n".join(f"- {hint}" for hint in exercise.hints)
        
        # Construct the full exercise markdown
        return f"""## {exercise.title}

```yaml
type: NormalExercise
key: {exercise_key}
xp: {exercise.xp}
```

{exercise.context}

`@instructions`
{instructions_formatted}

`@hint`
{hints_formatted}

`@pre_exercise_code`
```{{{exercise.language}}}
{exercise.pre_exercise_code}
```

`@sample_code`
```{{{exercise.language}}}
{exercise.sample_code}
```

`@solution`
```{{{exercise.language}}}
{exercise.solution_code}
```

`@sct`
```{{{exercise.language}}}
success_msg("{exercise.success_message}")
```"""
