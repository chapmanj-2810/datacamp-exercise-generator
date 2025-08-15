# DataCamp Exercise Generator

An intelligent system for automatically generating DataCamp exercises from video content.

## Features
- 🤖 Intelligent exercise type selection
- 📝 Multiple choice questions (single and multiple answer)
- 🏷️ Drag-and-drop classification exercises
- 📋 Drag-and-drop ordering exercises for workflows and processes
- 🎯 Learning objective-driven generation  
- 🏗️ Modular, extensible architecture
- 💻 Both CLI and Python API support

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

## Configuration

Set your OpenAI API key:
```bash
export OPENAI_API_KEY="your-api-key-here"
```

## Usage

### 🚀 Quick Start (Python Cells/Notebooks)

```python
from datacamp_exercise_generator.main import generate_exercises_intelligent, print_exercises

# Generate exercises with your own objectives
objectives = [
    "Understand what fragile evaluation is and why it's problematic",
    "Identify strategies for robust evaluation of AI systems",
    "Recognize the importance of diverse, real-world testing scenarios"
]

exercises = generate_exercises_intelligent("your_video.md", objectives)
print_exercises(exercises)
```

### 💻 Command Line Interface

```bash
# Intelligent design with custom objectives
python -m datacamp_exercise_generator video.md --objectives "Understand X" "Learn Y"

# Auto-generated objectives
python -m datacamp_exercise_generator video.md --type intelligent

# Generate only single-answer MCQs
python -m datacamp_exercise_generator video.md --type single_mcq

# Generate drag-and-drop classify exercises
python -m datacamp_exercise_generator video.md --type drag_drop_classify

# Save to file
python -m datacamp_exercise_generator video.md --objectives "Learn X" --output exercises.md
```

### 📚 Python API Usage Options

#### Option 1: Convenience Functions (Recommended for most users)

```python
from datacamp_exercise_generator.main import generate_exercises_intelligent, generate_exercises_single_type, print_exercises

# Intelligent type selection
exercises = generate_exercises_intelligent("video.md", objectives=["Learn X", "Understand Y"])
print_exercises(exercises)

# Single exercise type
exercises = generate_exercises_single_type("video.md", "drag_drop_classify", objectives=["Learn Z"])
print_exercises(exercises)

# Auto-generated objectives
exercises = generate_exercises_intelligent("video.md")  # No objectives = auto-generate
print_exercises(exercises)
```

#### Option 2: Direct Library Usage (Advanced users)

```python
from datacamp_exercise_generator.core import LearningDesigner, load_video_content

video_content = load_video_content('video.md')
designer = LearningDesigner()

# Custom objectives with intelligent type selection
plan = designer.create_learning_plan(video_content, ["Objective 1", "Objective 2"])
exercises = designer.execute_learning_plan(video_content, plan)

for i, exercise_md in enumerate(exercises, 1):
    if i > 1:
        print("\n---\n")
    print(exercise_md)
```

#### Option 3: Manual Single-Type Generation

```python
from datacamp_exercise_generator.generators import get_exercise_generator
from datacamp_exercise_generator.core import load_video_content

video_content = load_video_content('video.md')

# Generate only drag-and-drop classify exercises
generator = get_exercise_generator("drag_drop_classify")
exercises = generator.generate_markdown_exercises(video_content, ["Your objective"])

for exercise in exercises:
    print(exercise)
```

## CLI Options

```bash
python -m datacamp_exercise_generator --help

arguments:
  video_file              Path to the video transcript markdown file

options:
  --objectives [OBJECTIVES ...]    Learning objectives (optional)
  --type {single_mcq,multiple_mcq,drag_drop_classify,intelligent}    Exercise generation type (default: intelligent)
  --model MODEL           OpenAI model to use (default: gpt-4o)
  --output OUTPUT         Output file (optional, prints to stdout if not provided)
```

## Project Structure

```
datacamp-exercise-generator/
├── models/          # Pydantic models and examples
├── generators/      # Exercise generators for different types
├── formatters/      # Markdown/YAML formatters
├── core/           # Learning designer and utilities
└── main.py         # CLI and convenience functions
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

#### Multiple Choice Exercise
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

#### Drag-and-Drop Classification Exercise
```markdown
## Multi-agent design patterns

```yaml
type: DragAndDropExercise
key: 
xp: 100
version: v2
data:
  assignment: >-
    One of things you notice as you review your colleague's codebase is that
    they've built their own multi-agent collaboration framework...
  hint: >-
    - Recall that a supervisor multi-agent is like a manager at a company with
    worker agents underneath to delegate tasks to.
  instructions: >-
    - Classify these statements as describing either a **supervisor** or a
    **network** multi-agent.
  question:
    correctnessConditions:
      checks:
        - condition: check_target(item_1) == supervisor_zone
          message: >-
            In a supervisor multi-agent architecture...
          shouldBe: true
    flavor: Classify
    solution:
      - id: options
        title: Options
      - draggableItems:
          - content: One agent delegates tasks to the others
            id: item_1
            incorrectMessage: >-
              In a supervisor multi-agent architecture...
        id: supervisor_zone
        title: Supervisor Multi-Agent
```

## Development

### Running Tests
```bash
# Add your test files to tests/ directory
python -m pytest tests/
```

### Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes with proper relative imports
4. Add tests for new functionality
5. Submit a pull request
