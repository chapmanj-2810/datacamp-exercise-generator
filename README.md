# DataCamp Exercise Generator

An intelligent system for automatically generating DataCamp exercises from video content.

## Features
- 🤖 Intelligent exercise type selection
- 📝 Multiple choice questions (single and multiple answer)
- 🎯 Learning objective-driven generation  
- 🏗️ Modular, extensible architecture

## Installation

### From GitHub (Development)
```bash
git clone https://github.com/chapmanj-2810/datacamp-exercise-generator.git
cd datacamp-exercise-generator
pip install -r requirements.txt
```

### Local Development Setup
```bash
# Install in editable mode for development
pip install -e .
```

### Dependencies Only
```bash
pip install -r requirements.txt
```

## Quick Start

```python
from datacamp_exercise_generator.core import LearningDesigner, load_video_content

# Load your video content
video_content = load_video_content('your_video.md')

# Create learning designer
designer = LearningDesigner()

# Generate exercises with intelligent type selection
learning_plan = designer.create_learning_plan(video_content)
exercises = designer.execute_learning_plan(video_content, learning_plan)

# Output exercises
for i, exercise_md in enumerate(exercises, 1):
    if i > 1:
        print("\n---\n")
    print(exercise_md)
```

## Usage Options

### Option 1: Intelligent Design with Custom Objectives

```python
from datacamp_exercise_generator.core import LearningDesigner, load_video_content

video_content = load_video_content('your_video.md')
designer = LearningDesigner()

# Provide your own learning objectives
objectives = [
    "Understand what fragile evaluation is and why it's problematic",
    "Identify strategies for robust evaluation of AI systems",
    "Recognize the importance of diverse, real-world testing scenarios"
]

plan = designer.create_learning_plan(video_content, objectives)
exercises = designer.execute_learning_plan(video_content, plan)

# Output clean markdown/YAML exercises
for i, exercise_md in enumerate(exercises, 1):
    if i > 1:
        print("\n---\n")
    print(exercise_md)
```

### Option 2: Intelligent Design with Auto-Generated Objectives

```python
from datacamp_exercise_generator.core import LearningDesigner, load_video_content

video_content = load_video_content('your_video.md')
designer = LearningDesigner()

# Let the AI determine the best learning objectives
plan = designer.create_learning_plan(video_content)  # No objectives provided
exercises = designer.execute_learning_plan(video_content, plan)

for i, exercise_md in enumerate(exercises, 1):
    if i > 1:
        print("\n---\n")
    print(exercise_md)
```

### Option 3: Manual Single-Type Generation

```python
from datacamp_exercise_generator.generators import get_exercise_generator
from datacamp_exercise_generator.core import load_video_content

video_content = load_video_content('your_video.md')

# Generate only single-answer multiple choice questions
generator = get_exercise_generator("single_mcq")
exercises = generator.generate_markdown_exercises(video_content)

# Or generate only multiple-answer multiple choice questions
generator = get_exercise_generator("multiple_mcq")
exercises = generator.generate_markdown_exercises(video_content)

for i, exercise_md in enumerate(exercises, 1):
    if i > 1:
        print("\n---\n")
    print(exercise_md)
```

## Project Structure

```
datacamp-exercise-generator/
├── models/          # Pydantic models and examples
├── generators/      # Exercise generators for different types
├── formatters/      # Markdown/YAML formatters
├── core/            # Learning designer and utilities
└── main.py          # Usage examples
```

## Configuration

Set your OpenAI API key:
```bash
export OPENAI_API_KEY="your-api-key-here"
```

## Extending the System

### Adding New Exercise Types

1. Create a new exercise model in `models/exercises.py`
2. Add examples to `models/examples.py`
3. Create a generator in `generators/`
4. Create a formatter in `formatters/`
5. Register in the factory function

### Example Output

The system generates clean DataCamp exercise format:

```markdown
## Understanding Fragile Evaluation

```yaml
type: PureMultipleChoiceExercise
key:
kind: PureMultipleChoice
xp: 50
```

You have developed an AI travel assistant that is facing issues...

**What is a key strategy to address the fragile evaluation of AI agents?**

`@hint`
- Consider the diversity of user inputs.

`@possible_answers`
- Use only ideal test cases
- [Use real queries that include slang, partial sentences, and typos.]
- Ignore multilingual inputs

`@feedback`
- Ideal test cases do not reflect real-world usage.
- Correct! Using real queries helps the AI agent handle diverse inputs effectively.
- Ignoring multilingual inputs can lead to user dissatisfaction.
```
