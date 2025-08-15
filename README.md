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

### 💻 Command Line Interface

```bash
# Auto-generated objectives and exercise types
python -m datacamp_exercise_generator video.md

# Custom objectives
python -m datacamp_exercise_generator video.md --objectives "Understand X" "Learn Y"

# Specific exercise types
python -m datacamp_exercise_generator video.md --exercise-types single_mcq drag_drop_order

# Save to file
python -m datacamp_exercise_generator video.md --objectives "Learn X" --output exercises.md
```

### 🐍 Python API

```python
from datacamp_exercise_generator.core import LearningDesigner, load_video_content

video_content = load_video_content('video.md')
designer = LearningDesigner()

# Auto-intelligent
plan = designer.create_learning_plan(video_content)
exercises = designer.execute_learning_plan(video_content, plan)

# With constraints
plan = designer.create_learning_plan(
    video_content, 
    provided_objectives=["Objective 1", "Objective 2"], 
    exercise_types=["single_mcq", "drag_drop_order"]
)
exercises = designer.execute_learning_plan(video_content, plan)

# Print results
for i, exercise in enumerate(exercises, 1):
    if i > 1: print("\n---\n")
    print(exercise)
```

**Available Exercise Types:**
- `single_mcq` - Single-answer multiple choice
- `multiple_mcq` - Multiple-answer multiple choice  
- `drag_drop_classify` - Classification exercises
- `drag_drop_order` - Ordering exercises for workflows

## CLI Options

```bash
python -m datacamp_exercise_generator --help

arguments:
  video_file              Path to the video transcript markdown file

options:
  --objectives [OBJECTIVES ...]    Learning objectives (optional)
  --exercise-types [EXERCISE_TYPES ...]    Specific exercise types to use: single_mcq, multiple_mcq, drag_drop_classify, drag_drop_order (optional)
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
