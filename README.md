# DataCamp Exercise Generator

An intelligent system for automatically generating DataCamp exercises from video content.

## Features
- 🤖 Intelligent exercise type selection
- 📝 Multiple choice questions (single and multiple answer)
- 🎯 Learning objective-driven generation  
- 🏗️ Modular, extensible architecture

## Installation
```bash
pip install -r requirements.txt
```

## Quick Start
```python
from core import LearningDesigner, load_video_content

# Load your video content
video_content = load_video_content('your_video.md')

# Create learning designer
designer = LearningDesigner()

# Generate exercises with intelligent type selection
learning_plan = designer.create_learning_plan(video_content)
exercises = designer.execute_learning_plan(video_content, learning_plan)

# Output exercises
for exercise in exercises:
    print(exercise)
```

## Usage Options

### Option 1: Intelligent Design with Custom Objectives

```python
objectives = ["Understand concept X", "Apply technique Y"]
plan = designer.create_learning_plan(video_content, objectives)
exercises = designer.execute_learning_plan(video_content, plan)
```

### Option 2: Manual Single-Type Generation

```python
from generators import get_exercise_generator

generator = get_exercise_generator("single_mcq")
exercises = generator.generate_markdown_exercises(video_content)
```
