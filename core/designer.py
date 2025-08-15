"""
Learning designer for intelligent exercise planning.
"""

import os
import json
from openai import OpenAI
from ..models.planning import LearningPlan
from ..generators.factory import get_exercise_generator


class LearningDesigner:
    """Analyzes video content and creates learning plans like a curriculum designer would."""
    
    def __init__(self, model="gpt-4o", temperature=0.3):
        """Initialize with slightly higher temperature for more creative planning."""
        self.client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
        self.model = model
        
        # GPT-5 models only support temperature=1
        if model.startswith("gpt-5"):
            self.temperature = 1.0
            if temperature != 0.3:  # Only warn if user explicitly set a different temperature
                print(f"Warning: {model} only supports temperature=1. Adjusting from {temperature} to 1.0")
        else:
            self.temperature = temperature
    
    def create_learning_plan(self, video_content: str, provided_objectives: list[str] = None, exercise_types: list[str] = None) -> LearningPlan:
        """Analyze video content and create a comprehensive learning plan."""
        
        # Handle user-specified exercise types
        if exercise_types:
            # Validate provided exercise types
            valid_types = ["single_mcq", "multiple_mcq", "drag_drop_classify", "drag_drop_order"]
            invalid_types = [t for t in exercise_types if t not in valid_types]
            if invalid_types:
                raise ValueError(f"Invalid exercise types: {invalid_types}. Valid types: {valid_types}")
            
            exercise_types_instruction = f"""
EXERCISE TYPE CONSTRAINTS:
You must ONLY use these exercise types: {exercise_types}
Distribute exercises across these types based on which is most appropriate for each objective.
"""
        else:
            exercise_types_instruction = ""
        
        # Available exercise types and their characteristics
        exercise_type_guide = """
AVAILABLE EXERCISE TYPES:

1. **single_mcq** (Single-Answer Multiple Choice):
   - Best for: Testing specific factual knowledge, definitions, concepts
   - Use when: There's one clear correct answer
   - Example: "What is the primary benefit of X?" 

2. **multiple_mcq** (Multiple-Answer Multiple Choice):
   - Best for: Testing understanding of multiple related concepts, identifying several correct approaches
   - Use when: Multiple correct answers exist or learners need to identify all applicable items
   - Example: "Which of the following statements about Y are correct?"

3. **drag_drop_classify** (Drag-and-Drop Classification):
   - Best for: Testing ability to categorize, classify, or sort concepts into groups
   - Use when: Learners need to demonstrate understanding of how items relate to categories
   - Example: "Classify these algorithms as supervised or unsupervised learning"

4. **drag_drop_order** (Drag-and-Drop Ordering):
   - Best for: Testing understanding of sequential processes, workflows, or procedures
   - Use when: Learners need to demonstrate knowledge of step-by-step processes
   - Example: "Order the steps in the machine learning pipeline from data collection to deployment"
"""

        # Handle provided objectives vs. auto-generated objectives
        if provided_objectives:
            objectives_count = len(provided_objectives)
            objectives_list = "\n".join(f'- {obj}' for obj in provided_objectives)
            
            if objectives_count <= 3:
                # 1:1 mapping for 3 or fewer objectives
                objectives_section = f"""
PROVIDED LEARNING OBJECTIVES:
{objectives_list}

IMPORTANT: Create exactly {objectives_count} exercise(s), with each exercise targeting one specific learning objective from the list above."""
                task_instruction = f"Create exactly {objectives_count} exercise(s), one for each provided learning objective."
            else:
                # Amalgamate objectives for 4+ objectives
                objectives_section = f"""
PROVIDED LEARNING OBJECTIVES:
{objectives_list}

IMPORTANT: You have {objectives_count} learning objectives, but create only 2-3 exercises total. Combine related objectives into single exercises that can test multiple concepts together. Each exercise should target 2-3 related learning objectives from the list above."""
                task_instruction = f"Create 2-3 exercises that combine the {objectives_count} learning objectives. Group related objectives together into single exercises."
        else:
            objectives_section = ""
            task_instruction = "Analyze the video content and create 2-3 exercises covering the key concepts."

        planning_prompt = f"""You are an expert learning designer and curriculum architect for DataCamp. {task_instruction}

Determine which exercise types are most appropriate for each learning objective and the optimal order and difficulty progression.

{exercise_type_guide}
{exercise_types_instruction}

LEARNING DESIGN PRINCIPLES:
- Start with foundational concepts (single MCQ for definitions/basic understanding)
- Progress to application and synthesis (multiple MCQ for identifying multiple approaches/benefits)
- Use drag-drop classification for categorization and grouping concepts
- Use drag-drop ordering for sequential processes, workflows, and procedures
- Each exercise should target one specific, measurable learning objective
- Vary exercise types to maintain engagement
- Consider cognitive load and difficulty progression
- Create 2-3 exercises total
{objectives_section}

Video Content:
{video_content}

Respond with ONLY valid JSON in this exact format:
{{
  "video_title": "Descriptive title for the video content",
  "video_summary": "Brief summary of what the video covers",
  "exercise_plans": [
    {{
      "exercise_type": "single_mcq",
      "learning_objective": "Specific learning objective this exercise targets",
      "rationale": "Why this exercise type is appropriate for this objective",
      "difficulty_level": "Beginner"
    }},
    {{
      "exercise_type": "drag_drop_order",
      "learning_objective": "Sequential process learning objective",
      "rationale": "Why drag-drop ordering is appropriate for this objective",
      "difficulty_level": "Intermediate"
    }}
  ]
}}"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": planning_prompt}],
            temperature=self.temperature
        )
        
        # Clean and parse response
        content = response.choices[0].message.content.strip()
        if content.startswith("```json"):
            content = content[7:]
        if content.endswith("```"):
            content = content[:-3]
        content = content.strip()
        
        parsed = json.loads(content)
        return LearningPlan(**parsed)
    
    def execute_learning_plan(self, video_content: str, learning_plan: LearningPlan, use_plan_objectives: bool = True) -> list[str]:
        """Execute a learning plan by generating the planned exercises.
        
        Args:
            video_content: The video transcript content
            learning_plan: The generated learning plan
            use_plan_objectives: If True, uses objectives from the plan. If False, lets generators create exercises freely.
        """
        all_exercises = []
        
        if use_plan_objectives:
            # Group plans by exercise type for efficient generation (1:1 with objectives)
            plans_by_type = {}
            for plan in learning_plan.exercise_plans:
                if plan.exercise_type not in plans_by_type:
                    plans_by_type[plan.exercise_type] = []
                plans_by_type[plan.exercise_type].append(plan.learning_objective)
            
            # Generate exercises for each type using specific objectives
            for exercise_type, objectives in plans_by_type.items():
                generator = get_exercise_generator(exercise_type.value, model=self.model)
                exercises = generator.generate_markdown_exercises(video_content, objectives)
                all_exercises.extend(exercises)
        else:
            # Generate exercises by type without specific objectives (let generators decide content)
            exercise_types = [plan.exercise_type for plan in learning_plan.exercise_plans]
            for exercise_type in exercise_types:
                generator = get_exercise_generator(exercise_type.value, model=self.model)
                # Generate 1 exercise of this type without specific objective
                exercises = generator.generate_markdown_exercises(video_content, learning_objectives=None)
                # Take only the first exercise to match the plan count
                all_exercises.append(exercises[0])
        
        return all_exercises
