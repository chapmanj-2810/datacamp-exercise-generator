"""
Learning designer for intelligent exercise planning.
"""

import os
import json
from langchain_openai import ChatOpenAI
from models.planning import LearningPlan
from generators.factory import get_exercise_generator


class LearningDesigner:
    """Analyzes video content and creates learning plans like a curriculum designer would."""
    
    def __init__(self, model="gpt-4o", temperature=0.3):
        """Initialize with slightly higher temperature for more creative planning."""
        self.llm = ChatOpenAI(
            model=model,
            temperature=temperature,
            api_key=os.environ["OPENAI_API_KEY"]
        )
    
    def create_learning_plan(self, video_content: str, provided_objectives: list[str] = None) -> LearningPlan:
        """Analyze video content and create a comprehensive learning plan."""
        
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
   - Example: "Which of the following are benefits of Y?" (select all that apply)
"""

        # Handle provided objectives vs. auto-generated objectives
        if provided_objectives:
            objectives_section = f"""
PROVIDED LEARNING OBJECTIVES:
{chr(10).join(f'- {obj}' for obj in provided_objectives)}

IMPORTANT: Create exactly {len(provided_objectives)} exercise(s), with each exercise targeting one specific learning objective from the list above."""
            task_instruction = f"Create exactly {len(provided_objectives)} exercise(s), one for each provided learning objective."
        else:
            objectives_section = ""
            task_instruction = "Analyze the video content and create 3-4 exercises covering the key concepts."

        planning_prompt = f"""You are an expert learning designer and curriculum architect for DataCamp. {task_instruction}

Determine which exercise types are most appropriate for each learning objective and the optimal order and difficulty progression.

{exercise_type_guide}

LEARNING DESIGN PRINCIPLES:
- Start with foundational concepts (single MCQ for definitions/basic understanding)
- Progress to application and synthesis (multiple MCQ for identifying multiple approaches/benefits)
- Each exercise should target one specific, measurable learning objective
- Vary exercise types to maintain engagement
- Consider cognitive load and difficulty progression
- Aim for 3-4 exercises total unless the video is very comprehensive
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
      "exercise_type": "multiple_mcq", 
      "learning_objective": "Another learning objective",
      "rationale": "Why multiple choice with multiple answers fits this objective",
      "difficulty_level": "Intermediate"
    }}
  ]
}}"""

        response = self.llm.invoke(planning_prompt)
        
        # Clean and parse response
        content = response.content.strip()
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
                generator = get_exercise_generator(exercise_type.value, model="gpt-4o")
                exercises = generator.generate_markdown_exercises(video_content, objectives)
                all_exercises.extend(exercises)
        else:
            # Generate exercises by type without specific objectives (let generators decide content)
            exercise_types = [plan.exercise_type for plan in learning_plan.exercise_plans]
            for exercise_type in exercise_types:
                generator = get_exercise_generator(exercise_type.value, model="gpt-4o")
                # Generate 1 exercise of this type without specific objective
                exercises = generator.generate_markdown_exercises(video_content, learning_objectives=None)
                # Take only the first exercise to match the plan count
                all_exercises.append(exercises[0])
        
        return all_exercises
