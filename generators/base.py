"""
Base exercise generator abstract class.
"""

import os
import json
from abc import ABC, abstractmethod
from openai import OpenAI
from ..models.exercises import Exercise


class ExerciseGenerator(ABC):
    def __init__(self, model="gpt-4o", temperature=0):
        self.client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
        self.model = model
        
        # GPT-5 models only support temperature=1
        if model.startswith("gpt-5"):
            self.temperature = 1.0
            if temperature != 0:  # Only warn if user explicitly set a different temperature
                print(f"Warning: {model} only supports temperature=1. Adjusting from {temperature} to 1.0")
        else:
            self.temperature = temperature
    
    @abstractmethod
    def get_exercise_type(self) -> str:
        pass
    
    @abstractmethod
    def get_examples_section(self) -> str:
        pass
    
    @abstractmethod
    def get_json_schema(self) -> str:
        pass
    
    @abstractmethod
    def parse_exercises(self, parsed_json: dict) -> list[Exercise]:
        pass
    
    def generate_exercises(self, video_content: str, learning_objectives: list[str] = None) -> list[Exercise]:
        """Generate exercises from video content and optional learning objectives."""
        # Format objectives section
        if learning_objectives:
            objectives_list = "\n".join(f"- {obj}" for obj in learning_objectives)
            objectives_section = f"""Learning Objectives for this video:
{objectives_list}

IMPORTANT: Create exactly {len(learning_objectives)} exercise(s), with each exercise targeting one specific learning objective from the list above."""
            count_instruction = f"Create exactly {len(learning_objectives)} exercise(s), one for each learning objective."
        else:
            objectives_section = ""
            count_instruction = "Create 2-4 exercises covering different key concepts from the video."
        
        json_prompt = f"""You are an expert curriculum designer for DataCamp. Based on the provided video transcript, create {self.get_exercise_type()} exercises that test key concepts from the video.

{objectives_section}

{count_instruction}

Each exercise should:
1. Have a clear, engaging title
2. Provide relevant context or scenario that creates an immersive learning experience
3. Ask a specific question about video content
4. Include helpful guidance for learners
5. Provide constructive feedback
6. Test understanding without giving away answers

{self.get_examples_section()}

Video Content:
{video_content}

Create exercises with rich, engaging contexts similar to the examples above. Use scenarios, company names, realistic situations, and formatted code blocks where appropriate to make the exercises immersive and engaging.

{self.get_json_schema()}"""
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": json_prompt}],
            temperature=self.temperature
        )
        
        # Clean the response content
        content = response.choices[0].message.content.strip()
        if content.startswith("```json"):
            content = content[7:]
        if content.endswith("```"):
            content = content[:-3]
        content = content.strip()
        
        parsed = json.loads(content)
        return self.parse_exercises(parsed)
